# Prompt para o Codex: investigar um port nativo de SoulSilver para Switch

Abra o repositório https://github.com/GodPromettheus/hgss-sw e trabalhe nele como fork de https://github.com/sasantos/pokemon-ds-widescreen-switch.

Leia primeiro `AGENTS.md`, o README, `docs/NATIVE-PORT-MEMORY.md` e a documentação relevante de `ClickingMaster/ssrecomp`. Respeite todas as regras do repositório.

## Objetivo

Investigue se é viável criar uma versão homebrew para Nintendo Switch de Pokémon SoulSilver que:

- use uma única tela e controles do Switch;
- não inclua nem dependa do núcleo de emulação melonDS;
- reaproveite, onde for tecnicamente possível e compatível com as licenças, o código e o conhecimento do projeto de recompilação.

O requisito “nativo” significa que o jogo não deve depender de um Nintendo DS virtual com CPU, memória e periféricos emulados. Um `.nro` que embute melonDS ou código recompilado que ainda usa o runtime do melonDS não atende ao requisito.

## Primeira tarefa: estudo de viabilidade baseado no código

Não comece removendo o melonDS nem reescrevendo grandes partes. Faça primeiro uma investigação rastreável no código e entregue um relatório contendo:

1. O caminho de build e execução atual para Switch, desde `tools/recomp.py` e `gen/` até `frontend/main.cpp` e o runtime.
2. Quais interfaces, tipos e serviços do melonDS ainda são usados pelo código recompilado. Inclua CPU ARM9/ARM7, memória e barramento, BIOS/TCM, overlays, interrupções, temporização, cartucho, DMA, vídeo 2D/3D, áudio, RTC, entrada e saves.
3. O que a recompilação já transforma em código C++ hospedeiro e o que continua dependendo da semântica do DS ou do melonDS. Identifique instruções que ainda caem no interpretador e guardas/fallbacks do despachante.
4. Comparação de arquiteturas candidatas:
   - manter melonDS e melhorar desempenho/experiência;
   - manter a recompilação e substituir partes do runtime por interfaces próprias do Switch;
   - portar o jogo a partir de fontes de decompilação, implementando sistemas de jogo e apresentação para Switch.
   Para cada uma, descreva reutilização, riscos, dependências legais/técnicas, alcance funcional e custo relativo.
5. Proposta de um vertical slice mínimo que prove a arquitetura recomendada, com arquivos envolvidos, critério verificável de sucesso e como comparar o comportamento com o projeto atual.
6. Lista de bloqueios e perguntas que realmente dependem do usuário. Não solicite ROM, save ou outro conteúdo protegido; os testes, se necessários, devem usar arquivos locais fornecidos pelo usuário e nunca ser enviados ao GitHub.

## Regras

- Não publique ROMs, saves, dumps, save states, código gerado a partir da ROM (`gen/`), builds, assets proprietários ou arquivos de jogo.
- Não altere nem apague o caminho atual baseado em melonDS durante o estudo.
- Não declare que o resultado é “nativo” apenas por ser um `.nro`, por ter tela única ou por recompilar instruções ARM.
- Preserve licenças, avisos de copyright e atribuições. Verifique os termos antes de copiar ou adaptar código externo.
- Apoie conclusões com caminhos de arquivos, símbolos/funções e links para fontes primárias.
- Não faça benchmarks sem um método reproduzível e hardware apropriado; se não houver Switch físico, marque os resultados como pendentes.
- Após o relatório, proponha uma implementação pequena e isolada. Só comece mudanças de código quando a arquitetura e os critérios estiverem claros; mantenha o app atual funcionando como referência.

## Resultado esperado

Um relatório de viabilidade no próprio repositório, com uma recomendação honesta sobre se é possível retirar o melonDS reaproveitando o recompiler atual, quais partes seriam uma reimplementação substancial e qual experimento deve vir primeiro. A interface de uma tela é obrigatória, mas é um requisito de produto separado da escolha do runtime.