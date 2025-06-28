# controllers/produto_controller.py

from negocio.service import produto_service
from negocio.model.produto import Produto
import uuid

class ProdutoController:
    def __init__(self):
        produto_service.inicializar_produtos_json()

    def listar_produtos_por_artesao(self, artesao_email):
        return produto_service.listar_produtos(artesao_email)

    def listar_todos_produtos(self):
        return produto_service.listar_todos_os_produtos()

    def adicionar_produto(self, artesao_email, nome, descricao, preco, estoque, categoria):
        novo_produto = Produto(
            id=str(uuid.uuid4()),
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            estoque=estoque,
            artesao_id=artesao_email,
            fotos=[]
        )
        produtos = produto_service.carregar_produtos()
        produtos.append(novo_produto)
        produto_service.salvar_produtos(produtos)
        return True

    def remover_produto(self, artesao_email, idx):
        produtos = produto_service.carregar_produtos()
        meus_produtos = [p for p in produtos if p.artesao_id == artesao_email]

        if not meus_produtos or idx < 0 or idx >= len(meus_produtos):
            return False

        produto_removido = meus_produtos[idx]
        produtos = [p for p in produtos if p.id != produto_removido.id]
        produto_service.salvar_produtos(produtos)
        return True

    def editar_produto(self, artesao_email, idx, novos_dados):
        produtos = produto_service.carregar_produtos()
        meus_produtos = [p for p in produtos if p.artesao_id == artesao_email]

        if not meus_produtos or idx < 0 or idx >= len(meus_produtos):
            return False

        produto = meus_produtos[idx]

        produto.nome = novos_dados.get("nome", produto.nome)
        produto.descricao = novos_dados.get("descricao", produto.descricao)
        produto.preco = novos_dados.get("preco", produto.preco)
        produto.estoque = novos_dados.get("estoque", produto.estoque)
        produto.categoria = novos_dados.get("categoria", produto.categoria)

        produto_service.salvar_produtos(produtos)
        return True

    def buscar_produto_por_id(self, produto_id):
        return produto_service.buscar_produto_por_id(produto_id)
