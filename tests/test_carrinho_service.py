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

        carrinho_service.carregar_produtos = lambda: [type("Produto", (), self.produto_fake)]
        carrinho_service.salvar_carrinhos([])

    # Testes Unitários Básicos
    def test_adicionar_novo_produto_ao_carrinho(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 1)
        self.assertEqual(carrinhos[0].quantidade, 2)
        self.assertEqual(carrinhos[0].subtotal, 20.0)

    def test_adicionar_mesmo_produto_ao_carrinho_duplicado(self):
        carrinho = Carrinho(str(uuid.uuid4()), self.email, self.produto_id, 1, 10.0)
        carrinho_service.salvar_carrinhos([carrinho])
        carrinho.adicionar_produto = lambda pid, qtd, preco: setattr(carrinho, 'quantidade', carrinho.quantidade + qtd) or setattr(carrinho, 'subtotal', (carrinho.quantidade) * preco)
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(carrinhos[0].quantidade, 3)

    def test_adicionar_produto_inexistente(self):
        carrinho_service.carregar_produtos = lambda: []
        carrinho_service.adicionar_ao_carrinho(self.email, "fake", 1)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 0)

    # Testes de Remoção
    def test_remover_item_do_carrinho(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 1)
        carrinho_service.remover_item_carrinho(self.email, self.produto_id)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 0)

    def test_remover_produto_inexistente(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 1)
        carrinho_service.remover_item_carrinho(self.email, "produto-falso")
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 1)

    # Testes de Alterar Quantidade
    def test_alterar_quantidade_valida(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 1)
        carrinho = carrinho_service.carregar_carrinhos()[0]
        carrinho.alterar_quantidade = lambda qtd, preco: setattr(carrinho, 'quantidade', qtd) or setattr(carrinho, 'subtotal', qtd * preco)
        carrinho_service.alterar_quantidade_item(self.email, self.produto_id, 4)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(carrinhos[0].quantidade, 4)

    def test_alterar_quantidade_para_zero(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        carrinho_service.alterar_quantidade_item(self.email, self.produto_id, 0)
        carrinhos = carrinho_service.carregar_carrinhos()

        # A quantidade deve continuar inalterada (2), pois 0 é inválido
        self.assertEqual(carrinhos[0].quantidade, 2)

    def test_alterar_quantidade_produto_inexistente(self):
        carrinho_service.alterar_quantidade_item(self.email, "fake-id", 5)
        # não deve lançar erro

    # Testes de Listagem
    def test_listar_carrinho_usuario(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        itens = carrinho_service.listar_itens_carrinho(self.email)
        self.assertEqual(len(itens), 1)

    def test_listar_carrinho_vazio(self):
        itens = carrinho_service.listar_itens_carrinho("sem-nada@exemplo.com")
        self.assertEqual(len(itens), 0)

    # Testes de Limite
    def test_adicionar_quantidade_zero(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 0)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 0)

    def test_adicionar_quantidade_negativa(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, -1)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 0)

    # Persistência
    def test_salvar_e_recuperar_consistencia(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        antes = carrinho_service.carregar_carrinhos()
        carrinho_service.salvar_carrinhos(antes)
        depois = carrinho_service.carregar_carrinhos()
        self.assertEqual(antes[0].quantidade, depois[0].quantidade)

    # Serialização e robustez
    def test_serializacao_json_contem_dados(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 1)
        with open("carrinhos.json", "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn(self.email, data)
        self.assertIn(self.produto_id, data)

    def test_injecao_codigo_no_produto_id(self):
        malicioso = '"); os.remove("carrinhos.json"); #'
        carrinho_service.adicionar_ao_carrinho(self.email, malicioso, 1)
        self.assertTrue(os.path.exists("carrinhos.json"))

    def test_fluxo_completo_crud(self):
        carrinho_service.adicionar_ao_carrinho(self.email, self.produto_id, 2)
        carrinho_service.alterar_quantidade_item(self.email, self.produto_id, 3)
        carrinho_service.remover_item_carrinho(self.email, self.produto_id)
        carrinhos = carrinho_service.carregar_carrinhos()
        self.assertEqual(len(carrinhos), 0)

    def tearDown(self):
        if os.path.exists("carrinhos.json"):
            os.remove("carrinhos.json")

if __name__ == '__main__':
    unittest.main()