# 🧠 Análise Semântica

[← Anterior: Análise Sintática](03_analise_sintatica.md) | [↑ Índice](README.md) | [Próximo: Geração de Código →](05_geracao_codigo.md)

---

## 📋 Índice

- [O que é Análise Semântica?](#-para-iniciantes-o-que-é-análise-semântica)
- [Tabela de Símbolos](#-tabela-de-símbolos)
- [Detalhes Técnicos](#-detalhes-técnicos)
- [Verificações Semânticas](#-verificações-semânticas)
- [Exemplos de Erros](#-exemplos-de-erros-semânticos)

---

## 💡 Para Iniciantes: O que é Análise Semântica?

### Definição Simples

**Análise semântica** verifica se o código **faz sentido**, mesmo que esteja sintaticamente correto.

### Analogia

Considere estas frases em português:

```
✅ "O gato comeu o peixe."           (faz sentido)
❌ "O gato comeu a felicidade."      (gramática OK, mas sem sentido)
```

Ambas têm gramática correta, mas a segunda não faz sentido.

Com código é parecido:

```lua
✅ local x = 10                      (OK: declara e usa)
   print(x)

❌ print(y)                           (ERRO: y nunca foi declarado)
```

### O que a Análise Semântica verifica?

1. **Variáveis foram declaradas** antes de serem usadas?
2. **Tipos são compatíveis** nas operações?
3. **Não há declarações duplicadas**?
4. **Funções existem** quando chamadas?
5. **Número de argumentos** está correto?

### Diferença entre Erros Sintáticos e Semânticos

#### Erro Sintático (estrutura errada)
```lua
if x > 5  -- ❌ FALTA 'then'
    print("ok")
end
```

#### Erro Semântico (não faz sentido)
```lua
if x > 5 then  -- ❌ x não foi declarado!
    print("ok")
end
```

---

## 📚 Tabela de Símbolos

### O que é?

Uma **tabela de símbolos** é como um "dicionário" que mantém informações sobre todas as variáveis e funções declaradas no programa.

### Estrutura Básica

```python
tabela_simbolos = {
    'x': {
        'endereco': 0,
        'tipo': 'int'
    },
    'contador': {
        'endereco': 1,
        'tipo': 'int'
    },
    'nome': {
        'endereco': 2,
        'tipo': 'int'  # Nota: tipos simplificados
    }
}
```

### Informações Armazenadas

Para cada variável, armazenamos:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| **nome** | Identificador da variável | `"contador"` |
| **endereco** | Posição na memória (MEPA) | `0`, `1`, `2`, ... |
| **tipo** | Tipo da variável | `"int"` (simplificado) |

### Analogia: Lista Telefônica

```
┌─────────────────────────────────┐
│     TABELA DE SÍMBOLOS          │
├───────────┬──────────┬──────────┤
│   Nome    │ Endereço │   Tipo   │
├───────────┼──────────┼──────────┤
│ x         │    0     │   int    │
│ contador  │    1     │   int    │
│ total     │    2     │   int    │
└───────────┴──────────┴──────────┘
```

Quando o código usa `x`, o compilador consulta a tabela para:
1. ✅ Verificar se `x` existe
2. ✅ Obter seu endereço (para gerar código MEPA)
3. ✅ Verificar compatibilidade de tipos

---

## 🔧 Detalhes Técnicos

### Localização no Projeto

A análise semântica está **integrada** no parser:

```
src/parser/sintatico_moonlet.py
```

**Linhas relevantes:** ~140-260 (métodos semânticos dentro do parser)

### Integração com o Parser

```python
class AnalisadorSintaticoMoonlet:
    def __init__(self, lexer):
        # ...
        
        # 🧠 ESTRUTURAS PARA ANÁLISE SEMÂNTICA
        self.tabela_simbolos = {}           # Dict: nome → info
        self.proximo_endereco = 0           # Contador de endereços
```

### Por que está integrado?

**Decisão de design:** Análise semântica ocorre **durante** o parsing.

**Vantagens:**
- ✅ Menos passadas sobre a árvore
- ✅ Detecção imediata de erros
- ✅ Simplifica geração de código

**Desvantagens:**
- ❌ Menos modular
- ❌ Dificulta análises complexas

---

## 🔍 Verificações Semânticas

### 1. Declaração de Variáveis

#### Método: `_declarar_variavel()`

```python
def _declarar_variavel(self, nome: str):
    """Registra nova variável na tabela de símbolos"""
    
    # ❌ Verifica duplicidade
    if nome in self.tabela_simbolos:
        raise ErroSemantico(
            f"Variável '{nome}' já declarada",
            self._criar_posicao_erro()
        )
    
    # ✅ Registra na tabela
    self.tabela_simbolos[nome] = {
        'endereco': self.proximo_endereco,
        'tipo': 'int'  # Tipo simplificado
    }
    self.proximo_endereco += 1
```

**Quando é chamado?**

Durante o parsing de declarações `local`:

```python
def _analisar_declaracao_variavel(self):
    self._consumir_palavra_chave('local')
    nome = self.token_atual.lexema
    self._avancar_token()
    
    # 🧠 ANÁLISE SEMÂNTICA
    self._declarar_variavel(nome)  # ← Aqui!
    
    valor = None
    if self._verificar_operador('='):
        self._avancar_token()
        valor = self._analisar_expressao()
    
    return VariableDeclarationNode(nome, valor, local=True)
```

### 2. Uso de Variáveis

#### Método: `_obter_variavel()`

```python
def _obter_variavel(self, nome: str):
    """Verifica se variável foi declarada"""
    
    simbolo = self.tabela_simbolos.get(nome)
    
    # ❌ Variável não existe
    if simbolo is None:
        raise ErroSemantico(
            f"Variável '{nome}' não declarada",
            self._criar_posicao_erro()
        )
    
    # ✅ Retorna informações
    return simbolo
```

**Quando é chamado?**

Durante o parsing de identificadores:

```python
def _analisar_expressao_primaria(self):
    # ...
    if self.token_atual.tipo == IDENTIFICADOR:
        nome = self.token_atual.lexema
        self._avancar_token()
        
        # ...
        
        # 🧠 ANÁLISE SEMÂNTICA
        self._obter_variavel(nome)  # ← Verifica se existe
        
        # Geração de código MEPA
        if not self._suprimir_carregamento_identificador:
            simbolo = self.tabela_simbolos[nome]
            self._emitir(f"CRVL {simbolo['endereco']}")
        
        return IdentifierNode(nome)
```

### 3. Garantir Variável Existe

#### Método: `_assegurar_variavel()`

```python
def _assegurar_variavel(self, nome: str) -> int:
    """
    Garante que variável existe.
    Se não existir, cria automaticamente (para variáveis de laço).
    """
    if nome not in self.tabela_simbolos:
        self._declarar_variavel(nome)
    return self.tabela_simbolos[nome]['endereco']
```

**Uso:** Principalmente em laços `for` onde a variável de controle pode ser implícita.

---

## 🛡️ Tipos de Erros Semânticos

### Classe ErroSemantico

```python
class ErroSemantico(ErroCompilacao):
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None):
        super().__init__(f"Erro semântico: {mensagem}", posicao)
```

Localização: `src/errors/erros_moonlet.py`

### Como são Lançados

```python
if condicao_invalida:
    raise ErroSemantico(
        "Mensagem descritiva do erro",
        self._criar_posicao_erro()  # Linha atual
    )
```

---

## 📝 Exemplos de Erros Semânticos

### Exemplo 1: Variável Não Declarada

**Código:**
```lua
-- ❌ ERRO: y não foi declarado
if y > 0 then
    y = y + 1
end
```

**Erro gerado:**
```
Erro semântico: Variável 'y' não declarada
    em linha 2, coluna 0
```

**Como corrigir:**
```lua
-- ✅ OK: declara y primeiro
local y = 5

if y > 0 then
    y = y + 1
end
```

### Exemplo 2: Declaração Duplicada

**Código:**
```lua
local a = 1
-- ❌ ERRO: a já foi declarado
local a = 2
```

**Erro gerado:**
```
Erro semântico: Variável 'a' já declarada
    em linha 3, coluna 0
```

**Como corrigir:**
```lua
-- ✅ OK: usa nomes diferentes
local a = 1
local b = 2

-- OU reatribui sem 'local'
local a = 1
a = 2  -- ✅ OK: não é nova declaração
```

### Exemplo 3: Uso Antes de Declaração

**Código:**
```lua
x = x + 1  -- ❌ ERRO: x não existe ainda
local x = 10
```

**Erro gerado:**
```
Erro semântico: Variável 'x' não declarada
    em linha 1, coluna 0
```

**Como corrigir:**
```lua
-- ✅ OK: declara antes de usar
local x = 10
x = x + 1
```

### Exemplo 4: Código Correto

**Código:**
```lua
-- ✅ Tudo OK
local contador = 0
local limite = 10

if contador < limite then
    contador = contador + 1
end
```

**Tabela de símbolos resultante:**
```python
{
    'contador': {'endereco': 0, 'tipo': 'int'},
    'limite':   {'endereco': 1, 'tipo': 'int'}
}
```

**Nenhum erro!** ✅

---

## 🔄 Fluxo de Verificação Semântica

### Durante Declaração

```
Código:  local x = 10
            │
            ▼
    Parser reconhece 'local'
            │
            ▼
    Extrai nome: "x"
            │
            ▼
    🧠 _declarar_variavel("x")
            │
            ├─ Verifica duplicidade
            │   ❌ Se existe → ErroSemantico
            │   ✅ Se não existe → continua
            │
            └─ Adiciona à tabela:
                tabela_simbolos["x"] = {
                    'endereco': 0,
                    'tipo': 'int'
                }
```

### Durante Uso

```
Código:  print(x)
              │
              ▼
    Parser reconhece identificador "x"
              │
              ▼
    🧠 _obter_variavel("x")
              │
              ├─ Busca na tabela
              │   ❌ Se não existe → ErroSemantico
              │   ✅ Se existe → retorna info
              │
              └─ Gera código MEPA:
                  CRVL 0  (carrega variável do endereço 0)
```

---

## 🎯 Alocação de Endereços

### Como Funciona

Cada variável recebe um **endereço sequencial** único:

```python
self.proximo_endereco = 0  # Inicia em 0

# Primeira variável
local x = 10  → endereco: 0, proximo_endereco = 1

# Segunda variável
local y = 20  → endereco: 1, proximo_endereco = 2

# Terceira variável
local z = 30  → endereco: 2, proximo_endereco = 3
```

### Exemplo Completo

**Código:**
```lua
local a = 1
local b = 2
local c = 3

a = a + b + c
```

**Tabela de símbolos:**
```python
{
    'a': {'endereco': 0, 'tipo': 'int'},
    'b': {'endereco': 1, 'tipo': 'int'},
    'c': {'endereco': 2, 'tipo': 'int'}
}
```

**Código MEPA gerado:**
```assembly
; Declarações
CRCT 1          ; Empilha 1
ARMZ 0          ; a = 1

CRCT 2          ; Empilha 2
ARMZ 1          ; b = 2

CRCT 3          ; Empilha 3
ARMZ 2          ; c = 3

; Atribuição: a = a + b + c
CRVL 0          ; Carrega a
CRVL 1          ; Carrega b
SOMA            ; a + b
CRVL 2          ; Carrega c
SOMA            ; (a + b) + c
ARMZ 0          ; Armazena em a
```

---

## 🧪 Testando Análise Semântica

### Teste 1: Erro de Variável Não Declarada

```python
from src.lexer.lexico_moonlet import AnalisadorLexicoMoonlet
from src.parser.sintatico_moonlet import AnalisadorSintaticoMoonlet
from src.errors.erros_moonlet import ErroSemantico

codigo = """
if y > 0 then
    y = y + 1
end
"""

lexer = AnalisadorLexicoMoonlet(codigo)
parser = AnalisadorSintaticoMoonlet(lexer)

try:
    ast = parser.analisar()
except ErroSemantico as e:
    print(f"❌ {e}")
    # Saída: Erro semântico: Variável 'y' não declarada
```

### Teste 2: Erro de Declaração Duplicada

```python
codigo = """
local a = 1
local a = 2
"""

lexer = AnalisadorLexicoMoonlet(codigo)
parser = AnalisadorSintaticoMoonlet(lexer)

try:
    ast = parser.analisar()
except ErroSemantico as e:
    print(f"❌ {e}")
    # Saída: Erro semântico: Variável 'a' já declarada
```

### Teste 3: Código Válido

```python
codigo = """
local x = 10
local y = 20

x = x + y
"""

lexer = AnalisadorLexicoMoonlet(codigo)
parser = AnalisadorSintaticoMoonlet(lexer)

try:
    ast = parser.analisar()
    print("✅ Análise semântica OK!")
    print(f"Tabela de símbolos: {parser.tabela_simbolos}")
    # Saída:
    # ✅ Análise semântica OK!
    # Tabela de símbolos: {
    #     'x': {'endereco': 0, 'tipo': 'int'},
    #     'y': {'endereco': 1, 'tipo': 'int'}
    # }
except ErroSemantico as e:
    print(f"❌ {e}")
```

---

## ⚠️ Limitações

### 1. Tipos Simplificados

**Limitação:** Todos os tipos são marcados como `'int'` (genérico).

```python
self.tabela_simbolos[nome] = {
    'endereco': self.proximo_endereco,
    'tipo': 'int'  # ← Sempre 'int'
}
```

**Impacto:**
- ❌ Sem verificação de tipos real
- ❌ Não detecta: `x = "string" + 10`

### 2. Escopo Global Único

**Limitação:** Apenas um escopo global.

```lua
-- Funciona
local x = 1

function foo()
    local x = 2  -- ❌ Conflita com x global
end
```

**Impacto:**
- ❌ Sem escopos aninhados
- ❌ Variáveis em funções conflitam com globais

### 3. Sem Verificação de Funções

**Limitação:** Não verifica se funções existem.

```lua
foo()  -- ✅ Compila, mas foo pode não existir
```

---

## 🎓 Conceitos Avançados

### Escopo (Simplificado)

**Escopo** define onde uma variável é válida:

```lua
local x = 1      -- Escopo global

if true then
    local y = 2  -- Escopo do if (não implementado completamente)
end

print(y)         -- ❌ Deveria dar erro, mas não está totalmente implementado
```

### Tipos (Teoria)

Em linguagens tipadas, a tabela de símbolos guardaria:

```python
{
    'x': {'endereco': 0, 'tipo': 'int'},
    'nome': {'endereco': 1, 'tipo': 'string'},
    'ativo': {'endereco': 2, 'tipo': 'boolean'}
}
```

E verificaria:
```lua
x = nome  -- ❌ ERRO: int ≠ string
```

---

## ✅ Resumo

### O que a Análise Semântica faz?

✅ Mantém tabela de símbolos  
✅ Verifica declarações de variáveis  
✅ Detecta uso antes de declaração  
✅ Detecta declarações duplicadas  
✅ Aloca endereços de memória  
✅ Prepara para geração de código  

### O que ela NÃO faz (limitações)?

❌ Verificação de tipos completa  
❌ Escopos aninhados complexos  
❌ Verificação de funções  
❌ Análise de fluxo de controle  

---

## 🎯 Próximos Passos

Agora que você entende como o compilador verifica o significado do código, vamos ver como ele **gera código de máquina**:

[▶️ Próximo: Geração de Código →](05_geracao_codigo.md)

Ou explore outros tópicos:

- [🌳 Voltar à Análise Sintática](03_analise_sintatica.md)
- [📚 Ver Exemplos Práticos](08_exemplos_uso.md)
- [🔧 Referência Técnica Completa](09_referencia_tecnica.md)

---

[← Anterior: Análise Sintática](03_analise_sintatica.md) | [↑ Índice](README.md) | [Próximo: Geração de Código →](05_geracao_codigo.md)

