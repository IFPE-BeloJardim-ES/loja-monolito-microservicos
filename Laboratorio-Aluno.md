# **Laboratório: a mesma loja, duas arquiteturas** 

Estilos Arquiteturais V · Microsserviços 

Nomes: ____________________________________ 

Vocês vão rodar a **mesma loja** de dois jeitos: como um **monolito** (um processo, um banco) e como **microsserviços** (quatro processos, um banco por serviço). As duas versões têm as mesmas rotas. Ninguém precisa programar — só um experimento pede para mudar um número no código. 

O objetivo é descobrir, na prática, **onde os microsserviços ganham e onde eles cobram** . 

|**Versão**|**Endereço**|**Onde ficam os dados**|
|---|---|---|
|Monolito|http://localhost:8000|dados/monolito.json|
|Microsserviços|http://localhost:9000 (Vitrine)|dados/estoque.json e<br>dados/pedidos.json|
|Rotas nas duas|/produto/1 · /comprar/1 · /relatorio||
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

||**Monolito**|**Microsserviços**|
|---|---|---|
|Quanto tempo ficou fora do ar?|||
|O que parou de funcionar?|||
|O que continuou funcionando?|||

**Responda** Poder ou problema dos microsserviços? Por quê? 

### **Experimento 2 · Latência** 

**Faça** Num terminal livre, rode: 

`python comparar.py</mark>` 

**Faça** Abra de novo /produto/1 nas duas abas e compare o campo tempo_interno_ms. 

||**Monolito**|**Microsserviços**|
|---|---|---|
|Tempo médio por página (comparar.py)|||
|tempo_interno_ms|||

**Responda** Aqui tudo roda no mesmo computador. O que aconteceria com essa diferença se cada serviço estivesse numa máquina diferente? 

### - **Experimento 3 · Consistência** 

Na demonstração, o professor derrubou o Estoque e a loja em microsserviços **continuou vendendo** . Agora vocês vão ver o preço disso. 

**Faça a)** Abra <localhost:9000/relatorio> e anote os números. **b)** Derrube só o Estoque: <localhost:9002/desligar>. **c)** Compre duas vezes: <localhost:9000/comprar/1>. **d)** Religue o Estoque: `python estoque.py`. **e)** Abra <localhost:9000/relatorio> de novo. 

**Deve aparecer** Em (c): "aviso": "Estoque fora do ar: pedido registrado SEM baixa de estoque". Em (e): "pedidos_pendentes": 2 e "consistente": false. 

|**/relatorio (microsserviços)**|**Antes**|**Depois**|
|---|---|---|
|pedidos_confirmados|||
|pedidos_pendentes|||
|baixas_de_estoque|||
|consistente|||


**Faça** Abra a pasta dados/. Compare pedidos.json e estoque.json: cada banco conta uma história diferente. 

**Responda** No monolito, o bug do Estoque derrubou a loja inteira: nenhuma venda, mas nenhum dado errado. Nos microsserviços, a loja vendeu, mas os bancos discordam. **Qual dos dois a loja prefere? Quem decide isso?** 

### **Experimento 4 · Operação** 

**Faça** Faça uma compra em cada versão (/comprar/2 nas duas) e olhe os terminais. 

|**Para uma compra…**|**Monolito**<br>**Microsserviços**|
|---|---|



|Quantos processos estão rodando?|
|---|
|Quantas portas?|
|Quantos arquivos de banco?|
|Quantas linhas de log apareceram?|
|Em quantos serviços?|


**Responda** Se a compra desse errado, onde vocês procurariam o erro em cada versão? 

## **Placar da dupla** 

|**Experimento**|**Quem saiu melhor?**|**Para microsserviços, é poder ou**<br>**problema?**|
|---|---|---|
|Bug fatal (demonstração)|||
|1 · Deploy|||
|2 · Latência|||
|3 · Consistência|||
|4 · Operação|||


**Para fechar** Uma loja com **3 desenvolvedores** deveria usar qual das duas versões? E uma com **300** ? Usem o placar como argumento. 

Para recomeçar do zero: desliguem tudo (Ctrl+C nos terminais) e rodem `python resetar.py`. 

