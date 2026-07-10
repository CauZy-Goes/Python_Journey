# 🐳 Docker Compose — Conceitos e Comandos

Guia de referência sobre Docker Compose: o que é, como o arquivo é estruturado e os comandos mais usados no dia a dia.

---

## 1. O que é o Docker Compose

O **Docker Compose** é uma ferramenta pra definir e rodar **múltiplos containers** como se fossem um único sistema, usando um arquivo de configuração (`docker-compose.yml`) em vez de digitar vários `docker run` na mão.

Sem Compose, subir seu ambiente (SQL Server + SQLPad, por exemplo) seria algo assim:

```bash
docker run -d --name mssql -e ACCEPT_EULA=Y -e MSSQL_SA_PASSWORD=... -p 1433:1433 mcr.microsoft.com/mssql/server:2022-latest
docker run -d --name sqlpad -e SQLPAD_ADMIN=... -p 8081:3000 sqlpad/sqlpad:latest
```

Com Compose, você define tudo isso **uma vez** no `.yml` e sobe com um único comando: `docker compose up`.

---

## 2. Anatomia do `docker-compose.yml`

```yaml
services:        # Lista de containers que vão rodar
  mssql:         # Nome do serviço (você escolhe)
    image: ...   # Qual imagem usar (do Docker Hub ou registro privado)
    container_name: ...  # Nome fixo do container (opcional, senão o Docker gera um)
    restart: always      # Política de reinício
    environment:          # Variáveis de ambiente passadas pro container
      CHAVE: valor
    ports:
      - "porta_local:porta_container"
    volumes:
      - nome_do_volume:/caminho/dentro/do/container
    depends_on:
      - outro_servico   # Ordem de inicialização

volumes:          # Volumes nomeados, declarados fora de "services"
  nome_do_volume:
```

### Principais campos, explicados

| Campo | Pra que serve |
|---|---|
| `image` | Qual imagem Docker usar como base do container |
| `container_name` | Nome fixo pro container (facilita em comandos `docker exec`, `docker logs`, etc) |
| `restart` | `always` (sempre reinicia), `on-failure` (só se falhar), `no` (nunca) |
| `environment` | Configurações passadas como variáveis de ambiente pro processo dentro do container |
| `ports` | Mapeia `"porta_da_sua_máquina:porta_do_container"` — permite acessar o serviço de fora do Docker |
| `volumes` | Persiste dados em disco, mesmo se o container for destruído e recriado |
| `depends_on` | Define ordem de inicialização (⚠️ não garante que o serviço já está *pronto*, só que o container já *subiu* — ver seção 6) |

---

## 3. Comandos Essenciais

### Subir os containers

```bash
docker compose up
```

Roda em primeiro plano (o terminal fica "preso" mostrando os logs).

```bash
docker compose up -d
```

Roda em background (**detached**) — o terminal fica livre. Esse é o mais usado no dia a dia.

### Parar os containers

```bash
docker compose stop
```

Para os containers, mas **mantém** eles criados (e os volumes intactos) — só "desliga".

### Parar e remover os containers

```bash
docker compose down
```

Remove os containers e a rede criada pelo Compose. **Os volumes nomeados continuam existindo** (a menos que você use a flag abaixo).

```bash
docker compose down -v
```

Remove containers **e volumes** — ⚠️ isso apaga os dados persistidos (ex: o banco de dados inteiro). Use com cuidado.

### Ver o status dos containers

```bash
docker compose ps
```

Mostra quais serviços estão rodando, portas expostas e status.

### Ver logs

```bash
docker compose logs
```

Mostra os logs de todos os serviços.

```bash
docker compose logs -f mssql
```

`-f` (**follow**) acompanha os logs em tempo real, só do serviço `mssql`.

### Reconstruir as imagens (quando você mudou algo no Dockerfile/config)

```bash
docker compose up -d --build
```

### Reiniciar um serviço específico

```bash
docker compose restart mssql
```

### Executar um comando dentro de um container já rodando

```bash
docker compose exec mssql bash
```

Abre um terminal dentro do container `mssql` (útil pra rodar `sqlcmd`, verificar arquivos, etc).

```bash
docker compose exec mssql /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "SuaSenha" -C
```

Roda um comando específico direto, sem precisar entrar interativamente.

### Parar e remover tudo relacionado ao projeto (containers, redes, volumes, imagens órfãs)

```bash
docker compose down -v --rmi local
```

---

## 4. `docker compose` vs `docker-compose`

Você pode ver os dois formatos em tutoriais/documentações antigas:

- `docker-compose` (com hífen) → versão antiga, um binário separado (Compose V1, hoje descontinuado).
- `docker compose` (sem hífen, como subcomando do `docker`) → versão atual (Compose V2), já vem integrada ao Docker CLI.

Hoje em dia, use sempre `docker compose` (sem hífen).

---

## 5. Volumes: por que usar

Containers são **efêmeros** — se você remover um container (`docker compose down`), tudo que estava só "dentro" dele some. Um volume é uma pasta gerenciada pelo Docker, **fora** do ciclo de vida do container, onde os dados continuam existindo mesmo se o container for recriado.

```yaml
volumes:
  - mssql_data:/var/opt/mssql   # nomeado (Docker gerencia o local no disco)
  - ./sql:/scripts               # bind mount (aponta pra uma pasta real da sua máquina)
```

| Tipo | Quando usar |
|---|---|
| **Volume nomeado** (`mssql_data:/caminho`) | Dados que só importam pro container (ex: dados do banco) |
| **Bind mount** (`./pasta:/caminho`) | Quando você quer editar arquivos na sua máquina e ver refletido no container (ex: scripts SQL, código em hot-reload) |

Ver todos os volumes existentes na sua máquina:

```bash
docker volume ls
```

Remover um volume específico (com o container já parado):

```bash
docker volume rm nome_do_volume
```

---

## 6. `depends_on` — uma pegadinha comum

```yaml
sqlpad:
  depends_on:
    - mssql
```

Isso garante que o container `mssql` **inicia antes** do `sqlpad` — mas **não** garante que o SQL Server já terminou de inicializar e está pronto pra aceitar conexões. Tem uma diferença entre "container rodando" e "serviço pronto pra uso".

Se você tiver problemas de "conexão recusada" logo no primeiro `docker compose up`, é normalmente por causa disso — o banco ainda está inicializando internamente quando o outro serviço já tenta se conectar. Formas de lidar com isso:

- Rodar `docker compose up -d` de novo depois de alguns segundos (resolve na prática, já que o serviço dependente geralmente tenta reconectar).
- Usar `healthcheck` no serviço do banco + `condition: service_healthy` no `depends_on` (mais robusto, mas mais avançado).

---

## 7. Fluxo Típico de Uso (no seu dia a dia)

```bash
# Primeira vez / depois de mudanças no docker-compose.yml
docker compose up -d

# Ver se subiu certo
docker compose ps

# Acompanhar logs se algo não conectar
docker compose logs -f mssql

# Encerrar o expediente
docker compose stop

# Voltar a trabalhar no dia seguinte
docker compose start

# Se quiser realmente destruir tudo (cuidado com os dados)
docker compose down -v
```

`stop` + `start` é o par mais usado no dia a dia (mantém tudo intacto). `down` só quando você realmente quer desmontar o ambiente.