import json
import os
import uuid
from datetime import datetime
from negocio.model.pedido import Pedido
from negocio.service.carrinho_service import listar_itens_carrinho, salvar_carrinhos, carregar_carrinhos

PEDIDOS_JSON = "pedidos.json"

def inicializar_pedidos_json():
    if not os.path.exists(PEDIDOS_JSON):
        with open(PEDIDOS_JSON, "w", encoding="utf-8") as f:
            f.write("[]")

def carregar_pedidos():
    with open(PEDIDOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Pedido(**p) for p in data]

def salvar_pedidos(pedidos):
    with open(PEDIDOS_JSON, "w", encoding="utf-8") as f:
        json.dump([p.__dict__ for p in pedidos], f, indent=2, ensure_ascii=False)

def salvar_pedido(pedido):
    pedidos = carregar_pedidos()
    pedidos.append(pedido)
    salvar_pedidos(pedidos)

def finalizar_compra(email):
    itens = listar_itens_carrinho(email)
    if not itens:
        print("Carrinho vazio. Não é possível finalizar a compra.")
        return

    total = sum(item.subtotal for item in itens)
    pedido = Pedido(
        id=str(uuid.uuid4()),
        usuario_id=email,
        data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total=total
    )
    pedido.itens = [item.__dict__ for item in itens]


    salvar_pedido(pedido)

    # Limpa o carrinho do usuário
    carrinhos = carregar_carrinhos()
    carrinhos = [c for c in carrinhos if c.pedido_id != email]
    salvar_carrinhos(carrinhos)

    print("Compra finalizada com sucesso!")
    print(f"Total: R${total:.2f}")