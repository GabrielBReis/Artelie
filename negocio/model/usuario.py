class Usuario:
    def __init__(self, id, nome, email, senha, foto_perfil=None, biografia=None, data_nasc=None, enderecos=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.foto_perfil = foto_perfil
        self.biografia = biografia
        self.data_nasc = data_nasc
        self.enderecos = enderecos or []
        self.produtos = []  # Lista de Produto
        self.pedidos = []   # Lista de Pedido
        self.avaliacoes = []  # Lista de Avaliacao
