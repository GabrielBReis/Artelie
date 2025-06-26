import unittest
import os
import uuid
from negocio.model.carrinho import Carrinho
from negocio.service import carrinho_service

class TestCarrinhoService(unittest.TestCase):
    def setUp(self):
        self.email = "cliente@teste.com"
        self.produto_id = "prod-001"
        self.produto_fake = {
            "id": self.produto_id,
            "nome": "Produto Teste",
            "descricao": "Exemplo",
            "preco": 10.0,
            "categoria": "Teste",
            "estoque": 100,
            "artesao_id": "artesao@teste.com"
        }

        # Mockando função de carregar_produtos
        carrinho_service.carregar_produtos = lambda: [type("Produto", (), self.produto_fake)]

        # Limpa carrinhos antes de cada teste
        carrinho_service.salvar_carrinhos([])

    def test_adicionar_novo_produto_ao_carrinho(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 1)
        self.assertEqual(carrinhos[0].quantidade, 2)
        self.assertEqual(carrinhos[0].subtotal, 20.0)

    def test_adicionar_mesmo_produto_ao_carrinho_duplicado(self):
        # Primeiro carrinho simulado (manual)
        carrinho = Carrinho(
            id=str(uuid.uuid4()),
            pedido_id=self.email,
            produto_id=self.produto_id,
            quantidade=1,
            subtotal=10.0
        )
        carrinho_service.salvar_carrinhos([carrinho])

        # Mock da função que não depende de adicionar_produto()
        def fake_adicionar(produto_id, quantidade, preco):
            carrinho.quantidade += quantidade
            carrinho.subtotal = carrinho.quantidade * preco

        carrinho.adicionar_produto = fake_adicionar

        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(carrinhos[0].quantidade, 3)
        self.assertEqual(carrinhos[0].subtotal, 30.0)

    def test_adicionar_produto_inexistente(self):
        carrinho_service.carregar_produtos = lambda: []
        carrinho_service.adicionar_ao_carrinho(self.email, "fake", 1)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 0)

    def test_remover_item_do_carrinho(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 1)
        carrinho_service.remover_item_carrinho(self.email, self.produto_id)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 0)

    def test_remover_produto_inexistente(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 1)
        carrinho_service.remover_item_carrinho(self.email, "produto-falso")
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 1)  # ainda existe

    def test_alterar_quantidade_valida(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 1)

        def fake_alterar(nova_qtd, preco):
            carrinho = carrinho_service.carregar_carrinhos()[0]
            carrinho.quantidade = nova_qtd
            carrinho.subtotal = nova_qtd * preco

        carrinho = carrinho_service.carregar_carrinhos()[0]
        carrinho.alterar_quantidade = fake_alterar

        carrinho_service.alterar_quantidade_item(self.email, self.produto_id, 4)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(carrinhos[0].quantidade, 4)
        self.assertEqual(carrinhos[0].subtotal, 40.0)

    def test_alterar_quantidade_produto_inexistente(self):
        carrinho_service.alterar_quantidade_item(self.email, "fake-id", 5)
        # nada deve acontecer, sem crash

    def test_listar_carrinho_usuario(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        itens = carrinho_service.listar_itens_carrinho(self.email)
        self.assertEqual(len(itens), 1)

    def test_listar_carrinho_vazio(self):
        itens = carrinho_service.listar_itens_carrinho("sem-nada@exemplo.com")
        self.assertEqual(len(itens), 0)

    def tearDown(self):
        if os.path.exists("carrinhos.json"):
            os.remove("carrinhos.json")

if __name__ == '__main__':
    unittest.main()
