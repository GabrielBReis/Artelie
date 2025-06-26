import unittest
import os
import uuid
from negocio.model.produto import Produto
from negocio.service import produto_service

class TestProdutoService(unittest.TestCase):
    def setUp(self):
        self.email = "artesao@teste.com"
        self.produto = Produto(
            id=str(uuid.uuid4()),
            nome="Produto Teste",
            descricao="Desc teste",
            preco=99.90,
            categoria="Categoria Teste",
            estoque=10,
            artesao_id=self.email,
            fotos=[]
        )
        produto_service.salvar_produtos([self.produto])

    def tearDown(self):
        if os.path.exists("produtos.json"):
            os.remove("produtos.json")

    def test_carregar_produtos(self):
        produtos = produto_service.carregar_produtos()
        self.assertEqual(len(produtos), 1)
        self.assertEqual(produtos[0].nome, self.produto.nome)

    def test_salvar_produtos(self):
        novo = Produto(
            id=str(uuid.uuid4()),
            nome="Novo Produto",
            descricao="Nova descrição",
            preco=20.0,
            categoria="Nova Cat",
            estoque=5,
            artesao_id=self.email
        )
        produto_service.salvar_produtos([novo])
        produtos = produto_service.carregar_produtos()
        self.assertEqual(len(produtos), 1)
        self.assertEqual(produtos[0].nome, "Novo Produto")

    def test_buscar_produto_por_id_existente(self):
        p = produto_service.buscar_produto_por_id(self.produto.id)
        self.assertIsNotNone(p)
        self.assertEqual(p.id, self.produto.id)

    def test_buscar_produto_por_id_inexistente(self):
        p = produto_service.buscar_produto_por_id("id-nao-existe")
        self.assertIsNone(p)

    def test_listar_produtos_por_artesao(self):
        produtos = produto_service.carregar_produtos()
        filtrados = [p for p in produtos if p.artesao_id == self.email]
        self.assertGreaterEqual(len(filtrados), 1)

    def test_remover_produto_valido(self):
        produto_service.salvar_produtos([self.produto])
        produtos = produto_service.carregar_produtos()
        self.assertEqual(len(produtos), 1)

        # Simula remoção manual (sem input)
        produtos = [p for p in produtos if p.id != self.produto.id]
        produto_service.salvar_produtos(produtos)

        produtos = produto_service.carregar_produtos()
        self.assertEqual(len(produtos), 0)

    def test_editar_produto_valores_diferentes(self):
        produto = self.produto
        produto.nome = "Nome Editado"
        produto.descricao = "Nova descrição"
        produto.preco = 55.5
        produto.estoque = 50
        produto.categoria = "Nova categoria"

        produto_service.salvar_produtos([produto])
        p = produto_service.carregar_produtos()[0]

        self.assertEqual(p.nome, "Nome Editado")
        self.assertEqual(p.preco, 55.5)
        self.assertEqual(p.estoque, 50)

if __name__ == '__main__':
    unittest.main()
