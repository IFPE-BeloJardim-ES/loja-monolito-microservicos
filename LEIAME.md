# Laboratório — a mesma loja, duas arquiteturas

Requisito: Python 3.8 ou superior. Nada para instalar. No macOS/Linux use `python3`.

| Versão | Como subir | Endereço |
|---|---|---|
| Monolito | `python monolito.py` | http://localhost:8000 |
| Microsserviços | `python iniciar_microsservicos.py` | http://localhost:9000 |

As duas têm as mesmas rotas: `/produto/1`, `/comprar/1`, `/relatorio`, `/bug/estoque`.

Para derrubar um serviço só: `http://localhost:<porta>/desligar`.
Para recomeçar do zero: desligue tudo e rode `python resetar.py`.

Os bancos de cada versão ficam na pasta `dados/`.
