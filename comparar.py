"""Abre a mesma página 200 vezes em cada arquitetura e mostra o tempo médio."""
import time
from urllib.request import urlopen

N = 200
ALVOS = [
    ("Monolito", "http://127.0.0.1:8000/produto/1", 0),
    ("Microsserviços", "http://127.0.0.1:9000/produto/1", 2),
]

print(f"{'':<16} {'média':>9}   chamadas de rede internas por página")
for nome, url, saltos in ALVOS:
    try:
        inicio = time.perf_counter()
        for _ in range(N):
            with urlopen(url, timeout=5) as resposta:
                resposta.read()
        media = (time.perf_counter() - inicio) / N * 1000
        print(f"{nome:<16} {media:6.2f} ms   {saltos}")
    except OSError as erro:
        print(f"{nome:<16} não respondeu ({erro})")
