from negocio.model.usuario import Usuario
from infra.repository.usuario_repository import UsuarioRepository
from negocio.exceptions.usuario_exceptions import EmailJaCadastradoException

class UsuarioService:
    def __init__(self, usuario_repository):
        self.repository = usuario_repository

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
