# 🌳 Análise Sintática (Parsing e AST)

[← Anterior: Análise Léxica](02_analise_lexica.md) | [↑ Índice](README.md) | [Próximo: Análise Semântica →](04_analise_semantica.md)

---

## 📋 Índice

- [O que é Análise Sintática?](#-para-iniciantes-o-que-é-análise-sintática)
- [Árvore Sintática Abstrata (AST)](#-árvore-sintática-abstrata-ast)
- [Detalhes Técnicos](#-detalhes-técnicos)
- [Nós da AST](#-nós-da-ast)
- [Recuperação de Erros](#-recuperação-de-erros)
- [Exemplos Práticos](#-exemplos-práticos)

---

## 💡 Para Iniciantes: O que é Análise Sintática?

### Definição Simples

**Análise sintática** (ou **parsing**) é o processo de **verificar se os tokens estão na ordem correta** e **construir uma estrutura de árvore** que representa o programa.

### Analogia: Gramática de Linguagem Natural

Quando você lê uma frase em português, verifica automaticamente se a gramática está correta:

```
✅ "O gato comeu o peixe."          (correto)
❌ "Gato o comeu peixe o."          (errado)
```

O parser faz o mesmo com código:

```lua
✅ if x > 5 then print("ok") end    (correto)
❌ if x > then 5 print("ok")         (errado)
```

### O que é uma Árvore Sintática?

Uma **árvore** que representa a estrutura do código:

```lua
x = 5 + 3
```

Se transforma em:

```
    ATRIBUIÇÃO
      /     \
     x       +
            / \
           5   3
```

### Por que isso é importante?

- 🎯 **Valida** a estrutura do código
- 🌳 **Organiza** tokens em hierarquia
- 🔍 **Facilita** análise semântica
- ⚡ **Permite** geração de código

---

## 🌳 Árvore Sintática Abstrata (AST)

### O que é AST?

**AST** (Abstract Syntax Tree) é uma representação **estruturada** do código que:
- **Remove** detalhes desnecessários (espaços, pontuação)
- **Mantém** apenas informações relevantes
- **Organiza** em hierarquia de nós

### Exemplo Visual Completo

**Código:**
```lua
local x = 10

if x > 5 then
    print("ok")
end
```

**AST:**
```
PROGRAM
├── VARIABLE_DECLARATION (local)
│   ├── Nome: "x"
│   └── Valor: LITERAL(10)
│
└── IF_STATEMENT
    ├── Condição: BINARY_OP(>)
    │   ├── Esquerda: IDENTIFIER("x")
    │   └── Direita: LITERAL(5)
    │
    └── Bloco:
        └── FUNCTION_CALL
            ├── Nome: "print"
            └── Argumentos: [STRING("ok")]
```

---

## 🔧 Detalhes Técnicos

### Localização no Projeto

```
src/parser/sintatico_moonlet.py
```

**Linhas de código:** ~796  
**Classe principal:** `AnalisadorSintaticoMoonlet`  
**Nós AST:** 15 classes diferentes

### Estratégia: Recursive Descent Parser

O compilador Moonlet usa **parsing recursivo descendente**, onde:

1. Cada **regra gramatical** = **um método**
2. Métodos se **chamam recursivamente**
3. Produz AST **durante o parsing**

```python
class AnalisadorSintaticoMoonlet:
    def _analisar_expressao(self):
        # Chama regras de precedência
        return self._analisar_expressao_or()
    
    def _analisar_expressao_or(self):
        esquerda = self._analisar_expressao_and()
        while self._verificar_palavra_chave('or'):
            # ...
        return esquerda
    
    def _analisar_expressao_and(self):
        esquerda = self._analisar_expressao_relacional()
        # ...
```

### Estrutura Principal

```python
class AnalisadorSintaticoMoonlet:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_atual = None
        self.relatorio_erros = RelatorioErros()
        
        # Semântica
        self.tabela_simbolos = {}
        self.proximo_endereco = 0
        
        # Geração de código MEPA
        self.codigo_mepa = []
        self._contador_rotulos = 0
        
        self._avancar_token()
    
    def analisar(self) -> ProgramNode:
        """Ponto de entrada do parser"""
        declaracoes = []
        while self.token_atual.tipo != EOS:
            decl = self._analisar_declaracao()
            declaracoes.append(decl)
        return ProgramNode(declaracoes)
```

---

## 📦 Nós da AST

### Hierarquia de Nós

```
ASTNode (classe base)
├── LiteralNode           # Literais: 10, "texto", true
├── IdentifierNode        # Identificadores: x, contador
├── BinaryOpNode          # Operações: +, -, *, >, ==
├── UnaryOpNode           # Operações unárias: -, not, #
├── FunctionCallNode      # Chamadas: print("ok")
├── TableAccessNode       # Acesso: t[1], t.campo
├── VariableDeclarationNode  # Declarações: local x = 10
├── AssignmentNode        # Atribuições: x = 5
├── IfStatementNode       # Condicionais: if...then...else
├── WhileLoopNode         # Laço while
├── RepeatLoopNode        # Laço repeat...until
├── ForLoopNode           # Laço for numérico
├── ForInLoopNode         # Laço for...in
├── BreakNode             # break
├── GotoNode              # goto label
├── LabelNode             # ::label::
├── ReturnNode            # return valores
├── FunctionDefinitionNode   # function nome(params)...end
├── AnonymousFunctionNode    # function(params)...end
├── BlockNode             # Bloco de comandos
└── ProgramNode           # Programa completo
```

### Nós Principais Explicados

#### 1. LiteralNode

Representa valores constantes:

```python
class LiteralNode(ASTNode):
    def __init__(self, valor, tipo):
        self.valor = valor  # 10, "texto", True, None
        self.tipo = tipo    # 'number', 'string', 'boolean', 'nil'
```

**Exemplos:**
```lua
10          → LiteralNode(10, 'number')
"hello"     → LiteralNode("hello", 'string')
true        → LiteralNode(True, 'boolean')
nil         → LiteralNode(None, 'nil')
```

#### 2. IdentifierNode

Representa nomes de variáveis/funções:

```python
class IdentifierNode(ASTNode):
    def __init__(self, nome):
        self.nome = nome  # "x", "contador", "print"
```

#### 3. BinaryOpNode

Representa operações binárias:

```python
class BinaryOpNode(ASTNode):
    def __init__(self, operador, esquerda, direita):
        self.operador = operador  # '+', '-', '>', '==', etc.
        self.esquerda = esquerda  # Nó esquerdo
        self.direita = direita    # Nó direito
```

**Exemplo:**
```lua
x + 5
```

Se torna:
```
BinaryOpNode('+')
├── esquerda: IdentifierNode('x')
└── direita: LiteralNode(5)
```

#### 4. IfStatementNode

Representa estruturas condicionais:

```python
class IfStatementNode(ASTNode):
    def __init__(self, condicoes, blocos, bloco_else=None):
        self.condicoes = condicoes  # Lista de condições (if, elseif, ...)
        self.blocos = blocos        # Lista de blocos correspondentes
        self.bloco_else = bloco_else  # Bloco else (opcional)
```

**Exemplo:**
```lua
if x > 10 then
    print("grande")
elseif x > 5 then
    print("médio")
else
    print("pequeno")
end
```

Se torna:
```
IfStatementNode
├── condicoes[0]: BinaryOpNode('>', IdentifierNode('x'), LiteralNode(10))
├── blocos[0]: [FunctionCallNode('print', ["grande"])]
├── condicoes[1]: BinaryOpNode('>', IdentifierNode('x'), LiteralNode(5))
├── blocos[1]: [FunctionCallNode('print', ["médio"])]
└── bloco_else: [FunctionCallNode('print', ["pequeno"])]
```

#### 5. WhileLoopNode

```python
class WhileLoopNode(ASTNode):
    def __init__(self, condicao, corpo):
        self.condicao = condicao  # Expressão de condição
        self.corpo = corpo        # Lista de comandos
```

#### 6. ForLoopNode

```python
class ForLoopNode(ASTNode):
    def __init__(self, variavel, inicio, fim, passo, corpo):
        self.variavel = variavel  # Nome da variável de controle
        self.inicio = inicio      # Expressão inicial
        self.fim = fim            # Expressão final
        self.passo = passo        # Expressão de passo (opcional)
        self.corpo = corpo        # Lista de comandos
```

#### 7. FunctionCallNode

```python
class FunctionCallNode(ASTNode):
    def __init__(self, nome, argumentos):
        self.nome = nome          # Nome da função
        self.argumentos = argumentos  # Lista de expressões
```

#### 8. VariableDeclarationNode

```python
class VariableDeclarationNode(ASTNode):
    def __init__(self, nome, valor, local=False):
        self.nome = nome      # Nome da variável
        self.valor = valor    # Expressão de inicialização
        self.local = local    # True se declarada com 'local'
```

---

## 🔄 Pattern Visitor

### O que é?

O **Pattern Visitor** permite percorrer a AST sem modificar as classes dos nós.

### Implementação

Todos os nós implementam:

```python
class ASTNode:
    def accept(self, visitor):
        """Aceita um visitante"""
        class_name = self.__class__.__name__.lower().replace('node', '')
        method_name = f'visit_{class_name}'
        method = getattr(visitor, method_name, None)
        if method:
            return method(self)
```

### Exemplo: Impressor de AST

```python
class ImpressorAST:
    def visit_literal(self, node):
        print(f"LITERAL ({node.tipo}): {node.valor}")
    
    def visit_binary_op(self, node):
        print(f"OPERAÇÃO: {node.operador}")
        node.esquerda.accept(self)
        node.direita.accept(self)
```

**Uso:**
```python
ast = parser.analisar()
impressor = ImpressorAST()
ast.accept(impressor)
```

---

## 📊 Precedência de Operadores

O parser respeita a **precedência de operadores** usando métodos hierárquicos:

```
Precedência (maior → menor):

1. Primárias:    literais, identificadores, ( )
2. Unárias:      -, not, #
3. Multiplicativas:  *, /, %, ^
4. Aditivas:     +, -
5. Concatenação: ..
6. Relacionais:  <, >, <=, >=, ==, ~=
7. And:          and
8. Or:           or
```

### Implementação

```python
def _analisar_expressao(self):
    return self._analisar_expressao_or()  # Menor precedência

def _analisar_expressao_or(self):
    esquerda = self._analisar_expressao_and()
    while self._verificar_palavra_chave('or'):
        # ...
    return esquerda

def _analisar_expressao_and(self):
    esquerda = self._analisar_expressao_relacional()
    # ...

def _analisar_expressao_relacional(self):
    esquerda = self._analisar_expressao_concat()
    # ...

def _analisar_expressao_concat(self):
    esquerda = self._analisar_expressao_aditiva()
    # ...

def _analisar_expressao_aditiva(self):
    esquerda = self._analisar_expressao_multiplicativa()
    # ...

def _analisar_expressao_multiplicativa(self):
    esquerda = self._analisar_expressao_unaria()
    # ...

def _analisar_expressao_unaria(self):
    # not, -, #
    return self._analisar_expressao_primaria()

def _analisar_expressao_primaria(self):
    # Literais, identificadores, ( ), funções anônimas
```

### Exemplo de Precedência

```lua
x = 2 + 3 * 4
```

**Parsing:**
```
_analisar_expressao()
  └─ _analisar_expressao_or()
      └─ _analisar_expressao_and()
          └─ _analisar_expressao_relacional()
              └─ _analisar_expressao_concat()
                  └─ _analisar_expressao_aditiva()  ← Aqui!
                      ├─ esquerda: 2
                      ├─ operador: +
                      └─ direita: _analisar_expressao_multiplicativa()
                          ├─ esquerda: 3
                          ├─ operador: *
                          └─ direita: 4
```

**AST resultante:**
```
ASSIGNMENT
├── variavel: IDENTIFIER('x')
└── valor: BINARY_OP(+)
    ├── esquerda: LITERAL(2)
    └── direita: BINARY_OP(*)
        ├── esquerda: LITERAL(3)
        └── direita: LITERAL(4)
```

Resultado correto: `2 + (3 * 4) = 14`

---

## ⚠️ Recuperação de Erros

### Estratégia: Panic Mode

Quando o parser encontra um erro, ele tenta **recuperar** para continuar analisando:

```python
def _analisar_comando_if(self):
    self._consumir_palavra_chave('if')
    condicao = self._analisar_expressao()
    
    # ✅ Tenta consumir 'then'
    if self._verificar_palavra_chave('then'):
        self._avancar_token()
    else:
        # ❌ ERRO: Reporta mas continua
        erro = criar_erro_token_esperado('then', ...)
        self.relatorio_erros.adicionar_erro(erro)
        print(f"⚠️ ERRO SINTÁTICO: {erro}")
    
    # Continua parsing do bloco
    bloco = self._analisar_bloco()
    # ...
```

### Pontos de Sincronização

O parser tenta se recuperar pulando para tokens "seguros":

```python
def _pular_ate_proximo_valido(self):
    """Pula tokens até encontrar palavra-chave ou identificador"""
    while (self.token_atual and 
           self.token_atual.tipo not in [EOS, PALAVRA_CHAVE] and
           not (self.token_atual.tipo == IDENTIFICADOR)):
        print(f"🔄 Pulando token: '{self.token_atual.lexema}'")
        self._avancar_token()
```

### Exemplo de Recuperação

**Código com erro:**
```lua
if x > 5  -- ❌ FALTA 'then'
    print("ok")
end
```

**Comportamento:**
```
⚠️ ERRO SINTÁTICO: Esperado 'then', encontrado 'print'
🔄 Parser continua...
✓ Bloco analisado
✓ 'end' encontrado
```

**Resultado:**
- ❌ Erro reportado
- ✅ AST parcial gerado
- ✅ Análise continua

---

## 📝 Exemplos Práticos

### Exemplo 1: Expressão Simples

**Código:**
```lua
x = 5 + 3
```

**AST:**
```
PROGRAM
└── ASSIGNMENT
    ├── variavel: IDENTIFIER("x")
    └── valor: BINARY_OP(+)
        ├── esquerda: LITERAL(5)
        └── direita: LITERAL(3)
```

### Exemplo 2: Condicional

**Código:**
```lua
if x > 10 then
    print("grande")
else
    print("pequeno")
end
```

**AST:**
```
PROGRAM
└── IF_STATEMENT
    ├── condicoes[0]: BINARY_OP(>)
    │   ├── esquerda: IDENTIFIER("x")
    │   └── direita: LITERAL(10)
    ├── blocos[0]:
    │   └── FUNCTION_CALL("print")
    │       └── argumentos: [STRING("grande")]
    └── bloco_else:
        └── FUNCTION_CALL("print")
            └── argumentos: [STRING("pequeno")]
```

### Exemplo 3: Laço While

**Código:**
```lua
local i = 1
while i <= 5 do
    i = i + 1
end
```

**AST:**
```
PROGRAM
├── VARIABLE_DECLARATION (local)
│   ├── nome: "i"
│   └── valor: LITERAL(1)
│
└── WHILE_LOOP
    ├── condicao: BINARY_OP(<=)
    │   ├── esquerda: IDENTIFIER("i")
    │   └── direita: LITERAL(5)
    │
    └── corpo:
        └── ASSIGNMENT
            ├── variavel: IDENTIFIER("i")
            └── valor: BINARY_OP(+)
                ├── esquerda: IDENTIFIER("i")
                └── direita: LITERAL(1)
```

### Exemplo 4: Laço For

**Código:**
```lua
for i = 1, 10, 2 do
    print(i)
end
```

**AST:**
```
PROGRAM
└── FOR_LOOP
    ├── variavel: "i"
    ├── inicio: LITERAL(1)
    ├── fim: LITERAL(10)
    ├── passo: LITERAL(2)
    └── corpo:
        └── FUNCTION_CALL("print")
            └── argumentos: [IDENTIFIER("i")]
```

### Exemplo 5: Função

**Código:**
```lua
function soma(a, b)
    return a + b
end
```

**AST:**
```
PROGRAM
└── FUNCTION_DEFINITION
    ├── nome: "soma"
    ├── parametros: ["a", "b"]
    └── corpo:
        └── RETURN
            └── valores: [BINARY_OP(+)
                ├── esquerda: IDENTIFIER("a")
                └── direita: IDENTIFIER("b")]
```

---

## 🛠️ Métodos Principais do Parser

### 1. Declarações

```python
def _analisar_declaracao(self) -> ASTNode:
    """Analisa uma declaração de alto nível"""
    if self._verificar_palavra_chave('local'):
        return self._analisar_declaracao_variavel()
    
    if self._verificar_palavra_chave('function'):
        return self._analisar_definicao_funcao()
    
    if self._verificar_simbolo('::'):
        return self._analisar_label()
    
    return self._analisar_comando()
```

### 2. Comandos

```python
def _analisar_comando(self) -> ASTNode:
    """Analisa um comando"""
    if self._verificar_palavra_chave('if'):
        return self._analisar_comando_if()
    
    if self._verificar_palavra_chave('while'):
        return self._analisar_comando_while()
    
    if self._verificar_palavra_chave('for'):
        return self._analisar_comando_for()
    
    if self._verificar_token(IDENTIFICADOR):
        return self._analisar_atribuicao_ou_chamada()
    
    # ...
```

### 3. Expressões

```python
def _analisar_expressao(self) -> ASTNode:
    """Ponto de entrada para expressões"""
    return self._analisar_expressao_or()
```

---

## 🧪 Testando o Parser

### Código de Teste

```python
from src.lexer.lexico_moonlet import AnalisadorLexicoMoonlet
from src.parser.sintatico_moonlet import AnalisadorSintaticoMoonlet

codigo = """
local x = 10
if x > 5 then
    print("ok")
end
"""

lexer = AnalisadorLexicoMoonlet(codigo)
parser = AnalisadorSintaticoMoonlet(lexer)

ast = parser.analisar()

# Imprimir AST
from src.ast.compilador_moonlet import ImpressorAST
impressor = ImpressorAST()
ast.accept(impressor)
```

### Saída Esperada

```
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
            LITERAL (string): ok
```

---

## ✅ Resumo

### O que o Analisador Sintático faz?

✅ Verifica estrutura gramatical  
✅ Constrói AST  
✅ Respeita precedência de operadores  
✅ Recupera de erros sintáticos  
✅ Prepara para análise semântica  

### O que ele NÃO faz?

❌ Verificar significado (análise semântica)  
❌ Otimizar código  
❌ Executar o programa  

---

## 🎯 Próximos Passos

Agora que você entende como a AST é construída, vamos ver como verificamos se o código **faz sentido**:

[▶️ Próximo: Análise Semântica →](04_analise_semantica.md)

Ou explore outros tópicos:

- [🔍 Voltar à Análise Léxica](02_analise_lexica.md)
- [📚 Ver Exemplos Práticos](08_exemplos_uso.md)
- [🔧 Referência Técnica Completa](09_referencia_tecnica.md)

---

[← Anterior: Análise Léxica](02_analise_lexica.md) | [↑ Índice](README.md) | [Próximo: Análise Semântica →](04_analise_semantica.md)

