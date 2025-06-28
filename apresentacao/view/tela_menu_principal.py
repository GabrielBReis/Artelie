from apresentacao.view.tela_login import login
from apresentacao.view.tela_cadastro import cadastro

def tela_menu_principal():
    while True:
        print("Seja bem-vindo(a) ao Arteliê (*￣3￣)╭")
        print("\n==== Tela Inicial ====")
        print("1. Login")
        print("2. Cadastro")
        print("3. Sair")

        opcao = input("Escolha uma opção (apenas números): ")

        if opcao == "1":
            print("Aguarde um momento...")
            login()
        elif opcao == "2":
            print("Aguarde um momento...")
            cadastro()
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
    else:
        print("Obrigado por utilizar o Arteliê! Até logo! ")   
