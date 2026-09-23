"""Serviço de Pedidos — porta 9003.

Dono dos pedidos. Banco próprio: dados/pedidos.json.
Para vender, pergunta o preço ao Catálogo e pede a baixa ao Estoque — pela rede.

Rotas:
  /comprar/<id>
  /resumo
"""
from base import Banco, Indisponivel, Recusado, chamar, servir

CATALOGO = "http://127.0.0.1:9001"
ESTOQUE = "http://127.0.0.1:9002"
TEMPO_DE_SUBIDA = 4  # simulado

banco = Banco("pedidos.json", {"pedidos": []})


def comprar(pid):
    produto = chamar("Catálogo", f"{CATALOGO}/produtos/{pid}")

    # Gravação 1 — no banco de Pedidos
    with banco.trava:
        pedido = {
            "numero": len(banco.dados["pedidos"]) + 1,
            "produto": produto["nome"],
            "valor": produto["preco"],
            "status": "pendente",
        }
        banco.dados["pedidos"].append(pedido)
        banco.salvar()

    # Gravação 2 — no banco de Estoque, em outro processo
    try:
        chamar("Estoque", f"{ESTOQUE}/baixar/{pid}")
    except Recusado:
        with banco.trava:
            pedido["status"] = "cancelado"
            banco.salvar()
        return 409, {"erro": "sem estoque", "pedido": pedido}
    except Indisponivel:
        # Decisão de negócio: não perder a venda. O pedido fica pendente, sem baixa de estoque.
        return 202, {"pedido": pedido, "aviso": "Estoque fora do ar: pedido registrado SEM baixa de estoque"}

    with banco.trava:
        pedido["status"] = "confirmado"
        banco.salvar()
    return {"pedido": pedido}


def resumo():
    contagem = {"confirmado": 0, "pendente": 0, "cancelado": 0}
    for pedido in banco.dados["pedidos"]:
        contagem[pedido["status"]] += 1
    return {"confirmados": contagem["confirmado"], "pendentes": contagem["pendente"], "cancelados": contagem["cancelado"]}


if __name__ == "__main__":
    servir("pedidos", 9003, {"comprar": comprar, "resumo": resumo}, tempo_de_subida=TEMPO_DE_SUBIDA)
