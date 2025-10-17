# 🔧 Referência Técnica Completa

[← Anterior: Exemplos de Uso](08_exemplos_uso.md) | [↑ Índice](README.md)

---

## 📋 Índice

- [Classes Principais](#-classes-principais)
- [API do Analisador Léxico](#-api-do-analisador-léxico)
- [API do Analisador Sintático](#-api-do-analisador-sintático)
- [Nós da AST](#-nós-da-ast)
- [Sistema de Erros](#-sistema-de-erros)
- [Glossário](#-glossário)

---

## 🎯 Classes Principais

### Visão Geral

| Classe | Módulo | Responsabilidade |
|--------|--------|------------------|
| `AnalisadorLexicoMoonlet` | `src/lexer/lexico_moonlet.py` | Tokenização |
| `AnalisadorSintaticoMoonlet` | `src/parser/sintatico_moonlet.py` | Parsing + Semântica + MEPA |
| `AnalisadorMoonlet` | `src/ast/compilador_moonlet.py` | Orquestração |
| `ImpressorAST` | `src/ast/compilador_moonlet.py` | Impressão da AST |
| `ErroCompilacao` | `src/errors/erros_moonlet.py` | Erros de compilação |
| `RelatorioErros` | `src/errors/erros_moonlet.py` | Relatório de erros |

---

## 🔍 API do Analisador Léxico

### Classe: `Token`

```python
class Token(NamedTuple):
    tipo: int
    lexema: str
    valor: Union[int, float, str, None]
    linha: int
```

**Campos:**
- `tipo`: Tipo do token (0-8)
- `lexema`: Texto original
- `valor`: Valor processado (para números, strings)
- `linha`: Número da linha

**Exemplo:**
```python
Token(tipo=3, lexema="123", valor=123, linha=5)
```

### Classe: `AnalisadorLexicoMoonlet`

#### Construtor

```python
def __init__(self, codigo_fonte: str):
    """
    Cria um analisador léxico.
    
    Args:
        codigo_fonte: String contendo o código Moonlet
    """
```

**Exemplo:**
```python
lexer = AnalisadorLexicoMoonlet("local x = 10")
```

#### Método: `proximo_token()`

```python
def proximo_token(self) -> Token:
    """
    Retorna o próximo token do código fonte.
    
    Returns:
        Token: Próximo token reconhecido
    """
```

**Exemplo:**
```python
token = lexer.proximo_token()
print(f"{token.tipo} | {token.lexema}")
```

#### Método: `proximo_char()`

```python
def proximo_char(self) -> str:
    """
    Consome e retorna o próximo caractere.
    
    Returns:
        str: Próximo caractere
    """
```

#### Método: `retrair()`

```python
def retrair(self):
    """Retrocede um caractere no buffer."""
```

### Constantes de Tipos de Token

```python
ERRO = 0
IDENTIFICADOR = 1
PALAVRA_CHAVE = 2
NUMERO = 3
STRING = 4
OPERADOR = 5
SIMBOLO_ESPECIAL = 6
COMENTARIO = 7
EOS = 8
```

### Constantes de Palavras-Chave

```python
PALAVRAS_CHAVE = {
    'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
    'function', 'goto', 'if', 'in', 'local', 'nil', 'not', 'or',
    'repeat', 'return', 'then', 'true', 'until', 'while'
}
```

**Total:** 23 palavras-chave

### Constantes de Operadores

```python
OPERADORES_DUPLOS = {'==', '~=', '<=', '>=', '..'}
```

### Constantes de Símbolos

```python
SIMBOLOS_ESPECIAIS = '()[]{}#;:,.\\'
```

---

## 🌳 API do Analisador Sintático

### Classe: `AnalisadorSintaticoMoonlet`

#### Construtor

```python
def __init__(self, lexer: AnalisadorLexicoMoonlet):
    """
    Cria um analisador sintático.
    
    Args:
        lexer: Analisador léxico inicializado
    """
```

**Atributos públicos:**
- `tabela_simbolos`: Dict com símbolos declarados
- `codigo_mepa`: Lista de instruções MEPA
- `relatorio_erros`: Relatório de erros

**Exemplo:**
```python
lexer = AnalisadorLexicoMoonlet(codigo)
parser = AnalisadorSintaticoMoonlet(lexer)
```

#### Método: `analisar()`

```python
def analisar(self) -> ProgramNode:
    """
    Analisa o código fonte e retorna a AST.
    
    Returns:
        ProgramNode: Raiz da árvore sintática
    
    Raises:
        ErroSintatico: Se houver erro sintático fatal
        ErroSemantico: Se houver erro semântico
    """
```

**Exemplo:**
```python
try:
    ast = parser.analisar()
except ErroSintatico as e:
    print(f"Erro: {e}")
```

### Métodos Privados Principais

#### Declarações

```python
def _analisar_declaracao(self) -> Optional[ASTNode]:
    """Analisa uma declaração de alto nível."""

def _analisar_declaracao_variavel(self) -> VariableDeclarationNode:
    """Analisa declaração de variável (local)."""

def _analisar_definicao_funcao(self) -> FunctionDefinitionNode:
    """Analisa definição de função."""
```

#### Comandos

```python
def _analisar_comando(self) -> Optional[ASTNode]:
    """Analisa um comando."""

def _analisar_comando_if(self) -> IfStatementNode:
    """Analisa estrutura if-elseif-else."""

def _analisar_comando_while(self) -> WhileLoopNode:
    """Analisa laço while."""

def _analisar_comando_for(self) -> Union[ForLoopNode, ForInLoopNode]:
    """Analisa laço for (numérico ou for-in)."""

def _analisar_comando_repeat(self) -> RepeatLoopNode:
    """Analisa laço repeat-until."""
```

#### Expressões

```python
def _analisar_expressao(self) -> ASTNode:
    """Analisa uma expressão (ponto de entrada)."""

def _analisar_expressao_or(self) -> ASTNode:
    """Analisa expressão com operador 'or'."""

def _analisar_expressao_and(self) -> ASTNode:
    """Analisa expressão com operador 'and'."""

def _analisar_expressao_relacional(self) -> ASTNode:
    """Analisa expressão relacional (<, >, ==, etc)."""

def _analisar_expressao_aditiva(self) -> ASTNode:
    """Analisa expressão aditiva (+, -)."""

def _analisar_expressao_multiplicativa(self) -> ASTNode:
    """Analisa expressão multiplicativa (*, /, %, ^)."""

def _analisar_expressao_unaria(self) -> ASTNode:
    """Analisa expressão unária (-, not, #)."""

def _analisar_expressao_primaria(self) -> ASTNode:
    """Analisa expressão primária (literais, identificadores, etc)."""
```

#### Análise Semântica

```python
def _declarar_variavel(self, nome: str):
    """
    Declara uma variável na tabela de símbolos.
    
    Args:
        nome: Nome da variável
    
    Raises:
        ErroSemantico: Se variável já foi declarada
    """

def _obter_variavel(self, nome: str):
    """
    Obtém informações de uma variável.
    
    Args:
        nome: Nome da variável
    
    Returns:
        Dict com 'endereco' e 'tipo'
    
    Raises:
        ErroSemantico: Se variável não foi declarada
    """

def _assegurar_variavel(self, nome: str) -> int:
    """
    Garante que variável existe, criando se necessário.
    
    Args:
        nome: Nome da variável
    
    Returns:
        int: Endereço da variável
    """
```

#### Geração de Código MEPA

```python
def _emitir(self, instr: str):
    """
    Emite uma instrução MEPA.
    
    Args:
        instr: String da instrução
    """

def _novo_rotulo(self, base: str = 'L') -> str:
    """
    Gera um novo rótulo único.
    
    Args:
        base: Prefixo do rótulo
    
    Returns:
        str: Rótulo único (ex: "L0", "W1")
    """

def _alocar_temporario(self, hint: str = "t") -> int:
    """
    Aloca uma variável temporária.
    
    Args:
        hint: Dica para o nome
    
    Returns:
        int: Endereço da variável temporária
    """
```

---

## 🎨 Nós da AST

### Hierarquia Completa

```
ASTNode (classe base abstrata)
│
├── LiteralNode
├── IdentifierNode
├── BinaryOpNode
├── UnaryOpNode
├── FunctionCallNode
├── TableAccessNode
├── VariableDeclarationNode
├── AssignmentNode
├── IfStatementNode
├── WhileLoopNode
├── RepeatLoopNode
├── ForLoopNode
├── ForInLoopNode
├── BreakNode
├── GotoNode
├── LabelNode
├── ReturnNode
├── FunctionDefinitionNode
├── AnonymousFunctionNode
├── BlockNode
└── ProgramNode
```

### Classe Base: `ASTNode`

```python
class ASTNode:
    def accept(self, visitor):
        """
        Aceita um visitante (Visitor Pattern).
        
        Args:
            visitor: Objeto visitante
        
        Returns:
            Resultado da visita (depende do visitante)
        """
```

### Nós de Expressão

#### `LiteralNode`

```python
class LiteralNode(ASTNode):
    def __init__(self, valor, tipo):
        """
        Args:
            valor: Valor literal (int, float, str, bool, None)
            tipo: Tipo do literal ('number', 'string', 'boolean', 'nil')
        """
        self.valor = valor
        self.tipo = tipo
```

**Exemplo:**
```python
LiteralNode(10, 'number')
LiteralNode("hello", 'string')
LiteralNode(True, 'boolean')
LiteralNode(None, 'nil')
```

#### `IdentifierNode`

```python
class IdentifierNode(ASTNode):
    def __init__(self, nome):
        """
        Args:
            nome: Nome do identificador
        """
        self.nome = nome
```

#### `BinaryOpNode`

```python
class BinaryOpNode(ASTNode):
    def __init__(self, operador, esquerda, direita):
        """
        Args:
            operador: Operador binário ('+', '-', '*', etc)
            esquerda: Nó da expressão esquerda
            direita: Nó da expressão direita
        """
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita
```

**Operadores suportados:**
- Aritméticos: `+`, `-`, `*`, `/`, `%`, `^`
- Relacionais: `<`, `>`, `<=`, `>=`, `==`, `~=`
- Lógicos: `and`, `or`
- Concatenação: `..`

#### `UnaryOpNode`

```python
class UnaryOpNode(ASTNode):
    def __init__(self, operador, operando):
        """
        Args:
            operador: Operador unário ('-', 'not', '#')
            operando: Nó da expressão
        """
        self.operador = operador
        self.operando = operando
```

### Nós de Comando

#### `VariableDeclarationNode`

```python
class VariableDeclarationNode(ASTNode):
    def __init__(self, nome, valor, local=False):
        """
        Args:
            nome: Nome da variável
            valor: Nó da expressão de inicialização (opcional)
            local: True se declarada com 'local'
        """
        self.nome = nome
        self.valor = valor
        self.local = local
```

#### `AssignmentNode`

```python
class AssignmentNode(ASTNode):
    def __init__(self, variavel, valor):
        """
        Args:
            variavel: Nó da variável (IdentifierNode ou TableAccessNode)
            valor: Nó da expressão do valor
        """
        self.variavel = variavel
        self.valor = valor
```

#### `IfStatementNode`

```python
class IfStatementNode(ASTNode):
    def __init__(self, condicoes, blocos, bloco_else=None):
        """
        Args:
            condicoes: Lista de nós de condições (if + elseifs)
            blocos: Lista de listas de comandos
            bloco_else: Lista de comandos do else (opcional)
        """
        self.condicoes = condicoes
        self.blocos = blocos
        self.bloco_else = bloco_else
```

#### `WhileLoopNode`

```python
class WhileLoopNode(ASTNode):
    def __init__(self, condicao, corpo):
        """
        Args:
            condicao: Nó da expressão de condição
            corpo: Lista de comandos
        """
        self.condicao = condicao
        self.corpo = corpo
```

#### `RepeatLoopNode`

```python
class RepeatLoopNode(ASTNode):
    def __init__(self, corpo, condicao):
        """
        Args:
            corpo: Lista de comandos
            condicao: Nó da expressão de condição (para sair)
        """
        self.corpo = corpo
        self.condicao = condicao
```

#### `ForLoopNode`

```python
class ForLoopNode(ASTNode):
    def __init__(self, variavel, inicio, fim, passo, corpo):
        """
        Args:
            variavel: Nome da variável de controle
            inicio: Nó da expressão inicial
            fim: Nó da expressão final
            passo: Nó da expressão de passo (opcional)
            corpo: Lista de comandos
        """
        self.variavel = variavel
        self.inicio = inicio
        self.fim = fim
        self.passo = passo
        self.corpo = corpo
```

#### `ForInLoopNode`

```python
class ForInLoopNode(ASTNode):
    def __init__(self, variaveis, iterador, corpo):
        """
        Args:
            variaveis: Lista de nomes de variáveis
            iterador: Nó da expressão iteradora
            corpo: Lista de comandos
        """
        self.variaveis = variaveis
        self.iterador = iterador
        self.corpo = corpo
```

### Nós de Função

#### `FunctionCallNode`

```python
class FunctionCallNode(ASTNode):
    def __init__(self, nome, argumentos):
        """
        Args:
            nome: Nome da função
            argumentos: Lista de nós de argumentos
        """
        self.nome = nome
        self.argumentos = argumentos
```

#### `FunctionDefinitionNode`

```python
class FunctionDefinitionNode(ASTNode):
    def __init__(self, nome, parametros, corpo, local=False):
        """
        Args:
            nome: Nome da função
            parametros: Lista de nomes de parâmetros
            corpo: Lista de comandos
            local: True se declarada com 'local'
        """
        self.nome = nome
        self.parametros = parametros
        self.corpo = corpo
        self.local = local
```

#### `AnonymousFunctionNode`

```python
class AnonymousFunctionNode(ASTNode):
    def __init__(self, parametros, corpo):
        """
        Args:
            parametros: Lista de nomes de parâmetros
            corpo: Lista de comandos
        """
        self.parametros = parametros
        self.corpo = corpo
```

### Nós Estruturais

#### `ProgramNode`

```python
class ProgramNode(ASTNode):
    def __init__(self, declaracoes):
        """
        Args:
            declaracoes: Lista de nós de declarações
        """
        self.declaracoes = declaracoes
```

#### `BlockNode`

```python
class BlockNode(ASTNode):
    def __init__(self, declaracoes):
        """
        Args:
            declaracoes: Lista de nós de comandos
        """
        self.declaracoes = declaracoes
```

---

## ⚠️ Sistema de Erros

### Classe: `PosicaoErro`

```python
@dataclass
class PosicaoErro:
    linha: int
    coluna: int
    arquivo: Optional[str] = None
    
    def __str__(self):
        """Retorna representação legível da posição."""
```

**Exemplo:**
```python
posicao = PosicaoErro(linha=5, coluna=10, arquivo="exemplo.moonlet")
print(posicao)  # exemplo.moonlet:5:10
```

### Classe: `ErroCompilacao`

```python
class ErroCompilacao(Exception):
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None):
        """
        Args:
            mensagem: Descrição do erro
            posicao: Posição onde ocorreu o erro
        """
        self.mensagem = mensagem
        self.posicao = posicao
```

### Classe: `ErroLexico`

```python
class ErroLexico(ErroCompilacao):
    """Erro durante análise léxica."""
```

### Classe: `ErroSintatico`

```python
class ErroSintatico(ErroCompilacao):
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None, 
                 token_esperado: Optional[str] = None, 
                 token_encontrado: Optional[str] = None):
        """
        Args:
            mensagem: Descrição do erro
            posicao: Posição do erro
            token_esperado: Token que era esperado
            token_encontrado: Token que foi encontrado
        """
```

### Classe: `ErroSemantico`

```python
class ErroSemantico(ErroCompilacao):
    """Erro durante análise semântica."""
```

### Classe: `RelatorioErros`

```python
class RelatorioErros:
    def __init__(self):
        """Cria relatório vazio."""
        self.erros: List[ErroCompilacao] = []
        self.avisos: List[str] = []
    
    def adicionar_erro(self, erro: ErroCompilacao):
        """Adiciona erro ao relatório."""
    
    def tem_erros(self) -> bool:
        """Verifica se há erros."""
    
    def imprimir_relatorio(self):
        """Imprime todos os erros."""
```

---

## 🎨 Pattern Visitor

### Interface Visitor

```python
class ASTVisitor:
    """Classe base para visitantes da AST."""
    
    def visit_literal(self, node: LiteralNode):
        pass
    
    def visit_identifier(self, node: IdentifierNode):
        pass
    
    def visit_binary_op(self, node: BinaryOpNode):
        pass
    
    # ... métodos para cada tipo de nó
```

### Exemplo de Implementação: ImpressorAST

```python
class ImpressorAST(ASTVisitor):
    def __init__(self):
        self.indentacao = 0
    
    def visit_program(self, node: ProgramNode):
        self._imprimir("PROGRAMA")
        self._entrar_escopo()
        for decl in node.declaracoes:
            decl.accept(self)
        self._sair_escopo()
    
    def visit_literal(self, node: LiteralNode):
        self._imprimir(f"LITERAL ({node.tipo}): {node.valor}")
    
    # ... outros métodos visit_*
```

### Usando o Visitor

```python
ast = parser.analisar()
impressor = ImpressorAST()
ast.accept(impressor)
```

---

## 📊 Instruções MEPA

### Tabela de Referência

| Instrução | Formato | Stack Antes | Stack Depois | Descrição |
|-----------|---------|-------------|--------------|-----------|
| **CRCT** | `CRCT k` | [...] | [..., k] | Empilha constante k |
| **CRVL** | `CRVL n` | [...] | [..., mem[n]] | Carrega variável |
| **ARMZ** | `ARMZ n` | [..., v] | [...] | Armazena v em mem[n] |
| **SOMA** | `SOMA` | [..., a, b] | [..., a+b] | Soma |
| **SUBT** | `SUBT` | [..., a, b] | [..., a-b] | Subtração |
| **MULT** | `MULT` | [..., a, b] | [..., a*b] | Multiplicação |
| **DIVI** | `DIVI` | [..., a, b] | [..., a/b] | Divisão |
| **MODI** | `MODI` | [..., a, b] | [..., a%b] | Módulo |
| **POTI** | `POTI` | [..., a, b] | [..., a^b] | Potência |
| **INVR** | `INVR` | [..., a] | [..., -a] | Negação |
| **CMIG** | `CMIG` | [..., a, b] | [..., a==b] | Igual |
| **CMDG** | `CMDG` | [..., a, b] | [..., a~=b] | Diferente |
| **CMME** | `CMME` | [..., a, b] | [..., a<b] | Menor |
| **CMMA** | `CMMA` | [..., a, b] | [..., a>b] | Maior |
| **CMEG** | `CMEG` | [..., a, b] | [..., a<=b] | Menor igual |
| **CMAG** | `CMAG` | [..., a, b] | [..., a>=b] | Maior igual |
| **DSVS** | `DSVS L` | [...] | [...] | Pula para L |
| **DSVF** | `DSVF L` | [..., c] | [...] | Se c==0, pula para L |
| **NADA** | `NADA` | [...] | [...] | Sem operação |

---

## 📚 Glossário

### A

**AST (Abstract Syntax Tree)** - Árvore Sintática Abstrata: Estrutura de dados que representa o código fonte.

**Análise Léxica** - Primeira fase da compilação: quebra código em tokens.

**Análise Sintática** - Segunda fase: verifica estrutura gramatical e constrói AST.

**Análise Semântica** - Terceira fase: verifica significado do código.

### C

**Compilador** - Programa que traduz código de uma linguagem para outra.

**Comentário** - Texto ignorado pelo compilador (-- ou --[[ ]]).

### E

**EOS (End of Stream)** - Marcador de fim de arquivo.

**Escopo** - Região onde uma variável é válida.

### G

**Geração de Código** - Fase final: produz código de máquina (MEPA).

**Gramática** - Conjunto de regras que definem a sintaxe da linguagem.

### I

**Identificador** - Nome de variável ou função.

### L

**Lexema** - Texto original de um token.

**Lexer** - Analisador léxico.

### M

**MEPA** - Máquina de Execução Para Autômatos: linguagem alvo.

### P

**Parser** - Analisador sintático.

**Precedência** - Ordem de avaliação de operadores.

### R

**Recursive Descent** - Estratégia de parsing recursivo.

**Recuperação de Erros** - Continuar compilação após encontrar erro.

### S

**Símbolo** - Variável ou função na tabela de símbolos.

**Stack (Pilha)** - Estrutura de dados LIFO usada pelo MEPA.

### T

**Tabela de Símbolos** - Dicionário de variáveis declaradas.

**Token** - Unidade léxica básica (palavra-chave, número, operador).

**Tokenização** - Processo de quebrar código em tokens.

### V

**Visitor Pattern** - Padrão de design para percorrer AST.

---

## 🔗 Links Rápidos

### Documentação

- [Introdução](01_introducao.md)
- [Análise Léxica](02_analise_lexica.md)
- [Análise Sintática](03_analise_sintatica.md)
- [Análise Semântica](04_analise_semantica.md)
- [Geração de Código](05_geracao_codigo.md)
- [Tratamento de Erros](06_tratamento_erros.md)
- [Estrutura do Projeto](07_estrutura_projeto.md)
- [Exemplos de Uso](08_exemplos_uso.md)

### Código Fonte

- `src/lexer/lexico_moonlet.py` - Análise léxica
- `src/parser/sintatico_moonlet.py` - Parsing + Semântica + MEPA
- `src/ast/compilador_moonlet.py` - Orquestração
- `src/errors/erros_moonlet.py` - Sistema de erros

---

## ✅ Resumo da API

### Uso Básico

```python
# 1. Importar módulos
from src.lexer.lexico_moonlet import AnalisadorLexicoMoonlet
from src.parser.sintatico_moonlet import AnalisadorSintaticoMoonlet
from src.ast.compilador_moonlet import ImpressorAST

# 2. Criar analisador léxico
codigo = "local x = 10"
lexer = AnalisadorLexicoMoonlet(codigo)

# 3. Criar analisador sintático
parser = AnalisadorSintaticoMoonlet(lexer)

# 4. Analisar e gerar AST
ast = parser.analisar()

# 5. Imprimir AST
impressor = ImpressorAST()
ast.accept(impressor)

# 6. Acessar código MEPA
for instr in parser.codigo_mepa:
    print(instr)
```

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Consulte a [documentação completa](README.md)
2. Veja [exemplos práticos](08_exemplos_uso.md)
3. Revise a [estrutura do projeto](07_estrutura_projeto.md)

---

**Fim da Referência Técnica**

[← Anterior: Exemplos de Uso](08_exemplos_uso.md) | [↑ Voltar ao Índice](README.md)

