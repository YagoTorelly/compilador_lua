# 🚨 Tratamento de Erros

[← Anterior: Geração de Código](05_geracao_codigo.md) | [↑ Índice](README.md) | [Próximo: Estrutura do Projeto →](07_estrutura_projeto.md)

---

## 📋 Índice

- [O que é Tratamento de Erros?](#-para-iniciantes-o-que-é-tratamento-de-erros)
- [Tipos de Erros](#-tipos-de-erros)
- [Sistema de Erros](#-detalhes-técnicos-sistema-de-erros)
- [Recuperação de Erros](#-recuperação-de-erros)
- [Exemplos Práticos](#-exemplos-práticos)

---

## 💡 Para Iniciantes: O que é Tratamento de Erros?

### Definição Simples

**Tratamento de erros** é o processo de **detectar problemas** no código e **informar o programador** de forma clara sobre o que está errado e onde.

### Por que é importante?

Imagine escrever código e receber mensagens assim:

❌ **Ruim:**
```
Erro na linha 42
```

✅ **Bom:**
```
Erro sintático na linha 42: Esperado 'then', encontrado 'print'
  if x > 5
           ^
  Dica: Estruturas 'if' requerem 'then' antes do bloco
```

### Tipos de Problemas

Um compilador pode encontrar três tipos principais de problemas:

1. **Erros Léxicos** - Caracteres inválidos
2. **Erros Sintáticos** - Estrutura errada
3. **Erros Semânticos** - Não faz sentido

---

## 📚 Tipos de Erros

### 1. Erros Léxicos ❌

**Quando ocorrem?** Durante a tokenização (análise léxica).

**O que detectam?** Caracteres inválidos na linguagem.

#### Exemplo:

**Código:**
```lua
local x = @10
```

**Erro:**
```
⚠️ ERRO LÉXICO: Caractere inválido '@' na linha 1
```

**Token gerado:**
```
Linha 1 | ERRO | '@'
```

**Explicação:** O caractere `@` não é válido em Moonlet.

### 2. Erros Sintáticos ❌

**Quando ocorrem?** Durante o parsing (análise sintática).

**O que detectam?** Estrutura gramatical incorreta.

#### Exemplo 1: Falta 'then'

**Código:**
```lua
if x > 5
    print("ok")
end
```

**Erro:**
```
Erro sintático: Token esperado não encontrado
  Esperado 'then', encontrado 'print'
  em linha 2, coluna 0
```

#### Exemplo 2: Falta 'end'

**Código:**
```lua
if x > 5 then
    print("ok")
-- ❌ Falta 'end'
```

**Erro:**
```
Erro sintático: Esperado 'end', encontrado 'EOS'
```

### 3. Erros Semânticos ❌

**Quando ocorrem?** Durante análise semântica.

**O que detectam?** Código que não faz sentido.

#### Exemplo 1: Variável não declarada

**Código:**
```lua
if y > 0 then  -- ❌ y nunca foi declarado
    print("ok")
end
```

**Erro:**
```
Erro semântico: Variável 'y' não declarada
  em linha 1, coluna 0
```

#### Exemplo 2: Declaração duplicada

**Código:**
```lua
local a = 1
local a = 2  -- ❌ a já foi declarado
```

**Erro:**
```
Erro semântico: Variável 'a' já declarada
  em linha 2, coluna 0
```

---

## 🔧 Detalhes Técnicos: Sistema de Erros

### Localização no Projeto

```
src/errors/erros_moonlet.py
```

**Linhas de código:** ~111

### Hierarquia de Classes

```
ErroCompilacao (base)
├── ErroLexico
├── ErroSintatico
└── ErroSemantico
```

### Estrutura de Posição de Erro

```python
@dataclass
class PosicaoErro:
    """Representa a posição de um erro no código fonte"""
    linha: int
    coluna: int
    arquivo: Optional[str] = None
    
    def __str__(self):
        if self.arquivo:
            return f"{self.arquivo}:{self.linha}:{self.coluna}"
        return f"linha {self.linha}, coluna {self.coluna}"
```

**Exemplo de uso:**
```python
posicao = PosicaoErro(linha=5, coluna=10, arquivo="exemplo.moonlet")
print(posicao)
# Saída: exemplo.moonlet:5:10
```

---

## 🎯 Classes de Erro

### 1. ErroCompilacao (Classe Base)

```python
class ErroCompilacao(Exception):
    """Classe base para todos os erros de compilação"""
    
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None):
        self.mensagem = mensagem
        self.posicao = posicao
        super().__init__(self._formatar_mensagem())
    
    def _formatar_mensagem(self) -> str:
        if self.posicao:
            return f"Erro em {self.posicao}: {self.mensagem}"
        return self.mensagem
```

### 2. ErroLexico

```python
class ErroLexico(ErroCompilacao):
    """Erro durante a análise léxica"""
    
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None):
        super().__init__(f"Erro léxico: {mensagem}", posicao)
```

**Exemplo:**
```python
raise ErroLexico(
    "Caractere inválido '@'",
    PosicaoErro(linha=1, coluna=10)
)
```

### 3. ErroSintatico

```python
class ErroSintatico(ErroCompilacao):
    """Erro durante a análise sintática"""
    
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None, 
                 token_esperado: Optional[str] = None, 
                 token_encontrado: Optional[str] = None):
        self.token_esperado = token_esperado
        self.token_encontrado = token_encontrado
        
        if token_esperado and token_encontrado:
            mensagem_completa = (
                f"Erro sintático: {mensagem}. "
                f"Esperado '{token_esperado}', encontrado '{token_encontrado}'"
            )
        else:
            mensagem_completa = f"Erro sintático: {mensagem}"
            
        super().__init__(mensagem_completa, posicao)
```

**Exemplo:**
```python
raise ErroSintatico(
    "Token esperado não encontrado",
    PosicaoErro(linha=3, coluna=0),
    token_esperado='then',
    token_encontrado='print'
)
```

### 4. ErroSemantico

```python
class ErroSemantico(ErroCompilacao):
    """Erro durante a análise semântica"""
    
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None):
        super().__init__(f"Erro semântico: {mensagem}", posicao)
```

**Exemplo:**
```python
raise ErroSemantico(
    "Variável 'x' não declarada",
    PosicaoErro(linha=5, coluna=0)
)
```

---

## 📊 Relatório de Erros

### Classe RelatorioErros

```python
class RelatorioErros:
    """Classe para coletar e reportar múltiplos erros"""
    
    def __init__(self):
        self.erros: List[ErroCompilacao] = []
        self.avisos: List[str] = []
    
    def adicionar_erro(self, erro: ErroCompilacao):
        """Adiciona um erro ao relatório"""
        self.erros.append(erro)
    
    def tem_erros(self) -> bool:
        """Verifica se há erros"""
        return len(self.erros) > 0
    
    def imprimir_relatorio(self):
        """Imprime todos os erros"""
        if self.tem_erros():
            print("=== ERROS ENCONTRADOS ===")
            for i, erro in enumerate(self.erros, 1):
                print(f"{i}. {erro}")
            print()
```

### Uso no Parser

```python
class AnalisadorSintaticoMoonlet:
    def __init__(self, lexer):
        # ...
        self.relatorio_erros = RelatorioErros()
    
    def analisar(self):
        declaracoes = []
        
        while self.token_atual.tipo != EOS:
            try:
                decl = self._analisar_declaracao()
                declaracoes.append(decl)
            except ErroSintatico as e:
                # ✅ Adiciona erro ao relatório
                self.relatorio_erros.adicionar_erro(e)
                print(f"⚠️ ERRO SINTÁTICO: {e}")
                
                # Tenta recuperar
                self._pular_ate_proximo_valido()
        
        return ProgramNode(declaracoes)
```

---

## 🔄 Recuperação de Erros

### O que é?

**Recuperação de erros** permite que o compilador continue analisando o código mesmo após encontrar um erro, detectando **múltiplos erros** em uma única execução.

### Estratégia: Panic Mode

Quando o parser encontra um erro, ele **pula tokens** até encontrar um ponto seguro para continuar.

#### Método: `_pular_ate_proximo_valido()`

```python
def _pular_ate_proximo_valido(self):
    """Pula tokens até encontrar um válido para continuar análise"""
    while (self.token_atual and 
           self.token_atual.tipo not in [EOS, PALAVRA_CHAVE] and
           not (self.token_atual.tipo == IDENTIFICADOR)):
        print(f"🔄 Pulando token: '{self.token_atual.lexema}'")
        self._avancar_token()
```

### Pontos de Sincronização

Tokens considerados "seguros" para continuar:

- **Palavras-chave:** `if`, `while`, `for`, `local`, `function`, `end`
- **Identificadores:** Início de comandos
- **EOS:** Fim do arquivo

### Exemplo de Recuperação

**Código com múltiplos erros:**
```lua
if x > 5  -- ❌ ERRO 1: falta 'then'
    print("ok")
end

local a = 1
local a = 2  -- ❌ ERRO 2: declaração duplicada
```

**Comportamento:**
```
⚠️ ERRO SINTÁTICO: Esperado 'then', encontrado 'print'
🔄 Pulando token: 'print'
✓ Bloco analisado
✓ 'end' encontrado

⚠️ ERRO SEMÂNTICO: Variável 'a' já declarada

=== ERROS ENCONTRADOS ===
1. Erro sintático: Token esperado não encontrado. 
   Esperado 'then', encontrado 'print' em linha 1, coluna 0
2. Erro semântico: Variável 'a' já declarada em linha 6, coluna 0
```

### Recuperação Tolerante

O parser tenta continuar mesmo com erros:

```python
def _analisar_comando_if(self):
    self._consumir_palavra_chave('if')
    condicao = self._analisar_expressao()
    
    # ✅ Tenta consumir 'then'
    if self._verificar_palavra_chave('then'):
        self._avancar_token()
    else:
        # ❌ ERRO: Reporta mas CONTINUA
        erro = criar_erro_token_esperado('then', ...)
        self.relatorio_erros.adicionar_erro(erro)
        print(f"⚠️ ERRO SINTÁTICO: {erro}")
    
    # 🔄 Continua parsing do bloco
    bloco = self._analisar_bloco()
    # ...
```

---

## 🛠️ Funções Auxiliares

### 1. criar_erro_token_esperado()

```python
def criar_erro_token_esperado(
    token_esperado: str, 
    token_encontrado: str, 
    posicao: PosicaoErro
) -> ErroSintatico:
    return ErroSintatico(
        "Token esperado não encontrado",
        posicao,
        token_esperado=token_esperado,
        token_encontrado=token_encontrado
    )
```

**Uso:**
```python
if not self._verificar_palavra_chave('then'):
    raise criar_erro_token_esperado(
        'then',
        self.token_atual.lexema,
        self._criar_posicao_erro()
    )
```

### 2. criar_erro_fim_arquivo_inesperado()

```python
def criar_erro_fim_arquivo_inesperado(posicao: PosicaoErro) -> ErroSintatico:
    return ErroSintatico(
        "Fim de arquivo inesperado",
        posicao
    )
```

### 3. criar_erro_token_inesperado()

```python
def criar_erro_token_inesperado(
    token_encontrado: str, 
    posicao: PosicaoErro
) -> ErroSintatico:
    return ErroSintatico(
        "Token inesperado",
        posicao,
        token_encontrado=token_encontrado
    )
```

---

## 📝 Exemplos Práticos

### Exemplo 1: Erro Léxico Simples

**Código:**
```lua
local x = $10
```

**Execução:**
```python
lexer = AnalisadorLexicoMoonlet(codigo)
token = lexer.proximo_token()

while token.tipo != EOS:
    if token.tipo == ERRO:
        print(f"⚠️ ERRO LÉXICO: Caractere inválido '{token.lexema}'")
    token = lexer.proximo_token()
```

**Saída:**
```
Linha 1 | PALAVRA_CHAVE  | 'local'
Linha 1 | IDENTIFICADOR  | 'x'
Linha 1 | OPERADOR       | '='
Linha 1 | ERRO           | '$'     ⚠️ ERRO LÉXICO
Linha 1 | NUMERO         | '10'
```

### Exemplo 2: Erro Sintático com Recuperação

**Código:**
```lua
if x > 5
    print("ok")
end
```

**Execução:**
```python
try:
    lexer = AnalisadorLexicoMoonlet(codigo)
    parser = AnalisadorSintaticoMoonlet(lexer)
    ast = parser.analisar()
    
    # Verifica se houve erros
    if parser.relatorio_erros.tem_erros():
        parser.relatorio_erros.imprimir_relatorio()
        
except Exception as e:
    print(f"Erro fatal: {e}")
```

**Saída:**
```
⚠️ ERRO SINTÁTICO: Esperado 'then', encontrado 'print'
🔄 Parser continua...

=== ERROS ENCONTRADOS ===
1. Erro sintático: Token esperado não encontrado. 
   Esperado 'then', encontrado 'print' em linha 2, coluna 0
```

### Exemplo 3: Múltiplos Erros

**Código:**
```lua
-- Erro 1: falta 'then'
if x > 5
    print("ok")
end

-- Erro 2: variável não declarada
y = 10

-- Erro 3: declaração duplicada
local a = 1
local a = 2
```

**Saída:**
```
⚠️ ERRO SINTÁTICO: Esperado 'then', encontrado 'print'
⚠️ ERRO SEMÂNTICO: Variável 'y' não declarada
⚠️ ERRO SEMÂNTICO: Variável 'a' já declarada

=== ERROS ENCONTRADOS ===
1. Erro sintático: Token esperado não encontrado. 
   Esperado 'then', encontrado 'print' em linha 2, coluna 0
2. Erro semântico: Variável 'y' não declarada em linha 6, coluna 0
3. Erro semântico: Variável 'a' já declarada em linha 10, coluna 0

⚠️ 3 erro(s) encontrado(s)!
```

---

## 🎓 Boas Práticas

### 1. Mensagens Claras

❌ **Ruim:**
```
Erro
```

✅ **Bom:**
```
Erro sintático: Esperado 'then', encontrado 'print'
  em linha 3, coluna 5
```

### 2. Informar Localização

```python
raise ErroSintatico(
    "Token inválido",
    PosicaoErro(linha=token.linha, coluna=0)
)
```

### 3. Continuar Após Erros

Não pare no primeiro erro - detecte o máximo possível em uma execução.

### 4. Categorizar Erros

Use hierarquia de classes para diferentes tipos de erros.

---

## 📊 Comparação de Erros

| Tipo | Fase | Detecta | Exemplo |
|------|------|---------|---------|
| **Léxico** | Tokenização | Caracteres inválidos | `@`, `$` |
| **Sintático** | Parsing | Estrutura incorreta | Falta `then`, `end` |
| **Semântico** | Análise semântica | Sem sentido | Var não declarada |

---

## ✅ Resumo

### O que o Sistema de Erros faz?

✅ Detecta erros léxicos  
✅ Detecta erros sintáticos  
✅ Detecta erros semânticos  
✅ Reporta múltiplos erros  
✅ Tenta recuperar e continuar  
✅ Fornece mensagens claras  

### Características

✅ Hierarquia de classes  
✅ Posicionamento preciso  
✅ Relatórios formatados  
✅ Panic mode recovery  

---

## 🎯 Próximos Passos

Agora que você entende como o compilador trata erros, vamos ver a **estrutura completa do projeto**:

[▶️ Próximo: Estrutura do Projeto →](07_estrutura_projeto.md)

Ou explore outros tópicos:

- [⚙️ Voltar à Geração de Código](05_geracao_codigo.md)
- [📚 Ver Exemplos Práticos](08_exemplos_uso.md)
- [🔧 Referência Técnica Completa](09_referencia_tecnica.md)

---

[← Anterior: Geração de Código](05_geracao_codigo.md) | [↑ Índice](README.md) | [Próximo: Estrutura do Projeto →](07_estrutura_projeto.md)

