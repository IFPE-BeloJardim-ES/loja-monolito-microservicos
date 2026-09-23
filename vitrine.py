"""Vitrine (API Gateway) — porta 9000.

A porta de entrada da versão em microsserviços. Não tem banco nem regra de negócio:
monta as respostas chamando os outros serviços. Tem as MESMAS rotas do monolito.

Rotas:
  /produto/<id>
  /comprar/<id>
  /relatorio
  /bug/estoque
"""
import time

from base import Indisponivel, chamar, servir

CATALOGO = "http://127.0.0.1:9001"
ESTOQUE = "http://127.0.0.1:9002"
PEDIDOS = "http://127.0.0.1:9003"
TEMPO_DE_SUBIDA = 4  # simulado


def produto(pid):
    inicio = time.perf_counter()
    dados = chamar("Catálogo", f"{CATALOGO}/produtos/{pid}")
    try:
        dados["em_estoque"] = chamar("Estoque", f"{ESTOQUE}/estoque/{pid}")["quantidade"]
    except Indisponivel:
        dados["em_estoque"] = "desconhecido (Estoque fora do ar)"
    dados["tempo_interno_ms"] = round((time.perf_counter() - inicio) * 1000, 3)
    return dados


def comprar(pid):
    return chamar("Pedidos", f"{PEDIDOS}/comprar/{pid}")


def relatorio():
    pedidos = chamar("Pedidos", f"{PEDIDOS}/resumo")
    estoque = chamar("Estoque", f"{ESTOQUE}/resumo")
    return {
        "pedidos_confirmados": pedidos["confirmados"],
        "pedidos_pendentes": pedidos["pendentes"],
        "baixas_de_estoque": estoque["baixas"],
        "consistente": pedidos["pendentes"] == 0 and pedidos["confirmados"] == estoque["baixas"],
    }


def bug(modulo="estoque"):
    return chamar("Estoque", f"{ESTOQUE}/bug")


if __name__ == "__main__":
    servir("vitrine", 9000, {"produto": produto, "comprar": comprar, "relatorio": relatorio, "bug": bug},
           tempo_de_subida=TEMPO_DE_SUBIDA)
