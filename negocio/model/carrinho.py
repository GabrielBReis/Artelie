class Carrinho:
    def __init__(self, id, pedido_id, produto_id, quantidade, subtotal):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.subtotal = subtotal

        def adicionar_produto(self, produto_id, quantidade, preco_unitario):
            if self.produto_id == produto_id:
                self.quantidade += quantidade
                self.subtotal += preco_unitario * quantidade
            else:
                print("Produto diferente. Não é possível adicionar neste carrinho.")

        def remover_produto(self):
            self.quantidade = 0
            self.subtotal = 0

        def alterar_quantidade(self, nova_quantidade, preco_unitario):
            if nova_quantidade < 1:
                print("Quantidade inválida.")
                return
            self.quantidade = nova_quantidade
            self.subtotal = preco_unitario * nova_quantidade

        def exibir_item(self):
            return {
                "id": self.id,
                "pedido_id": self.pedido_id,
                "produto_id": self.produto_id,
                "quantidade": self.quantidade,
                "subtotal": self.subtotal
            }