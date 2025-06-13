import json
import os

USUARIOS_JSON = "usuarios.json"

class Usuario:
    def __init__(self, nome, email, senha, foto_perfil=None, biografia=None, data_nasc=None, enderecos=None):
        self.id = None  # Será atribuído ao salvar
        self.nome = nome
        self.email = email
        self.senha = senha
        self.foto_perfil = foto_perfil
        self.biografia = biografia
        self.data_nasc = data_nasc
        self.enderecos = enderecos or []
        self.produtos = []
        self.pedidos = []
        self.avaliacoes = []

    def salvar(self):
        usuarios = Usuario.carregar_usuarios()

        # Gera um ID único
        ids_existentes = [u.get("id", 0) for u in usuarios]
        novo_id = max(ids_existentes, default=0) + 1
        self.id = novo_id

        novo_usuario = {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "foto_perfil": self.foto_perfil,
            "biografia": self.biografia,
            "data_nasc": self.data_nasc,
            "enderecos": self.enderecos
        }

        usuarios.append(novo_usuario)

        with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

    @staticmethod
    def carregar_usuarios():
        if not os.path.exists(USUARIOS_JSON):
            return []
        with open(USUARIOS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def autenticar(email, senha):
        usuarios = Usuario.carregar_usuarios()
        for u in usuarios:
            if u["email"] == email and u["senha"] == senha:
                return True
        return False
