import unittest
import os
import uuid
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

from negocio.model.pedido import Pedido
from negocio.model.carrinho import Carrinho
from negocio.service import pedido_service


class TestPedidoService(unittest.TestCase):

    def setUp(self):
        self.email = "cliente@teste.com"
        self.pedido_json_path = pedido_service.PEDIDOS_JSON

        if os.path.exists(self.pedido_json_path):
            os.remove(self.pedido_json_path)

        pedido_service.inicializar_pedidos_json()

        self.fake_item = Carrinho(
            id=str(uuid.uuid4()),
            pedido_id=self.email,
            produto_id="prod-123",
            quantidade=2,
            subtotal=30.0
        )

    def test_inicializar_pedidos_json_cria_arquivo(self):
        self.assertTrue(os.path.exists(self.pedido_json_path))

    def test_salvar_e_carregar_pedido(self):
        pedido = Pedido(
            id=str(uuid.uuid4()),
            usuario_id=self.email,
            data="2025-06-26 12:00:00",
            total=100.0,
            itens=[self.fake_item.__dict__]
        )

        pedido_service.salvar_pedido(pedido)
        pedidos = pedido_service.carregar_pedidos()
        self.assertEqual(len(pedidos), 1)
        self.assertEqual(pedidos[0].usuario_id, self.email)
        self.assertEqual(pedidos[0].total, 100.0)

    @patch("negocio.service.pedido_service.listar_itens_carrinho")
    @patch("negocio.service.pedido_service.carregar_carrinhos")
    @patch("negocio.service.pedido_service.salvar_carrinhos")
    def test_finalizar_compra_com_itens(
        self,
        mock_salvar_carrinhos,
        mock_carregar_carrinhos,
        mock_listar_itens
    ):
        mock_listar_itens.return_value = [self.fake_item]
        mock_carregar_carrinhos.return_value = [self.fake_item]

        pedido_service.finalizar_compra(self.email)

        pedidos = pedido_service.carregar_pedidos()
        self.assertEqual(len(pedidos), 1)
        self.assertEqual(pedidos[0].usuario_id, self.email)
        self.assertAlmostEqual(pedidos[0].total, 30.0)

        mock_salvar_carrinhos.assert_called_once()

    @patch("negocio.service.pedido_service.listar_itens_carrinho")
    def test_finalizar_compra_carrinho_vazio(self, mock_listar_itens):
        mock_listar_itens.return_value = []
        pedido_service.finalizar_compra(self.email)
        pedidos = pedido_service.carregar_pedidos()
        self.assertEqual(len(pedidos), 0)

    def tearDown(self):
        if os.path.exists(self.pedido_json_path):
            os.remove(self.pedido_json_path)


if __name__ == "__main__":
    unittest.main()
