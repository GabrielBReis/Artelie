from datetime import datetime
import re
from negocio.exceptions.usuarios_exception import EmailJaCadastradoException
from negocio.model.usuario import Usuario
from utils.utils import valida_input_eh_num
from datetime import datetime
import json
import os

USUARIOS_JSON = os.environ.get("USUARIOS_JSON", "usuarios.json")


def inicializar_json():
    if not os.path.exists(USUARIOS_JSON):
        with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")
            
def cadastrar_usuario(self, dto):
    if self.repository.buscar_por_email(dto.email):
        raise EmailJaCadastradoException()
    
    usuario = Usuario(
        id=None,
        nome=dto.nome,
        email=dto.email,
        senha=dto.senha,  
        perfil=dto.perfil
    )
    return self.repository.salvar(usuario)

def salvar(self):
    usuarios = carregar_usuarios()
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

def carregar_usuarios():
    if not os.path.exists(USUARIOS_JSON):
        return []
    with open(USUARIOS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def autenticar(email, senha):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["email"] == email and u["senha"] == senha:
            return True
    return False

def autenticar_email(email):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["email"] == email:
            return True
    return False

def validar_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

def validar_senha(senha):
    return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", senha) is not None

def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False
    
def validar_endereco(endereco):
    return endereco and len(endereco.strip()) >= 5

def verificar_email(email):
    if not autenticar_email(email):
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
    

def buscar_por_email(email):
    usuarios = carregar_usuarios()
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
