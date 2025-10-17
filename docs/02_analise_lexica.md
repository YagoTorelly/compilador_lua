# 🔍 Análise Léxica (Tokenização)

[← Anterior: Introdução](01_introducao.md) | [↑ Índice](README.md) | [Próximo: Análise Sintática →](03_analise_sintatica.md)

---

## 📋 Índice

- [O que é Análise Léxica?](#-para-iniciantes-o-que-é-análise-léxica)
- [Detalhes Técnicos](#-detalhes-técnicos)
- [Tipos de Tokens](#-tipos-de-tokens)
- [Implementação](#-implementação-do-analisadorleximoonlet)
- [Exemplos Práticos](#-exemplos-práticos)

---

## 💡 Para Iniciantes: O que é Análise Léxica?

### Definição Simples

**Análise léxica** é o processo de **quebrar o código em pedaços menores** chamados **tokens**, como separar uma frase em palavras.

### Analogia

Imagine que você está lendo um texto:

```
"O gato pulou."
```

Você naturalmente separa em: `["O", "gato", "pulou", "."]`

O analisador léxico faz o mesmo com código:

```lua
local x = 10
```

Separa em: `["local", "x", "=", "10"]`

### Por que isso é importante?

- 🎯 **Simplifica** o trabalho do próximo estágio (parsing)
- 🔍 **Identifica** elementos básicos (palavras-chave, números, operadores)
- ⚡ **Valida** caracteres inválidos
- 📝 **Ignora** espaços e comentários desnecessários

### Exemplo Visual

```
Entrada:
┌─────────────────────────────┐
│ local contador = 0          │
│                             │
│ if contador > 5 then        │
│     print("ok")             │
│ end                         │
└─────────────────────────────┘
                │
                ▼
        ANÁLISE LÉXICA
                │
                ▼
Saída (Stream de Tokens):
┌─────────────────────────────┐
│ [PALAVRA_CHAVE: "local"]    │
│ [IDENTIFICADOR: "contador"] │
│ [OPERADOR: "="]             │
│ [NUMERO: 0]                 │
│ [PALAVRA_CHAVE: "if"]       │
│ [IDENTIFICADOR: "contador"] │
│ [OPERADOR: ">"]             │
│ [NUMERO: 5]                 │
│ [PALAVRA_CHAVE: "then"]     │
│ [IDENTIFICADOR: "print"]    │
│ [SIMBOLO: "("]              │
│ [STRING: "ok"]              │
│ [SIMBOLO: ")"]              │
│ [PALAVRA_CHAVE: "end"]      │
│ [EOS]                       │
└─────────────────────────────┘
```

---

## 🔧 Detalhes Técnicos

### Localização no Projeto

```
src/lexer/lexico_moonlet.py
```

**Linhas de código:** ~174  
**Classe principal:** `AnalisadorLexicoMoonlet`

### Estratégia de Implementação

O analisador léxico do Moonlet usa uma abordagem **baseada em caracteres**:

```python
class AnalisadorLexicoMoonlet:
    def __init__(self, codigo_fonte: str):
        self.codigo = codigo_fonte + '\0'  # Adiciona sentinela
        self.linha = 1                      # Rastreamento de linha
        self.i = 0                          # Índice atual
    
    def proximo_char(self) -> str:
        """Consome próximo caractere"""
        c = self.codigo[self.i]
        self.i += 1
        return c
    
    def proximo_token(self) -> Token:
        """Retorna próximo token"""
        # Lógica de reconhecimento...
```

### Estrutura de Token

```python
class Token(NamedTuple):
    tipo: int           # IDENTIFICADOR, NUMERO, etc.
    lexema: str         # Texto original ("local", "123")
    valor: Union[...]   # Valor processado (int, float, str)
    linha: int          # Número da linha (para erros)
```

**Exemplo:**
```python
Token(
    tipo=NUMERO,
    lexema="123",
    valor=123,
    linha=5
)
```

---

## 📊 Tipos de Tokens

### Tabela Completa de Tokens

| Tipo | Valor | Descrição | Exemplos |
|------|-------|-----------|----------|
| `ERRO` | 0 | Token inválido | `@`, `$` |
| `IDENTIFICADOR` | 1 | Nome de variável/função | `x`, `contador`, `_temp` |
| `PALAVRA_CHAVE` | 2 | Palavra reservada | `if`, `while`, `local` |
| `NUMERO` | 3 | Literal numérico | `10`, `3.14` |
| `STRING` | 4 | Literal de texto | `"hello"`, `'world'` |
| `OPERADOR` | 5 | Operador aritmético/lógico | `+`, `-`, `==`, `<=` |
| `SIMBOLO_ESPECIAL` | 6 | Pontuação e delimitadores | `(`, `)`, `,`, `.` |
| `COMENTARIO` | 7 | Comentário (ignorado) | `-- texto`, `--[[ bloco ]]` |
| `EOS` | 8 | Fim do arquivo | (final do código) |

### 1. Palavras-Chave (Keywords)

Palavras reservadas da linguagem que **não podem** ser usadas como identificadores:

```python
PALAVRAS_CHAVE = {
    'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
    'function', 'goto', 'if', 'in', 'local', 'nil', 'not', 'or',
    'repeat', 'return', 'then', 'true', 'until', 'while'
}
```

**Total:** 23 palavras-chave

### 2. Identificadores

**Regra:** Começa com letra ou `_`, seguido de letras, dígitos ou `_`

```
Válidos:    x, contador, _temp, var123, _
Inválidos:  1x (começa com dígito)
            x-y (contém hífen)
```

### 3. Números

**Suportados:**
- Inteiros: `0`, `123`, `999`
- Decimais: `3.14`, `0.5`, `10.0`

**Não suportados:**
- Notação científica: `1e10`
- Hexadecimal: `0xFF`
- Binário: `0b1010`

### 4. Strings

**Delimitadores:** `"` (aspas duplas) ou `'` (aspas simples)

```lua
"Hello, World!"
'Olá, Mundo!'
```

**Limitações:**
- ❌ Sem escape sequences (`\n`, `\t`)
- ❌ Sem strings multilinha

### 5. Operadores

#### Operadores Simples (1 caractere)
```
+  -  *  /  %  ^  <  >  =  ~
```

#### Operadores Duplos (2 caracteres)
```python
OPERADORES_DUPLOS = {'==', '~=', '<=', '>=', '..'}
```

| Operador | Significado |
|----------|-------------|
| `==` | Igual a |
| `~=` | Diferente de |
| `<=` | Menor ou igual |
| `>=` | Maior ou igual |
| `..` | Concatenação de strings |

### 6. Símbolos Especiais

```python
SIMBOLOS_ESPECIAIS = '()[]{}#;:,.\\'
```

| Símbolo | Uso |
|---------|-----|
| `( )` | Agrupamento, chamadas de função |
| `[ ]` | Acesso a tabelas |
| `{ }` | Construção de tabelas |
| `#` | Operador de comprimento |
| `;` | Separador de comandos (opcional) |
| `:` | Métodos de tabelas |
| `::` | Labels para goto |
| `,` | Separador de elementos |
| `.` | Acesso a campos |
| `\` | (Reservado) |

### 7. Comentários

#### Comentário de Linha
```lua
-- Isto é um comentário de linha
local x = 10  -- Comentário após código
```

#### Comentário de Bloco
```lua
--[[
   Isto é um comentário
   que abrange múltiplas
   linhas
]]
```

**Importante:** Comentários são **ignorados** pelo parser (não geram nós na AST).

---

## 🛠️ Implementação do AnalisadorLexicoMoonlet

### Fluxo de Reconhecimento

```
proximo_token()
    │
    ├─ Espaço/Tab? ────────▶ Ignora, continua
    │
    ├─ \n (nova linha)? ───▶ Incrementa contador de linha
    │
    ├─ \0 (fim)? ──────────▶ Retorna EOS
    │
    ├─ -- (comentário)? ───▶ tratar_comentario()
    │
    ├─ letra ou _? ────────▶ tratar_identificador_ou_palavra_chave()
    │
    ├─ dígito? ────────────▶ tratar_numero()
    │
    ├─ " ou '? ────────────▶ tratar_string()
    │
    ├─ operador/símbolo? ──▶ tratar_operador_ou_simbolo()
    │
    └─ outro? ─────────────▶ Token(ERRO)
```

### Métodos Principais

#### 1. `tratar_identificador_ou_palavra_chave()`

```python
def tratar_identificador_ou_palavra_chave(self) -> Token:
    lexema = ''
    c = self.proximo_char()
    
    # Consome [a-zA-Z0-9_]
    while c.isalnum() or c == '_':
        lexema += c
        c = self.proximo_char()
    
    self.retrair()  # Devolve último char não consumido
    
    # Verifica se é palavra-chave
    if lexema in PALAVRAS_CHAVE:
        return Token(PALAVRA_CHAVE, lexema, lexema, self.linha)
    else:
        return Token(IDENTIFICADOR, lexema, lexema, self.linha)
```

**Exemplos:**
- `"local"` → `Token(PALAVRA_CHAVE, "local", ...)`
- `"contador"` → `Token(IDENTIFICADOR, "contador", ...)`

#### 2. `tratar_numero()`

```python
def tratar_numero(self) -> Token:
    lexema = ''
    tem_ponto = False
    c = self.proximo_char()
    
    # Consome [0-9] e opcionalmente um '.'
    while c.isdigit() or (c == '.' and not tem_ponto):
        if c == '.':
            tem_ponto = True
        lexema += c
        c = self.proximo_char()
    
    self.retrair()
    
    # Converte para int ou float
    if tem_ponto:
        return Token(NUMERO, lexema, float(lexema), self.linha)
    else:
        return Token(NUMERO, lexema, int(lexema), self.linha)
```

**Exemplos:**
- `"123"` → `Token(NUMERO, "123", 123, ...)`
- `"3.14"` → `Token(NUMERO, "3.14", 3.14, ...)`

#### 3. `tratar_string()`

```python
def tratar_string(self, delimitador: str) -> Token:
    lexema = delimitador  # " ou '
    c = self.proximo_char()
    
    # Consome até encontrar delimitador de fechamento
    while c != delimitador and c != '\0':
        lexema += c
        c = self.proximo_char()
    
    if c == '\0':
        # String não terminada!
        return Token(ERRO, lexema, "String não terminada", self.linha)
    
    lexema += delimitador  # Adiciona " ou ' de fechamento
    valor_string = lexema[1:-1]  # Remove delimitadores
    
    return Token(STRING, lexema, valor_string, self.linha)
```

**Exemplos:**
- `"hello"` → `Token(STRING, '"hello"', "hello", ...)`
- `'world'` → `Token(STRING, "'world'", "world", ...)`

#### 4. `tratar_comentario()`

```python
def tratar_comentario(self) -> Token:
    lexema = '--'
    self.proximo_char()  # Consome segundo '-'
    
    # Verifica se é comentário de bloco --[[
    if self.codigo[self.i] == '[' and self.codigo[self.i+1] == '[':
        lexema += '[['
        self.i += 2
        
        # Consome até encontrar ]]
        while not (self.codigo[self.i] == ']' and self.codigo[self.i+1] == ']'):
            char = self.proximo_char()
            if char == '\n':
                self.linha += 1
            lexema += char
        
        lexema += ']]'
        self.i += 2
        return Token(COMENTARIO, lexema, None, self.linha)
    else:
        # Comentário de linha: consome até \n
        while self.codigo[self.i] not in ['\n', '\0']:
            lexema += self.proximo_char()
        
        return Token(COMENTARIO, lexema, None, self.linha)
```

#### 5. `tratar_operador_ou_simbolo()`

```python
def tratar_operador_ou_simbolo(self) -> Token:
    c1 = self.proximo_char()
    c2 = self.codigo[self.i]  # Lookahead sem consumir
    
    # Trata :: (label)
    if c1 == ':' and c2 == ':':
        self.proximo_char()
        return Token(SIMBOLO_ESPECIAL, '::', None, self.linha)
    
    # Trata operadores duplos: ==, ~=, <=, >=, ..
    lexema = c1 + c2
    if lexema in OPERADORES_DUPLOS:
        self.proximo_char()  # Consome segundo caractere
        return Token(OPERADOR, lexema, None, self.linha)
    
    # Operador simples
    if c1 in ['+', '-', '*', '/', '%', '^', '<', '>', '=', '~']:
        return Token(OPERADOR, c1, None, self.linha)
    
    # Símbolo especial
    if c1 in SIMBOLOS_ESPECIAIS:
        return Token(SIMBOLO_ESPECIAL, c1, None, self.linha)
    
    # Caractere desconhecido
    return Token(ERRO, c1, None, self.linha)
```

---

## 📝 Exemplos Práticos

### Exemplo 1: Código Simples

**Entrada:**
```lua
local x = 10
```

**Saída (Tokens):**
```
Linha 1 | PALAVRA_CHAVE      | 'local'
Linha 1 | IDENTIFICADOR      | 'x'
Linha 1 | OPERADOR           | '='
Linha 1 | NUMERO             | '10'
Linha 1 | EOS                | ''
```

### Exemplo 2: Estrutura Condicional

**Entrada:**
```lua
if x > 5 then
    print("ok")
end
```

**Saída (Tokens):**
```
Linha 1 | PALAVRA_CHAVE      | 'if'
Linha 1 | IDENTIFICADOR      | 'x'
Linha 1 | OPERADOR           | '>'
Linha 1 | NUMERO             | '5'
Linha 1 | PALAVRA_CHAVE      | 'then'
Linha 2 | IDENTIFICADOR      | 'print'
Linha 2 | SIMBOLO_ESPECIAL   | '('
Linha 2 | STRING             | '"ok"'
Linha 2 | SIMBOLO_ESPECIAL   | ')'
Linha 3 | PALAVRA_CHAVE      | 'end'
Linha 3 | EOS                | ''
```

### Exemplo 3: Comentários

**Entrada:**
```lua
-- Comentário de linha
local x = 10  -- Após código

--[[
  Comentário de bloco
  multilinha
]]
```

**Saída (Tokens):**
```
Linha 1 | COMENTARIO         | '-- Comentário de linha'
Linha 2 | PALAVRA_CHAVE      | 'local'
Linha 2 | IDENTIFICADOR      | 'x'
Linha 2 | OPERADOR           | '='
Linha 2 | NUMERO             | '10'
Linha 2 | COMENTARIO         | '-- Após código'
Linha 4 | COMENTARIO         | '--[[...(multilinha)...]]'
Linha 7 | EOS                | ''
```

**Nota:** Durante o parsing, comentários são **ignorados** automaticamente.

### Exemplo 4: Operadores Duplos

**Entrada:**
```lua
x == 10
y ~= 5
z <= 3
nome = "João" .. " Silva"
```

**Saída (Tokens):**
```
Linha 1 | IDENTIFICADOR      | 'x'
Linha 1 | OPERADOR           | '=='
Linha 1 | NUMERO             | '10'
Linha 2 | IDENTIFICADOR      | 'y'
Linha 2 | OPERADOR           | '~='
Linha 2 | NUMERO             | '5'
Linha 3 | IDENTIFICADOR      | 'z'
Linha 3 | OPERADOR           | '<='
Linha 3 | NUMERO             | '3'
Linha 4 | IDENTIFICADOR      | 'nome'
Linha 4 | OPERADOR           | '='
Linha 4 | STRING             | '"João"'
Linha 4 | OPERADOR           | '..'
Linha 4 | STRING             | '" Silva"'
```

### Exemplo 5: Erro Léxico

**Entrada:**
```lua
local x = @10
```

**Saída (Tokens):**
```
Linha 1 | PALAVRA_CHAVE      | 'local'
Linha 1 | IDENTIFICADOR      | 'x'
Linha 1 | OPERADOR           | '='
Linha 1 | ERRO               | '@'     ⚠️ ERRO LÉXICO
Linha 1 | NUMERO             | '10'
Linha 1 | EOS                | ''
```

**Mensagem de erro:**
```
⚠️ ERRO LÉXICO: Caractere inválido '@' na linha 1
```

---

## 🎯 Diagrama de Estados (Simplificado)

```
         ┌─────────────────┐
         │     INÍCIO      │
         └────────┬────────┘
                  │
       ┌──────────┴──────────┐
       │                     │
    [letra/_]            [dígito]
       │                     │
       ▼                     ▼
 ┌──────────────┐    ┌──────────────┐
 │ IDENTIFICADOR│    │    NUMERO    │
 │  ou KEYWORD  │    │  (int/float) │
 └──────────────┘    └──────────────┘
       │                     │
       │  ┌─────────────────┘
       │  │   [" ou ']
       │  │     │
       │  │     ▼
       │  │ ┌──────────────┐
       │  │ │    STRING    │
       │  │ └──────────────┘
       │  │
       │  │  [- seguido de -]
       │  │     │
       │  │     ▼
       │  │ ┌──────────────┐
       │  │ │  COMENTARIO  │
       │  │ └──────────────┘
       │  │
       │  │  [operador/símbolo]
       │  │     │
       │  │     ▼
       │  │ ┌──────────────┐
       │  └▶│OPERADOR/SIMB.│
       │    └──────────────┘
       │
       └──────────▶ TOKEN FINAL
```

---

## 🧪 Testando o Analisador Léxico

### Como Executar

```python
from src.lexer.lexico_moonlet import AnalisadorLexicoMoonlet, EOS, TOKEN_MAP

# Código de teste
codigo = """
local x = 10
if x > 5 then
    print("ok")
end
"""

# Criar analisador
lexer = AnalisadorLexicoMoonlet(codigo)

# Iterar sobre tokens
token = lexer.proximo_token()
while token.tipo != EOS:
    print(f"Linha {token.linha:02d} | {TOKEN_MAP[token.tipo]:<18} | '{token.lexema}'")
    token = lexer.proximo_token()

print(f"Linha {token.linha:02d} | {TOKEN_MAP[token.tipo]:<18} | '{token.lexema}'")
```

### Saída Esperada

```
Linha 02 | PALAVRA_CHAVE      | 'local'
Linha 02 | IDENTIFICADOR      | 'x'
Linha 02 | OPERADOR           | '='
Linha 02 | NUMERO             | '10'
Linha 03 | PALAVRA_CHAVE      | 'if'
Linha 03 | IDENTIFICADOR      | 'x'
Linha 03 | OPERADOR           | '>'
Linha 03 | NUMERO             | '5'
Linha 03 | PALAVRA_CHAVE      | 'then'
Linha 04 | IDENTIFICADOR      | 'print'
Linha 04 | SIMBOLO_ESPECIAL   | '('
Linha 04 | STRING             | '"ok"'
Linha 04 | SIMBOLO_ESPECIAL   | ')'
Linha 05 | PALAVRA_CHAVE      | 'end'
Linha 06 | EOS                | ''
```

---

## 🔍 Casos Especiais

### 1. Números com Ponto Decimal

```lua
x = 3.14
```

**Token gerado:**
```python
Token(NUMERO, "3.14", 3.14, linha)
```

### 2. Strings com Diferentes Delimitadores

```lua
s1 = "aspas duplas"
s2 = 'aspas simples'
```

**Ambos geram:** `Token(STRING, ...)`

### 3. Operador `..` vs `.`

```lua
s = "hello" .. "world"  -- OPERADOR: '..'
t.campo                  -- SIMBOLO: '.' + IDENTIFICADOR: 'campo'
```

### 4. Comentários Aninhados (Não Suportados)

```lua
--[[ 
  Comentário externo
  --[[ Comentário interno ]]  ❌ Termina aqui!
  Isto NÃO é mais comentário
]]
```

**Comportamento:** Fecha no primeiro `]]` encontrado.

---

## 📚 Conceitos Avançados

### Lookahead

O lexer usa **lookahead de 1 caractere** para reconhecer operadores duplos:

```python
c1 = self.proximo_char()        # Consome
c2 = self.codigo[self.i]         # Espia (não consome)

if c1 + c2 == '==':              # Operador duplo
    self.proximo_char()          # Agora consome c2
    return Token(OPERADOR, '==', ...)
```

### Sentinela (`\0`)

O lexer adiciona `\0` ao final do código para evitar verificações de bounds:

```python
self.codigo = codigo_fonte + '\0'
```

Assim, sempre há um caractere para ler.

### Rastreamento de Linha

Essencial para mensagens de erro:

```python
if c == '\n':
    self.linha += 1
```

---

## ✅ Resumo

### O que o Analisador Léxico faz?

✅ Quebra código em tokens  
✅ Identifica palavras-chave  
✅ Reconhece números (int e float)  
✅ Processa strings  
✅ Detecta operadores (simples e duplos)  
✅ Ignora comentários e espaços  
✅ Rastreia números de linha  
✅ Reporta erros léxicos  

### O que ele NÃO faz?

❌ Verificar sintaxe (isso é trabalho do parser)  
❌ Entender significado (isso é análise semântica)  
❌ Gerar código  

---

## 🎯 Próximos Passos

Agora que você entende como o código é quebrado em tokens, vamos ver como esses tokens são **organizados em uma estrutura** (árvore sintática):

[▶️ Próximo: Análise Sintática →](03_analise_sintatica.md)

Ou explore outros tópicos:

- [📘 Voltar à Introdução](01_introducao.md)
- [📚 Ver Exemplos Práticos](08_exemplos_uso.md)
- [🔧 Referência Técnica Completa](09_referencia_tecnica.md)

---

[← Anterior: Introdução](01_introducao.md) | [↑ Índice](README.md) | [Próximo: Análise Sintática →](03_analise_sintatica.md)

