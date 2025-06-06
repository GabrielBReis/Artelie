class Carrinho:
    def __init__(self, id, pedido_id, produto_id, quantidade, subtotal):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.subtotal = subtotal
