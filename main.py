import numbers
import os
import re
from datetime import datetime
import negocio.model.usuario as usuario
from negocio.service.produto_service import (
    adicionar_produto,
    editar_produto,
    inicializar_produtos_json,
    listar_produtos,
    remover_produto
)
from utils.utils import valida_input_eh_num

USUARIOS_JSON = "usuarios.json"

def inicializar_json():
    if not os.path.exists(USUARIOS_JSON):
        with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")

def tela_inicial():
    while True:
        print("Seja bem vindo(a) ao Arteliê (*￣3￣)╭")
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

def verificar_email(email):
    if not usuario.Usuario.autenticar_email(email):
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
                    tela_inicial()
                    return
                else:
                    print("Opção inválida.")
            else:
                print("Por favor, insira apenas números.")

    senha = input("Senha: ")
    if usuario.Usuario.autenticar(email, senha):
        print("Login efetuado com sucesso.\nAcessando perfil de usuário...")
        tela_usuario(email)
    else:
        print("Senha incorreta.")

def cadastro():
    tipo = input("Você quer se cadastrar como um usuário (u) ou artesão(a)? ")
    print("\n=== Tela de Cadastro ===")
    nome = input("Nome: ")
    while True:
        email = input("Email: ")
        if not usuario.Usuario.validar_email(email):
            print("Email inválido. Tente novamente.")
        else:
            break
    while True:
        senha = input("Senha: ")
        if not usuario.Usuario.validar_senha(senha):
            print("A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula e um número.")
            continue
        senha2 = input("Confirme a senha: ")
        if senha != senha2:
            print("As senhas não coincidem. Tente novamente.")
        else:
            break
    while True:
        data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
        if not usuario.Usuario.validar_data(data_nasc):
            print("Data inválida. Use o formato DD/MM/AAAA.")
        else:
            break
    enderecos = []
    if input("Deseja adicionar endereços? (s/n): ").lower() == 's':
        while True:
            end = input("Endereço: ")
            if usuario.Usuario.validar_endereco(end):
                enderecos.append(end)
            else:
                print("Endereço inválido. Deve ter pelo menos 5 caracteres.")
            if input("Adicionar outro endereço? (s/n): ").lower() != 's':
                break
    if usuario.Usuario.autenticar(email, senha):
        print("Já existe um usuário cadastrado com este email.")
        tela_inicial()
    else:
        novoCadastro = usuario.Usuario(nome, email, senha, tipo, data_nasc, enderecos)
        novoCadastro.salvar()
        print("Cadastro realizado com sucesso!")
        tela_inicial()

def tela_usuario(email):
    usuario_obj = usuario.Usuario.buscar_por_email(email)
    if usuario_obj:
        print(f"\nBem-vindo, {usuario_obj.nome}!")

        if usuario_obj.tipo.lower().startswith('a'):
            while True:
                print("\n=== Menu do Artesão ===")
                print("1. Listar produtos")
                print("2. Adicionar produto")
                print("3. Editar produto")
                print("4. Remover produto")
                print("5. Sair")
                opcao = input("Escolha uma opção: ")

                if opcao == "1":
                    listar_produtos(email)
                elif opcao == "2":
                    adicionar_produto(email)
                elif opcao == "3":
                    editar_produto(email)
                elif opcao == "4":
                    remover_produto(email)
                elif opcao == "5":
                    break
                else:
                    print("Opção inválida.")
        else:
            print("Você está logado como usuário comum.")
            while True:
                print("\n=== Menu do Usuário ===")
                print("1. Ver perfil")
                print("2. Sair")
                opcao = input("Escolha uma opção: ")

                if opcao == "1":
                    print(f"\nPerfil do usuário:")
                    print(f"Nome: {usuario_obj.nome}")
                    print(f"Email: {usuario_obj.email}")
                    print(f"Tipo: {usuario_obj.tipo}")
                elif opcao == "2":
                    break
                else:
                    print("Opção inválida.")
    else:
        print(f"\nUsuário não encontrado.")

if __name__ == "__main__":
    inicializar_json()
    inicializar_produtos_json()
    tela_inicial()
