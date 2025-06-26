from apresentacao.view.tela_cadastro import cadastro
from apresentacao.view.tela_login import login
import negocio.model.usuario as usuario
from negocio.service.produto_service import *

USUARIOS_JSON = "usuarios.json"

def tela_inicial():
    while True:
        print("Seja bem vindo(a) ao Arteliê")
        print("\n==== Tela Inicial ====")
        print("1. Login")
        print("2. Cadastro")
        print("3. Sair")
        opcao = input("Escolha uma opção (apenas números): ")

        if opcao.isdigit() and len(opcao) == 1:
            opcao = int(opcao)
        else:
            print("Por favor, insira apenas um número.")
            continue

        if opcao == 1:
            print("Aguarde um momento...")
            login()
        elif opcao == 2:
            print("Aguarde um momento...")
            cadastro()
        elif opcao == 3:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")