class EmailJaCadastradoException(Exception):
    def __init__(self):
        super().__init__("E-mail já cadastrado.")
