import json
import os
import uuid
from negocio.model.produto import Produto

PRODUTOS_JSON = "produtos.json"

def inicializar_produtos_json():
    if not os.path.exists(PRODUTOS_JSON):
        with open(PRODUTOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")

def carregar_produtos():
    with open(PRODUTOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Produto(**p) for p in data]

def salvar_produtos(produtos):
    with open(PRODUTOS_JSON, "w", encoding="utf-8") as f:
        json.dump([p.__dict__ for p in produtos], f, indent=2, ensure_ascii=False)

def listar_produtos(artesao_email):
    produtos = carregar_produtos()
    encontrados = [p for p in produtos if p.artesao_id == artesao_email]
    if not encontrados:
        print("Nenhum produto cadastrado.")
    else:
        for i, p in enumerate(encontrados, 1):
            print(f"{i}. {p.nome} - {p.descricao} - R${p.preco:.2f} | Estoque: {p.estoque} | Categoria: {p.categoria}")
            
def listar_todos_os_produtos():
    produtos = carregar_produtos()
    if not produtos:
        print("Nenhum produto disponível.")
    else:
        print("\n=== Produtos Disponíveis ===")
        for i, p in enumerate(produtos, 1):
            print(f"{i}. {p.nome} - {p.descricao} - R${p.preco:.2f} | Estoque: {p.estoque} | Categoria: {p.categoria} | Artesão: {p.artesao_id}")

def adicionar_produto(artesao_email):
    nome = input("Nome do produto: ")
    descricao = input("Descrição: ")
    try:
        preco = float(input("Preço: "))
        estoque = int(input("Estoque: "))
    except ValueError:
        print("Preço ou estoque inválidos.")
        return
    categoria = input("Categoria: ")
    
    novo = Produto(
        id=str(uuid.uuid4()),
        nome=nome,
        descricao=descricao,
        preco=preco,
        categoria=categoria,
        estoque=estoque,
        artesao_id=artesao_email,
        fotos=[]
    )

    produtos = carregar_produtos()
    produtos.append(novo)
    salvar_produtos(produtos)
    print("Produto adicionado com sucesso!")

def remover_produto(artesao_email):
    produtos = carregar_produtos()
    meus_produtos = [p for p in produtos if p.artesao_id == artesao_email]
    listar_produtos(artesao_email)
    if not meus_produtos:
        return
    idx = input("Digite o número do produto a remover: ")
    if idx.isdigit():
        idx = int(idx) - 1
        if 0 <= idx < len(meus_produtos):
            produto_removido = meus_produtos[idx]
            produtos = [p for p in produtos if p.id != produto_removido.id]
            salvar_produtos(produtos)
            print(f"Produto '{produto_removido.nome}' removido.")
        else:
            print("Índice inválido.")
    else:
        print("Entrada inválida.")

def buscar_produto_por_id(produto_id):
    produtos = carregar_produtos()
    for p in produtos:
        if p.id == produto_id:
            return p
    return None

def editar_produto(artesao_email):
    produtos = carregar_produtos()
    meus_produtos = [p for p in produtos if p.artesao_id == artesao_email]
    listar_produtos(artesao_email)
    if not meus_produtos:
        return
    idx = input("Digite o número do produto a editar: ")
    if idx.isdigit():
        idx = int(idx) - 1
        if 0 <= idx < len(meus_produtos):
            p = meus_produtos[idx]
            print("Deixe em branco se não quiser alterar.")
            novo_nome = input(f"Novo nome ({p.nome}): ") or p.nome
            nova_desc = input(f"Nova descrição ({p.descricao}): ") or p.descricao
            try:
                novo_preco = float(input(f"Novo preço ({p.preco}): ") or p.preco)
                novo_estoque = int(input(f"Novo estoque ({p.estoque}): ") or p.estoque)
            except ValueError:
                print("Preço ou estoque inválidos.")
                return
            nova_categoria = input(f"Nova categoria ({p.categoria}): ") or p.categoria

            p.nome = novo_nome
            p.descricao = nova_desc
            p.preco = novo_preco
            p.estoque = novo_estoque
            p.categoria = nova_categoria

            salvar_produtos(produtos)
            print("Produto atualizado com sucesso.")
        else:
            print("Índice inválido.")
    else:
        print("Entrada inválida.")