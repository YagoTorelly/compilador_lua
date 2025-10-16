import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ast.compilador_moonlet import AnalisadorMoonlet


def testar_arquivo(nome_arquivo):
    """Testa um arquivo específico"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(base_dir, "examples", nome_arquivo)
    if os.path.exists(caminho):
        print(f"\n{'='*60}")
        print(f"TESTANDO: {nome_arquivo}")
        print('='*60)
        
        compilador = AnalisadorMoonlet()
        ast = compilador.analisar_arquivo(caminho)
        
        if ast:
            compilador.imprimir_ast(ast)
        
        print(f"\n{'='*60}")
    else:
        print(f"Arquivo {caminho} não encontrado!")


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        # Se arquivo foi especificado, testar apenas ele
        nome_arquivo = sys.argv[1]
        testar_arquivo(nome_arquivo)
    else:
        # Testar todos os exemplos
        exemplos = [
            "exemplo.moonlet",
            "exemplo_erro.moonlet", 
        ]
        
        print("TESTANDO COMPILADOR MOONLET")
        print("Executando todos os exemplos...")
        
        for exemplo in exemplos:
            try:
                testar_arquivo(exemplo)
                input("\nPressione Enter para continuar...")
            except KeyboardInterrupt:
                print("\nTeste interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"Erro ao testar {exemplo}: {e}")
                input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
