# controllers/usuario_controller.py

from negocio.model.usuario import Usuario
from negocio.service import usuario_service
from negocio.exceptions.usuarios_exception import EmailJaCadastradoException

def cadastrar_usuario(nome, email, senha, tipo, data_nasc, enderecos):
    if usuario_service.autenticar_email(email):
        raise EmailJaCadastradoException("Email já está cadastrado.")
    
    novo_usuario = Usuario(nome, email, senha, tipo, data_nasc, enderecos)
    usuario_service.salvar(novo_usuario)
    return True

def autenticar_usuario(email, senha):
    return usuario_service.autenticar(email, senha)

def verificar_email_existente(email):
    return usuario_service.autenticar_email(email)

def obter_usuario_por_email(email):
    return usuario_service.buscar_por_email(email)

def validar_entrada_email(email):
    return usuario_service.validar_email(email)

def validar_entrada_senha(senha):
    return usuario_service.validar_senha(senha)

def validar_entrada_data(data):
    return usuario_service.validar_data(data)

def validar_entrada_endereco(endereco):
    return usuario_service.validar_endereco(endereco)
