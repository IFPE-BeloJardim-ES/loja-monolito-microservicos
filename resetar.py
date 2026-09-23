"""Apaga os bancos em dados/ para recomeçar com estoque cheio e nenhum pedido.

Rode com todos os serviços desligados.
"""
from pathlib import Path

pasta = Path(__file__).with_name("dados")
apagados = [arquivo.name for arquivo in pasta.glob("*.json")] if pasta.exists() else []
for nome in apagados:
    (pasta / nome).unlink()
print("Apagados: " + (", ".join(apagados) if apagados else "nada para apagar"))
