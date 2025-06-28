from datetime import datetime

class Pedido:
    def __init__(self, id, usuario_id, data, total, itens=None):
        self.id = id
        self.usuario_id = usuario_id
        self.data = data or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.total = total
        self.itens = itens if itens is not None else []

    def adicionar_item(self, item):
        self.itens.append(item)
        self.total += item.subtotal