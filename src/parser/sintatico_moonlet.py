from typing import List, Optional, Union
from ..errors.erros_moonlet import (
    ErroSintatico, PosicaoErro, RelatorioErros,
    criar_erro_token_esperado, criar_erro_fim_arquivo_inesperado,
    ErroSemantico
)
from ..lexer.lexico_moonlet import (
    ERRO, IDENTIFICADOR, PALAVRA_CHAVE, NUMERO, STRING,
    OPERADOR, SIMBOLO_ESPECIAL, COMENTARIO, EOS,
    TOKEN_MAP, PALAVRAS_CHAVE, OPERADORES_DUPLOS, SIMBOLOS_ESPECIAIS,
    Token, AnalisadorLexicoMoonlet
)

# --- Definições de nós de AST simples ---
class ASTNode: 
    def accept(self, visitor):
        """Método para padrão Visitor"""
        # Obter o nome da classe sem o sufixo 'Node' e em minúsculas
        class_name = self.__class__.__name__.lower().replace('node', '')
        method_name = f'visit_{class_name}'
        method = getattr(visitor, method_name, None)
        if method:
            return method(self)
        else:
            return visitor.generic_visit(self) if hasattr(visitor, 'generic_visit') else None

class LiteralNode(ASTNode):
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo

class IdentifierNode(ASTNode):
    def __init__(self, nome):
        self.nome = nome

class BinaryOpNode(ASTNode):
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

class UnaryOpNode(ASTNode):
    def __init__(self, operador, operando):
        self.operador = operador
        self.operando = operando

class FunctionCallNode(ASTNode):
    def __init__(self, nome, argumentos):
        self.nome = nome
        self.argumentos = argumentos

class TableAccessNode(ASTNode):
    def __init__(self, tabela, chave, notacao_ponto=False):
        self.tabela = tabela
        self.chave = chave
        self.notacao_ponto = notacao_ponto

class VariableDeclarationNode(ASTNode):
    def __init__(self, nome, valor, local=False):
        self.nome = nome
        self.valor = valor
        self.local = local

class AssignmentNode(ASTNode):
    def __init__(self, variavel, valor):
        self.variavel = variavel
        self.valor = valor

class IfStatementNode(ASTNode):
    def __init__(self, condicoes, blocos, bloco_else=None):
        self.condicoes = condicoes
        self.blocos = blocos
        self.bloco_else = bloco_else

class WhileLoopNode(ASTNode):
    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo

class RepeatLoopNode(ASTNode):
    def __init__(self, corpo, condicao):
        self.corpo = corpo
        self.condicao = condicao

class ForLoopNode(ASTNode):
    def __init__(self, variavel, inicio, fim, passo, corpo):
        self.variavel = variavel
        self.inicio = inicio
        self.fim = fim
        self.passo = passo
        self.corpo = corpo

class ForInLoopNode(ASTNode):
    def __init__(self, variaveis, iterador, corpo):
        self.variaveis = variaveis
        self.iterador = iterador
        self.corpo = corpo

class BreakNode(ASTNode):
    pass

class GotoNode(ASTNode):
    def __init__(self, label):
        self.label = label

class LabelNode(ASTNode):
    def __init__(self, nome):
        self.nome = nome

class ReturnNode(ASTNode):
    def __init__(self, valores):
        self.valores = valores

class FunctionDefinitionNode(ASTNode):
    def __init__(self, nome, parametros, corpo, local=False):
        self.nome = nome
        self.parametros = parametros
        self.corpo = corpo
        self.local = local

class AnonymousFunctionNode(ASTNode):
    def __init__(self, parametros, corpo):
        self.parametros = parametros
        self.corpo = corpo

class BlockNode(ASTNode):
    def __init__(self, declaracoes):
        self.declaracoes = declaracoes

class ProgramNode(ASTNode):
    def __init__(self, declaracoes):
        self.declaracoes = declaracoes


class AnalisadorSintaticoMoonlet:
    def __init__(self, lexer: AnalisadorLexicoMoonlet):
        self.lexer = lexer
        self.token_atual: Optional[Token] = None
        self.relatorio_erros = RelatorioErros()
        self._avancar_token()  # ✅ CORRIGIDO: Inicializar token atual    self._avancar_token()
        # ---------------- Semântica ----------------
        # Tabela de símbolos simples: nome -> {endereco: int, tipo: str}
        self.tabela_simbolos = {}
        self.proximo_endereco = 0  # endereço sequencial de variáveis
        # Estrutura para geração de código (MEPA)
        self.codigo_mepa = []  # lista de strings de instruções MEPA
        self._contador_rotulos = 0
        # Flag para suprimir carregamento de identificadores quando em contexto de LHS (atribuição)
        self._suprimir_carregamento_identificador = False
        # Gerador de temporários
        self._temp_id = 0

    # ---------------- Suporte a MEPA ----------------
    def _novo_rotulo(self, base: str = 'L') -> str:
        rot = f"{base}{self._contador_rotulos}"
        self._contador_rotulos += 1
        return rot

    def _emitir(self, instr: str):
        self.codigo_mepa.append(instr)
    
    def _alocar_temporario(self, hint: str = "t") -> int:
        nome = f"__tmp{self._temp_id}_{hint}"
        self._temp_id += 1
        # Registrar no quadro de símbolos como variável interna
        self.tabela_simbolos[nome] = { 'endereco': self.proximo_endereco, 'tipo': 'int' }
        self.proximo_endereco += 1
        return self.tabela_simbolos[nome]['endereco']

    def _assegurar_variavel(self, nome: str) -> int:
        """Garante que a variável exista na tabela de símbolos e retorna seu endereço."""
        if nome not in self.tabela_simbolos:
            self._declarar_variavel(nome)
        return self.tabela_simbolos[nome]['endereco']
    
    def _avancar_token(self):
        """Avança token ignorando comentários"""
        self.token_atual = self.lexer.proximo_token()
        # Pular comentários durante análise sintática
        while self.token_atual and self.token_atual.tipo == COMENTARIO:
            self.token_atual = self.lexer.proximo_token()
    
    def _criar_posicao_erro(self) -> PosicaoErro:
        if self.token_atual:
            return PosicaoErro(self.token_atual.linha, 0)
        return PosicaoErro(0, 0)
    
    def _verificar_token_especifico(self, tipo: int, valor: str = None) -> bool:
        if not self.token_atual:
            return False
        if self.token_atual.tipo != tipo:
            return False
        if valor is not None and self.token_atual.lexema != valor:
            return False
        return True
    
    def _consumir_token_especifico(self, tipo: int, valor: str, mensagem_erro: str = "") -> Token:
        if not self._verificar_token_especifico(tipo, valor):
            token_encontrado = self.token_atual.lexema if self.token_atual else "EOF"
            raise criar_erro_token_esperado(valor, token_encontrado, self._criar_posicao_erro())
        token = self.token_atual
        self._avancar_token()
        return token
    
    def _verificar_operador(self, operador: str) -> bool:
        return self._verificar_token_especifico(OPERADOR, operador)
    
    def _verificar_palavra_chave(self, palavra: str) -> bool:
        return self._verificar_token_especifico(PALAVRA_CHAVE, palavra)
    
    def _verificar_simbolo(self, simbolo: str) -> bool:
        return self._verificar_token_especifico(SIMBOLO_ESPECIAL, simbolo)
    
    def _verificar_token(self, tipo: int) -> bool:
        return self._verificar_token_especifico(tipo)
    
    def _consumir_operador(self, operador: str) -> Token:
        return self._consumir_token_especifico(OPERADOR, operador)
    
    def _consumir_simbolo(self, simbolo: str) -> Token:
        return self._consumir_token_especifico(SIMBOLO_ESPECIAL, simbolo)
    
    def _consumir_palavra_chave(self, palavra: str) -> Token:
        return self._consumir_token_especifico(PALAVRA_CHAVE, palavra)
    
    def _consumir_token(self, tipo_esperado: int, mensagem_erro: str = "") -> Token:
        if not self.token_atual:
            raise criar_erro_fim_arquivo_inesperado(self._criar_posicao_erro())
        if self.token_atual.tipo == tipo_esperado:
            token = self.token_atual
            self._avancar_token()
            return token
        raise criar_erro_token_esperado(
            TOKEN_MAP.get(tipo_esperado, "desconhecido"),
            TOKEN_MAP.get(self.token_atual.tipo, "desconhecido"),
            self._criar_posicao_erro()
        )

    # ---------------- Utilitários semânticos ----------------
    def _declarar_variavel(self, nome: str):
        if nome in self.tabela_simbolos:
            raise ErroSemantico(
                f"Variável '{nome}' já declarada",
                self._criar_posicao_erro()
            )
        self.tabela_simbolos[nome] = { 'endereco': self.proximo_endereco, 'tipo': 'int' }
        self.proximo_endereco += 1

    def _obter_variavel(self, nome: str):
        simbolo = self.tabela_simbolos.get(nome)
        if simbolo is None:
            raise ErroSemantico(
                f"Variável '{nome}' não declarada",
                self._criar_posicao_erro()
            )
        return simbolo
    
    def analisar(self) -> ProgramNode:
        declaracoes = []
        
        while self.token_atual and self.token_atual.tipo != EOS:
            try:
                declaracao = self._analisar_declaracao()
                if declaracao:
                    declaracoes.append(declaracao)
            except ErroSintatico as e:
                self.relatorio_erros.adicionar_erro(e)
                print(f"           ⚠️  ERRO SINTÁTICO: {e}")
                # Tentar recuperar pulando para próximo token válido
                self._pular_ate_proximo_valido()
                
        return ProgramNode(declaracoes)
    
    def _pular_ate_proximo_valido(self):
        """Pula tokens até encontrar um válido para continuar análise"""
        while (self.token_atual and 
               self.token_atual.tipo not in [EOS, PALAVRA_CHAVE] and
               not (self.token_atual.tipo == IDENTIFICADOR)):
            print(f"           🔄 Pulando token: '{self.token_atual.lexema}'")
            self._avancar_token()
    
    def _tentar_recuperar_erro(self) -> ProgramNode:
        while self.token_atual and self.token_atual.tipo != EOS:
            if (self.token_atual.tipo == PALAVRA_CHAVE and 
                self.token_atual.lexema in ['end', 'else', 'elseif', 'until', ';', '\n']):
                break
            self._avancar_token()
        return ProgramNode([])
    
    def _analisar_declaracao(self) -> Optional[ASTNode]:
        if not self.token_atual:
            return None
            
        # ✅ CORRIGIDO: Tratar tokens de erro
        if self.token_atual.tipo == ERRO:
            print(f"           ⚠️  ERRO SINTÁTICO: Token inválido '{self.token_atual.lexema}' na linha {self.token_atual.linha}")
            self._avancar_token()  # Pular token de erro
            return None
            
        if self._verificar_palavra_chave('local'):
            return self._analisar_declaracao_variavel()
        if self._verificar_palavra_chave('function'):
            return self._analisar_definicao_funcao()
        if self._verificar_simbolo('::'):
            return self._analisar_label()
        return self._analisar_comando()
    
    def _analisar_declaracao_variavel(self) -> VariableDeclarationNode:
        self._consumir_palavra_chave('local')
        if not self._verificar_token(IDENTIFICADOR):
            raise criar_erro_token_esperado("identificador", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
        nome = self.token_atual.lexema
        self._avancar_token()
        # Semântica: declarar variável na tabela (checa duplicidade)
        self._declarar_variavel(nome)
        valor = None
        if self._verificar_operador('='):
            self._avancar_token()
            valor = self._analisar_expressao()
        # MEPA: reserva endereço para variável (ALME apenas exemplificativo)
        # Em muitas arquiteturas didáticas, a alocação é tratada na entrada do programa;
        # aqui apenas registramos simbolicamente.
        self._emitir(f"; decl local {nome} @ {self.tabela_simbolos[nome]['endereco']}")
        return VariableDeclarationNode(nome, valor, local=True)
    
    def _analisar_definicao_funcao(self) -> 'FunctionDefinitionNode':
        local = False
        if self._verificar_palavra_chave('local'):
            self._avancar_token()
            local = True
        self._consumir_palavra_chave('function')
        if not self._verificar_token(IDENTIFICADOR):
            raise criar_erro_token_esperado("identificador", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
        nome = self.token_atual.lexema
        self._avancar_token()
        parametros = self._analisar_lista_parametros()
        corpo = self._analisar_bloco()
        self._consumir_palavra_chave('end')
        return FunctionDefinitionNode(nome, parametros, corpo, local)
    
    def _analisar_lista_parametros(self) -> List[str]:
        self._consumir_simbolo('(')
        parametros = []
        if not self._verificar_simbolo(')'):
            while True:
                if not self._verificar_token(IDENTIFICADOR):
                    raise criar_erro_token_esperado("identificador", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
                parametros.append(self.token_atual.lexema)
                self._avancar_token()
                if self._verificar_simbolo(','):
                    self._avancar_token()
                else:
                    break
        self._consumir_simbolo(')')
        return parametros
    
    def _analisar_label(self) -> LabelNode:
        self._consumir_simbolo('::')
        if not self._verificar_token(IDENTIFICADOR):
            raise criar_erro_token_esperado("identificador", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
        nome = self.token_atual.lexema
        self._avancar_token()
        self._consumir_simbolo('::')
        return LabelNode(nome)
    
    def _analisar_comando(self) -> Optional[ASTNode]:
        if not self.token_atual:
            return None
        if self._verificar_palavra_chave('if'):
            return self._analisar_comando_if()
        if self._verificar_palavra_chave('while'):
            return self._analisar_comando_while()
        if self._verificar_palavra_chave('repeat'):
            return self._analisar_comando_repeat()
        if self._verificar_palavra_chave('for'):
            return self._analisar_comando_for()
        if self._verificar_palavra_chave('break'):
            self._avancar_token()
            return BreakNode()
        if self._verificar_palavra_chave('goto'):
            return self._analisar_comando_goto()
        if self._verificar_palavra_chave('return'):
            return self._analisar_comando_return()
        if self._verificar_token(IDENTIFICADOR):
            return self._analisar_atribuicao_ou_chamada()
        return None
    
    def _analisar_comando_if(self) -> IfStatementNode:
        self._consumir_palavra_chave('if')
        condicoes = []
        blocos = []
        rotulo_fim = self._novo_rotulo('I')

        # IF principal
        condicao = self._analisar_expressao()
        condicoes.append(condicao)
        rotulo_proximo = self._novo_rotulo('I')
        # Se condição for falsa, pula para o próximo ramo
        self._emitir("DSVF " + rotulo_proximo)
        
        # ✅ Tentar consumir 'then' mas continuar se falhar
        if self._verificar_palavra_chave('then'):
            self._avancar_token()
        else:
            erro = criar_erro_token_esperado('then', self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
            self.relatorio_erros.adicionar_erro(erro)
            print(f"           ⚠️  ERRO SINTÁTICO: {erro}")
        
        bloco = self._analisar_bloco()
        blocos.append(bloco)
        # Após executar o bloco do IF, salta para o fim do IF
        self._emitir("DSVS " + rotulo_fim)
        # Rótulo do próximo ramo (ELSEIF/ELSE)
        self._emitir(f"{rotulo_proximo}:")
        
        # ELSEIFs
        while self._verificar_palavra_chave('elseif'):
            self._avancar_token()
            condicao = self._analisar_expressao()
            condicoes.append(condicao)
            rotulo_proximo = self._novo_rotulo('I')
            self._emitir("DSVF " + rotulo_proximo)
            if self._verificar_palavra_chave('then'):
                self._avancar_token()
            else:
                erro = criar_erro_token_esperado('then', self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
                self.relatorio_erros.adicionar_erro(erro)
                print(f"           ⚠️  ERRO SINTÁTICO: {erro}")
            bloco = self._analisar_bloco()
            blocos.append(bloco)
            self._emitir("DSVS " + rotulo_fim)
            self._emitir(f"{rotulo_proximo}:")
            
        # ELSE opcional
        bloco_else = None
        if self._verificar_palavra_chave('else'):
            self._avancar_token()
            bloco_else = self._analisar_bloco()
            # (queda direta para o fim)
            
        # ✅ Consumir 'end' (reportar se faltar)
        if self._verificar_palavra_chave('end'):
            self._avancar_token()
        else:
            erro = criar_erro_token_esperado('end', self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
            self.relatorio_erros.adicionar_erro(erro)
            print(f"           ⚠️  ERRO SINTÁTICO: {erro}")
        
        # Rótulo de fim do IF
        self._emitir(f"{rotulo_fim}:")
        
        return IfStatementNode(condicoes, blocos, bloco_else)
    
    def _analisar_comando_while(self) -> WhileLoopNode:
        self._consumir_palavra_chave('while')
        rot_inicio = self._novo_rotulo('W')
        rot_fim = self._novo_rotulo('W')
        self._emitir(f"{rot_inicio}:")
        condicao = self._analisar_expressao()
        # MEPA: expressão no topo da pilha; salto se falso para fim
        self._emitir("DSVF " + rot_fim)
        self._consumir_palavra_chave('do')
        corpo = self._analisar_bloco()
        # MEPA: volta para o início e coloca rótulo fim
        self._emitir("DSVS " + rot_inicio)
        self._emitir(f"{rot_fim}:")
        self._consumir_palavra_chave('end')
        return WhileLoopNode(condicao, corpo)
    
    def _analisar_comando_repeat(self) -> RepeatLoopNode:
        self._consumir_palavra_chave('repeat')
        rot_inicio = self._novo_rotulo('R')
        self._emitir(f"{rot_inicio}:")
        corpo = self._analisar_bloco()
        self._consumir_palavra_chave('until')
        condicao = self._analisar_expressao()
        # Repete enquanto condição for falsa
        self._emitir("DSVF " + rot_inicio)
        return RepeatLoopNode(corpo, condicao)
    
    def _analisar_comando_for(self) -> Union[ForLoopNode, ForInLoopNode]:
        self._consumir_palavra_chave('for')
        if not self._verificar_token(IDENTIFICADOR):
            raise criar_erro_token_esperado("identificador", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
        variavel = self.token_atual.lexema
        self._avancar_token()
        if self._verificar_operador('='):
            self._avancar_token()
            # início
            inicio = self._analisar_expressao()
            # armazenar valor inicial na variável do laço
            end_var = self._assegurar_variavel(variavel)
            self._emitir(f"ARMZ {end_var}")
            self._consumir_simbolo(',')
            # fim
            fim = self._analisar_expressao()
            end_tmp_fim = self._alocar_temporario('fim')
            self._emitir(f"ARMZ {end_tmp_fim}")
            passo = None
            if self._verificar_simbolo(','):
                self._avancar_token()
                passo = self._analisar_expressao()
                end_tmp_passo = self._alocar_temporario('passo')
                self._emitir(f"ARMZ {end_tmp_passo}")
            else:
                # passo padrão = 1
                end_tmp_passo = self._alocar_temporario('passo')
                self._emitir("CRCT 1")
                self._emitir(f"ARMZ {end_tmp_passo}")
            self._consumir_palavra_chave('do')
            # MEPA do laço
            rot_inicio = self._novo_rotulo('F')
            rot_fim = self._novo_rotulo('F')
            self._emitir(f"{rot_inicio}:")
            # condição: var <= fim (assumimos passo positivo)
            self._emitir(f"CRVL {end_var}")
            self._emitir(f"CRVL {end_tmp_fim}")
            self._emitir("CMEG")
            self._emitir(f"DSVF {rot_fim}")
            # corpo
            corpo = self._analisar_bloco()
            # incremento: var = var + passo
            self._emitir(f"CRVL {end_var}")
            self._emitir(f"CRVL {end_tmp_passo}")
            self._emitir("SOMA")
            self._emitir(f"ARMZ {end_var}")
            self._emitir(f"DSVS {rot_inicio}")
            self._emitir(f"{rot_fim}:")
            self._consumir_palavra_chave('end')
            return ForLoopNode(variavel, inicio, fim, passo, corpo)
        elif self._verificar_palavra_chave('in'):
            self._avancar_token()
            # Suporte a for-in numérico: for v in inicio, fim[, passo] do ... end
            # Parse 'inicio'
            inicio_expr = self._analisar_expressao()
            # Guardar em variável do laço
            end_var = self._assegurar_variavel(variavel)
            self._emitir(f"ARMZ {end_var}")
            # Esperar pelo menos uma vírgula e 'fim'
            if not self._verificar_simbolo(','):
                raise ErroSemantico("for-in numérico requer pelo menos duas expressões (início, fim)", self._criar_posicao_erro())
            self._avancar_token()
            fim_expr = self._analisar_expressao()
            end_tmp_fim = self._alocar_temporario('fim')
            self._emitir(f"ARMZ {end_tmp_fim}")
            # Passo opcional
            if self._verificar_simbolo(','):
                self._avancar_token()
                passo_expr = self._analisar_expressao()
                end_tmp_passo = self._alocar_temporario('passo')
                self._emitir(f"ARMZ {end_tmp_passo}")
            else:
                end_tmp_passo = self._alocar_temporario('passo')
                self._emitir("CRCT 1")
                self._emitir(f"ARMZ {end_tmp_passo}")
            self._consumir_palavra_chave('do')
            # MEPA do laço (mesma lógica do for numérico)
            rot_inicio = self._novo_rotulo('G')
            rot_fim = self._novo_rotulo('G')
            self._emitir(f"{rot_inicio}:")
            self._emitir(f"CRVL {end_var}")
            self._emitir(f"CRVL {end_tmp_fim}")
            self._emitir("CMEG")
            self._emitir(f"DSVF {rot_fim}")
            corpo = self._analisar_bloco()
            self._emitir(f"CRVL {end_var}")
            self._emitir(f"CRVL {end_tmp_passo}")
            self._emitir("SOMA")
            self._emitir(f"ARMZ {end_var}")
            self._emitir(f"DSVS {rot_inicio}")
            self._emitir(f"{rot_fim}:")
            self._consumir_palavra_chave('end')
            return ForInLoopNode([variavel], fim_expr, corpo)
        else:
            raise criar_erro_token_esperado("'=' ou 'in'", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
    
    def _analisar_comando_goto(self) -> GotoNode:
        self._consumir_palavra_chave('goto')
        if not self._verificar_token(IDENTIFICADOR):
            raise criar_erro_token_esperado("identificador", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
        label = self.token_atual.lexema
        self._avancar_token()
        return GotoNode(label)
    
    def _analisar_comando_return(self) -> ReturnNode:
        self._consumir_palavra_chave('return')
        valores = []
        if not self._verificar_palavra_chave('end') and not self._verificar_simbolo(';'):
            while True:
                valor = self._analisar_expressao()
                valores.append(valor)
                if self._verificar_simbolo(','):
                    self._avancar_token()
                else:
                    break
        return ReturnNode(valores)
    
    def _analisar_atribuicao_ou_chamada(self) -> Union[AssignmentNode, FunctionCallNode]:
        # Para lado esquerdo (LHS) de atribuição, suprimir CRVL de identificadores
        flag_antigo = self._suprimir_carregamento_identificador
        self._suprimir_carregamento_identificador = True
        expressao = self._analisar_expressao()
        self._suprimir_carregamento_identificador = flag_antigo
        if self._verificar_operador('='):
            self._avancar_token()
            valor = self._analisar_expressao()
            # MEPA para atribuição simples: variável à esquerda deve ser identificador
            if isinstance(expressao, IdentifierNode):
                simbolo = self._obter_variavel(expressao.nome)
                self._emitir(f"ARMZ {simbolo['endereco']}")
            return AssignmentNode(expressao, valor)
        if isinstance(expressao, FunctionCallNode):
            return expressao
        return expressao
    
    def _analisar_bloco(self) -> List[ASTNode]:
        comandos = []
        while (self.token_atual and self.token_atual.tipo != EOS and
               not self._verificar_palavra_chave('end') and
               not self._verificar_palavra_chave('else') and
               not self._verificar_palavra_chave('elseif') and
               not self._verificar_palavra_chave('until')):
            comando = self._analisar_declaracao()
            if comando:
                comandos.append(comando)
        return comandos
    
    def _analisar_expressao(self) -> ASTNode:
        return self._analisar_expressao_or()
    
    def _analisar_expressao_or(self) -> ASTNode:
        esquerda = self._analisar_expressao_and()
        while self._verificar_palavra_chave('or'):
            operador = self.token_atual.lexema
            self._avancar_token()
            direita = self._analisar_expressao_and()
            esquerda = BinaryOpNode(operador, esquerda, direita)
        return esquerda
    
    def _analisar_expressao_and(self) -> ASTNode:
        esquerda = self._analisar_expressao_relacional()
        while self._verificar_palavra_chave('and'):
            operador = self.token_atual.lexema
            self._avancar_token()
            direita = self._analisar_expressao_relacional()
            esquerda = BinaryOpNode(operador, esquerda, direita)
        return esquerda
    
    def _analisar_expressao_relacional(self) -> ASTNode:
        esquerda = self._analisar_expressao_concat()
        for op in ['<', '>', '<=', '>=', '==', '~=']:
            if self._verificar_operador(op):
                operador = self.token_atual.lexema
                self._avancar_token()
                direita = self._analisar_expressao_concat()
                esquerda = BinaryOpNode(operador, esquerda, direita)
                # MEPA: após avaliar, comparar no topo da pilha
                mapa = {
                    '<': 'CMME', '>': 'CMMA', '<=': 'CMEG', '>=': 'CMAG', '==': 'CMIG', '~=': 'CMDG'
                }
                self._emitir(mapa[operador])
        return esquerda
    
    def _analisar_expressao_concat(self) -> ASTNode:
        esquerda = self._analisar_expressao_aditiva()
        while self._verificar_operador('..'):
            operador = self.token_atual.lexema
            self._avancar_token()
            direita = self._analisar_expressao_aditiva()
            esquerda = BinaryOpNode(operador, esquerda, direita)
        return esquerda
    
    def _analisar_expressao_aditiva(self) -> ASTNode:
        esquerda = self._analisar_expressao_multiplicativa()
        while self._verificar_operador('+') or self._verificar_operador('-'):
            operador = self.token_atual.lexema
            self._avancar_token()
            direita = self._analisar_expressao_multiplicativa()
            esquerda = BinaryOpNode(operador, esquerda, direita)
            self._emitir('SOMA' if operador == '+' else 'SUBT')
        return esquerda
    
    def _analisar_expressao_multiplicativa(self) -> ASTNode:
        esquerda = self._analisar_expressao_unaria()
        for op in ['*', '/', '%', '^']:
            if self._verificar_operador(op):
                operador = self.token_atual.lexema
                self._avancar_token()
                direita = self._analisar_expressao_unaria()
                esquerda = BinaryOpNode(operador, esquerda, direita)
                if operador == '*':
                    self._emitir('MULT')
                elif operador == '/':
                    self._emitir('DIVI')
                elif operador == '%':
                    self._emitir('MODI')
                elif operador == '^':
                    self._emitir('POTI')
        return esquerda
    
    def _analisar_expressao_unaria(self) -> ASTNode:
        if self._verificar_palavra_chave('not'):
            operador = self.token_atual.lexema
            self._avancar_token()
            operando = self._analisar_expressao_unaria()
            return UnaryOpNode(operador, operando)
        for operador in ['-', '#']:
            if self._verificar_operador(operador):
                self._avancar_token()
                operando = self._analisar_expressao_unaria()
                if operador == '-':
                    self._emitir('INVR')
                return UnaryOpNode(operador, operando)
        return self._analisar_expressao_primaria()
    
    def _analisar_expressao_primaria(self) -> ASTNode:
        if not self.token_atual:
            raise criar_erro_fim_arquivo_inesperado(self._criar_posicao_erro())
        if self.token_atual.tipo == NUMERO:
            valor = self.token_atual.valor
            self._avancar_token()
            # MEPA: empilha literal numérico
            self._emitir(f"CRCT {valor}")
            return LiteralNode(valor, 'number')
        if self.token_atual.tipo == STRING:
            valor = self.token_atual.valor
            self._avancar_token()
            return LiteralNode(valor, 'string')
        for palavra, (valor, tipo) in {'true': (True, 'boolean'), 'false': (False, 'boolean'), 'nil': (None, 'nil')}.items():
            if self._verificar_palavra_chave(palavra):
                self._avancar_token()
                return LiteralNode(valor, tipo)
        if self.token_atual.tipo == IDENTIFICADOR:
            nome = self.token_atual.lexema
            self._avancar_token()
            if self._verificar_simbolo('('):
                return self._analisar_chamada_funcao(nome)
            if self._verificar_simbolo('[') or self._verificar_simbolo('.'):
                return self._analisar_acesso_tabela(IdentifierNode(nome))
            # Semântica: uso de variável – deve ter sido declarada
            self._obter_variavel(nome)
            # MEPA: carrega variável (se não estivermos suprimindo em contexto de LHS)
            if not self._suprimir_carregamento_identificador:
                simbolo = self.tabela_simbolos[nome]
                self._emitir(f"CRVL {simbolo['endereco']}")
            return IdentifierNode(nome)
        if self._verificar_simbolo('('):
            self._avancar_token()
            expressao = self._analisar_expressao()
            self._consumir_simbolo(')')
            return expressao
        if self._verificar_palavra_chave('function'):
            return self._analisar_funcao_anonima()
        if self._verificar_simbolo('{'):
            self._consumir_simbolo('{')
            # Tabela vazia por simplicidade
            self._consumir_simbolo('}')
            return LiteralNode({}, 'table')
        raise criar_erro_token_esperado("expressão", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
    
    def _analisar_chamada_funcao(self, nome: str) -> FunctionCallNode:
        self._consumir_simbolo('(')
        argumentos = []
        if not self._verificar_simbolo(')'):
            while True:
                argumento = self._analisar_expressao()
                argumentos.append(argumento)
                if self._verificar_simbolo(','):
                    self._avancar_token()
                else:
                    break
        self._consumir_simbolo(')')
        return FunctionCallNode(nome, argumentos)
    
    def _analisar_acesso_tabela(self, tabela) -> TableAccessNode:
        if self._verificar_simbolo('['):
            self._avancar_token()
            chave = self._analisar_expressao()
            self._consumir_simbolo(']')
            return TableAccessNode(tabela, chave, False)
        elif self._verificar_simbolo('.'):
            self._avancar_token()
            if not self._verificar_token(IDENTIFICADOR):
                raise criar_erro_token_esperado("identificador", self.token_atual.lexema if self.token_atual else "EOF", self._criar_posicao_erro())
            chave = IdentifierNode(self.token_atual.lexema)
            self._avancar_token()
            return TableAccessNode(tabela, chave, True)
        return tabela
    
    def _analisar_funcao_anonima(self):
        self._consumir_palavra_chave('function')
        parametros = self._analisar_lista_parametros()
        corpo = self._analisar_bloco()
        self._consumir_palavra_chave('end')
        return AnonymousFunctionNode(parametros, corpo)
