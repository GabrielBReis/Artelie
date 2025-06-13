import numbers
import os
import negocio.model.usuario as usuario
from utils.utils import valida_input_eh_num

USUARIOS_JSON = "usuarios.json"

def inicializar_json():
    if not os.path.exists(USUARIOS_JSON):
        with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")  # lista vazia de usuários

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
    tipo=input("Você quer se cadastrar como um usuário (u) ou artesão(a)?")
    print("\n=== Tela de Cadastro ===")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    senha2 = input("Confirme a senha: ")
    if senha != senha2:
        print("As senhas não coincidem. Tente novamente.")
        cadastro()
    data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
    enderecos = input("Endereços (separados por vírgula): ").split(",") if input("Deseja adicionar endereços? (s/n): ").lower() == 's' else []
    if usuario.Usuario.autenticar(email, senha):
        print("Já existe um usuário cadastrado com este email.")
        tela_inicial()
    else:
        novoCadastro = usuario.Usuario(nome, email, senha, tipo, data_nasc, enderecos)
        novoCadastro.salvar()  # agora salva de fato no JSON
        print("Cadastro realizado com sucesso!")
        tela_inicial()

def tela_usuario(email):
    print(f"\nBem-vindo, {email}!")

if __name__ == "__main__":
    inicializar_json()
    tela_inicial()
