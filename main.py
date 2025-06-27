from apresentacao.view.tela_menu_principal import tela_menu_principal
from negocio.service.carrinho_service import inicializar_carrinhos_json
from negocio.service.pedido_service import inicializar_pedidos_json
from negocio.service.produto_service import inicializar_produtos_json

if  __name__ == "__main__":
    inicializar_carrinhos_json()
    inicializar_produtos_json()
    inicializar_pedidos_json()
    tela_menu_principal()