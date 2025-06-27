class Carrinho:
    def __init__(self, id, pedido_id, produto_id, nome_produto, quantidade, subtotal):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.subtotal = subtotal

    def adicionar_produto(self, quantidade, preco_unitario):
        self.quantidade += quantidade
        self.subtotal = self.quantidade * preco_unitario

    def alterar_quantidade(self, nova_quantidade, preco_unitario):
        self.quantidade = nova_quantidade
        self.subtotal = self.quantidade * preco_unitario
