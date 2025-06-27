import negocio.model.usuario as usuario
from negocio.service.pedido_service import finalizar_pedido
from negocio.service.produto_service import carregar_produtos, listar_todos_os_produtos, buscar_produto_por_id
from negocio.service.carrinho_service import (
    adicionar_ao_carrinho,
    listar_itens_carrinho,
    remover_item_carrinho,
    alterar_quantidade_item
)

from apresentacao.view.tela_produto import menu_produtos
from negocio.service.usuario_service import buscar_por_email


def tela_usuario(email):
    usuario_obj = buscar_por_email(email)
    if usuario_obj:
        print(f"\nBem-vindo, {usuario_obj.nome}!")

        if usuario_obj.tipo.lower().startswith('a'):
            menu_produtos(usuario_obj.email)

        else:
            print("Você está logado como cliente.")
            while True:
                print("\n=== Menu do Cliente ===")
                print("1. Ver perfil")
                print("2. Ver produtos disponíveis")
                print("3. Adicionar produto ao carrinho")
                print("4. Ver carrinho")
                print("5. Finalizar pedido")
                print("6. Sair")
                opcao = input("Escolha uma opção: ")

                if opcao == "1":
                    print(f"\nPerfil do usuário:")
                    print(f"Nome: {usuario_obj.nome}")
                    print(f"Email: {usuario_obj.email}")
                    print(f"Tipo: {usuario_obj.tipo}")

                elif opcao == "2":
                    listar_todos_os_produtos()

                elif opcao == "3":
                    listar_todos_os_produtos()
                    produtos = carregar_produtos()
                    opcao = input("Digite o número do produto que deseja adicionar: ")

                    if not opcao.isdigit() or int(opcao) < 1 or int(opcao) > len(produtos):
                        print("Produto não encontrado.")
                        return

                    produto_escolhido = produtos[int(opcao) - 1]
                    #adicionar_ao_carrinho(email, produto_escolhido.id, produto_escolhido.preco)

                    produto = buscar_produto_por_id(produto_escolhido.id)
                    if produto:
                        try:
                            quantidade = int(input("Digite a quantidade: "))
                            if quantidade <= 0:
                                print("Quantidade inválida.")
                                continue
                            adicionar_ao_carrinho(email, produto_escolhido.id, quantidade)
                            print("Produto adicionado ao carrinho.")
                        except ValueError:
                            print("Quantidade inválida.")
                    else:
                        print("Produto não encontrado.")

                elif opcao == "4":
                    while True:
                        print("\n=== Carrinho de Compras ===")
                        itens = listar_itens_carrinho(email)
                        if not itens:
                            print("Carrinho vazio.")
                            break
                        
                        for i, item in enumerate(itens, 1):
                            print(f"{i}. Produto ID: {item.id} |Nome do produto: {item.nome_produto} | Quantidade: {item.quantidade} | Subtotal: R${item.subtotal:.2f}")

                        print("\n1. Alterar quantidade")
                        print("2. Remover item")
                        print("3. Voltar")
                        sub_opcao = input("Escolha uma opção: ")

                        if sub_opcao == "1":
                            idx = input("Digite o número do item que deseja alterar: ")
                            if idx.isdigit() and 1 <= int(idx) <= len(itens):
                                item = itens[int(idx) - 1]
                                nova_qtd = int(input("Nova quantidade: "))
                                alterar_quantidade_item(email, item.id, nova_qtd)
                                print("Quantidade atualizada.")
                            else:
                                print("Índice inválido.")

                        elif sub_opcao == "2":
                            idx = input("Digite o número do item que deseja remover: ")
                            if idx.isdigit() and 1 <= int(idx) <= len(itens):
                                item = itens[int(idx) - 1]
                                remover_item_carrinho(email, item.id)
                                print("Item removido.")
                            else:
                                print("Índice inválido.")

                        elif sub_opcao == "3":
                            break
                        else:
                            print("Opção inválida.")
                elif opcao == "5":
                    finalizar_pedido(email)
                elif opcao == "6":
                    break
                else:
                    print("Opção inválida.")
    else:
        print(f"\nUsuário não encontrado.")
