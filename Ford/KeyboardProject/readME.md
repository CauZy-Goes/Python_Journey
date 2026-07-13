# ⌨️ KeyboardProject

Projeto de estudo criado como preparação para a vaga na **Ford Motor Company Brasil** (Bolsa INOVA IEL — projeto *AutoTest Framework*).

Começou simples — só exibir no terminal qual tecla estava sendo pressionada — e foi evoluindo até virar uma aplicação completa: captura de teclado, persistência em arquivo e em banco de dados relacional, ORM, containerização com Docker e reconstrução de texto digitado a partir do histórico salvo.

---

## 🎯 O que o projeto faz

1. Escuta o teclado em tempo real (usando `pynput`).
2. Exibe no terminal qual tecla foi pressionada.
3. Salva cada tecla pressionada:
   - Em um arquivo local `.jsonl` (JSON Lines).
   - No banco de dados **SQL Server**, via SQLAlchemy (ORM).
4. Permite **reconstruir o texto digitado** em um intervalo de tempo, aplicando regras (espaço, backspace, ignorar teclas especiais) — tanto a partir do arquivo local quanto direto do banco.
5. Interface visual do banco (SQLPad) rodando em container, pra consultar os dados manualmente.

---

## 🗂️ Estrutura do Projeto

```
KeyboardProject/
├── start_listener.py           # Ponto de entrada da aplicação
├── recovery_key.py              # Script para reconstruir o texto digitado
├── requirements.txt
├── docker-compose.yml           # SQL Server + SQLPad
├── .gitignore
│
├── Model/
│   ├── key_history.py           # Dataclass KeyHistory (objeto usado na aplicação)
│   └── Orm/
│       └── key_history_orm.py   # Model ORM (mapeamento da tabela no banco)
│
├── Config/
│   ├── database.py              # Conexão com o banco (engine, sessão, init_db)
│   └── Log/
│       └── log_config.py        # Configuração do log técnico da aplicação
│
├── Service/
│   ├── keyboard_listener.py     # Captura do teclado (pynput)
│   └── log_service.py           # Persistência: salvar/ler no .jsonl e no banco
│
├── data/
│   └── key_history.jsonl        # Gerado automaticamente — histórico local
│
└── logs/
    └── app.log                  # Gerado automaticamente — log técnico
```

---

## ⚙️ Pré-requisitos

- Python 3.12+
- Docker Desktop (com WSL2 habilitado, no Windows)
- Nenhum driver ODBC precisa ser instalado — a conexão com o SQL Server usa `pymssql`, que já vem com o driver embutido no próprio pacote Python.

---

## 🚀 Como rodar

### 1. Subir o banco de dados (Docker)

```bash
docker compose up -d
```

Isso sobe dois containers:
| Serviço | Acesso |
|---|---|
| SQL Server | `localhost:1433` (usuário `sa`) |
| SQLPad (interface visual) | http://localhost:8081 |

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a aplicação

```bash
python .\start_listener.py
```

Isso já cria a tabela `KeyHistory` no banco automaticamente (via `init_db()`, usando o próprio ORM — sem precisar de migrations) e começa a escutar o teclado.

Pressione **ESC** para encerrar.

### 5. Reconstruir o texto digitado

```bash
python .\recovery_key.py
```

Reconstrói o que foi digitado nos últimos minutos, aplicando as regras de espaço/backspace/teclas especiais.

### 6. Encerrar o ambiente

```bash
docker compose stop
wsl --shutdown
```

---

## 🧩 Principais Conceitos Aplicados

- **Ambientes virtuais Python** (`venv`) e gerenciamento de dependências (`requirements.txt`)
- **pynput**: captura de eventos de teclado, diferenciando `KeyCode` (teclas normais) de `Key` (teclas especiais)
- **Dataclasses**: `KeyHistory` como model de dados da aplicação
- **Persistência em arquivo**: JSON Lines (`.jsonl`) — um registro por linha, resiliente a falhas no meio da escrita
- **SQLAlchemy (ORM)**: mapeamento objeto-relacional entre `KeyHistoryORM` e a tabela `KeyHistory`
- **Docker Compose**: orquestração de containers (SQL Server + SQLPad)
- **Logging**: log técnico da aplicação separado dos dados de negócio (módulo `logging` nativo)
- **Arquitetura em camadas**: separação entre captura (`keyboard_listener.py`), persistência (`log_service.py`) e modelos (`Model/`)

---

## 📌 Próximos Passos (ideias)

- [ ] Detectar combinações de teclas (ex: `Ctrl+C`)
- [ ] Adicionar testes automatizados (Pytest) — conectando com o que será usado na vaga da Ford
- [ ] Expor os dados via uma API simples (FastAPI/Flask)
- [ ] Adicionar métricas (quantidade de teclas por sessão, teclas mais usadas, etc)

---

## ⚠️ Aviso

Este projeto foi criado **exclusivamente para fins de estudo pessoal**, rodando localmente e capturando apenas o próprio teclado do desenvolvedor, sem qualquer coleta, transmissão ou armazenamento de dados de terceiros.
