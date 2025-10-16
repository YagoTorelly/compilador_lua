"""AST e classes relacionadas"""
from .compilador_moonlet import ImpressorAST, AnalisadorMoonlet

# Classes base para AST (definidas no parser por simplicidade)
from ..parser.sintatico_moonlet import ASTNode, ProgramNode

# Visitor pattern
class ASTVisitor:
    """Classe base para visitantes da AST"""
    def visit(self, node):
        """Método genérico de visitação"""
        method_name = f'visit_{node.__class__.__name__.lower().replace("node", "")}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        """Visitação genérica para nós não tratados especificamente"""
        pass
