import numbers
import os
import re
from datetime import datetime
import negocio.model.usuario as usuario
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

        if isinstance(int(opcao) , numbers.Number) and len(opcao) == 1:
            opcao = int(opcao)
        else:
            print("Por favor, insira apenas um número")

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

def validar_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

def validar_senha(senha):
    return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", senha) is not None

def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_endereco(endereco):
    return endereco and len(endereco.strip()) >= 5

def login():
    print("\n=== Tela de Login ===")
    email = input("Email: ")
    senha = input("Senha: ")
    if not validar_email(email):
        print("Email inválido.")
        return
    if usuario.Usuario.autenticar(email, senha):
        print("Login realizado com sucesso!")
        tela_usuario(email)
def verificar_email(email):
    if not usuario.Usuario.autenticar_email(email):
        print("Email não encontrado. Você já possui cadastro?\n1. Sim\n2. Não")
        resposta = input("Insira apenas números: ")

        if valida_input_eh_num(resposta):
            resposta = int(resposta)
            if resposta == 1:
                print("Tente novamente com um email válido.")
                return 0  # Email inválido, mas o usuário já possui cadastro
            elif resposta == 2:
                return 2  # Deseja se cadastrar
            else:
                print("Por favor, insira um número válido.")
        return 0  # Email inválido, tentativa incompleta
    else:
        return 1  # Email válido


def login():
    print("\n==== Tela de Login ====")
    print("Insira as informações solicitadas.")
    
    while True:
        email = input("Email: ")
        print("Verificando email no banco de dados...")
        resultado = verificar_email(email)

        if resultado == 1:  # Email válido
            break
        
        elif resultado == 0:  # Email inválido, mas quer tentar novamente
            continue  # Volta ao início do loop para pedir outro e-mail
        
        elif resultado == 2:  # Deseja se cadastrar
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
    # autenticação da senha aqui
    print("Login efetuado com sucesso.\nAcessando perfil de usuário...")


def cadastro():
    tipo = input("Você quer se cadastrar como um usuário (u) ou artesão(a)? ")
    print("\n=== Tela de Cadastro ===")
    nome = input("Nome: ")
    while True:
        email = input("Email: ")
        if not validar_email(email):
            print("Email inválido. Tente novamente.")
        else:
            break
    while True:
        senha = input("Senha: ")
        if not validar_senha(senha):
            print("A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula e um número.")
            continue
        senha2 = input("Confirme a senha: ")
        if senha != senha2:
            print("As senhas não coincidem. Tente novamente.")
        else:
            break
    while True:
        data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
        if not validar_data(data_nasc):
            print("Data inválida. Use o formato DD/MM/AAAA.")
        else:
            break
    enderecos = []
    if input("Deseja adicionar endereços? (s/n): ").lower() == 's':
        while True:
            end = input("Endereço: ")
            if validar_endereco(end):
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
    else:
        print(f"\nBem-vindo, {email}!")

if __name__ == "__main__":
    inicializar_json()
    tela_inicial()
