# PR Estruturado

## Título sugerido
Documenta e preenche o roteiro dos experimentos 1 a 4 com estimativas e conclusões orientadas

## Contexto
O laboratório compara monolito e microsserviços em cenários de deploy, latência, consistência e operação.
Antes desta mudança, o README tinha várias tabelas sem preenchimento e uma tabela do experimento 4 quebrada em markdown.

## Objetivo
Entregar um roteiro pronto para uso em sala, com valores estimados coerentes com o comportamento esperado do sistema, reduzindo ambiguidade na execução.

## Escopo
- Preenchimento estimado das tabelas dos experimentos 1, 2, 3 e 4 no README.
- Inclusão de respostas estimadas para as perguntas analíticas de cada experimento.
- Correção estrutural da tabela do experimento 4 para ficar válida e legível.
- Preenchimento do placar final e sugestão de conclusão para times de tamanhos diferentes.

## Principais mudanças
- README com aviso explícito de que os valores são estimados.
- Experimento 1 com:
  - tempo fora do ar por arquitetura,
  - impacto funcional durante deploy,
  - análise de poder x custo dos microsserviços.
- Experimento 2 com:
  - valores médios estimados de latência,
  - interpretação para cenário distribuído em máquinas distintas.
- Experimento 3 com:
  - antes/depois preenchido para consistência,
  - interpretação de trade-off entre disponibilidade e consistência.
- Experimento 4 com:
  - tabela corrigida e preenchida,
  - visão operacional para troubleshooting.
- Placar final preenchido e fechamento argumentativo para equipe pequena x grande.

## Arquivos alterados
- README.md
- monolito.py (DESCONTO ajustado para 10 durante o experimento)
- catalogo.py (DESCONTO ajustado para 10 durante o experimento)

## Validação realizada
- Revisão de consistência entre o conteúdo escrito no README e o comportamento esperado das rotas no código.
- Verificação visual da estrutura de tabelas em markdown para evitar quebra de renderização.

## Riscos e observações
- Os números de latência são estimativas e podem variar conforme máquina, carga local e estado dos processos.
- O valor de DESCONTO em monolito.py e catalogo.py está em 10 para refletir o experimento de promoção.

## Fora de escopo
- Execução automática dos experimentos para coleta de métricas reais.
- Ajustes em lógica de negócio ou arquitetura dos serviços.

## Checklist para abertura do PR
- Confirmar se o time quer manter DESCONTO em 10 ou voltar para 0 após a aula.
- Confirmar se arquivos de cache Python não serão enviados no PR.
- Executar uma leitura final do README com render markdown no editor.

## Passos de teste sugeridos
1. Subir monolito e microsserviços.
2. Validar rotas principais em ambas as arquiteturas.
3. Rodar comparar.py e confrontar com os valores estimados do README.
4. Simular queda do estoque e verificar consistência no relatório.

## Resultado esperado
Material didático pronto para aplicação imediata, com roteiro guiado, tabelas preenchidas e respostas base para discussão em sala.
