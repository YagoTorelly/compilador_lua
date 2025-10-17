# 🏗️ Estrutura do Projeto

[← Anterior: Tratamento de Erros](06_tratamento_erros.md) | [↑ Índice](README.md) | [Próximo: Exemplos de Uso →](08_exemplos_uso.md)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Organização de Diretórios](#-organização-de-diretórios)
- [Módulos e Responsabilidades](#-módulos-e-responsabilidades)
- [Fluxo de Execução](#-fluxo-de-execução)
- [Dependências](#-dependências)

---

## 🎯 Visão Geral

O Compilador Moonlet é organizado em uma estrutura modular clara, separando responsabilidades em diferentes módulos e pacotes.

### Estrutura Completa

```
compilador_lua/
│
├── main.py                          # 🚪 Ponto de entrada do compilador
│
├── src/                             # 📦 Código fonte principal
│   ├── __init__.py
│   ├── utils.py                     # 🛠️ Utilitários e configurações
│   │
│   ├── lexer/                       # 🔍 Análise Léxica
│   │   ├── __init__.py
│   │   └── lexico_moonlet.py        # Tokenização
│   │
│   ├── parser/                      # 🌳 Análise Sintática
│   │   ├── __init__.py
│   │   └── sintatico_moonlet.py     # Parser + AST + Semântica + MEPA
│   │
│   ├── ast/                         # 🎨 Compilador Principal
│   │   ├── __init__.py
│   │   └── compilador_moonlet.py    # Orquestração + Impressão AST
│   │
│   └── errors/                      # ⚠️ Sistema de Erros
│       ├── __init__.py
│       └── erros_moonlet.py         # Classes de erro
│
├── examples/                        # 📝 Exemplos de código Moonlet
│   ├── exemplo.moonlet
│   ├── exemplo_erro.moonlet
│   ├── mepa_if.moonlet
│   ├── mepa_while.moonlet
│   ├── mepa_for.moonlet
│   ├── mepa_for_in.moonlet
│   ├── mepa_for_in_numeric.moonlet
│   ├── mepa_repeat.moonlet
│   ├── mepa_ops.moonlet
│   ├── semantico_duplicidade.moonlet
│   ├── semantico_nao_declarada.moonlet
│   └── exemplos_moonlet.py
│
├── docs/                            # 📚 Esta documentação
│   ├── README.md
│   ├── 01_introducao.md
│   ├── 02_analise_lexica.md
│   ├── 03_analise_sintatica.md
│   ├── 04_analise_semantica.md
│   ├── 05_geracao_codigo.md
│   ├── 06_tratamento_erros.md
│   ├── 07_estrutura_projeto.md      # ← Você está aqui
│   ├── 08_exemplos_uso.md
│   └── 09_referencia_tecnica.md
│
└── trab02.pdf                       # 📄 Especificação do trabalho
```

---

## 📁 Organização de Diretórios

### Diretório Raiz (`/`)

```
compilador_lua/
├── main.py                 # Ponto de entrada
├── trab02.pdf             # Especificação
└── [diretórios...]
```

#### main.py

**Função:** Ponto de entrada do compilador.

**Responsabilidades:**
- Processar argumentos da linha de comando
- Ler arquivo de entrada
- Instanciar o compilador
- Exibir resultados

**Linhas de código:** ~59

### Diretório `src/`

Contém todo o código-fonte do compilador, organizado em submódulos:

```
src/
├── __init__.py              # Torna 'src' um pacote Python
├── utils.py                 # Utilitários compartilhados
├── lexer/                   # Análise léxica
├── parser/                  # Análise sintática
├── ast/                     # Compilador principal
└── errors/                  # Sistema de erros
```

#### utils.py

**Função:** Configurações e utilitários compartilhados.

**Conteúdo:**
- `TOKEN_MAP`: Mapeamento de tipos de token
- `CONFIG`: Configurações globais
- `MENSAGENS`: Mensagens do sistema

**Linhas de código:** ~36

### Submódulo `src/lexer/`

```
src/lexer/
├── __init__.py
└── lexico_moonlet.py
```

#### lexico_moonlet.py

**Função:** Análise léxica (tokenização).

**Classes principais:**
- `Token` (NamedTuple)
- `AnalisadorLexicoMoonlet`

**Constantes:**
- `PALAVRAS_CHAVE`
- `OPERADORES_DUPLOS`
- `SIMBOLOS_ESPECIAIS`

**Linhas de código:** ~174

### Submódulo `src/parser/`

```
src/parser/
├── __init__.py
└── sintatico_moonlet.py
```

#### sintatico_moonlet.py

**Função:** Análise sintática, semântica e geração de código.

**Classes AST (15 tipos):**
- `ASTNode` (base)
- `LiteralNode`
- `IdentifierNode`
- `BinaryOpNode`
- `UnaryOpNode`
- `FunctionCallNode`
- `TableAccessNode`
- `VariableDeclarationNode`
- `AssignmentNode`
- `IfStatementNode`
- `WhileLoopNode`
- `RepeatLoopNode`
- `ForLoopNode`
- `ForInLoopNode`
- `BreakNode`
- `GotoNode`
- `LabelNode`
- `ReturnNode`
- `FunctionDefinitionNode`
- `AnonymousFunctionNode`
- `BlockNode`
- `ProgramNode`

**Classe principal:**
- `AnalisadorSintaticoMoonlet`

**Linhas de código:** ~796

### Submódulo `src/ast/`

```
src/ast/
├── __init__.py
└── compilador_moonlet.py
```

#### compilador_moonlet.py

**Função:** Orquestração do compilador e impressão da AST.

**Classes principais:**
- `ASTVisitor` (base)
- `ImpressorAST` (Visitor para impressão)
- `AnalisadorMoonlet` (orquestrador)

**Linhas de código:** ~352

### Submódulo `src/errors/`

```
src/errors/
├── __init__.py
└── erros_moonlet.py
```

#### erros_moonlet.py

**Função:** Sistema de tratamento de erros.

**Classes:**
- `PosicaoErro` (dataclass)
- `ErroCompilacao` (base)
- `ErroLexico`
- `ErroSintatico`
- `ErroSemantico`
- `RelatorioErros`

**Funções auxiliares:**
- `criar_erro_token_inesperado()`
- `criar_erro_token_esperado()`
- `criar_erro_fim_arquivo_inesperado()`

**Linhas de código:** ~111

### Diretório `examples/`

```
examples/
├── exemplo.moonlet                    # Exemplo básico
├── exemplo_erro.moonlet               # Com erros
├── mepa_if.moonlet                    # IF/ELSEIF/ELSE
├── mepa_while.moonlet                 # Laço WHILE
├── mepa_for.moonlet                   # Laço FOR
├── mepa_for_in.moonlet                # Laço FOR-IN
├── mepa_for_in_numeric.moonlet        # FOR-IN numérico
├── mepa_repeat.moonlet                # Laço REPEAT
├── mepa_ops.moonlet                   # Operações
├── semantico_duplicidade.moonlet      # Erro: var duplicada
├── semantico_nao_declarada.moonlet    # Erro: var não declarada
└── exemplos_moonlet.py                # Exemplos programáticos
```

### Diretório `docs/`

```
docs/
├── README.md                          # Índice principal
├── 01_introducao.md                   # Introdução
├── 02_analise_lexica.md               # Análise léxica
├── 03_analise_sintatica.md            # Análise sintática
├── 04_analise_semantica.md            # Análise semântica
├── 05_geracao_codigo.md               # Geração de código
├── 06_tratamento_erros.md             # Tratamento de erros
├── 07_estrutura_projeto.md            # Este arquivo
├── 08_exemplos_uso.md                 # Exemplos práticos
└── 09_referencia_tecnica.md           # Referência completa
```

---

## 🧩 Módulos e Responsabilidades

### Matriz de Responsabilidades

| Módulo | Responsabilidade | Entrada | Saída |
|--------|------------------|---------|-------|
| **main.py** | Ponto de entrada | Arquivo `.moonlet` | Resultados na tela |
| **lexico_moonlet.py** | Tokenização | String de código | Stream de tokens |
| **sintatico_moonlet.py** | Parsing + Semântica + MEPA | Lexer | AST + Código MEPA |
| **compilador_moonlet.py** | Orquestração | Arquivo ou código | AST impresso |
| **erros_moonlet.py** | Tratamento de erros | Erros | Mensagens formatadas |
| **utils.py** | Utilitários | - | Constantes/configs |

### Dependências entre Módulos

```
┌──────────────┐
│   main.py    │
└──────┬───────┘
       │
       ▼
┌────────────────────────┐
│ compilador_moonlet.py  │
└──────┬─────────────────┘
       │
       ├────────────┐
       │            │
       ▼            ▼
┌─────────────┐  ┌──────────────────┐
│ lexico_     │─▶│ sintatico_       │
│ moonlet.py  │  │ moonlet.py       │
└─────────────┘  └─────────┬────────┘
       │                   │
       ▼                   ▼
┌─────────────────────────────────┐
│     erros_moonlet.py            │
└─────────────────────────────────┘
       ▲
       │
┌─────────────┐
│  utils.py   │
└─────────────┘
```

---

## 🔄 Fluxo de Execução

### Visão Geral

```
1. main.py
   ├─ Lê arquivo
   └─ Cria AnalisadorMoonlet

2. AnalisadorMoonlet
   ├─ Cria AnalisadorLexicoMoonlet
   ├─ Exibe tokens
   ├─ Cria AnalisadorSintaticoMoonlet
   └─ Imprime AST e MEPA

3. AnalisadorLexicoMoonlet
   └─ Gera stream de tokens

4. AnalisadorSintaticoMoonlet
   ├─ Constrói AST
   ├─ Verifica semântica
   └─ Gera código MEPA

5. ImpressorAST
   └─ Percorre AST (Visitor)
```

### Detalhado

#### 1. Entrada do Usuário

```bash
python main.py examples/exemplo.moonlet
```

#### 2. main.py

```python
def main():
    # Lê arquivo
    arquivo = sys.argv[1]
    
    # Cria compilador
    compilador = AnalisadorMoonlet()
    
    # Analisa
    ast = compilador.analisar_arquivo(arquivo)
    
    # Imprime resultados
    if ast:
        compilador.imprimir_ast(ast)
```

#### 3. AnalisadorMoonlet

```python
def analisar_arquivo(self, caminho):
    with open(caminho, 'r') as f:
        codigo = f.read()
    
    return self.analisar_codigo(codigo, caminho)

def analisar_codigo(self, codigo, nome):
    # 1. ANÁLISE LÉXICA
    lexer = AnalisadorLexicoMoonlet(codigo)
    # [Exibe tokens...]
    
    # 2. ANÁLISE SINTÁTICA
    lexer = AnalisadorLexicoMoonlet(codigo)  # Reinicia
    parser = AnalisadorSintaticoMoonlet(lexer)
    ast = parser.analisar()
    
    return ast
```

#### 4. AnalisadorLexicoMoonlet

```python
def proximo_token(self):
    # Lê caractere por caractere
    # Reconhece padrões
    # Retorna Token
    return Token(tipo, lexema, valor, linha)
```

#### 5. AnalisadorSintaticoMoonlet

```python
def analisar(self):
    declaracoes = []
    
    while self.token_atual.tipo != EOS:
        # Parsing
        decl = self._analisar_declaracao()
        
        # Semântica (integrada)
        # MEPA (integrada)
        
        declaracoes.append(decl)
    
    return ProgramNode(declaracoes)
```

#### 6. ImpressorAST

```python
def visit_program(self, node):
    self._imprimir("PROGRAMA")
    for decl in node.declaracoes:
        decl.accept(self)  # Visitor pattern
```

---

## 📊 Estatísticas do Projeto

### Linhas de Código

| Arquivo | LOC | Descrição |
|---------|-----|-----------|
| `main.py` | 59 | Ponto de entrada |
| `lexico_moonlet.py` | 174 | Análise léxica |
| `sintatico_moonlet.py` | 796 | Parsing + Semântica + MEPA |
| `compilador_moonlet.py` | 352 | Orquestração |
| `erros_moonlet.py` | 111 | Tratamento de erros |
| `utils.py` | 36 | Utilitários |
| **TOTAL** | **~1528** | Linhas de código |

### Distribuição de Complexidade

```
sintatico_moonlet.py:  52% ████████████████████
compilador_moonlet.py: 23% ███████████
lexico_moonlet.py:     11% █████
erros_moonlet.py:       7% ███
main.py:                4% ██
utils.py:               2% █
```

---

## 🔗 Dependências

### Bibliotecas Python Usadas

O projeto usa **apenas bibliotecas padrão** do Python:

```python
# Bibliotecas padrão
import sys          # Argumentos da linha de comando
import os           # Manipulação de arquivos/diretórios
from typing import  # Type hints (List, Optional, Union, etc.)
from dataclasses import dataclass  # Classes de dados
```

**Nenhuma dependência externa!** ✅

### Por que sem dependências?

- ✅ **Portabilidade:** Funciona em qualquer ambiente Python
- ✅ **Educacional:** Foco no aprendizado, não em frameworks
- ✅ **Simplicidade:** Fácil de instalar e executar

---

## 🎨 Padrões de Design Utilizados

### 1. Visitor Pattern

**Onde:** `ASTNode` e `ImpressorAST`

**Propósito:** Percorrer a AST sem modificar as classes dos nós.

```python
class ASTNode:
    def accept(self, visitor):
        # Delega para método específico do visitor
        method = getattr(visitor, f'visit_{tipo}')
        return method(self)

class ImpressorAST:
    def visit_literal(self, node):
        # ...
    
    def visit_binary_op(self, node):
        # ...
```

### 2. NamedTuple

**Onde:** `Token`

**Propósito:** Estrutura imutável e leve para tokens.

```python
class Token(NamedTuple):
    tipo: int
    lexema: str
    valor: Union[...]
    linha: int
```

### 3. Dataclass

**Onde:** `PosicaoErro`

**Propósito:** Representação simples de dados estruturados.

```python
@dataclass
class PosicaoErro:
    linha: int
    coluna: int
    arquivo: Optional[str] = None
```

### 4. Hierarquia de Exceções

**Onde:** Sistema de erros

**Propósito:** Tratamento específico por tipo de erro.

```python
ErroCompilacao (base)
├── ErroLexico
├── ErroSintatico
└── ErroSemantico
```

---

## 🧪 Como Adicionar Novos Recursos

### 1. Adicionar Nova Palavra-Chave

**Arquivo:** `src/lexer/lexico_moonlet.py`

```python
PALAVRAS_CHAVE = {
    'and', 'break', ..., 'while',
    'nova_keyword'  # ← Adicionar aqui
}
```

### 2. Adicionar Novo Tipo de Nó AST

**Arquivo:** `src/parser/sintatico_moonlet.py`

```python
class NovoNode(ASTNode):
    def __init__(self, parametros):
        self.parametros = parametros
```

**Adicionar método no Visitor:**

**Arquivo:** `src/ast/compilador_moonlet.py`

```python
class ImpressorAST:
    def visit_novo(self, node):
        self._imprimir("NOVO_NODE")
        # ...
```

### 3. Adicionar Nova Instrução MEPA

**Arquivo:** `src/parser/sintatico_moonlet.py`

```python
def _analisar_nova_estrutura(self):
    # ...
    self._emitir("NOVA_INSTR")
    # ...
```

---

## 📝 Convenções de Código

### Nomenclatura

- **Classes:** `PascalCase` (`AnalisadorLexicoMoonlet`)
- **Funções/Métodos:** `snake_case` (`proximo_token`)
- **Constantes:** `UPPER_CASE` (`PALAVRAS_CHAVE`)
- **Métodos privados:** `_prefixo_underscore` (`_analisar_expressao`)

### Organização de Imports

```python
# 1. Bibliotecas padrão
import sys
import os

# 2. Type hints
from typing import List, Optional

# 3. Imports internos
from ..lexer import AnalisadorLexicoMoonlet
from ..errors import ErroSintatico
```

### Docstrings

```python
def metodo(self, parametro: str) -> int:
    """Breve descrição do método.
    
    Args:
        parametro: Descrição do parâmetro
    
    Returns:
        Descrição do retorno
    """
    pass
```

---

## ✅ Resumo

### Estrutura do Projeto

✅ Organização modular clara  
✅ Separação de responsabilidades  
✅ Sem dependências externas  
✅ Padrões de design bem aplicados  
✅ Código bem documentado  

### Arquivos Principais

- `main.py`: Ponto de entrada (59 LOC)
- `lexico_moonlet.py`: Análise léxica (174 LOC)
- `sintatico_moonlet.py`: Parsing + Semântica + MEPA (796 LOC)
- `compilador_moonlet.py`: Orquestração (352 LOC)
- `erros_moonlet.py`: Tratamento de erros (111 LOC)

---

## 🎯 Próximos Passos

Agora que você entende a estrutura do projeto, vamos ver **exemplos práticos de uso**:

[▶️ Próximo: Exemplos de Uso →](08_exemplos_uso.md)

Ou explore outros tópicos:

- [🚨 Voltar ao Tratamento de Erros](06_tratamento_erros.md)
- [🔧 Ver Referência Técnica Completa](09_referencia_tecnica.md)
- [📘 Voltar à Introdução](01_introducao.md)

---

[← Anterior: Tratamento de Erros](06_tratamento_erros.md) | [↑ Índice](README.md) | [Próximo: Exemplos de Uso →](08_exemplos_uso.md)

