# Laboratório — a mesma loja, duas arquiteturas

Estilos Arquiteturais V · Microsserviços 

Nomes: ____________________________________ 

Vocês vão rodar a **mesma loja** de dois jeitos: como um **monolito** (um processo, um banco) e como **microsserviços** (quatro processos, um banco por serviço). As duas versões têm as mesmas rotas. Ninguém precisa programar — só um experimento pede para mudar um número no código. 

Requisito: Python 3.8 ou superior. Nada para instalar. No macOS/Linux use `python3`.

| Versão | Como subir | Endereço |
|---|---|---|
| Monolito | `python monolito.py` | http://localhost:8000 |
| Microsserviços | `python iniciar_microsservicos.py` | http://localhost:9000 |

O objetivo é descobrir, na prática, **onde os microsserviços ganham e onde eles cobram** . 

|**Versão**|**Endereço**|**Onde ficam os dados**|
|---|---|---|
|Monolito|http://localhost:8000|dados/monolito.json|
|Microsserviços|http://localhost:9000 (Vitrine)|dados/estoque.json e<br>dados/pedidos.json|
|Rotas nas duas| `/produto/1`, `/comprar/1`, `/relatorio`, `/bug/estoque`||
|Derrubar um serviço|http://localhost:<porta>/desligar|Catálogo 9001 · Estoque 9002 ·<br>Pedidos 9003|

**Faça** Abra dois terminais na pasta laboratorio. 

<mark># terminal 1 — leva 10 s para subir</mark> `python monolito.py` 

<mark># terminal 2 — sobe 4 processos</mark> `python iniciar_microsservicos.py` 

**Faça** Abra duas abas no navegador, lado a lado: 

http://localhost:8000/produto/1,  http://localhost:9000/produto/1 

**Deve aparecer** O mesmo produto nas duas: Teclado mecânico, R$ 250, 5 em estoque. 

### **Experimento 1 · Deploy de uma promoção** 

O time de vendas quer 10% de desconto. Vocês vão "publicar" essa mudança nas duas versões e observar **o que sai do ar enquanto isso**. 

**Faça — monolito a)** Em monolito.py, mude DESCONTO = 0 para DESCONTO = 10. **b)** No terminal 1, Ctrl+C e rode `python monolito.py` de novo. **c)** Durante os 10s de subida, tente abrir <localhost:8000/relatorio>. 

**Faça — microsserviços a)** Em catalogo.py, mude DESCONTO = 0 para DESCONTO = 10. **b)** Abra <localhost:9001/desligar> para derrubar só o Catálogo. **c)** Num terceiro terminal, rode `python catalogo.py`. **d)** Durante os 4s de subida, tente <localhost:9000/relatorio> e <localhost:9000/produto/1>.   

**Deve aparecer** Depois da subida, o preço é R$ 225 nas duas. 

> Valores abaixo são **estimados** para deixar o roteiro pronto. Na execução real, podem variar um pouco.

||**Monolito**|**Microsserviços**|
|---|---|---|
|Quanto tempo ficou fora do ar?|~10 s (reinício total)|~4 s (só o Catálogo)|
|O que parou de funcionar?|Tudo (`/produto`, `/comprar`, `/relatorio`)|Rotas que dependem do Catálogo (`/produto` e `/comprar`)|
|O que continuou funcionando?|Nada na API|`/relatorio` continuou (depende de Pedidos + Estoque)|

**Responda** Poder ou problema dos microsserviços? Por quê? 

**Resposta estimada:** Poder, porque permite deploy isolado e reduz indisponibilidade global. Problema, porque exige coordenar processos e lidar com falhas parciais.

### **Experimento 2 · Latência** 

**Faça** Num terminal livre, rode: 

`python comparar.py</mark>` 

**Faça** Abra de novo /produto/1 nas duas abas e compare o campo tempo_interno_ms. 

||**Monolito**|**Microsserviços**|
|---|---|---|
|Tempo médio por página (comparar.py)|~2,5 ms|~8,5 ms|
|tempo_interno_ms|~0,02 ms|~2,00 ms|

**Responda** Aqui tudo roda no mesmo computador. O que aconteceria com essa diferença se cada serviço estivesse numa máquina diferente? 

**Resposta estimada:** A diferença aumentaria. Em máquinas separadas entram latência de rede, variação de rota, timeout e overhead de serialização em cada chamada entre serviços.

### - **Experimento 3 · Consistência** 

Na demonstração, o professor derrubou o Estoque e a loja em microsserviços **continuou vendendo** . Agora vocês vão ver o preço disso. 

**Faça a)** Abra <localhost:9000/relatorio> e anote os números. **b)** Derrube só o Estoque: <localhost:9002/desligar>. **c)** Compre duas vezes: <localhost:9000/comprar/1>. **d)** Religue o Estoque: `python estoque.py`. **e)** Abra <localhost:9000/relatorio> de novo. 

**Deve aparecer** Em (c): "aviso": "Estoque fora do ar: pedido registrado SEM baixa de estoque". Em (e): "pedidos_pendentes": 2 e "consistente": false. 

|**/relatorio (microsserviços)**|**Antes**|**Depois**|
|---|---|---|
|pedidos_confirmados|0|0|
|pedidos_pendentes|0|2|
|baixas_de_estoque|0|0|
|consistente|true|false|


**Faça** Abra a pasta dados/. Compare pedidos.json e estoque.json: cada banco conta uma história diferente. 

**Responda** No monolito, o bug do Estoque derrubou a loja inteira: nenhuma venda, mas nenhum dado errado. Nos microsserviços, a loja vendeu, mas os bancos discordam. **Qual dos dois a loja prefere? Quem decide isso?** 

**Resposta estimada:** Depende da regra de negócio. Se prioridade é não vender com dado inconsistente, monolito (ou fluxo transacional forte) é melhor. Se prioridade é não parar de vender, microsserviços com consistência eventual é melhor. Essa decisão é do negócio com arquitetura e operação.

### **Experimento 4 · Operação** 

**Faça** Faça uma compra em cada versão (/comprar/2 nas duas) e olhe os terminais. 

|**Para uma compra...**|**Monolito**|**Microsserviços**|
|---|---|---|
|Quantos processos estão rodando?|1|4 (Vitrine + 3 serviços)|
|Quantas portas?|1 (8000)|4 (9000, 9001, 9002, 9003)|
|Quantos arquivos de banco?|1 (`dados/monolito.json`)|2 (`dados/pedidos.json` e `dados/estoque.json`)|
|Quantas linhas de log apareceram?|~1|~5|
|Em quantos serviços?|1|3 (Vitrine, Pedidos, Estoque) + Catálogo na consulta de preço|


**Responda** Se a compra desse errado, onde vocês procurariam o erro em cada versão? 

**Resposta estimada:** No monolito, olhar um processo e um log central já cobre quase tudo. Nos microsserviços, é preciso seguir a chamada entre Vitrine, Pedidos, Catálogo e Estoque, correlacionando logs de múltiplos processos.

## **Placar da dupla** 

|**Experimento**|**Quem saiu melhor?**|**Para microsserviços, é poder ou**<br>**problema?**|
|---|---|---|
|Bug fatal (demonstração)|Microsserviços (degradação parcial)|Poder|
|1 · Deploy|Microsserviços|Poder|
|2 · Latência|Monolito|Problema|
|3 · Consistência|Monolito (consistência forte)|Problema (trade-off de consistência)|
|4 · Operação|Monolito (simplicidade)|Problema (maior complexidade operacional)|


**Para fechar** Uma loja com **3 desenvolvedores** deveria usar qual das duas versões? E uma com **300** ? Usem o placar como argumento. 

**Resposta estimada para discussão final:**
- Com 3 desenvolvedores: monolito tende a ser melhor pela simplicidade, menor custo de operação e depuração mais direta.
- Com 300 desenvolvedores: microsserviços tendem a ser melhores pela autonomia de times, deploy independente e escalabilidade organizacional.

Para recomeçar do zero: desliguem tudo (Ctrl+C nos terminais) e rodem `python resetar.py`. 


