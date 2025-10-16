"""
Compilador completo para o subconjunto Moonlet
Demonstra todas as funcionalidades: análise léxica, sintática e geração de AST
"""

import sys
import os
from typing import Optional

# Adicionar path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

# Imports da estrutura organizada
from ..lexer import AnalisadorLexicoMoonlet
from ..parser import AnalisadorSintaticoMoonlet
from ..parser.sintatico_moonlet import ProgramNode
from ..errors import RelatorioErros
from ..utils import TOKEN_MAP, EOS, ERRO, CONFIG, MENSAGENS
from examples.exemplos_moonlet import obter_exemplo


class ASTVisitor:
    """Classe base para visitantes da AST usando padrão Visitor"""
    pass


class ImpressorAST(ASTVisitor):
    """Visitante para imprimir a AST de forma legível"""
    
    def __init__(self):
        self.indentacao = 0
    
    def _imprimir(self, texto: str):
        """Imprime texto com indentação"""
        print(CONFIG['indentacao_ast'] * self.indentacao + texto)
    
    def _entrar_escopo(self):
        """Aumenta indentação"""
        self.indentacao += 1
    
    def _sair_escopo(self):
        """Diminui indentação"""
        self.indentacao -= 1
    
    def visit_program(self, node: ProgramNode):
        self._imprimir("PROGRAMA")
        self._entrar_escopo()
        for decl in node.declaracoes:
            decl.accept(self)
        self._sair_escopo()
    
    def visit_variable_declaration(self, node):
        local_str = "local " if node.local else ""
        self._imprimir(f"{local_str}DECLARAÇÃO: {node.nome}")
        if node.valor:
            self._entrar_escopo()
            self._imprimir("VALOR:")
            node.valor.accept(self)
            self._sair_escopo()
    
    def visit_assignment(self, node):
        self._imprimir("ATRIBUIÇÃO:")
        self._entrar_escopo()
        self._imprimir("VARIÁVEL:")
        node.variavel.accept(self)
        self._imprimir("VALOR:")
        node.valor.accept(self)
        self._sair_escopo()
    
    def visit_if_statement(self, node):
        self._imprimir("IF-STATEMENT")
        self._entrar_escopo()
        for i, (cond, bloco) in enumerate(zip(node.condicoes, node.blocos)):
            if i == 0:
                self._imprimir("IF:")
            else:
                self._imprimir(f"ELSEIF {i}:")
            self._entrar_escopo()
            self._imprimir("CONDIÇÃO:")
            cond.accept(self)
            self._imprimir("BLOCO:")
            for cmd in bloco:
                cmd.accept(self)
            self._sair_escopo()
        
        if node.bloco_else:
            self._imprimir("ELSE:")
            self._entrar_escopo()
            for cmd in node.bloco_else:
                cmd.accept(self)
            self._sair_escopo()
        self._sair_escopo()
    
    def visit_while_loop(self, node):
        self._imprimir("WHILE-LOOP")
        self._entrar_escopo()
        self._imprimir("CONDIÇÃO:")
        node.condicao.accept(self)
        self._imprimir("CORPO:")
        for cmd in node.corpo:
            cmd.accept(self)
        self._sair_escopo()
    
    def visit_for_loop(self, node):
        self._imprimir(f"FOR-LOOP: {node.variavel}")
        self._entrar_escopo()
        self._imprimir("INÍCIO:")
        node.inicio.accept(self)
        self._imprimir("FIM:")
        node.fim.accept(self)
        if node.passo:
            self._imprimir("PASSO:")
            node.passo.accept(self)
        self._imprimir("CORPO:")
        for cmd in node.corpo:
            cmd.accept(self)
        self._sair_escopo()
    
    def visit_repeat_loop(self, node):
        self._imprimir("REPEAT-LOOP")
        self._entrar_escopo()
        self._imprimir("CORPO:")
        for cmd in node.corpo:
            cmd.accept(self)
        self._imprimir("CONDIÇÃO:")
        node.condicao.accept(self)
        self._sair_escopo()
    
    def visit_function_call(self, node):
        self._imprimir(f"CHAMADA: {node.nome}")
        if node.argumentos:
            self._entrar_escopo()
            self._imprimir("ARGUMENTOS:")
            for arg in node.argumentos:
                arg.accept(self)
            self._sair_escopo()
    
    def visit_function_definition(self, node):
        local_str = "local " if node.local else ""
        self._imprimir(f"{local_str}FUNÇÃO: {node.nome}")
        self._entrar_escopo()
        if node.parametros:
            self._imprimir(f"PARÂMETROS: {', '.join(node.parametros)}")
        self._imprimir("CORPO:")
        for cmd in node.corpo:
            cmd.accept(self)
        self._sair_escopo()
    
    def visit_binary_op(self, node):
        self._imprimir(f"OPERAÇÃO: {node.operador}")
        self._entrar_escopo()
        self._imprimir("ESQUERDA:")
        node.esquerda.accept(self)
        self._imprimir("DIREITA:")
        node.direita.accept(self)
        self._sair_escopo()
    
    def visit_unary_op(self, node):
        self._imprimir(f"OPERAÇÃO UNÁRIA: {node.operador}")
        self._entrar_escopo()
        self._imprimir("OPERANDO:")
        node.operando.accept(self)
        self._sair_escopo()
    
    def visit_literal(self, node):
        self._imprimir(f"LITERAL ({node.tipo}): {node.valor}")
    
    def visit_identifier(self, node):
        self._imprimir(f"IDENTIFICADOR: {node.nome}")
    
    def visit_break(self, node):
        self._imprimir("BREAK")
    
    def visit_goto(self, node):
        self._imprimir(f"GOTO: {node.label}")
    
    def visit_label(self, node):
        self._imprimir(f"LABEL: {node.nome}")
    
    def visit_return(self, node):
        self._imprimir("RETURN")
        if node.valores:
            self._entrar_escopo()
            for valor in node.valores:
                valor.accept(self)
            self._sair_escopo()
    
    def visit_table_access(self, node):
        self._imprimir("ACESSO TABELA")
        self._entrar_escopo()
        self._imprimir("TABELA:")
        node.tabela.accept(self)
        self._imprimir("CHAVE:")
        node.chave.accept(self)
        self._sair_escopo()
    
    def visit_anonymous_function(self, node):
        self._imprimir("FUNÇÃO ANÔNIMA")
        self._entrar_escopo()
        if node.parametros:
            self._imprimir(f"PARÂMETROS: {', '.join(node.parametros)}")
        self._imprimir("CORPO:")
        for cmd in node.corpo:
            cmd.accept(self)
        self._sair_escopo()
    
    def visit_for_in_loop(self, node):
        self._imprimir(f"FOR-IN-LOOP: {', '.join(node.variaveis)}")
        self._entrar_escopo()
        self._imprimir("ITERADOR:")
        node.iterador.accept(self)
        self._imprimir("CORPO:")
        for cmd in node.corpo:
            cmd.accept(self)
        self._sair_escopo()
    
    def visit_block(self, node):
        self._imprimir("BLOCO")
        self._entrar_escopo()
        for decl in node.declaracoes:
            decl.accept(self)
        self._sair_escopo()


class AnalisadorMoonlet:
    """Classe principal do compilador Moonlet"""
    
    def __init__(self):
        self.relatorio_erros = RelatorioErros()
    
    def analisar_arquivo(self, caminho_arquivo: str) -> Optional[ProgramNode]:
        """Analisa um arquivo Moonlet"""
        try:
            with open(caminho_arquivo, 'r', encoding=CONFIG['encoding']) as arquivo:
                codigo = arquivo.read()
            return self.analisar_codigo(codigo, caminho_arquivo)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return None
    
    def analisar_codigo(self, codigo: str, nome_arquivo: str = "<código>") -> Optional[ProgramNode]:
        """Analisa código Moonlet"""
        print(f"=== ANALISANDO: {nome_arquivo} ===\n")
        
        # Análise léxica
        print("1. ANÁLISE LÉXICA")
        print(CONFIG['separador_linha'])
        lexer = AnalisadorLexicoMoonlet(codigo)
        
        # Mostrar tokens
        token = lexer.proximo_token()
        contador_tokens = 0
        erros_lexicos = 0
        
        while token.tipo != EOS:
            print(f"Linha {token.linha:02d} | {TOKEN_MAP[token.tipo]:<18} | '{token.lexema}'")
            if token.tipo == ERRO:
                erros_lexicos += 1
                print(f"           ⚠️  ERRO LÉXICO: Caractere inválido '{token.lexema}' na linha {token.linha}")
            token = lexer.proximo_token()
            contador_tokens += 1
        
        # Mostrar token EOS
        print(f"Linha {token.linha:02d} | {TOKEN_MAP[token.tipo]:<18} | '{token.lexema}'")
        
        if erros_lexicos > 0:
            print(f"\n⚠️  {erros_lexicos} erro(s) léxico(s) encontrado(s)!")
        
        print(f"\nTotal de tokens: {contador_tokens}")
        
        # Análise sintática
        print("\n2. ANÁLISE SINTÁTICA")
        print(CONFIG['separador_linha'])
        
        lexer = AnalisadorLexicoMoonlet(codigo)  # Reinicializar lexer
        parser = AnalisadorSintaticoMoonlet(lexer)
        # Guardar referência para recuperar MEPA depois
        self._ultimo_parser = parser
        
        try:
            ast = parser.analisar()
            print(f"✓ {MENSAGENS['sucesso_analise_sintatica']}")
            
            # Mostrar relatório de erros se houver
            if parser.relatorio_erros.tem_erros():
                print("\n⚠️  Erros encontrados durante a análise:")
                parser.relatorio_erros.imprimir_relatorio()
            
            return ast
            
        except Exception as e:
            print(f"✗ {MENSAGENS['erro_analise_sintatica']}: {e}")
            return None
    
    def imprimir_ast(self, ast: ProgramNode):
        """Imprime a AST de forma legível"""
        print("\n3. ÁRVORE SINTÁTICA ABSTRATA (AST)")
        print(CONFIG['separador_linha'])
        impressor = ImpressorAST()
        ast.accept(impressor)
        # Também exibir o código MEPA gerado, se houver
        print("\n4. CÓDIGO INTERMEDIÁRIO (MEPA)")
        print(CONFIG['separador_linha'])
        try:
            codigo_mepa = getattr(self, '_ultimo_parser', None).codigo_mepa  # type: ignore[attr-defined]
            if codigo_mepa:
                for instr in codigo_mepa:
                    print(instr)
            else:
                print("(sem instruções MEPA geradas)")
        except Exception:
            print("(MEPA indisponível nesta execução)")
    
    def executar_teste_exemplo(self):
        """Executa um exemplo de teste"""
        codigo_exemplo = obter_exemplo('completo')
        ast = self.analisar_codigo(codigo_exemplo, "exemplo.moonlet")
        if ast:
            self.imprimir_ast(ast)


def main():
    """Função principal"""
    print("=== COMPILADOR MOONLET ===")
    print("Subconjunto da linguagem Lua")
    print(CONFIG['separador_principal'])
    
    compilador = AnalisadorMoonlet()
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
        if os.path.exists(arquivo):
            ast = compilador.analisar_arquivo(arquivo)
            if ast:
                compilador.imprimir_ast(ast)
        else:
            print(f"Arquivo '{arquivo}' não encontrado.")
    else:
        # Executar exemplo se nenhum arquivo for fornecido
        print("Nenhum arquivo especificado. Executando exemplo...\n")
        compilador.executar_teste_exemplo()
    
    print("\n" + CONFIG['separador_principal'])
    print("Compilação concluída!")


if __name__ == "__main__":
    main()