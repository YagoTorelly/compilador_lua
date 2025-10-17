# ⚙️ Geração de Código MEPA

[← Anterior: Análise Semântica](04_analise_semantica.md) | [↑ Índice](README.md) | [Próximo: Tratamento de Erros →](06_tratamento_erros.md)

---

## 📋 Índice

- [O que é Geração de Código?](#-para-iniciantes-o-que-é-geração-de-código)
- [Máquina MEPA](#-máquina-mepa)
- [Instruções MEPA](#-instruções-mepa)
- [Geração para Estruturas](#-geração-para-estruturas)
- [Exemplos Completos](#-exemplos-completos)

---

## 💡 Para Iniciantes: O que é Geração de Código?

### Definição Simples

**Geração de código** é a etapa final do compilador, onde o programa é traduzido para **instruções de máquina** que podem ser executadas.

### Analogia: Receita de Bolo

Imagine que você tem uma receita em português (seu código Moonlet) e precisa traduzir para instruções que um robô de cozinha entende:

**Código Moonlet:**
```lua
local x = 10
x = x + 5
```

**"Instruções do Robô" (MEPA):**
```assembly
CRCT 10      ; Pegue o número 10
ARMZ 0       ; Guarde na gaveta 0 (variável x)
CRVL 0       ; Pegue o que está na gaveta 0
CRCT 5       ; Pegue o número 5
SOMA         ; Some os dois números
ARMZ 0       ; Guarde o resultado na gaveta 0
```

### O que é MEPA?

**MEPA** = **M**áquina de **E**xecução **P**ara **A**utômatos

É uma "linguagem de máquina" educacional criada para ensinar compiladores. Pense nela como assembly simplificado.

---

## 🖥️ Máquina MEPA

### Modelo de Execução

A máquina MEPA funciona com uma **pilha** (stack):

```
┌─────────────┐
│   PILHA     │
├─────────────┤
│     15      │ ← Topo
│     10      │
│      5      │
│      3      │
└─────────────┘

┌─────────────┐
│  MEMÓRIA    │
├─────────────┤
│  [0]: 10    │  (variável x)
│  [1]: 20    │  (variável y)
│  [2]: 30    │  (variável z)
│  ...        │
└─────────────┘
```

### Conceitos Principais

#### 1. Pilha (Stack)

- **Armazena** valores temporários
- **Operações** são feitas no topo
- **Cresce** para cima

#### 2. Memória

- **Armazena** variáveis
- Cada variável tem um **endereço** fixo
- Acesso por **índice**

#### 3. Registrador PC (Program Counter)

- Aponta para **próxima instrução**
- Incrementa automaticamente
- Modificado por desvios (jumps)

---

## 📜 Instruções MEPA

### Tabela Completa de Instruções

| Instrução | Parâmetros | Descrição | Exemplo |
|-----------|------------|-----------|---------|
| **CRCT** | valor | Empilha constante | `CRCT 10` |
| **CRVL** | endereco | Empilha valor da variável | `CRVL 0` |
| **ARMZ** | endereco | Desempilha e armazena | `ARMZ 0` |
| **SOMA** | - | Soma dois valores do topo | `SOMA` |
| **SUBT** | - | Subtração | `SUBT` |
| **MULT** | - | Multiplicação | `MULT` |
| **DIVI** | - | Divisão inteira | `DIVI` |
| **MODI** | - | Módulo (resto) | `MODI` |
| **POTI** | - | Potenciação | `POTI` |
| **INVR** | - | Inverte sinal (negação) | `INVR` |
| **CMIG** | - | Compara igual (==) | `CMIG` |
| **CMDG** | - | Compara diferente (~=) | `CMDG` |
| **CMME** | - | Compara menor (<) | `CMME` |
| **CMMA** | - | Compara maior (>) | `CMMA` |
| **CMEG** | - | Compara menor ou igual (<=) | `CMEG` |
| **CMAG** | - | Compara maior ou igual (>=) | `CMAG` |
| **DSVS** | rotulo | Desvio incondicional (goto) | `DSVS L1` |
| **DSVF** | rotulo | Desvio se falso (if not) | `DSVF L2` |
| **NADA** | - | Nenhuma operação | `NADA` |

### Categorias de Instruções

#### 🔢 Constantes e Variáveis

```assembly
CRCT 10      ; Empilha constante 10
CRVL 0       ; Carrega valor da variável no endereço 0
ARMZ 0       ; Armazena topo da pilha no endereço 0
```

#### ➕ Operações Aritméticas

```assembly
SOMA         ; a + b
SUBT         ; a - b
MULT         ; a * b
DIVI         ; a / b (divisão inteira)
MODI         ; a % b (resto)
POTI         ; a ^ b (potência)
INVR         ; -a (negação)
```

#### 🔀 Comparações

```assembly
CMIG         ; a == b (igual)
CMDG         ; a ~= b (diferente)
CMME         ; a < b (menor)
CMMA         ; a > b (maior)
CMEG         ; a <= b (menor ou igual)
CMAG         ; a >= b (maior ou igual)
```

Todas retornam:
- `1` (verdadeiro)
- `0` (falso)

#### 🔄 Desvios (Jumps)

```assembly
DSVS L1      ; Salta para rótulo L1 (incondicional)
DSVF L2      ; Salta para L2 se topo da pilha for 0 (falso)
```

---

## 🔧 Detalhes Técnicos

### Localização no Projeto

A geração de código está **integrada** no parser:

```
src/parser/sintatico_moonlet.py
```

### Estrutura de Dados

```python
class AnalisadorSintaticoMoonlet:
    def __init__(self, lexer):
        # ...
        
        # ⚙️ GERAÇÃO DE CÓDIGO
        self.codigo_mepa = []            # Lista de instruções
        self._contador_rotulos = 0       # Contador de labels
```

### Métodos Auxiliares

#### 1. Emitir Instrução

```python
def _emitir(self, instr: str):
    """Adiciona instrução ao código MEPA"""
    self.codigo_mepa.append(instr)
```

**Uso:**
```python
self._emitir("CRCT 10")
self._emitir("ARMZ 0")
```

#### 2. Gerar Rótulos

```python
def _novo_rotulo(self, base: str = 'L') -> str:
    """Gera um novo rótulo único"""
    rot = f"{base}{self._contador_rotulos}"
    self._contador_rotulos += 1
    return rot
```

**Uso:**
```python
rot_inicio = self._novo_rotulo('W')  # "W0"
rot_fim = self._novo_rotulo('W')     # "W1"
```

#### 3. Alocar Temporário

```python
def _alocar_temporario(self, hint: str = "t") -> int:
    """Aloca variável temporária"""
    nome = f"__tmp{self._temp_id}_{hint}"
    self._temp_id += 1
    
    # Registra na tabela de símbolos
    self.tabela_simbolos[nome] = {
        'endereco': self.proximo_endereco,
        'tipo': 'int'
    }
    self.proximo_endereco += 1
    
    return self.tabela_simbolos[nome]['endereco']
```

---

## 🏗️ Geração para Estruturas

### 1. Expressões Aritméticas

#### Código Moonlet:
```lua
x = 5 + 3
```

#### Durante o Parsing:

```python
def _analisar_expressao_aditiva(self):
    esquerda = self._analisar_expressao_multiplicativa()
    
    while self._verificar_operador('+'):
        operador = self.token_atual.lexema
        self._avancar_token()
        direita = self._analisar_expressao_multiplicativa()
        
        esquerda = BinaryOpNode(operador, esquerda, direita)
        
        # ⚙️ GERAÇÃO DE CÓDIGO
        self._emitir('SOMA')  # ← Emite instrução
    
    return esquerda
```

#### Código MEPA Gerado:

```assembly
CRCT 5       ; Empilha 5
CRCT 3       ; Empilha 3
SOMA         ; 5 + 3 = 8
ARMZ 0       ; x = 8
```

### 2. Estrutura IF

#### Código Moonlet:
```lua
if x < 5 then
    print("menor")
else
    print("maior")
end
```

#### Estratégia:

```
┌─────────────────────────────────┐
│  Avaliar condição               │
│  Se falso, pula para ELSE       │
├─────────────────────────────────┤
│  Bloco THEN                     │
│  Pula para FIM                  │
├─────────────────────────────────┤
│  Rótulo ELSE:                   │
│  Bloco ELSE                     │
├─────────────────────────────────┤
│  Rótulo FIM:                    │
└─────────────────────────────────┘
```

#### Código MEPA Gerado:

```assembly
; Avaliar condição: x < 5
CRVL 0       ; Carrega x
CRCT 5       ; Carrega 5
CMME         ; x < 5 ? (resultado: 1 ou 0)
DSVF I1      ; Se falso, vai para ELSE (rótulo I1)

; Bloco THEN
; (código de print("menor"))
DSVS I0      ; Pula para FIM (rótulo I0)

; Bloco ELSE
I1:
; (código de print("maior"))

; FIM
I0:
```

#### Implementação no Parser:

```python
def _analisar_comando_if(self):
    self._consumir_palavra_chave('if')
    
    condicoes = []
    blocos = []
    rotulo_fim = self._novo_rotulo('I')  # I0
    
    # IF principal
    condicao = self._analisar_expressao()
    condicoes.append(condicao)
    
    rotulo_proximo = self._novo_rotulo('I')  # I1
    self._emitir("DSVF " + rotulo_proximo)  # Se falso, pula
    
    self._consumir_palavra_chave('then')
    bloco = self._analisar_bloco()
    blocos.append(bloco)
    
    self._emitir("DSVS " + rotulo_fim)  # Pula para fim
    self._emitir(f"{rotulo_proximo}:")  # Rótulo do ELSE
    
    # ELSE opcional
    bloco_else = None
    if self._verificar_palavra_chave('else'):
        self._avancar_token()
        bloco_else = self._analisar_bloco()
    
    self._consumir_palavra_chave('end')
    self._emitir(f"{rotulo_fim}:")  # Rótulo do FIM
    
    return IfStatementNode(condicoes, blocos, bloco_else)
```

### 3. Laço WHILE

#### Código Moonlet:
```lua
while x < 3 do
    x = x + 1
end
```

#### Estratégia:

```
┌─────────────────────────────────┐
│  Rótulo INÍCIO:                 │
│  Avaliar condição               │
│  Se falso, pula para FIM        │
├─────────────────────────────────┤
│  Corpo do laço                  │
│  Pula para INÍCIO               │
├─────────────────────────────────┤
│  Rótulo FIM:                    │
└─────────────────────────────────┘
```

#### Código MEPA Gerado:

```assembly
W0:          ; Rótulo INÍCIO
CRVL 0       ; Carrega x
CRCT 3       ; Carrega 3
CMME         ; x < 3 ?
DSVF W1      ; Se falso, vai para FIM

; Corpo do laço
CRVL 0       ; Carrega x
CRCT 1       ; Carrega 1
SOMA         ; x + 1
ARMZ 0       ; x = x + 1

DSVS W0      ; Volta para INÍCIO

W1:          ; Rótulo FIM
```

#### Implementação:

```python
def _analisar_comando_while(self):
    self._consumir_palavra_chave('while')
    
    rot_inicio = self._novo_rotulo('W')
    rot_fim = self._novo_rotulo('W')
    
    self._emitir(f"{rot_inicio}:")  # Rótulo INÍCIO
    
    condicao = self._analisar_expressao()
    self._emitir("DSVF " + rot_fim)  # Se falso, sai
    
    self._consumir_palavra_chave('do')
    corpo = self._analisar_bloco()
    
    self._emitir("DSVS " + rot_inicio)  # Volta ao início
    self._emitir(f"{rot_fim}:")  # Rótulo FIM
    
    self._consumir_palavra_chave('end')
    
    return WhileLoopNode(condicao, corpo)
```

### 4. Laço FOR Numérico

#### Código Moonlet:
```lua
for i = 1, 10, 2 do
    print(i)
end
```

#### Estratégia:

```
┌─────────────────────────────────┐
│  i = inicio                     │
│  fim = valor_fim                │
│  passo = valor_passo            │
├─────────────────────────────────┤
│  Rótulo INÍCIO:                 │
│  Se i > fim, pula para FIM      │
├─────────────────────────────────┤
│  Corpo do laço                  │
│  i = i + passo                  │
│  Pula para INÍCIO               │
├─────────────────────────────────┤
│  Rótulo FIM:                    │
└─────────────────────────────────┘
```

#### Código MEPA Gerado:

```assembly
; Inicialização
CRCT 1       ; Início: 1
ARMZ 0       ; i = 1

CRCT 10      ; Fim: 10
ARMZ 1       ; tmp_fim = 10

CRCT 2       ; Passo: 2
ARMZ 2       ; tmp_passo = 2

; Laço
F0:          ; Rótulo INÍCIO
CRVL 0       ; Carrega i
CRVL 1       ; Carrega fim
CMEG         ; i <= fim ?
DSVF F1      ; Se falso, sai

; Corpo do laço
; (código de print(i))

; Incremento
CRVL 0       ; Carrega i
CRVL 2       ; Carrega passo
SOMA         ; i + passo
ARMZ 0       ; i = i + passo

DSVS F0      ; Volta ao início

F1:          ; Rótulo FIM
```

### 5. Laço REPEAT

#### Código Moonlet:
```lua
repeat
    x = x + 1
until x > 5
```

#### Estratégia:

```
┌─────────────────────────────────┐
│  Rótulo INÍCIO:                 │
│  Corpo do laço                  │
│  Avaliar condição               │
│  Se falso, pula para INÍCIO     │
└─────────────────────────────────┘
```

**Diferença do WHILE:** Executa **pelo menos uma vez**.

#### Código MEPA Gerado:

```assembly
R0:          ; Rótulo INÍCIO

; Corpo do laço
CRVL 0       ; Carrega x
CRCT 1       ; Carrega 1
SOMA         ; x + 1
ARMZ 0       ; x = x + 1

; Condição de saída
CRVL 0       ; Carrega x
CRCT 5       ; Carrega 5
CMMA         ; x > 5 ?
DSVF R0      ; Se falso, repete
```

---

## 📝 Exemplos Completos

### Exemplo 1: Atribuição Simples

**Código Moonlet:**
```lua
local x = 10
x = x + 5
```

**Código MEPA:**
```assembly
; decl local x @ 0
CRCT 10
ARMZ 0
CRVL 0
CRCT 5
SOMA
ARMZ 0
```

**Execução passo a passo:**

| Passo | Instrução | Pilha | Memória[0] |
|-------|-----------|-------|------------|
| 1 | `CRCT 10` | `[10]` | ? |
| 2 | `ARMZ 0` | `[]` | 10 |
| 3 | `CRVL 0` | `[10]` | 10 |
| 4 | `CRCT 5` | `[10, 5]` | 10 |
| 5 | `SOMA` | `[15]` | 10 |
| 6 | `ARMZ 0` | `[]` | 15 |

**Resultado final:** `x = 15`

### Exemplo 2: Expressão Complexa

**Código Moonlet:**
```lua
local x = 2 + 3 * 4
```

**Código MEPA:**
```assembly
; decl local x @ 0
CRCT 2
CRCT 3
CRCT 4
MULT
SOMA
ARMZ 0
```

**Execução:**

| Passo | Instrução | Pilha | Descrição |
|-------|-----------|-------|-----------|
| 1 | `CRCT 2` | `[2]` | Empilha 2 |
| 2 | `CRCT 3` | `[2, 3]` | Empilha 3 |
| 3 | `CRCT 4` | `[2, 3, 4]` | Empilha 4 |
| 4 | `MULT` | `[2, 12]` | 3 * 4 = 12 |
| 5 | `SOMA` | `[14]` | 2 + 12 = 14 |
| 6 | `ARMZ 0` | `[]` | x = 14 |

**Resultado:** `x = 14` (precedência respeitada!)

### Exemplo 3: IF Completo

**Código Moonlet:**
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

**Código MEPA:**
```assembly
; decl local x @ 0
CRCT 5
ARMZ 0

; IF x < 5
CRVL 0
CRCT 5
CMME
DSVF I1      ; Se falso, vai para ELSEIF

; Bloco THEN
; (print("menor"))
DSVS I0      ; Pula para FIM

; ELSEIF x == 5
I1:
CRVL 0
CRCT 5
CMIG
DSVF I2      ; Se falso, vai para ELSE

; Bloco ELSEIF
; (print("igual"))
DSVS I0      ; Pula para FIM

; ELSE
I2:
; (print("maior"))

; FIM
I0:
```

### Exemplo 4: WHILE Completo

**Código Moonlet:**
```lua
local x = 0
while x < 3 do
    x = x + 1
end
```

**Código MEPA:**
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

**Trace de execução:**

| Iteração | Condição | Ação | x |
|----------|----------|------|---|
| Inicial | - | `x = 0` | 0 |
| 1 | `0 < 3` ✅ | `x = x + 1` | 1 |
| 2 | `1 < 3` ✅ | `x = x + 1` | 2 |
| 3 | `2 < 3` ✅ | `x = x + 1` | 3 |
| 4 | `3 < 3` ❌ | Sai do laço | 3 |

### Exemplo 5: FOR Completo

**Código Moonlet:**
```lua
local i = 1
for i = 1, 3 do
    i = i + 1
end
```

**Código MEPA:**
```assembly
; decl local i @ 0
CRCT 1
ARMZ 0

; FOR
CRCT 1
ARMZ 0
CRCT 3
ARMZ 1       ; tmp_fim @ 1
CRCT 1
ARMZ 2       ; tmp_passo @ 2

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

---

## 🔍 Otimizações (Não Implementadas)

### Otimizações Possíveis

1. **Constant Folding**
   ```lua
   x = 2 + 3  -- Poderia ser otimizado para x = 5
   ```

2. **Dead Code Elimination**
   ```lua
   if false then
       print("nunca executa")  -- Código morto
   end
   ```

3. **Peephole Optimization**
   ```assembly
   CRCT 0
   ARMZ 0
   CRVL 0    ; ← Desnecessário, já temos 0 na pilha
   ```

---

## ✅ Resumo

### O que a Geração de Código faz?

✅ Traduz AST para instruções MEPA  
✅ Gera código para expressões  
✅ Gera código para estruturas de controle  
✅ Gerencia rótulos para desvios  
✅ Aloca variáveis temporárias  
✅ Produz código executável  

### Características

✅ Geração em tempo de parsing  
✅ Código não otimizado  
✅ Instruções de pilha  
✅ Desvios com rótulos  

---

## 🎯 Próximos Passos

Agora que você entende como o código é gerado, vamos ver como o compilador **trata erros**:

[▶️ Próximo: Tratamento de Erros →](06_tratamento_erros.md)

Ou explore outros tópicos:

- [🧠 Voltar à Análise Semântica](04_analise_semantica.md)
- [📚 Ver Exemplos Práticos](08_exemplos_uso.md)
- [🔧 Referência Técnica Completa](09_referencia_tecnica.md)

---

[← Anterior: Análise Semântica](04_analise_semantica.md) | [↑ Índice](README.md) | [Próximo: Tratamento de Erros →](06_tratamento_erros.md)

