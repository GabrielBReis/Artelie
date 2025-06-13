import negocio.model.usuario as usuario

def tela_inicial():
    print("=== Tela Inicial ===")
    print("1. Login")
    print("2. Cadastro")
    print("3. Sair")
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
        login()
    elif opcao == "2":
        print("Saindo...")
    else:
        print("Opção inválida. Tente novamente.")
        tela_inicial()

def login():
    print("=== Tela de Login ===")
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    if usuario == "admin" and senha == "1234":
        print("Login realizado com sucesso!")
    else:
        print("Usuário ou senha incorretos.")

def cadastro(): 
    print("=== Tela de Cadastro ===")
    novoCadastro = usuario()
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha:")
    senha2 = input("Confirme a senha: ")
    if senha != senha2:
        print("As senhas não coincidem. Tente novamente.")
        cadastro()
    else:
        novoCadastro.__init__(nome=nome, email=email, senha=senha)
        print("Cadastro realizado com sucesso!")
        tela_inicial()

def tela_usuario():
    



if __name__ == "__main__":
    login()