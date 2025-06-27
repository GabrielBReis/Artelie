from datetime import datetime

class Pedido:
    def __init__(self, id, usuario_id, data=None, total=0.0):
        self.id = id
        self.usuario_id = usuario_id
        self.data = data or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.total = total
        self.itens = []  # Lista de objetos Carrinho

    def adicionar_item(self, item):
        self.itens.append(item)
        self.total += item.subtotal
