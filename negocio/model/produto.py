class Produto:
    def __init__(self, id, nome, descricao, preco, categoria, estoque, artesao_id, fotos=None, avaliacoes=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
        self.estoque = estoque
        self.artesao_id = artesao_id
        self.fotos = fotos or []
        self.avaliacoes = avaliacoes or []  # <- importante

