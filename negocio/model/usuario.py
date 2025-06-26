from datetime import datetime
import json
import os
import re

from utils.utils import valida_input_eh_num

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
    def validar_email(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

    @staticmethod
    def validar_senha(senha):
        return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", senha) is not None

    @staticmethod
    def validar_data(data):
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validar_endereco(endereco):
        return endereco and len(endereco.strip()) >= 5

    @staticmethod
    def verificar_email(email):
        if not Usuario.autenticar_email(email):
            print("Email não encontrado. Você já possui cadastro?\n1. Sim\n2. Não")
            resposta = input("Insira apenas números: ")

            if valida_input_eh_num(resposta):
                resposta = int(resposta)
                if resposta == 1:
                    print("Tente novamente com um email válido.")
                    return 0  # Email inválido, mas o usuário já possui cadastro
                elif resposta == 2:
                    return 2  # Deseja se cadastrar
                else:
                    print("Por favor, insira um número válido.")
            return 0  # Email inválido, tentativa incompleta
        else:
            return 1  # Email válido

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
