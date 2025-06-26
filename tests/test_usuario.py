import unittest
import os
import json
from datetime import datetime
from negocio.model.usuario import Usuario

class TestUsuario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configuração inicial para todos os testes
        cls.test_file = "test_usuarios.json"
        Usuario.USUARIOS_JSON = cls.test_file

    def setUp(self):
        # Executado antes de cada teste
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_criacao_usuario(self):
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        self.assertEqual(usuario.nome, "Teste")
        self.assertEqual(usuario.email, "teste@email.com")
        self.assertEqual(usuario.senha, "Senha123")

    def test_salvar_usuario(self):
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        usuario.salvar()
        
        with open(self.test_file, "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["nome"], "Teste")
            self.assertEqual(data[0]["email"], "teste@email.com")

    def test_carregar_usuarios(self):
        # Primeiro cria e salva um usuário
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        usuario.salvar()
        
        # Testa o carregamento
        usuarios = Usuario.carregar_usuarios()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0]["nome"], "Teste")

    def test_autenticar(self):
        usuario = Usuario("Teste", "teste@email.com", "Senha123")
        usuario.salvar()
        
        self.assertTrue(Usuario.autenticar("teste@email.com", "Senha123"))
        self.assertFalse(Usuario.autenticar("teste@email.com", "senhaerrada"))
        self.assertFalse(Usuario.autenticar("emailerrado@teste.com", "Senha123"))

    def test_validar_email(self):
        self.assertTrue(Usuario.validar_email("teste@email.com"))
        self.assertTrue(Usuario.validar_email("teste.email@dominio.com.br"))
        self.assertFalse(Usuario.validar_email("emailinvalido"))
        self.assertFalse(Usuario.validar_email("email@invalido."))

    def test_validar_senha(self):
        self.assertTrue(Usuario.validar_senha("Senha123"))
        self.assertTrue(Usuario.validar_senha("A1b2C3d4"))
        self.assertFalse(Usuario.validar_senha("senhafraca"))
        self.assertFalse(Usuario.validar_senha("12345678"))
        self.assertFalse(Usuario.validar_senha("SENHA123"))

    def test_validar_data(self):
        self.assertTrue(Usuario.validar_data("01/01/2000"))
        self.assertTrue(Usuario.validar_data("31/12/1999"))
        self.assertFalse(Usuario.validar_data("32/01/2000"))  # Dia inválido
        self.assertFalse(Usuario.validar_data("01/13/2000"))  # Mês inválido
        self.assertFalse(Usuario.validar_data("01-01-2000"))  # Formato inválido

    def tearDown(self):
        # Limpeza após cada teste
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()