"""Serviço de Estoque — porta 9002.

Dono das quantidades. Banco próprio: dados/estoque.json.

Rotas:
  /estoque/<id>    quantidade disponível
  /baixar/<id>     retira uma unidade
  /resumo          total de baixas
  /bug             simula um bug fatal no serviço
"""
from base import Banco, cair_em_breve, servir

TEMPO_DE_SUBIDA = 4  # simulado

banco = Banco("estoque.json", {"estoque": {"1": 5, "2": 5, "3": 5}, "baixas": 0})


def estoque(pid):
    return {"id": pid, "quantidade": banco.dados["estoque"][pid]}


def baixar(pid):
    with banco.trava:
        if banco.dados["estoque"][pid] <= 0:
            return 409, {"erro": "sem estoque"}
        banco.dados["estoque"][pid] -= 1
        banco.dados["baixas"] += 1
        banco.salvar()
    return {"id": pid, "quantidade": banco.dados["estoque"][pid]}


def resumo():
    return {"baixas": banco.dados["baixas"]}


def bug(*_):
    cair_em_breve()
    return {"aviso": "bug fatal no serviço de Estoque: o processo vai cair em instantes"}


if __name__ == "__main__":
    servir("estoque", 9002, {"estoque": estoque, "baixar": baixar, "resumo": resumo, "bug": bug},
           tempo_de_subida=TEMPO_DE_SUBIDA)
