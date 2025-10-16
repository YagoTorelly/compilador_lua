"""
Sistema de tratamento de erros para o compilador Moonlet (versão minimalista)
Implementa diferentes tipos de erros e exceções específicas
"""

from typing import Optional, List
from dataclasses import dataclass


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


class ErroLexico(ErroCompilacao):
    """Erro durante a análise léxica"""
    
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None):
        super().__init__(f"Erro léxico: {mensagem}", posicao)


class ErroSintatico(ErroCompilacao):
    """Erro durante a análise sintática"""
    
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None, 
                 token_esperado: Optional[str] = None, token_encontrado: Optional[str] = None):
        self.token_esperado = token_esperado
        self.token_encontrado = token_encontrado
        
        if token_esperado and token_encontrado:
            mensagem_completa = f"Erro sintático: {mensagem}. Esperado '{token_esperado}', encontrado '{token_encontrado}'"
        else:
            mensagem_completa = f"Erro sintático: {mensagem}"
            
        super().__init__(mensagem_completa, posicao)


class ErroSemantico(ErroCompilacao):
    """Erro durante a análise semântica (não usado nesta versão minimalista)"""
    
    def __init__(self, mensagem: str, posicao: Optional[PosicaoErro] = None):
        super().__init__(f"Erro semântico: {mensagem}", posicao)


class RelatorioErros:
    """Classe para coletar e reportar múltiplos erros"""
    
    def __init__(self):
        self.erros: List[ErroCompilacao] = []
        self.avisos: List[str] = []
    
    def adicionar_erro(self, erro: ErroCompilacao):
        self.erros.append(erro)
    
    def tem_erros(self) -> bool:
        return len(self.erros) > 0
    
    def imprimir_relatorio(self):
        if self.tem_erros():
            print("=== ERROS ENCONTRADOS ===")
            for i, erro in enumerate(self.erros, 1):
                print(f"{i}. {erro}")
            print()


# Utilitários de erro

def criar_erro_token_inesperado(token_encontrado: str, posicao: PosicaoErro) -> ErroSintatico:
    return ErroSintatico(
        "Token inesperado",
        posicao,
        token_encontrado=token_encontrado
    )


def criar_erro_token_esperado(token_esperado: str, token_encontrado: str, posicao: PosicaoErro) -> ErroSintatico:
    return ErroSintatico(
        "Token esperado não encontrado",
        posicao,
        token_esperado=token_esperado,
        token_encontrado=token_encontrado
    )


def criar_erro_fim_arquivo_inesperado(posicao: PosicaoErro) -> ErroSintatico:
    return ErroSintatico(
        "Fim de arquivo inesperado",
        posicao
    )