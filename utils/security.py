import bcrypt

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verificar_senha(senha_informada, senha_hash_armazenada):
    return bcrypt.checkpw(senha_informada.encode("utf-8"), senha_hash_armazenada.encode("utf-8"))
