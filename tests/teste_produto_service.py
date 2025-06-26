# tests/test_produto_service.py
import unittest
import os
from negocio.service import produto_service
from negocio.model.produto import Produto

class TestProdutoService(unittest.TestCase):
    def setUp(self):
        # preparar ambiente de teste
        self.produtos = [
            Produto("1", "Teste", "desc", 1.0, "Cat", 5, "email@example.com"),
            Produto("2", "Outro", "desc", 2.0, "Cat", 3, "email@example.com")
        ]
        produto_service.salvar_produtos(self.produtos)

    def test_carregar_produtos(self):
        produtos = produto_service.carregar_produtos()
        self.assertEqual(len(produtos), 2)
        self.assertEqual(produtos[0].nome, "Teste")

    def tearDown(self):
        # limpar o arquivo
        if os.path.exists("produtos.json"):
            os.remove("produtos.json")
