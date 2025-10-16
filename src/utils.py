"""
Utilitários e configurações para o compilador Moonlet
"""

from src.lexer.lexico_moonlet import (
    ERRO, IDENTIFICADOR, PALAVRA_CHAVE, NUMERO, STRING, 
    OPERADOR, SIMBOLO_ESPECIAL, COMENTARIO, EOS
)

# Mapeamento de tipos de token para nomes legíveis
TOKEN_MAP = {
    ERRO: 'ERRO', 
    IDENTIFICADOR: 'IDENTIFICADOR', 
    PALAVRA_CHAVE: 'PALAVRA_CHAVE',
    NUMERO: 'NUMERO', 
    STRING: 'STRING', 
    OPERADOR: 'OPERADOR',
    SIMBOLO_ESPECIAL: 'SIMBOLO_ESPECIAL', 
    COMENTARIO: 'COMENTARIO', 
    EOS: 'EOS'
}

# Configurações do compilador
CONFIG = {
    'encoding': 'utf-8',
    'indentacao_ast': '  ',  # Dois espaços para indentação na AST
    'separador_linha': '-' * 50,
    'separador_principal': '=' * 60
}

# Mensagens do sistema
MENSAGENS = {
    'sucesso_analise_sintatica': 'Análise sintática concluída com sucesso',
    'erro_analise_sintatica': 'Erro na análise sintática'
}
