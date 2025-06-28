import unittest
import os
import json
from unittest.mock import patch
from negocio.model.usuario import Usuario
from negocio.service.usuario_service import (
    autenticar,
    carregar_usuarios,
    salvar,
    validar_data,
    validar_email,
    validar_senha
)

class TestUsuario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file = "test_usuarios.json"

    def setUp(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("negocio.service.usuario_service.USUARIOS_JSON", new="test_usuarios.json")
    def test_criacao_usuario(self):
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        self.assertEqual(usuario.nome, "Teste")
        self.assertEqual(usuario.email, "teste@email.com")
        self.assertEqual(usuario.senha, "Senha123")

    @patch("negocio.service.usuario_service.USUARIOS_JSON", new="test_usuarios.json")
    def test_salvar_usuario(self):
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        salvar(usuario)

        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["nome"], "Teste")
            self.assertEqual(data[0]["email"], "teste@email.com")

    @patch("negocio.service.usuario_service.USUARIOS_JSON", new="test_usuarios.json")
    def test_carregar_usuarios(self):
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        salvar(usuario)

        usuarios = carregar_usuarios()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0]["email"], "teste@email.com")

    @patch("negocio.service.usuario_service.USUARIOS_JSON", new="test_usuarios.json")
    def test_autenticar(self):
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        salvar(usuario)

        self.assertTrue(autenticar("teste@email.com", "Senha123"))
        self.assertFalse(autenticar("teste@email.com", "senhaerrada"))
        self.assertFalse(autenticar("emailerrado@teste.com", "Senha123"))

    def test_validar_email(self):
        self.assertTrue(validar_email("teste@email.com"))
        self.assertTrue(validar_email("teste.email@dominio.com.br"))
        self.assertFalse(validar_email("emailinvalido"))
        self.assertFalse(validar_email("email@invalido."))
        self.assertFalse(validar_email("@vazio.com"))
        self.assertFalse(validar_email("email@.com"))

    def test_validar_senha(self):
        self.assertTrue(validar_senha("Senha123"))
        self.assertTrue(validar_senha("A1b2C3d4"))
        self.assertFalse(validar_senha("senhafraca"))
        self.assertFalse(validar_senha("12345678"))
        self.assertFalse(validar_senha("SENHA123"))
        self.assertFalse(validar_senha("abcdefgH"))

    def test_validar_data(self):
        self.assertTrue(validar_data("01/01/2000"))
        self.assertTrue(validar_data("31/12/1999"))
        self.assertFalse(validar_data("32/01/2000"))  # Dia inválido
        self.assertFalse(validar_data("01/13/2000"))  # Mês inválido
        self.assertFalse(validar_data("01-01-2000"))  # Formato inválido
        self.assertFalse(validar_data("2000/01/01"))  # Formato inválido
        self.assertFalse(validar_data("abcd"))

    @patch("negocio.service.usuario_service.USUARIOS_JSON", new="test_usuarios.json")
    def test_salvar_multiplos_usuarios(self):
        usuarios = [
            Usuario("User 1", "u1@email.com", "Senha123"),
            Usuario("User 2", "u2@email.com", "Senha456")
        ]
        for u in usuarios:
            salvar(u)

        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 2)
            emails = [u["email"] for u in data]
            self.assertIn("u1@email.com", emails)
            self.assertIn("u2@email.com", emails)

if __name__ == '__main__':
    unittest.main()
