class Pedido:
    def __init__(self, id, usuario_id, data, total):
        self.id = id
        self.usuario_id = usuario_id
        self.data = data
        self.total = total
        self.itens = []  # Lista de Carrinho
