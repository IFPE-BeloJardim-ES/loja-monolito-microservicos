# Laboratório — a mesma loja, duas arquiteturas

**Estilos Arquiteturais V · Microsserviços**

**Nomes:** Thiago da Silva Coimbra Patriota

Este laboratório executa a mesma loja de dois jeitos: como um **monolito** (um processo, um banco) e como **microsserviços** (quatro processos, um banco por serviço). As duas versões expõem as mesmas rotas principais.

> **Estado deste projeto após a realização do laboratório:** o Experimento 1 já foi aplicado, portanto `DESCONTO = 10` em `monolito.py` e `catalogo.py`. Assim, o Teclado mecânico aparece por **R$ 225,00**. Para repetir o laboratório desde o estado inicial, altere os dois descontos de volta para `0`.

## Como executar

Requisito: Python 3.8 ou superior. Nada para instalar. No macOS/Linux use `python3`.

| Versão | Como subir | Endereço |
|---|---|---|
| Monolito | `python monolito.py` | http://localhost:8000 |
| Microsserviços | `python iniciar_microsservicos.py` | http://localhost:9000 |

| Versão | Endereço | Onde ficam os dados |
|---|---|---|
| Monolito | http://localhost:8000 | `dados/monolito.json` |
| Microsserviços | http://localhost:9000 (Vitrine) | `dados/estoque.json` e `dados/pedidos.json` |
| Rotas nas duas | `/produto/1`, `/comprar/1`, `/relatorio`, `/bug/estoque` | |
| Derrubar um serviço | `http://localhost:<porta>/desligar` | Catálogo 9001 · Estoque 9002 · Pedidos 9003 |

Para subir as duas versões, abra dois terminais na pasta do projeto:

```bash
# terminal 1 — leva 10 s para subir
python monolito.py

# terminal 2 — sobe 4 processos
python iniciar_microsservicos.py
```

Antes da promoção, ao abrir `/produto/1` nas duas versões, o resultado esperado é o mesmo produto: **Teclado mecânico, R$ 250,00 e 5 unidades em estoque**.

---

## Experimento 1 · Deploy de uma promoção

O time de vendas quer 10% de desconto. Foi alterado:

```python
DESCONTO = 10
```

em `monolito.py` e `catalogo.py`.

No monolito foi necessário reiniciar o processo inteiro. Nos microsserviços foi reiniciado apenas o Catálogo.

### Resultado observado

| | Monolito | Microsserviços |
|---|---|---|
| Quanto tempo ficou fora do ar? | **≈ 10,6 s** para a aplicação inteira voltar | **≈ 4,6 s** apenas para rotas dependentes do Catálogo |
| O que parou de funcionar? | Todas as rotas, incluindo `/relatorio`, `/produto` e `/comprar` | `/produto` e `/comprar`, pois dependem do Catálogo |
| O que continuou funcionando? | Nada enquanto o processo reiniciava | `/relatorio` e os serviços que não dependiam do Catálogo continuaram respondendo |

Depois da subida, o produto passou de **R$ 250,00 para R$ 225,00** nas duas arquiteturas.

### Resposta — poder ou problema dos microsserviços?

Neste experimento, é principalmente um **poder** dos microsserviços. A alteração do preço exigiu reiniciar somente o serviço de Catálogo, mantendo outras partes independentes da aplicação disponíveis. Isso reduz o impacto de um deploy e permite atualizar partes do sistema separadamente. Em compensação, essa independência existe porque a aplicação passa a ter mais processos, comunicação em rede e componentes para administrar.

---

## Experimento 2 · Latência

Foi executado:

```bash
python comparar.py
```

O script fez 200 requisições para `/produto/1` em cada arquitetura.

### Resultado observado nesta execução

| | Monolito | Microsserviços |
|---|---:|---:|
| Tempo médio por página (`comparar.py`) | **0,55 ms** | **1,59 ms** |
| Chamadas de rede internas por página | **0** | **2** |
| `tempo_interno_ms` — média de 20 leituras | **≈ 0,012 ms** | **≈ 1,103 ms** |
| `tempo_interno_ms` — uma leitura observada | **0,011 ms** | **1,694 ms** |

Os números podem variar de uma máquina para outra, mas a relação observada é a importante: o monolito faz chamadas de função dentro do mesmo processo; a Vitrine dos microsserviços precisa consultar Catálogo e Estoque por HTTP.

### Resposta

Se cada serviço estivesse em uma máquina diferente, a diferença provavelmente aumentaria. Além do processamento do código, cada chamada precisaria atravessar uma rede real, ficando sujeita a latência de transporte, serialização, congestionamento, perda de pacotes e variação no tempo de resposta. Quanto maior o número de chamadas entre serviços para concluir uma requisição, maior tende a ser o custo acumulado de rede.

---

## Experimento 3 · Consistência

Primeiro foi consultado `/relatorio` com todos os serviços funcionando. Em seguida, somente o Estoque foi desligado e foram feitas duas compras de `/comprar/1`. Depois o Estoque foi iniciado novamente.

Durante as duas compras apareceu o aviso:

```json
{
  "aviso": "Estoque fora do ar: pedido registrado SEM baixa de estoque"
}
```

### Resultado observado

| `/relatorio` (microsserviços) | Antes | Depois |
|---|---:|---:|
| `pedidos_confirmados` | **0** | **0** |
| `pedidos_pendentes` | **0** | **2** |
| `baixas_de_estoque` | **0** | **0** |
| `consistente` | **true** | **false** |

Após o teste, `pedidos.json` registrava os dois pedidos como `pendente`, enquanto `estoque.json` ainda indicava 5 unidades do produto 1 e nenhuma baixa. Ou seja, os bancos passaram a representar estados diferentes do mesmo negócio.

### Resposta — qual dos dois a loja prefere? Quem decide?

Depende da regra de negócio. Se a prioridade for **não aceitar uma venda sem garantir o estoque**, o comportamento transacional do monolito é mais simples e mantém os dados consistentes: se o Estoque falha, a venda também falha. Se a prioridade for **continuar aceitando pedidos mesmo durante uma falha**, a estratégia dos microsserviços pode ser aceitável, desde que exista depois um processo de reconciliação para resolver os pedidos pendentes.

Essa decisão não deve ser apenas técnica. Ela precisa ser definida pelo negócio junto com a equipe de produto e arquitetura, considerando requisitos como disponibilidade, risco de vender sem estoque, experiência do cliente e custo de corrigir inconsistências.

---

## Experimento 4 · Operação

Foi feita uma compra de `/comprar/2` em cada arquitetura e foram observados processos, portas, bancos e logs.

### Resultado observado

| Para uma compra… | Monolito | Microsserviços |
|---|---:|---:|
| Quantos processos estão rodando? | **1** | **4** |
| Quantas portas? | **1** (`8000`) | **4** (`9000`, `9001`, `9002`, `9003`) |
| Quantos arquivos de banco? | **1** (`monolito.json`) | **2** (`pedidos.json` e `estoque.json`) |
| Quantas linhas de log apareceram na compra? | **1** | **4** |
| Em quantos serviços? | **1** | **4** — Vitrine, Pedidos, Catálogo e Estoque |

No monolito foi registrada uma linha semelhante a:

```text
[monolito] /comprar/2 -> 200
```

Nos microsserviços a mesma compra atravessou quatro componentes, gerando registros equivalentes em Catálogo, Estoque, Pedidos e Vitrine.

### Resposta

Se uma compra desse errado no monolito, a investigação começaria no único processo e no único banco, seguindo o fluxo das funções de Catálogo, Estoque e Pedidos dentro da mesma aplicação.

Nos microsserviços seria necessário identificar em qual etapa a falha ocorreu e correlacionar os logs de Vitrine, Pedidos, Catálogo e Estoque. Também seria necessário verificar a comunicação HTTP entre serviços e os dois arquivos de banco. Isso torna a operação e o diagnóstico distribuído mais trabalhosos e mostra por que sistemas reais de microsserviços normalmente precisam de observabilidade centralizada, correlação de requisições e monitoramento.

---

## Placar da dupla

| Experimento | Quem saiu melhor? | Para microsserviços, é poder ou problema? |
|---|---|---|
| Bug fatal (demonstração) | **Microsserviços** | **Poder** — a falha do Estoque fica isolada, sem necessariamente derrubar toda a loja |
| 1 · Deploy | **Microsserviços** | **Poder** — permite atualizar um serviço com impacto menor no restante do sistema |
| 2 · Latência | **Monolito** | **Problema** — chamadas HTTP internas adicionam custo e latência |
| 3 · Consistência | **Monolito** | **Problema** — bancos independentes podem ficar temporariamente inconsistentes |
| 4 · Operação | **Monolito** | **Problema** — há mais processos, portas, logs, comunicação e pontos de falha para administrar |

---

## Para fechar

Uma loja com **3 desenvolvedores** provavelmente se beneficia mais do **monolito**, porque o placar mostra que ele é mais simples de operar, mais fácil de depurar, tem menor latência interna e oferece consistência transacional de forma direta. Para uma equipe pequena, o custo operacional de quatro serviços pode superar os benefícios de independência.

Em uma loja com **300 desenvolvedores**, os **microsserviços podem fazer mais sentido**, principalmente se o sistema já tiver domínios bem separados, necessidade de escalar componentes independentemente e várias equipes trabalhando e fazendo deploys de forma autônoma. O Experimento 1 e a demonstração do bug mostram os benefícios de isolamento e deploy independente. Ainda assim, o tamanho da equipe sozinho não obriga a adoção de microsserviços: a empresa precisa aceitar os custos demonstrados nos Experimentos 2, 3 e 4 e ter infraestrutura para observabilidade, automação de deploy, comunicação e tratamento de falhas distribuídas.

---

## Recomeçar do zero

Desligue todos os processos e rode:

```bash
python resetar.py
```

Isso apaga os arquivos JSON de dados. Para repetir também o **Experimento 1 desde o preço original**, altere `DESCONTO = 10` de volta para `DESCONTO = 0` em `monolito.py` e `catalogo.py` antes de iniciar.
