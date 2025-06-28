class Usuario:
    def __init__(self, nome, email, senha, tipo=None, data_nasc=None, enderecos=None):
        self.id = None
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
        self.data_nasc = data_nasc
        self.enderecos = enderecos or []


