import os
import negocio.model.usuario as usuario

USUARIOS_JSON = "usuarios.json"

def inicializar_json():
    if not os.path.exists(USUARIOS_JSON):
        with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")  # lista vazia de usuários

def tela_inicial():
    while True:
        print("\n=== Tela Inicial ===")
        print("1. Login")
        print("2. Cadastro")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            login()
        elif opcao == "2":
            cadastro()
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def login():
    print("\n=== Tela de Login ===")
    email = input("Email: ")
    senha = input("Senha: ")
    if usuario.Usuario.autenticar(email, senha):
        print("Login realizado com sucesso!")
        tela_usuario(email)
    else:
        print("Usuário ou senha incorretos.")

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
