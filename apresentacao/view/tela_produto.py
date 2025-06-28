# interface/tela_produto.py

from negocio.service.produto_service import (
    listar_produtos,
    adicionar_produto,
    editar_produto,
    remover_produto
)

def menu_produtos(artesao_email):
    while True:
        print("\n=== Menu do Artesão ===")
        print("1. Listar produtos")
        print("2. Adicionar produto")
        print("3. Editar produto")
        print("4. Remover produto")
        print("5. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_produtos(artesao_email)
        elif opcao == "2":
            adicionar_produto(artesao_email)
        elif opcao == "3":
            editar_produto(artesao_email)
        elif opcao == "4":
            remover_produto(artesao_email)
        elif opcao == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")
