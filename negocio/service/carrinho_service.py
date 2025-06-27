import json
import os
import uuid
from negocio.model.carrinho import Carrinho
from negocio.service.produto_service import carregar_produtos


CARRINHOS_JSON = "carrinhos.json"

def inicializar_carrinhos_json():
    if not os.path.exists(CARRINHOS_JSON):
        with open(CARRINHOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")

def carregar_carrinhos():
    with open(CARRINHOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Carrinho(**c) for c in data]

def salvar_carrinhos(carrinhos):
    with open(CARRINHOS_JSON, "w", encoding="utf-8") as f:
        json.dump([c.__dict__ for c in carrinhos], f, indent=2, ensure_ascii=False)

def listar_carrinho_do_usuario(email):
    carrinhos = carregar_carrinhos()
    return [c for c in carrinhos if c.pedido_id == email]  # usamos email como identificador do carrinho temporário

from negocio.service.produto_service import carregar_produtos, salvar_produtos

def adicionar_ao_carrinho(email, produto_id, quantidade):
    produtos = carregar_produtos()
    produto = next((p for p in produtos if p.id == produto_id), None)
    if not produto:
        print("Produto não encontrado.")
        return

    if quantidade > produto.estoque:
        print(f"Estoque insuficiente. Disponível: {produto.estoque}")
        return

    carrinhos = carregar_carrinhos()

    for _ in range(quantidade):
        novo_item = Carrinho(
            id=str(uuid.uuid4()),
            pedido_id=email,
            produto_id=produto.id,
            nome_produto=produto.nome,
            quantidade=1,
            subtotal=produto.preco
        )
        carrinhos.append(novo_item)

    # Atualizar estoque
    produto.estoque -= quantidade
    salvar_carrinhos(carrinhos)
    salvar_produtos(produtos)

    print("Produto(s) adicionado(s) ao carrinho.")


def remover_item_carrinho(email, produto_id):
    carrinhos = carregar_carrinhos()
    carrinhos = [c for c in carrinhos if not (c.pedido_id == email and c.produto_id == produto_id)]
    salvar_carrinhos(carrinhos)
    print("Item removido do carrinho.")

def alterar_quantidade_item(email, produto_id, nova_quantidade):
    carrinhos = carregar_carrinhos()
    produtos = carregar_produtos()
    produto = next((p for p in produtos if p.id == produto_id), None)
    if not produto:
        print("Produto não encontrado.")
        return

    for c in carrinhos:
        if c.pedido_id == email and c.produto_id == produto_id:
            c.alterar_quantidade(nova_quantidade, produto.preco)
            break

    salvar_carrinhos(carrinhos)
    print("Quantidade atualizada.")

def listar_itens_carrinho(pedido_id):
    carrinho = carregar_carrinhos()
    return [item for item in carrinho if item.pedido_id == pedido_id]

def limpar_carrinho(email):
    carrinhos = carregar_carrinhos()
    carrinhos = [c for c in carrinhos if c.pedido_id != email]
    salvar_carrinhos(carrinhos)


