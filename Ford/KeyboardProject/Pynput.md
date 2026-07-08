# ⌨️ pynput — Entendendo `Key` vs `KeyCode` e seus atributos

Esse guia explica o erro que você teve (`'KeyCode' object has no attribute 'name'`) e como o `pynput` representa as teclas internamente.

---

## 1. O erro, em resumo

```
AttributeError: 'KeyCode' object has no attribute 'name'
```

Isso acontece porque o `pynput` usa **duas classes diferentes** para representar uma tecla pressionada, dependendo do tipo de tecla — e cada classe tem atributos diferentes. Seu código tentou acessar `.name` em um objeto que **não tem** esse atributo.

---

## 2. As Duas Classes de Tecla

Quando o `on_press(key)` é chamado, o parâmetro `key` pode ser um objeto de **duas classes possíveis**:

### `pynput.keyboard.KeyCode`
Representa teclas **"normais"** — letras, números, símbolos, ou seja, qualquer tecla que produz um **caractere**.

| Atributo | O que é | Exemplo |
|---|---|---|
| `.char` | O caractere digitado | `'a'`, `'5'`, `'@'` |
| `.vk` | Virtual key code (código numérico do sistema operacional) | `65` (para a tecla A no Windows) |

❌ **`KeyCode` NÃO tem atributo `.name`** — é exatamente por isso que seu código quebrou.

### `pynput.keyboard.Key`
Representa teclas **especiais** — que não produzem um caractere sozinhas (Enter, Shift, Ctrl, setas, F1-F12, ESC, etc).

| Atributo | O que é | Exemplo |
|---|---|---|
| `.name` | O nome da tecla especial | `'enter'`, `'shift'`, `'esc'`, `'space'` |
| `.value` | Um `KeyCode` interno associado (em alguns casos) | — |

❌ **`Key` NÃO tem atributo `.char`** — só existe em `KeyCode`.

---

## 3. Tabela Resumo

| Tipo de tecla | Classe do objeto `key` | Atributo que existe | Atributo que **NÃO** existe |
|---|---|---|---|
| Letra, número, símbolo (`a`, `5`, `@`) | `KeyCode` | `.char` | `.name` ❌ |
| Tecla especial (`Enter`, `Shift`, `Esc`, setas) | `Key` | `.name` | `.char` ❌ |

Ou seja: **você precisa checar qual classe o objeto é antes de decidir qual atributo usar.**

---

## 4. Como Corrigir — Padrão Recomendado

### Opção A — `try/except` (a que já usávamos no `main.py` original)
```python
def on_press(key):
    try:
        print(f"Tecla pressionada: '{key.char}'")   # KeyCode
    except AttributeError:
        print(f"Tecla especial pressionada: {key}")  # Key (usa __str__, não .name diretamente)
```
Aqui, em vez de usar `.name`, usamos o próprio objeto `key` no f-string — o `Key` já tem uma representação legível via `__str__` (ex: `Key.enter`, `Key.esc`).

### Opção B — Checagem explícita com `isinstance`
```python
from pynput import keyboard

def on_press(key):
    if isinstance(key, keyboard.KeyCode):
        print(f"Tecla normal: '{key.char}'")
    elif isinstance(key, keyboard.Key):
        print(f"Tecla especial: {key.name}")
```
Essa versão é mais explícita e evita usar exceção para controle de fluxo — mais fácil de ler e de dar manutenção.

### Opção C — Função utilitária para extrair um "nome" único, seja qual for o tipo
```python
def get_key_label(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char if key.char is not None else str(key)
    return key.name

def on_press(key):
    print(f"Tecla: {get_key_label(key)}")
```

---

## 5. Por que `.char` às vezes é `None`?

Mesmo em um `KeyCode`, o `.char` pode vir como `None` em alguns casos — por exemplo, teclas mortas (acentos) ou combinações com `Ctrl` (ex: `Ctrl+C` gera um `KeyCode` cujo `.char` pode ser um caractere de controle, não a letra "c"). Por isso é sempre bom checar:

```python
if key.char is not None:
    print(key.char)
```

---

## 6. Outros Atributos Úteis do `pynput`

| Atributo/Método | Onde usar | Descrição |
|---|---|---|
| `key.vk` | `KeyCode` | Código numérico da tecla no sistema operacional (útil para distinguir teclas que geram o mesmo char, ex: teclado numérico vs. teclado normal) |
| `str(key)` | `Key` ou `KeyCode` | Representação textual (`'a'`, `Key.enter`, `Key.shift`) |
| `keyboard.Key.esc`, `keyboard.Key.enter`, etc. | Comparação | Permite comparar `key == keyboard.Key.esc` para detectar teclas especiais específicas |
| `listener.stop()` | `Listener` | Para parar o listener manualmente (alternativa a retornar `False` no callback) |

---

## 7. Exemplo Completo Corrigido

```python
from pynput import keyboard


def on_press(key):
    if isinstance(key, keyboard.KeyCode):
        # Tecla normal (letra, número, símbolo)
        char = key.char if key.char is not None else "desconhecido"
        print(f"Tecla normal pressionada: '{char}'")
    else:
        # Tecla especial (Key)
        print(f"Tecla especial pressionada: {key.name}")

    if key == keyboard.Key.esc:
        print("\nESC pressionado. Encerrando...")
        return False


def main():
    print("Escutando o teclado... (pressione ESC para sair)\n")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
```

Esse código resolve exatamente o erro que você teve, porque agora `.name` só é chamado quando o objeto realmente é da classe `Key`.