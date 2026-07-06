# Markdown — Sintaxe e Dicas

## Títulos

```markdown
# H1
## H2
### H3
#### H4
```

Sempre com espaço depois do `#`. Use só um `#` (H1) por documento, geralmente o título principal.

## Ênfase

```markdown
*itálico* ou _itálico_
**negrito** ou __negrito__
***negrito itálico***
~~riscado~~
```

## Parágrafos e quebra de linha

- Parágrafos são separados por **linha em branco**.
- Pra quebrar linha sem criar novo parágrafo, termine a linha com **dois espaços** ou use `<br>`.

```markdown
Linha 1  
Linha 2 (funciona por causa dos 2 espaços no fim da linha 1)
```

## Listas

**Não ordenada** — pode usar `-`, `*` ou `+` (escolha um e mantenha consistente):

```markdown
- item 1
- item 2
  - subitem (indente com 2 espaços)
```

**Ordenada**:

```markdown
1. primeiro
2. segundo
3. terceiro
```

Dica: em listas ordenadas, o número real não importa muito — pode escrever `1.` em todos os itens que o Markdown numera automaticamente.

**Checklist** (funciona no GitHub):

```markdown
- [x] tarefa feita
- [ ] tarefa pendente
```

## Links

```markdown
[texto do link](https://exemplo.com)
[texto do link](https://exemplo.com "título ao passar o mouse")
```

Link de referência (bom para textos longos, evita poluir):

```markdown
[texto][1]

[1]: https://exemplo.com
```

## Imagens

```markdown
![texto alternativo](caminho-ou-url.png)
![texto alternativo](caminho-ou-url.png "título")
```

Igual link, mas com `!` na frente.

## Código

Inline: `` `código` ``

Bloco com destaque de sintaxe (indica a linguagem depois dos três acentos):

````markdown
```python
def ola():
    print("oi")
```
````

## Citação

```markdown
> texto citado
> continuação da citação
>> citação aninhada
```

## Linha horizontal

```markdown
---
```

(também funciona com `***` ou `___`)

## Tabelas

```markdown
| Coluna A | Coluna B |
|----------|----------|
| dado 1   | dado 2   |
```

Alinhamento de coluna:

```markdown
| Esquerda | Centro | Direita |
|:---------|:------:|--------:|
| a        |   b    |       c |
```

## Escapando caracteres

Se quiser mostrar um símbolo especial sem que ele vire formatação, use `\` antes:

```markdown
\*isso não vira itálico\*
```

## Notas de rodapé (suportado no GitHub e outros)

```markdown
Aqui vai um texto com nota[^1].

[^1]: Isso é a nota de rodapé.
```

## Dicas rápidas que fazem diferença

1. **Sempre deixe linha em branco** antes e depois de listas, títulos e blocos de código — evita bug de renderização.
2. **Seja consistente** com `-` vs `*` em listas (o linter vai reclamar se misturar).
3. `**negrito**` funciona melhor que `__negrito__` em texto misto com `_underscore_variavel_`, porque evita confundir com nomes de variáveis.
4. Em blocos de código, **sempre especifique a linguagem** (` ```python `, ` ```bash `) — ativa o highlight e deixa mais legível.
5. Para linkar uma seção do mesmo documento: `[texto](#nome-do-titulo-em-minusculo-com-hifen)`.
6. HTML puro funciona dentro de Markdown quando precisar de algo que a sintaxe não cobre (ex: `<br>`, `<sub>`, `<sup>`).
