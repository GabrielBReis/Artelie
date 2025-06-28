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
        json.dump([{
            "id": c.id,
            "pedido_id": c.pedido_id,
            "produto_id": c.produto_id,
            "quantidade": c.quantidade,
            "subtotal": c.subtotal
        } for c in carrinhos], f, indent=2, ensure_ascii=False)


def listar_carrinho_do_usuario(email):
    carrinhos = carregar_carrinhos()
    return [c for c in carrinhos if c.pedido_id == email]  # usamos email como identificador do carrinho temporário

def adicionar_ao_carrinho(email, produto_id, quantidade):
    if quantidade <= 0:
        print("Quantidade inválida. Deve ser maior que zero.")
        return

    produtos = carregar_produtos()
    produto = next((p for p in produtos if p.id == produto_id), None)
    if not produto:
        print("Produto não encontrado.")
        return

    carrinhos = carregar_carrinhos()
    carrinho_usuario = [c for c in carrinhos if c.pedido_id == email and c.produto_id == produto_id]

    if carrinho_usuario:
        carrinho = carrinho_usuario[0]
        carrinho.adicionar_produto(produto_id, quantidade, produto.preco)
    else:
        novo = Carrinho(
            id=str(uuid.uuid4()),
            pedido_id=email,
            produto_id=produto_id,
            quantidade=quantidade,
            subtotal=produto.preco * quantidade
        )
        carrinhos.append(novo)

    salvar_carrinhos(carrinhos)
    print("Produto adicionado ao carrinho.")


def remover_item_carrinho(email, produto_id):
    carrinhos = carregar_carrinhos()
    carrinhos = [c for c in carrinhos if not (c.pedido_id == email and c.produto_id == produto_id)]
    salvar_carrinhos(carrinhos)
    print("Item removido do carrinho.")

def alterar_quantidade_item(email, produto_id, nova_quantidade):
    if nova_quantidade <= 0:
        print("Quantidade inválida. Deve ser maior que zero.")
        return
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