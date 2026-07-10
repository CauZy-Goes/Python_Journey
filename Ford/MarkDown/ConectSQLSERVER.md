# 🗄️ Conectando o SGBD — SQL Server + SQLPad (KeyboardProject)

Passo a passo pra subir o ambiente, entrar no SQLPad e conectar no banco SQL Server.

---

## 1. Subir os containers

Na pasta onde está o `docker-compose.yml`:

```bash
docker compose up -d
```

Confirme que os dois serviços subiram:
```bash
docker compose ps
```
Você deve ver `keyboardproject_mssql` e `keyboardproject_sqlpad` com status `Up`.

⚠️ O SQL Server demora alguns segundos pra terminar de inicializar por dentro, mesmo já aparecendo como "Up". Se o primeiro passo de conexão falhar, espere ~15-20 segundos e tente de novo.

---

## 2. Acessar o SQLPad (a interface visual)

1. Abra o navegador em:
   ```
   http://localhost:8081
   ```
2. Faça login com as credenciais definidas no `docker-compose.yml`:
   - **Email:** `admin@admin.com`
   - **Senha:** `admin123`

Essa é a tela de administração do SQLPad — é daqui que você vai criar a conexão com o banco.

---

## 3. Criar a conexão com o SQL Server dentro do SQLPad

1. No menu lateral, clique em **Connections** (ou no ícone de engrenagem/conexões, dependendo da versão).
2. Clique em **New Connection**.
3. Preencha os campos:

| Campo | Valor |
|---|---|
| **Name** | `KeyboardProject` (ou qualquer nome pra identificar) |
| **Driver** | `SQL Server` |
| **Host/Server** | `mssql` |
| **Port** | `1433` |
| **Database** | `master` (banco padrão — depois você troca pro seu banco específico, se criar um) |
| **Username** | `sa` |
| **Password** | `KeyboardProject@123` |

### ⚠️ Por que o Host é `mssql` e não `localhost`?

Esse é o ponto que mais confunde no início: dentro da rede interna do Docker Compose, os containers se enxergam **pelo nome do serviço** definido no `docker-compose.yml` — nesse caso, `mssql` (o nome que você deu ao serviço, não o nome da imagem).

O SQLPad está rodando **dentro** de outro container, então ele não acessa o banco via `localhost:1433` (isso só funciona da sua máquina física para dentro do Docker, não de container para container). Para o SQLPad, o SQL Server está em `mssql:1433`.

4. Marque a opção de **desabilitar verificação de certificado / trust server certificate** se aparecer (algo como `Encrypt: false` ou `Trust Server Certificate: true`) — necessário porque o SQL Server em container usa um certificado autoassinado.
5. Clique em **Test** (ou **Test Connection**) para validar.
6. Se aparecer sucesso, clique em **Save**.

---

## 4. Rodar sua primeira query

1. No menu principal do SQLPad, clique em **New Query** (ou no ícone de "+").
2. Selecione a conexão `KeyboardProject` que você acabou de criar.
3. Digite uma query de teste:
   ```sql
   SELECT @@VERSION;
   ```
4. Rode com `Ctrl+Enter` (ou o botão de "Run").

Se retornar a versão do SQL Server, está tudo certo — o SQLPad está conversando com o banco.

---

## 5. Conectar direto pela sua máquina (fora do SQLPad)

Se você quiser conectar usando uma ferramenta na sua própria máquina (Azure Data Studio, DBeaver, ou até o `sqlcmd` no terminal), aí sim usa `localhost`, porque a conexão sai da sua máquina física pra dentro do Docker através da porta mapeada:

| Campo | Valor |
|---|---|
| **Server** | `localhost,1433` (no Azure Data Studio, a vírgula separa host e porta) |
| **Authentication** | SQL Login |
| **User** | `sa` |
| **Password** | `KeyboardProject@123` |
| **Trust server certificate** | ✅ marcado |

Via terminal, usando o próprio `sqlcmd` de dentro do container (não precisa instalar nada na sua máquina):
```bash
docker compose exec mssql /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "KeyboardProject@123" -C
```
O `-C` no final confia no certificado autoassinado (equivalente ao "Trust Server Certificate" da interface gráfica).

Dentro do `sqlcmd`, teste com:
```sql
SELECT @@VERSION;
GO
```
(`GO` é necessário no `sqlcmd` — é o comando que manda executar o bloco de SQL digitado até ali.)

---

## 6. Resumo — Dois "mundos" diferentes

| De onde você conecta | Host a usar | Por quê |
|---|---|---|
| De dentro de outro container do mesmo `docker-compose.yml` (ex: SQLPad) | `mssql` | Containers se enxergam pelo nome do serviço, na rede interna do Compose |
| Da sua máquina física (navegador, Azure Data Studio, terminal local) | `localhost` (ou `127.0.0.1`) | A porta `1433` foi mapeada pra sua máquina no `ports:` do compose |

Esse é o erro mais comum de quem está começando com Docker Compose: tentar usar `localhost` de dentro de um container pra falar com outro — não funciona, porque `localhost` ali dentro se refere ao **próprio container**, não à sua máquina nem aos outros serviços.

---

## 7. Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `Login failed for user 'sa'` | Senha errada, ou digitou depois do container já ter sido criado com outra senha antes | Confirme a senha no `docker-compose.yml`; se mudou a senha depois de já ter criado o volume, o container ignora a nova senha — apague o volume (`docker compose down -v`) e suba de novo |
| `Connection refused` / timeout | SQL Server ainda inicializando | Aguarde ~20s após o `docker compose up -d` e tente de novo |
| Erro de certificado (`certificate verify failed`) | Certificado autoassinado do SQL Server | Marque "Trust Server Certificate" na conexão, ou use `-C` no `sqlcmd` |
| SQLPad não acha o host `mssql` | Tentando conectar como se estivesse fora do Docker | Use `mssql` como host dentro do SQLPad (não `localhost`) |