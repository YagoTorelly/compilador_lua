from typing import NamedTuple, Union

# --- Constantes e estruturas ---
ERRO = 0
IDENTIFICADOR = 1
PALAVRA_CHAVE = 2
NUMERO = 3
STRING = 4
OPERADOR = 5
SIMBOLO_ESPECIAL = 6
COMENTARIO = 7
EOS = 8

TOKEN_MAP = {
    ERRO: 'ERRO', IDENTIFICADOR: 'IDENTIFICADOR', PALAVRA_CHAVE: 'PALAVRA_CHAVE',
    NUMERO: 'NUMERO', STRING: 'STRING', OPERADOR: 'OPERADOR',
    SIMBOLO_ESPECIAL: 'SIMBOLO_ESPECIAL', COMENTARIO: 'COMENTARIO', EOS: 'EOS'
}

PALAVRAS_CHAVE = {
    'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
    'function', 'goto', 'if', 'in', 'local', 'nil', 'not', 'or',
    'repeat', 'return', 'then', 'true', 'until', 'while'
}

OPERADORES_DUPLOS = {'==', '~=', '<=', '>=', '..'}
SIMBOLOS_ESPECIAIS = '()[]{}#;:,.\\'
CARACTERES_ESPACO = [' ', '\t', '\r']

class Token(NamedTuple):
    tipo: int
    lexema: str
    valor: Union[int, float, str, None]
    linha: int

# --- Lexer ---
class AnalisadorLexicoMoonlet:
    def __init__(self, codigo_fonte: str):
        self.codigo = codigo_fonte + '\0'
        self.linha = 1
        self.i = 0

    def proximo_char(self) -> str:
        c = self.codigo[self.i]
        self.i += 1
        return c

    def retrair(self):
        self.i -= 1

    def proximo_token(self) -> Token:
        while self.i < len(self.codigo):
            c = self.proximo_char()

            if c in CARACTERES_ESPACO:
                continue
            if c == '\n':
                self.linha += 1
                continue

            if c == '\0':
                return Token(EOS, '', None, self.linha)

            if c == '-':
                if self.codigo[self.i] == '-':
                    return self.tratar_comentario()
                else:
                    return Token(OPERADOR, '-', None, self.linha)

            if c.isalpha() or c == '_':
                self.retrair()
                return self.tratar_identificador_ou_palavra_chave()

            if c.isdigit():
                self.retrair()
                return self.tratar_numero()

            if c == '"' or c == "'":
                return self.tratar_string(delimitador=c)

            if (c in SIMBOLOS_ESPECIAIS) or (c in ['+', '*', '/', '%', '^', '<', '>', '=', '~', '.']):
                self.retrair()
                return self.tratar_operador_ou_simbolo()
            
            return Token(ERRO, c, None, self.linha)

    def tratar_comentario(self) -> Token:
        lexema = '--'
        self.proximo_char()
        
        if self.codigo[self.i] == '[' and self.codigo[self.i+1] == '[':
            lexema += '[['
            self.i += 2
            while not (self.codigo[self.i] == ']' and self.codigo[self.i+1] == ']'):
                char_comentario = self.proximo_char()
                if char_comentario == '\n': self.linha += 1
                lexema += char_comentario
            lexema += ']]'
            self.i += 2
            return Token(COMENTARIO, lexema, None, self.linha)
        else:
            while self.codigo[self.i] not in ['\n', '\0']:
                lexema += self.proximo_char()
            return Token(COMENTARIO, lexema, None, self.linha)

    def tratar_identificador_ou_palavra_chave(self) -> Token:
        lexema = ''
        c = self.proximo_char()
        while c.isalnum() or c == '_':
            lexema += c
            c = self.proximo_char()
        
        self.retrair()

        if lexema in PALAVRAS_CHAVE:
            return Token(PALAVRA_CHAVE, lexema, lexema, self.linha)
        else:
            return Token(IDENTIFICADOR, lexema, lexema, self.linha)

    def tratar_numero(self) -> Token:
        lexema = ''
        tem_ponto = False
        c = self.proximo_char()

        while c.isdigit() or (c == '.' and not tem_ponto):
            if c == '.': tem_ponto = True
            lexema += c
            c = self.proximo_char()
        
        self.retrair()

        if tem_ponto:
            return Token(NUMERO, lexema, float(lexema), self.linha)
        else:
            return Token(NUMERO, lexema, int(lexema), self.linha)

    def tratar_string(self, delimitador: str) -> Token:
        lexema = delimitador
        c = self.proximo_char()
        while c != delimitador and c != '\0':
            lexema += c
            c = self.proximo_char()
        
        if c == '\0':
            return Token(ERRO, lexema, "String não terminada", self.linha)
        
        lexema += delimitador
        valor_string = lexema[1:-1]
        return Token(STRING, lexema, valor_string, self.linha)

    def tratar_operador_ou_simbolo(self) -> Token:
        c1 = self.proximo_char()
        c2 = self.codigo[self.i]

        if c1 == ':' and c2 == ':':
            self.proximo_char()
            return Token(SIMBOLO_ESPECIAL, '::', None, self.linha)

        lexema = c1 + c2
        if lexema in OPERADORES_DUPLOS:
            self.proximo_char()
            return Token(OPERADOR, lexema, None, self.linha)

        if c1 == '.':
            return Token(SIMBOLO_ESPECIAL, c1, None, self.linha)

        if c1 in ['+', '-', '*', '/', '%', '^', '<', '>', '=', '~']:
            return Token(OPERADOR, c1, None, self.linha)

        if c1 in SIMBOLOS_ESPECIAIS:
            return Token(SIMBOLO_ESPECIAL, c1, None, self.linha)
        
        return Token(ERRO, c1, None, self.linha)
