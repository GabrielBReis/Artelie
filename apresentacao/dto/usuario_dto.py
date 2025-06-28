class UsuarioCadastroDTO:
    def __init__(self, nome, email, senha, perfil="CLIENTE"):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.perfil = perfil
