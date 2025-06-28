# apresentacao/view/tela_cadastro.py

import negocio.model.usuario as usuario
from negocio.service.usuario_service import autenticar, salvar, validar_data, validar_email, validar_endereco, validar_senha

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
    if autenticar(email, senha):
        print("Já existe um usuário cadastrado com este email.")
    else:
        novoCadastro = usuario.Usuario(nome, email, senha, tipo, data_nasc, enderecos)
        salvar(novoCadastro)
        print("Cadastro realizado com sucesso!")
