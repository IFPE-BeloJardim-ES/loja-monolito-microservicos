"""Peças compartilhadas pelos serviços do laboratório. Só biblioteca padrão do Python.

Não é preciso ler este arquivo para fazer os experimentos.
"""
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

PASTA_DADOS = Path(__file__).with_name("dados")


class Indisponivel(Exception):
    """O outro serviço não respondeu."""


class Recusado(Exception):
    """O outro serviço respondeu, mas com erro (ex.: sem estoque)."""

    def __init__(self, status, mensagem):
        super().__init__(mensagem)
        self.status = status


def chamar(servico, url):
    """Chama outro serviço pela rede e devolve a resposta JSON."""
    try:
        with urlopen(url, timeout=3) as resposta:
            return json.load(resposta)
    except HTTPError as erro:
        try:
            mensagem = json.load(erro).get("erro", "erro")
        except ValueError:
            mensagem = f"erro {erro.code}"
        raise Recusado(erro.code, mensagem)
    except OSError:
        raise Indisponivel(f"o serviço {servico}")


class Banco:
    """Um banco de dados do tamanho de um arquivo JSON, dentro da pasta dados/."""

    def __init__(self, arquivo, inicial):
        PASTA_DADOS.mkdir(exist_ok=True)
        self.caminho = PASTA_DADOS / arquivo
        if not self.caminho.exists():
            self.caminho.write_text(json.dumps(inicial, ensure_ascii=False, indent=2), encoding="utf-8")
        self.dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        self.trava = threading.Lock()

    def salvar(self):
        self.caminho.write_text(json.dumps(self.dados, ensure_ascii=False, indent=2), encoding="utf-8")


def cair_em_breve(codigo=1):
    """Derruba o processo inteiro 0,3 s depois de responder."""
    threading.Timer(0.3, os._exit, [codigo]).start()


def servir(nome, porta, rotas, tempo_de_subida=0):
    """Sobe um servidor HTTP. Toda rota responde JSON. /desligar existe em todos."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            partes = [p for p in self.path.split("?")[0].strip("/").split("/") if p]
            if partes == ["desligar"]:
                cair_em_breve(0)
                status, corpo = 200, {"aviso": f"{nome} desligando"}
            elif not partes or partes[0] not in rotas:
                status, corpo = 404, {"erro": "rota não encontrada", "rotas": ["/" + r for r in rotas]}
            else:
                try:
                    resultado = rotas[partes[0]](*partes[1:])
                    status, corpo = resultado if isinstance(resultado, tuple) else (200, resultado)
                except Indisponivel as erro:
                    status, corpo = 503, {"erro": f"{erro} está fora do ar"}
                except Recusado as erro:
                    status, corpo = erro.status, {"erro": str(erro)}
                except KeyError as erro:
                    status, corpo = 404, {"erro": f"produto {erro} não existe"}
                except Exception as erro:
                    status, corpo = 500, {"erro": f"{type(erro).__name__}: {erro}"}

            dados = json.dumps(corpo, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(dados)))
            self.end_headers()
            self.wfile.write(dados)
            if self.path != "/favicon.ico":
                print(f"[{nome}] {self.path} -> {status}", flush=True)

        def log_message(self, *args):
            pass

    if tempo_de_subida:
        print(f"[{nome}] subindo... ({tempo_de_subida} s)", flush=True)
        time.sleep(tempo_de_subida)
    print(f"[{nome}] no ar em http://localhost:{porta}", flush=True)
    try:
        ThreadingHTTPServer(("127.0.0.1", porta), Handler).serve_forever()
    except KeyboardInterrupt:
        print(f"[{nome}] encerrado", flush=True)
