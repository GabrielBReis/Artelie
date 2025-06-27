import uuid
import os
import json
from negocio.model.pedido import Pedido
from negocio.service.carrinho_service import listar_itens_carrinho, limpar_carrinho

PEDIDOS_JSON = "pedidos.json"

def inicializar_pedidos_json():
    if not os.path.exists(PEDIDOS_JSON):
        with open(PEDIDOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")

def carregar_pedidos():
    with open(PEDIDOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data  # Se quiser, pode converter para objetos Pedido

def salvar_pedido(pedido):
    pedidos = carregar_pedidos()
    pedidos.append({
        "id": pedido.id,
        "usuario_id": pedido.usuario_id,
        "data": pedido.data,
        "total": pedido.total,
        "itens": [item.__dict__ for item in pedido.itens]
    })
    with open(PEDIDOS_JSON, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=2, ensure_ascii=False)

def finalizar_pedido(usuario_email):
    itens = listar_itens_carrinho(usuario_email)
    if not itens:
        print("Carrinho vazio. Não é possível finalizar o pedido.")
        return

    pedido = Pedido(str(uuid.uuid4()), usuario_email)
    for item in itens:
        pedido.adicionar_item(item)

    salvar_pedido(pedido)
    limpar_carrinho(usuario_email)
    print("Pedido finalizado com sucesso!")
    print(f"Total: R${pedido.total:.2f}")
