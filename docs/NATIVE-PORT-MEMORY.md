# Memória do projeto: Pokémon SoulSilver nativo no Nintendo Switch

Atualizado em 2026-11-01.

## Repositório e objetivo

- Fork de trabalho: https://github.com/GodPromettheus/hgss-sw
- Base do fork: https://github.com/sasantos/pokemon-ds-widescreen-switch
- Recompilador de referência: https://github.com/ClickingMaster/ssrecomp
- Jogo inicial de interesse: Pokémon SoulSilver (Nintendo DS), com HeartGold como possível extensão.
- Meta: investigar uma versão homebrew para Nintendo Switch, jogável em uma única tela, que não dependa do núcleo emulador melonDS e reaproveite o máximo possível do trabalho de recompilação existente.

## Estado atual verificado no código

O projeto-base já compila um aplicativo homebrew para Switch e rearranja a interface de DS para uma tela widescreen. Esse executável ainda inclui o melonDS: o README descreve o jogo como executado no núcleo melonDS embutido e esclarece que não se trata de um port nativo do jogo.

O recompilador estático converte instruções ARM do jogo para C++, mas o código gerado ainda participa do runtime do melonDS. Os arquivos de runtime usam tipos como `melonDS::ARMv5`, estado de CPU, memória emulada, despachante de blocos e fallback para o interpretador. O CMake também adiciona o subprojeto `melonDS` e descreve esse núcleo como o runtime do hardware de DS.

Conclusão técnica provisória: recompilar instruções para código hospedeiro elimina parte da interpretação de CPU, mas não elimina por si só a emulação do hardware de DS. Um port realmente nativo exigiria substituir ou reescrever as dependências de hardware e de runtime; isso pode se aproximar de reimplementar uma camada substancial de emulação, ou de portar o jogo a partir de uma decompilação. A possibilidade, o custo e a cobertura ainda precisam ser demonstrados no código antes de escolher uma arquitetura.

## Fontes principais

- README do projeto Switch: https://github.com/sasantos/pokemon-ds-widescreen-switch/blob/main/README.md
- Regras para agentes e mapa do código: https://github.com/sasantos/pokemon-ds-widescreen-switch/blob/main/AGENTS.md
- Integração do melonDS no build: https://github.com/sasantos/pokemon-ds-widescreen-switch/blob/main/CMakeLists.txt
- Runtime de recompilação: https://github.com/sasantos/pokemon-ds-widescreen-switch/blob/main/runtime/recomp_rt.h
- Macros usadas pelo código recompilado: https://github.com/sasantos/pokemon-ds-widescreen-switch/blob/main/runtime/recomp_gen.h
- Recompilador de origem e documentação: https://github.com/ClickingMaster/ssrecomp

## Regras de trabalho

1. Começar com análise de arquitetura e um protótipo pequeno; não iniciar uma reescrita integral antes de provar o caminho.
2. Preservar o app atual baseado em melonDS como referência funcional até que uma alternativa nativa execute uma fatia verificável do jogo.
3. Não enviar, adicionar ou publicar ROMs, código gerado a partir da ROM (`gen/`), dumps, saves, save states, binários do jogo ou assets proprietários. O usuário pode usar uma cópia própria localmente.
4. Não afirmar que o port é nativo só porque o executável é um `.nro` ou porque instruções ARM foram recompiladas.
5. Preservar licenças, avisos de copyright e atribuições existentes; revisar compatibilidade antes de reutilizar componentes de outros projetos.
6. Tratar a interface de uma tela como requisito independente do runtime: reutilizar layouts existentes quando isso for compatível, mas não confundir a composição visual com a remoção do emulador.
7. Registrar medições, limitações e decisões com links para código e resultados reproduzíveis.

## Próxima etapa recomendada

Produzir um inventário de dependências do código gerado e do gameplay: CPU, memória/bus, interrupções, temporizadores, vídeo 2D/3D, áudio, DMA, cartucho, entrada, save e sistema operacional. Para cada dependência, indicar se pode ser abstraída, precisa de uma implementação Switch própria ou requer manter um componente emulador. Depois propor um vertical slice pequeno com critérios de sucesso e custo estimado.