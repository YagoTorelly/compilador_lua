# 📘 Introdução ao Compilador Moonlet

[← Voltar ao Índice](README.md) | [Próximo: Análise Léxica →](02_analise_lexica.md)

---

## 🎯 O que é Moonlet?

**Moonlet** é um subconjunto simplificado da linguagem **Lua**, criado para fins educacionais. Ele mantém a sintaxe familiar de Lua, mas com um conjunto reduzido de funcionalidades, tornando-o ideal para aprender sobre construção de compiladores.

### Exemplo de Código Moonlet

```lua
-- Declaração de variável
local contador = 0

-- Estrutura condicional
if contador == 0 then
    print("Iniciando contagem")
end

-- Laço de repetição
while contador < 5 do
    contador = contador + 1
    print("Contador: " .. contador)
end
```

---

## 💡 Para Iniciantes: O que é um Compilador?

### Definição Simples

Um **compilador** é um programa que traduz código escrito em uma linguagem de programação (como Moonlet) para outra forma que o computador possa executar.

### Analogia

Pense em um compilador como um **tradutor multilíngue**:
- 📝 **Entrada**: Código em Moonlet (linguagem que humanos entendem)
- 🔄 **Processamento**: Análise e tradução
- ⚙️ **Saída**: Código MEPA (linguagem que a máquina entende)

### As 4 Fases da Compilação

```
┌─────────────────┐
│  Código Fonte   │  local x = 10
│   (Moonlet)     │  if x > 5 then...
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  1️⃣ ANÁLISE     │  Divide em "pedaços" (tokens)
│     LÉXICA      │  [local, x, =, 10, if, ...]
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2️⃣ ANÁLISE     │  Entende a estrutura
│    SINTÁTICA    │  (cria árvore sintática)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3️⃣ ANÁLISE     │  Verifica significado
│    SEMÂNTICA    │  (x foi declarado? tipos corretos?)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4️⃣ GERAÇÃO     │  Produz código final
│    DE CÓDIGO    │  (instruções MEPA)
└─────────────────┘
```

#### 1️⃣ Análise Léxica (Tokenização)

**O que faz?** Quebra o código em "palavras" chamadas **tokens**.

**Exemplo:**
```lua
local x = 10
```

Se torna:
```
[PALAVRA_CHAVE: "local"]
[IDENTIFICADOR: "x"]
[OPERADOR: "="]
[NUMERO: 10]
```

#### 2️⃣ Análise Sintática (Parsing)

**O que faz?** Verifica se a ordem das palavras faz sentido e cria uma **árvore sintática**.

**Exemplo:**
```lua
x = 5 + 3
```

Se torna uma árvore:
```
    ATRIBUIÇÃO
      /     \
     x       +
            / \
           5   3
```

#### 3️⃣ Análise Semântica

**O que faz?** Verifica se o código faz **sentido**.

**Exemplos de erros semânticos:**
```lua
-- ❌ ERRO: variável não declarada
if y > 0 then  -- y nunca foi declarada!
    print("ok")
end

-- ❌ ERRO: declaração duplicada
local a = 1
local a = 2  -- a já foi declarada!
```

#### 4️⃣ Geração de Código

**O que faz?** Traduz para código de máquina (no nosso caso, **MEPA**).

**Exemplo:**
```lua
local x = 10
```

Se torna:
```assembly
CRCT 10      ; Carrega constante 10
ARMZ 0       ; Armazena no endereço 0 (variável x)
```

---

## 🔧 Detalhes Técnicos: Arquitetura do Compilador Moonlet

### Visão Geral da Arquitetura

```
┌──────────────────────────────────────────────────────────┐
│                    main.py                                │
│            (Ponto de Entrada do Compilador)               │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│              AnalisadorMoonlet                            │
│          (src/ast/compilador_moonlet.py)                  │
│    - Coordena todas as fases                              │
│    - Imprime AST                                          │
│    - Exibe código MEPA                                    │
└──────────────────┬───────────────────────────────────────┘
                   │
      ┌────────────┴────────────┐
      │                         │
      ▼                         ▼
┌─────────────────┐   ┌─────────────────────┐
│ AnalisadorLexico│   │ AnalisadorSintatico │
│   Moonlet       │──▶│      Moonlet        │
│ (lexico_moonlet)│   │ (sintatico_moonlet) │
└─────────────────┘   └──────────┬──────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
            ┌──────────────┐        ┌────────────────┐
            │ Nós da AST   │        │ Tabela de      │
            │ (15 tipos)   │        │ Símbolos       │
            └──────────────┘        └────────────────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │  Geração MEPA    │
                       │  (integrada)     │
                       └──────────────────┘
```

### Componentes Principais

#### 1. **main.py** - Ponto de Entrada
- Lê arquivo de entrada
- Instancia o compilador
- Exibe resultados

#### 2. **AnalisadorLexicoMoonlet** (`src/lexer/lexico_moonlet.py`)
- **Responsabilidade**: Tokenização
- **Entrada**: String com código fonte
- **Saída**: Stream de tokens
- **Linhas de código**: ~174

#### 3. **AnalisadorSintaticoMoonlet** (`src/parser/sintatico_moonlet.py`)
- **Responsabilidade**: Parsing + Semântica + Geração de código
- **Entrada**: Lexer
- **Saída**: AST + Código MEPA
- **Linhas de código**: ~796
- **Estratégia**: Recursive Descent Parser

#### 4. **Sistema de Erros** (`src/errors/erros_moonlet.py`)
- **Tipos de erro**: Léxico, Sintático, Semântico
- **Recuperação**: Estratégias de panic-mode
- **Relatórios**: Formatação amigável

#### 5. **Nós da AST** (dentro de `sintatico_moonlet.py`)
- 15 tipos de nós diferentes
- Pattern Visitor para travessia
- Representam estruturas da linguagem

### Fluxo de Execução

```python
# 1. Entrada
with open('exemplo.moonlet', 'r') as f:
    codigo = f.read()

# 2. Análise Léxica
lexer = AnalisadorLexicoMoonlet(codigo)

# 3. Análise Sintática (inclui semântica)
parser = AnalisadorSintaticoMoonlet(lexer)
ast = parser.analisar()

# 4. Geração de código (já feita durante parsing)
codigo_mepa = parser.codigo_mepa

# 5. Impressão da AST
impressor = ImpressorAST()
ast.accept(impressor)

# 6. Exibir código MEPA
for instrucao in codigo_mepa:
    print(instrucao)
```

---

## 🎨 Decisões de Design

### 1. **Parser Integrado**

**Decisão:** O analisador sintático também faz análise semântica e geração de código.

**Vantagens:**
- ✅ Simplicidade de implementação
- ✅ Menos passadas sobre a árvore
- ✅ Mais eficiente para projeto educacional

**Desvantagens:**
- ❌ Menos modular
- ❌ Dificulta otimizações posteriores

### 2. **AST com Pattern Visitor**

**Decisão:** Nós da AST implementam método `accept()` para padrão Visitor.

**Vantagens:**
- ✅ Extensível (fácil adicionar novas operações)
- ✅ Separação de responsabilidades
- ✅ Código limpo

**Exemplo:**
```python
class LiteralNode(ASTNode):
    def accept(self, visitor):
        return visitor.visit_literal(self)
```

### 3. **Geração de MEPA Inline**

**Decisão:** Código MEPA é gerado durante o parsing.

**Vantagens:**
- ✅ Imediato
- ✅ Simples de entender

**Desvantagens:**
- ❌ Sem otimizações
- ❌ Código MEPA não pode ser modificado depois

### 4. **Tabela de Símbolos Simples**

**Decisão:** Dict Python com endereços sequenciais.

**Limitações:**
- ❌ Apenas escopo global
- ❌ Sem suporte a escopos aninhados complexos

---

## ⚠️ Limitações Conhecidas

### Escopo

❌ **Não suportado**: Escopos aninhados complexos
```lua
-- Funciona com limitações
local x = 1

function foo()
    local y = 2  -- escopo limitado
end
```

### Funções

❌ **Não suportado**: Closures verdadeiros
```lua
-- NÃO funciona completamente
function criarContador()
    local count = 0
    return function()
        count = count + 1  -- closure
        return count
    end
end
```

### Tabelas

❌ **Funcionalidade limitada**: Apenas estrutura básica
```lua
-- Suporte limitado
local t = {}  -- OK
t[1] = 10     -- Parsing OK, geração limitada
```

### Módulos

❌ **Não suportado**: Sistema de módulos
```lua
-- NÃO funciona
require("modulo")
```

---

## 📚 Recursos de Aprendizagem

### Para Estudantes

1. 📖 **Leia na ordem:**
   - Esta introdução
   - [Análise Léxica](02_analise_lexica.md)
   - [Análise Sintática](03_analise_sintatica.md)
   - [Exemplos de Uso](08_exemplos_uso.md)

2. 🧪 **Experimente:**
   - Execute os exemplos em `examples/`
   - Modifique e veja os resultados
   - Crie seus próprios programas

3. 🔬 **Investigue:**
   - Adicione prints no código
   - Observe a AST gerada
   - Analise o código MEPA

### Para Desenvolvedores

1. 📖 **Referências rápidas:**
   - [Estrutura do Projeto](07_estrutura_projeto.md)
   - [Referência Técnica](09_referencia_tecnica.md)

2. 🔧 **Modifique:**
   - Adicione novos tipos de nós AST
   - Implemente novas instruções MEPA
   - Melhore a recuperação de erros

---

## 🎯 Próximos Passos

Agora que você entende o básico, escolha seu caminho:

### 👨‍🎓 Caminho do Estudante
[▶️ Ir para Análise Léxica](02_analise_lexica.md) - Entenda como o código é quebrado em tokens

### 👨‍💻 Caminho do Desenvolvedor
[▶️ Ir para Estrutura do Projeto](07_estrutura_projeto.md) - Veja a arquitetura completa

### 🧪 Caminho Prático
[▶️ Ir para Exemplos de Uso](08_exemplos_uso.md) - Compile seus primeiros programas

---

## 📖 Glossário Rápido

| Termo | Significado |
|-------|-------------|
| **Token** | "Palavra" básica da linguagem (if, =, 10, etc.) |
| **Lexema** | Texto original do token ("local", "123") |
| **AST** | Árvore Sintática Abstrata - representação estruturada do código |
| **Parser** | Analisador sintático |
| **MEPA** | Máquina de Execução Para Autômatos - nossa linguagem alvo |
| **Escopo** | Região onde uma variável é válida |
| **Símbolo** | Variável ou função na tabela de símbolos |

---

[← Voltar ao Índice](README.md) | [Próximo: Análise Léxica →](02_analise_lexica.md)

