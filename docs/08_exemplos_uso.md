# 📚 Exemplos de Uso

[← Anterior: Estrutura do Projeto](07_estrutura_projeto.md) | [↑ Índice](README.md) | [Próximo: Referência Técnica →](09_referencia_tecnica.md)

---

## 📋 Índice

- [Como Executar](#-como-executar-o-compilador)
- [Exemplo Básico](#-exemplo-1-programa-básico)
- [Estruturas de Controle](#-exemplo-2-estruturas-de-controle)
- [Laços](#-exemplo-3-laços)
- [Funções](#-exemplo-4-funções)
- [Análise de Erros](#-exemplo-5-análise-de-erros)

---

## 🚀 Como Executar o Compilador

### Pré-requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd compilador_lua
```

### Executar com Arquivo

```bash
# Sintaxe básica
python main.py <arquivo.moonlet>

# Exemplo
python main.py examples/exemplo.moonlet
```

### Executar Exemplos Fornecidos

```bash
# Exemplo básico
python main.py examples/exemplo.moonlet

# Estrutura IF
python main.py examples/mepa_if.moonlet

# Laço WHILE
python main.py examples/mepa_while.moonlet

# Laço FOR
python main.py examples/mepa_for.moonlet

# Erro semântico
python main.py examples/semantico_nao_declarada.moonlet
```

---

## 📝 Exemplo 1: Programa Básico

### Código: `exemplo_basico.moonlet`

```lua
-- Programa básico em Moonlet
local x = 10

if x > 5 then
    print("x é maior que 5")
end
```

### Executar

```bash
python main.py exemplo_basico.moonlet
```

### Saída Completa

#### 1. Análise Léxica

```
1. ANÁLISE LÉXICA
--------------------------------------------------
Linha 01 | COMENTARIO         | '-- Programa básico em Moonlet'
Linha 02 | PALAVRA_CHAVE      | 'local'
Linha 02 | IDENTIFICADOR      | 'x'
Linha 02 | OPERADOR           | '='
Linha 02 | NUMERO             | '10'
Linha 04 | PALAVRA_CHAVE      | 'if'
Linha 04 | IDENTIFICADOR      | 'x'
Linha 04 | OPERADOR           | '>'
Linha 04 | NUMERO             | '5'
Linha 04 | PALAVRA_CHAVE      | 'then'
Linha 05 | IDENTIFICADOR      | 'print'
Linha 05 | SIMBOLO_ESPECIAL   | '('
Linha 05 | STRING             | '"x é maior que 5"'
Linha 05 | SIMBOLO_ESPECIAL   | ')'
Linha 06 | PALAVRA_CHAVE      | 'end'
Linha 07 | EOS                | ''

Total de tokens: 15
```

#### 2. Análise Sintática

```
2. ANÁLISE SINTÁTICA
--------------------------------------------------
✓ Análise sintática concluída com sucesso
```

#### 3. AST (Árvore Sintática Abstrata)

```
3. ÁRVORE SINTÁTICA ABSTRATA (AST)
--------------------------------------------------
PROGRAMA
  local DECLARAÇÃO: x
    VALOR:
      LITERAL (number): 10
  IF-STATEMENT
    IF:
      CONDIÇÃO:
        OPERAÇÃO: >
          ESQUERDA:
            IDENTIFICADOR: x
          DIREITA:
            LITERAL (number): 5
      BLOCO:
        CHAMADA: print
          ARGUMENTOS:
            LITERAL (string): x é maior que 5
```

#### 4. Código MEPA Gerado

```
4. CÓDIGO INTERMEDIÁRIO (MEPA)
--------------------------------------------------
; decl local x @ 0
CRCT 10
ARMZ 0
CRVL 0
CRCT 5
CMME
DSVF I1
DSVS I0
I1:
I0:
```

---

## 📝 Exemplo 2: Estruturas de Controle

### Código: `exemplo_if_else.moonlet`

```lua
local x = 5

if x < 5 then
    print("menor")
elseif x == 5 then
    print("igual")
else
    print("maior")
end
```

### AST Gerado

```
PROGRAMA
  local DECLARAÇÃO: x
    VALOR:
      LITERAL (number): 5
  IF-STATEMENT
    IF:
      CONDIÇÃO:
        OPERAÇÃO: <
          ESQUERDA:
            IDENTIFICADOR: x
          DIREITA:
            LITERAL (number): 5
      BLOCO:
        CHAMADA: print
          ARGUMENTOS:
            LITERAL (string): menor
    ELSEIF 1:
      CONDIÇÃO:
        OPERAÇÃO: ==
          ESQUERDA:
            IDENTIFICADOR: x
          DIREITA:
            LITERAL (number): 5
      BLOCO:
        CHAMADA: print
          ARGUMENTOS:
            LITERAL (string): igual
    ELSE:
      CHAMADA: print
        ARGUMENTOS:
          LITERAL (string): maior
```

### Código MEPA Gerado

```assembly
; decl local x @ 0
CRCT 5
ARMZ 0

; IF x < 5
CRVL 0
CRCT 5
CMME
DSVF I1
; (print menor)
DSVS I0

; ELSEIF x == 5
I1:
CRVL 0
CRCT 5
CMIG
DSVF I2
; (print igual)
DSVS I0

; ELSE
I2:
; (print maior)

; FIM
I0:
```

---

## 📝 Exemplo 3: Laços

### 3.1 Laço WHILE

#### Código: `exemplo_while.moonlet`

```lua
local x = 0

while x < 3 do
    x = x + 1
end
```

#### AST

```
PROGRAMA
  local DECLARAÇÃO: x
    VALOR:
      LITERAL (number): 0
  WHILE-LOOP
    CONDIÇÃO:
      OPERAÇÃO: <
        ESQUERDA:
          IDENTIFICADOR: x
        DIREITA:
          LITERAL (number): 3
    CORPO:
      ATRIBUIÇÃO:
        VARIÁVEL:
          IDENTIFICADOR: x
        VALOR:
          OPERAÇÃO: +
            ESQUERDA:
              IDENTIFICADOR: x
            DIREITA:
              LITERAL (number): 1
```

#### Código MEPA

```assembly
; decl local x @ 0
CRCT 0
ARMZ 0

; WHILE
W0:
CRVL 0
CRCT 3
CMME
DSVF W1

; Corpo
CRVL 0
CRCT 1
SOMA
ARMZ 0

DSVS W0
W1:
```

### 3.2 Laço FOR

#### Código: `exemplo_for.moonlet`

```lua
local i = 1
for i = 1, 3 do
    i = i + 1
end
```

#### Código MEPA

```assembly
; decl local i @ 0
CRCT 1
ARMZ 0

; FOR
CRCT 1
ARMZ 0
CRCT 3
ARMZ 1
CRCT 1
ARMZ 2

F0:
CRVL 0
CRVL 1
CMEG
DSVF F1

; Corpo
CRVL 0
CRCT 1
SOMA
ARMZ 0

; Incremento
CRVL 0
CRVL 2
SOMA
ARMZ 0

DSVS F0
F1:
```

### 3.3 Laço REPEAT

#### Código: `exemplo_repeat.moonlet`

```lua
local x = 0

repeat
    x = x + 1
until x > 3
```

#### Código MEPA

```assembly
; decl local x @ 0
CRCT 0
ARMZ 0

; REPEAT
R0:

; Corpo
CRVL 0
CRCT 1
SOMA
ARMZ 0

; Condição (repete enquanto falso)
CRVL 0
CRCT 3
CMMA
DSVF R0
```

---

## 📝 Exemplo 4: Funções

### Código: `exemplo_funcao.moonlet`

```lua
function soma(a, b)
    return a + b
end

local resultado = soma(5, 3)
```

### AST

```
PROGRAMA
  FUNÇÃO: soma
    PARÂMETROS: a, b
    CORPO:
      RETURN
        OPERAÇÃO: +
          ESQUERDA:
            IDENTIFICADOR: a
          DIREITA:
            IDENTIFICADOR: b
  local DECLARAÇÃO: resultado
    VALOR:
      CHAMADA: soma
        ARGUMENTOS:
          LITERAL (number): 5
          LITERAL (number): 3
```

---

## 📝 Exemplo 5: Análise de Erros

### 5.1 Erro Sintático

#### Código: `erro_sintatico.moonlet`

```lua
-- Falta 'then'
if x > 5
    print("ok")
end
```

#### Saída

```
1. ANÁLISE LÉXICA
--------------------------------------------------
Linha 02 | PALAVRA_CHAVE      | 'if'
Linha 02 | IDENTIFICADOR      | 'x'
Linha 02 | OPERADOR           | '>'
Linha 02 | NUMERO             | '5'
Linha 03 | IDENTIFICADOR      | 'print'
Linha 03 | SIMBOLO_ESPECIAL   | '('
Linha 03 | STRING             | '"ok"'
Linha 03 | SIMBOLO_ESPECIAL   | ')'
Linha 04 | PALAVRA_CHAVE      | 'end'
Linha 05 | EOS                | ''

Total de tokens: 9

2. ANÁLISE SINTÁTICA
--------------------------------------------------
           ⚠️ ERRO SINTÁTICO: Erro sintático: Token esperado não encontrado. 
              Esperado 'then', encontrado 'print' em linha 3, coluna 0

⚠️ Erros encontrados durante a análise:
=== ERROS ENCONTRADOS ===
1. Erro sintático: Token esperado não encontrado. 
   Esperado 'then', encontrado 'print' em linha 3, coluna 0
```

### 5.2 Erro Semântico: Variável Não Declarada

#### Código: `erro_nao_declarada.moonlet`

```lua
-- y nunca foi declarado
if y > 0 then
    y = y + 1
end
```

#### Saída

```
2. ANÁLISE SINTÁTICA
--------------------------------------------------
           ⚠️ ERRO SINTÁTICO: Erro semântico: Variável 'y' não declarada em linha 2, coluna 0

✗ Erro na análise sintática: Variável 'y' não declarada
```

### 5.3 Erro Semântico: Declaração Duplicada

#### Código: `erro_duplicada.moonlet`

```lua
local a = 1
local a = 2  -- ❌ 'a' já foi declarado
```

#### Saída

```
2. ANÁLISE SINTÁTICA
--------------------------------------------------
           ⚠️ ERRO SINTÁTICO: Erro semântico: Variável 'a' já declarada em linha 2, coluna 0

✗ Erro na análise sintática: Variável 'a' já declarada
```

---

## 📝 Exemplo 6: Expressões Complexas

### Código: `exemplo_expressoes.moonlet`

```lua
local a = 2 + 3 * 4      -- Precedência: 2 + (3 * 4) = 14
local b = (2 + 3) * 4    -- Parênteses: (2 + 3) * 4 = 20
local c = 10 / 2 - 3     -- Esquerda para direita: (10 / 2) - 3 = 2
```

### Código MEPA para `a = 2 + 3 * 4`

```assembly
; decl local a @ 0
CRCT 2
CRCT 3
CRCT 4
MULT        ; 3 * 4 = 12
SOMA        ; 2 + 12 = 14
ARMZ 0
```

**Explicação da Precedência:**
- `*` tem maior precedência que `+`
- Logo, `3 * 4` é calculado primeiro (12)
- Depois soma com 2: `2 + 12 = 14`

---

## 📝 Exemplo 7: Operadores de Comparação

### Código: `exemplo_comparacao.moonlet`

```lua
local x = 10

if x == 10 then
    print("igual a 10")
end

if x ~= 5 then
    print("diferente de 5")
end

if x >= 10 then
    print("maior ou igual a 10")
end
```

### Código MEPA (trecho do primeiro IF)

```assembly
; x == 10
CRVL 0      ; Carrega x
CRCT 10     ; Carrega 10
CMIG        ; Compara igual
DSVF I1     ; Se falso (0), pula
; (print)
DSVS I0
I1:
I0:
```

---

## 📝 Exemplo 8: Código Completo

### Código: `programa_completo.moonlet`

```lua
-- Programa completo demonstrando várias funcionalidades
local contador = 0
local limite = 5

-- Laço while
while contador < limite do
    contador = contador + 1
    
    -- Estrutura if aninhada
    if contador == 3 then
        print("Meio do caminho!")
    end
end

-- Laço for
for i = 1, 3, 1 do
    print("Iteração for")
end

-- Estrutura condicional completa
if contador > 5 then
    print("Passou do limite")
elseif contador == 5 then
    print("Exatamente no limite")
else
    print("Abaixo do limite")
end
```

### Análise

Este programa demonstra:
- ✅ Declaração de variáveis
- ✅ Laço `while`
- ✅ Laço `for` com passo
- ✅ Estrutura `if-elseif-else`
- ✅ `if` aninhado
- ✅ Operadores relacionais
- ✅ Expressões aritméticas
- ✅ Chamadas de função

---

## 🧪 Testando Programaticamente

### Código Python

```python
from src.lexer.lexico_moonlet import AnalisadorLexicoMoonlet
from src.parser.sintatico_moonlet import AnalisadorSintaticoMoonlet
from src.ast.compilador_moonlet import ImpressorAST

# Código Moonlet
codigo = """
local x = 10
if x > 5 then
    print("ok")
end
"""

# Análise léxica
print("=== TOKENS ===")
lexer = AnalisadorLexicoMoonlet(codigo)
token = lexer.proximo_token()
while token.tipo != 8:  # EOS
    print(f"{token.tipo} | {token.lexema}")
    token = lexer.proximo_token()

# Análise sintática
print("\n=== AST ===")
lexer = AnalisadorLexicoMoonlet(codigo)
parser = AnalisadorSintaticoMoonlet(lexer)
ast = parser.analisar()

# Imprimir AST
impressor = ImpressorAST()
ast.accept(impressor)

# Código MEPA
print("\n=== CÓDIGO MEPA ===")
for instr in parser.codigo_mepa:
    print(instr)
```

---

## 📊 Comparação de Saídas

### Entrada vs Saída

| Código Moonlet | Tokens | Nós AST | Instruções MEPA |
|----------------|--------|---------|-----------------|
| `local x = 10` | 4 | 1 | 2 |
| `if...end` | 5+ | 1 | 4+ |
| `while...end` | 5+ | 1 | 5+ |
| `for...end` | 7+ | 1 | 8+ |

---

## 🎯 Dicas Práticas

### 1. Debugar Análise Léxica

Adicione prints no lexer para ver tokens sendo gerados:

```python
lexer = AnalisadorLexicoMoonlet(codigo)
while True:
    token = lexer.proximo_token()
    print(f"Token: {token}")
    if token.tipo == EOS:
        break
```

### 2. Visualizar AST

Use o impressor fornecido:

```python
impressor = ImpressorAST()
ast.accept(impressor)
```

### 3. Analisar Código MEPA

O código MEPA está em `parser.codigo_mepa`:

```python
for i, instr in enumerate(parser.codigo_mepa):
    print(f"{i:3d}: {instr}")
```

### 4. Tratar Erros

Verifique o relatório de erros:

```python
if parser.relatorio_erros.tem_erros():
    parser.relatorio_erros.imprimir_relatorio()
```

---

## ✅ Resumo

### Comandos Principais

```bash
# Executar arquivo
python main.py <arquivo.moonlet>

# Executar exemplos
python main.py examples/exemplo.moonlet
python main.py examples/mepa_if.moonlet
python main.py examples/mepa_while.moonlet
```

### Estrutura de Saída

1. **Análise Léxica** - Lista de tokens
2. **Análise Sintática** - Status
3. **AST** - Árvore sintática
4. **Código MEPA** - Instruções geradas

---

## 🎯 Próximos Passos

Agora que você viu exemplos práticos, consulte a **referência técnica completa**:

[▶️ Próximo: Referência Técnica →](09_referencia_tecnica.md)

Ou explore outros tópicos:

- [🏗️ Voltar à Estrutura do Projeto](07_estrutura_projeto.md)
- [📘 Voltar à Introdução](01_introducao.md)
- [↑ Voltar ao Índice](README.md)

---

[← Anterior: Estrutura do Projeto](07_estrutura_projeto.md) | [↑ Índice](README.md) | [Próximo: Referência Técnica →](09_referencia_tecnica.md)

