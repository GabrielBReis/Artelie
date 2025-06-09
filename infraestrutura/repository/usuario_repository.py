from negocio.model.usuario import Usuario

class UsuarioRepository:
    def __init__(self):
        self._usuarios = []
        self._next_id = 1

    def salvar(self, usuario):
        usuario.id = self._next_id
        self._next_id += 1
        self._usuarios.append(usuario)
        return usuario

    def buscar_por_email(self, email):
        return next((u for u in self._usuarios if u.email == email), None)
