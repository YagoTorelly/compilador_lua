# 📚 Documentação do Compilador Moonlet

Bem-vindo à documentação completa do **Compilador Moonlet** - um compilador educacional para um subconjunto da linguagem Lua.

---

## 📖 Índice da Documentação

### 🎯 Começando

1. **[Introdução](01_introducao.md)**
   - O que é Moonlet?
   - O que é um compilador?
   - Arquitetura geral do projeto

### 🔍 Fases de Compilação

2. **[Análise Léxica](02_analise_lexica.md)**
   - Tokenização
   - Reconhecimento de palavras-chave
   - Tratamento de comentários

3. **[Análise Sintática](03_analise_sintatica.md)**
   - Parsing e gramática
   - Árvore Sintática Abstrata (AST)
   - Recuperação de erros

4. **[Análise Semântica](04_analise_semantica.md)**
   - Tabela de símbolos
   - Verificação de tipos
   - Detecção de erros semânticos

5. **[Geração de Código](05_geracao_codigo.md)**
   - Máquina MEPA
   - Instruções geradas
   - Otimizações

### 🛠️ Infraestrutura

6. **[Tratamento de Erros](06_tratamento_erros.md)**
   - Sistema de erros hierárquico
   - Relatórios de erro
   - Estratégias de recuperação

7. **[Estrutura do Projeto](07_estrutura_projeto.md)**
   - Organização de diretórios
   - Módulos e dependências
   - Fluxo de execução

### 📝 Tutoriais e Referências

8. **[Exemplos de Uso](08_exemplos_uso.md)**
   - Como executar o compilador
   - Exemplos práticos
   - Análise passo a passo

9. **[Referência Técnica](09_referencia_tecnica.md)**
   - API completa
   - Classes e métodos
   - Glossário

---

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa necessária (biblioteca padrão Python)

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd compilador_lua

# Execute um exemplo
python main.py examples/exemplo.moonlet
```

### Primeiro Programa

Crie um arquivo `meu_programa.moonlet`:

```lua
local x = 10

if x > 5 then
    print("x é maior que 5")
end
```

Execute:

```bash
python main.py meu_programa.moonlet
```

---

## 🎓 Para Quem é Esta Documentação?

### 👨‍🎓 Estudantes e Iniciantes

Se você está aprendendo sobre compiladores, esta documentação foi feita para você! Cada seção começa com explicações de conceitos básicos antes de mergulhar nos detalhes técnicos.

**Comece por aqui:**
- [01_introducao.md](01_introducao.md) - Conceitos fundamentais
- [08_exemplos_uso.md](08_exemplos_uso.md) - Exemplos práticos

### 👨‍💻 Desenvolvedores e Técnicos

Se você já conhece compiladores e quer entender os detalhes de implementação:

**Comece por aqui:**
- [07_estrutura_projeto.md](07_estrutura_projeto.md) - Arquitetura
- [09_referencia_tecnica.md](09_referencia_tecnica.md) - API completa

---

## 📊 Estrutura do Projeto

```
compilador_lua/
├── main.py                    # Ponto de entrada
├── src/                       # Código fonte
│   ├── lexer/                 # Analisador léxico
│   │   └── lexico_moonlet.py
│   ├── parser/                # Analisador sintático
│   │   └── sintatico_moonlet.py
│   ├── ast/                   # Compilador principal
│   │   └── compilador_moonlet.py
│   ├── errors/                # Sistema de erros
│   │   └── erros_moonlet.py
│   └── utils.py              # Utilitários
├── examples/                  # Exemplos de código
│   ├── exemplo.moonlet
│   ├── mepa_if.moonlet
│   ├── mepa_while.moonlet
│   └── ...
└── docs/                      # Esta documentação
    └── ...
```

---

## 🎯 Recursos do Compilador

### ✅ Funcionalidades Implementadas

- ✅ **Análise Léxica completa**
  - Reconhecimento de tokens
  - Comentários de linha e bloco
  - Tratamento de strings e números

- ✅ **Análise Sintática robusta**
  - Parser recursivo descendente
  - Recuperação de erros
  - Construção de AST

- ✅ **Análise Semântica**
  - Tabela de símbolos
  - Verificação de declarações
  - Detecção de uso antes de declaração

- ✅ **Geração de Código MEPA**
  - Expressões aritméticas
  - Estruturas de controle (if, while, for, repeat)
  - Chamadas de função
  - Operações lógicas

### Participantes 

Yago 
Leo
Lucas Seiti
Cintia
