import json
import os

USUARIOS_JSON = "usuarios.json"

class Usuario:
    def __init__(self, nome, email, senha, tipo=None, data_nasc=None, enderecos=None):
        self.id = None  
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
        self.data_nasc = data_nasc
        self.enderecos = enderecos or []

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
            "tipo": self.tipo,
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
    
    @staticmethod
    def autenticar_email(email):
        usuarios = Usuario.carregar_usuarios()
        for u in usuarios:
            if u["email"] == email:
                return True
        return False

    @staticmethod
    def buscar_por_email(email):
        usuarios = Usuario.carregar_usuarios()
        for u in usuarios:
            if u["email"] == email:
                return Usuario(
                    nome=u["nome"],
                    email=u["email"],
                    senha=u["senha"],
                    tipo=u.get("tipo"),
                    data_nasc=u.get("data_nasc"),
                    enderecos=u.get("enderecos", [])
                )
        return None
