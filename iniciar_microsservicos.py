"""Sobe os quatro serviços da versão em microsserviços neste mesmo terminal.

Ctrl+C encerra todos. Para derrubar só um, abra http://localhost:<porta>/desligar.
"""
import subprocess
import sys
from pathlib import Path

SERVICOS = ["catalogo.py", "estoque.py", "pedidos.py", "vitrine.py"]
pasta = Path(__file__).parent

processos = [subprocess.Popen([sys.executable, str(pasta / s)], cwd=pasta) for s in SERVICOS]
print(f"{len(processos)} processos iniciados: catálogo 9001, estoque 9002, pedidos 9003, vitrine 9000", flush=True)
try:
    for p in processos:
        p.wait()
except KeyboardInterrupt:
    for p in processos:
        p.terminate()
    print("Todos os serviços encerrados.")
