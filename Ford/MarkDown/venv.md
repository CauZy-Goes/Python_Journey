# 🐍 Python — Ambientes Virtuais, pip e requirements.txt

Guia prático de comandos para o dia a dia de desenvolvimento/testes em Python.

---

## 1. Por que usar Ambiente Virtual (venv)?

Cada projeto pode precisar de **versões diferentes** das mesmas bibliotecas. Sem um ambiente isolado, tudo é instalado globalmente no sistema, o que causa conflitos (ex: um projeto precisa do `pytest 7.x`, outro precisa do `pytest 8.x`).

O **venv** cria uma "cópia isolada" do Python + pip só para aquele projeto, sem interferir no resto do sistema.

---

## 2. Criando e Ativando um venv

### Criar o ambiente

```bash
# Dentro da pasta do projeto
python -m venv venv
```

- `venv` (o segundo) é só o **nome da pasta** que será criada — pode ser `.venv`, `env`, etc. `venv` e `.venv` são as convenções mais comuns.

### Ativar o ambiente

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

Quando ativo, o terminal mostra o nome do ambiente entre parênteses:

```bash
(venv) usuario@maquina:~/projeto$
```

### Desativar o ambiente

```bash
deactivate
```

Funciona igual em qualquer sistema operacional.

### Verificar se está usando o Python certo

```bash
which python      # Linux/macOS
where python       # Windows

python --version
```

Se o venv estiver ativo, o caminho deve apontar para dentro da pasta `venv/`.

---

## 3. pip — Gerenciador de Pacotes

### Instalar um pacote

```bash
pip install pytest
```

### Instalar uma versão específica

```bash
pip install pytest==7.4.0
```

### Instalar uma versão mínima

```bash
pip install "pytest>=7.0"
```

### Atualizar um pacote

```bash
pip install --upgrade pytest
```

### Desinstalar um pacote

```bash
pip uninstall pytest
```

### Ver pacotes instalados

```bash
pip list
```

### Ver detalhes de um pacote específico

```bash
pip show pytest
```

### Atualizar o próprio pip

```bash
python -m pip install --upgrade pip
```

---

## 4. requirements.txt

É o arquivo que **lista as dependências** do projeto, para que qualquer pessoa (ou pipeline de CI/CD) consiga recriar o mesmo ambiente.

### Gerar o requirements.txt a partir do que está instalado

```bash
pip freeze > requirements.txt
```

Isso gera algo como:

```
pytest==7.4.0
python-can==4.3.1
pyserial==3.5
robotframework==7.0
```

⚠️ `pip freeze` inclui **tudo** que está instalado no ambiente, inclusive dependências de dependências. Em projetos maiores, isso pode poluir o arquivo.

### Instalar tudo que está listado no requirements.txt

```bash
pip install -r requirements.txt
```

Esse é o comando que você (ou o CI/CD) roda ao clonar o projeto pela primeira vez.

### Boas práticas

- Sempre **ative o venv antes** de rodar `pip freeze`, senão vai capturar pacotes globais do sistema também.
- Para projetos maiores, é comum ter dois arquivos:
  - `requirements.txt` → dependências de produção
  - `requirements-dev.txt` → dependências extras só para desenvolvimento/teste (ex: `pytest`, `flake8`, `black`)
  
  ```bash
  pip freeze > requirements-dev.txt
  pip install -r requirements-dev.txt
  ```

---

## 5. Fluxo Completo (do zero até rodar o projeto)

```bash
# 1. Clonar o projeto
git clone https://github.com/usuario/projeto.git
cd projeto

# 2. Criar o ambiente virtual
python -m venv venv

# 3. Ativar o ambiente
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 4. Instalar as dependências
pip install -r requirements.txt

# 5. Trabalhar normalmente...
pytest

# 6. Ao terminar
deactivate
```

---

## 6. Ignorar o venv no Git

O `venv/` **nunca** deve ser versionado (é pesado e específico de cada máquina). Adicione ao `.gitignore`:

```gitignore
venv/
.venv/
__pycache__/
*.pyc
.env
```

---

## 7. Comandos Úteis Extras

### Ver qual Python está sendo usado (útil para debugar erro de venv "path errado")

```bash
python -c "import sys; print(sys.executable)"
```

### Criar venv com uma versão específica do Python (se tiver várias instaladas)

```bash
python3.11 -m venv venv
```

### Rodar um comando sem ativar o venv (usando o Python de dentro da pasta diretamente)

```bash
./venv/bin/python -m pytest        # Linux/macOS
.\venv\Scripts\python -m pytest    # Windows
```

### Listar pacotes desatualizados

```bash
pip list --outdated
```

### Instalar um pacote em "modo edição" (útil quando você está desenvolvendo uma lib localmente)

```bash
pip install -e .
```

---

## 8. Alternativas ao venv (bom saber que existem)

| Ferramenta | Quando usar |
|---|---|
| `venv` | Built-in do Python, simples, suficiente para a maioria dos projetos |
| `virtualenv` | Similar ao venv, mas com mais recursos e compatível com Python 2 |
| `pipenv` | Junta pip + venv + arquivo de lock (Pipfile.lock) |
| `poetry` | Gerenciamento de dependências + empacotamento + publicação, muito usado em projetos modernos |
| `conda` | Comum em Data Science, gerencia até pacotes não-Python (ex: bibliotecas C) |

Para o contexto do projeto (automação de testes, scripts, integração com CI/CD), `venv` + `requirements.txt` é o padrão mais simples e mais provável de ser usado no ambiente da Ford.

---

## 9. Erros Comuns

| Erro | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError` mesmo após instalar | venv não estava ativado ao instalar, ou ativado errado | Confirme com `which python` / `where python` |
| `pip: command not found` | pip não está no PATH ou venv não ativado | Ative o venv ou use `python -m pip` |
| Pacotes global aparecendo no `pip freeze` | venv criado sem isolamento (`--system-site-packages`) | Recriar o venv sem essa flag |
| Erro de permissão ao instalar | Tentando instalar fora do venv, no Python do sistema | Ative o venv antes de instalar |