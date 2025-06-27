# apresentacao/view/tela_login.py

from negocio.service.usuario_service import (
     autenticar,
     autenticar_email,
     verificar_email
)
from apresentacao.view.tela_usuario import tela_usuario
from apresentacao.view.tela_cadastro import cadastro
from utils.utils import valida_input_eh_num

def verificar_email(email):
    if not autenticar_email(email):
        print("Email não encontrado. Você já possui cadastro?\n1. Sim\n2. Não")
        resposta = input("Insira apenas números: ")

        if valida_input_eh_num(resposta):
            resposta = int(resposta)
            if resposta == 1:
                print("Tente novamente com um email válido.")
                return 0
            elif resposta == 2:
                return 2
            else:
                print("Por favor, insira um número válido.")
        return 0
    else:
        return 1

def login():
    print("\n==== Tela de Login ====")
    print("Insira as informações solicitadas.")

    while True:
        email = input("Email: ")
        print("Verificando email no banco de dados...")
        resultado = verificar_email(email)
        if resultado == 1:
            break
        elif resultado == 0:
            continue
        elif resultado == 2:
            print("Gostaria de realizar o cadastro?\n1. Sim\n2. Não")
            resposta_cadastro = input("Insira apenas números: ")
            if valida_input_eh_num(resposta_cadastro):
                resposta_cadastro = int(resposta_cadastro)
                if resposta_cadastro == 1:
                    cadastro()
                    return
                elif resposta_cadastro == 2:
                    print("Voltando para a tela inicial...")
                    return
                else:
                    print("Opção inválida.")
            else:
                print("Por favor, insira apenas números.")

    senha = input("Senha: ")
    if autenticar(email, senha):
        print("Login efetuado com sucesso.\nAcessando perfil de usuário...")
        tela_usuario(email)
    else:
        print("Senha incorreta.")
