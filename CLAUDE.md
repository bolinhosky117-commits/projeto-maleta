# CLAUDE.md — Projeto Maleta

> **Origem:** este projeto foi feito pelo **Ez** (um dos jogadores) e enviado ao mestre do RPG. Nas seções abaixo,
> "o usuário" é o Ez. Se quem está te usando agora é o mestre, trate tudo aqui como **proposta do Ez**:
> pode adaptar, juntar com o site Mesa Sigilosa ou descartar partes. O acerto e o modificador dos anexos são decisão do mestre.

Contexto para o Claude (extensão do VS Code). Responda em português do Brasil.

## Objetivo

Sistema de inventário em grade inspirado na maleta do Resident Evil 4 Remake: itens ocupam retângulos de N×M
quadradinhos, giram em 4 posições e encaixam como Tetris. Feito para o RPG de um grupo de amigos.
O protótipo é HTML/JS puro; a stack do sistema final ainda não foi definida — pergunte antes de escolher uma.

## O que existe

- `assets/icons/*.png` — 55 ícones transparentes, já no tamanho da área do item (`cellSize` = 64px por célula).
  Orientação padrão: armas deitadas (cols ≥ rows); recovery/munição seguem a orientação da foto (ex.: ervas 1×2).
- `assets/items.json` — **a interface para o sistema**: `{ cellSize, items: [{ id, name, file, category, cols, rows, slots,
  sizeStatus, rotatedDeg, description, rpg }], recipes: [{ a, b, result }] }`. Gerado; não editar à mão.
- `data/item-sizes.json` — fonte de verdade dos tamanhos (`size: [maior, menor]`, `forceHorizontal`, `status`),
  das descrições (`description`) e das receitas (`recipes`).
- `data/rpg-stats.json` — números do RPG (dano, pente, recarga, cura, anexos…). Régua: humano tem até 12 PV, SG-09 R = 1d8.
  `precisaoJogo` guarda o Precision do jogo para o mestre converter em acerto. Ver `docs/conversao-rpg.md`.
- `tools/make_icons.py` — regenera `assets/` a partir de `data/` + `source-images/` (Python: pillow, numpy, scipy).
- `prototipo/maleta.src.html` — protótipo (HTML/CSS/JS, sem framework). `python tools/build_prototipo.py` gera
  `prototipo/maleta.html` com o `items.json` e os ícones embutidos. Não edite o `maleta.html` à mão.
- `extras/inventario-mochila-bau/` — pacote anterior do Ez (Catálogo, Armário, Mochila por espaços, Baú). A maleta em grade
  substitui a mochila de lá; o resto da ideia já está no protótipo da maleta.

## Decisões (14/11/2026)

- **Craft só de ervas** (as 7 misturas). Itens sem ícone ficam de fora.
- Rotação: **facas** giram em 4 posições; **o resto** fica deitado ou em pé apontando para baixo (2 posições); itens quadrados não giram.
- Ícones esticados para preencher o retângulo do item, no máximo 20% (`ESTICA_MAX` no `make_icons.py`) para não distorcer demais. `endireitar` no `data/` endireita um item que veio inclinado.
- Munição em balas: caixas com `balas`, armas com `carregado`; Atirar, Recarregar (pega só o que falta) e juntar caixas.
- Organizar testa vários jeitos e fica com o que deixa a área livre com menos cantos (e menos itens em pé).
- **Catálogo** (todos os itens) é só do mestre. **Armário** e **Baú** são objetos que o mestre põe na cena. O mestre define
  quais itens e quantos ficam em cada armário (quantidade ou ∞). O baú é por jogador (cada um só vê os próprios itens) e só
  abre se houver um Baú na cena. Só o mestre muda o tamanho da maleta.
- **Anexos** não fundem nem saem da grade: ficam equipados na arma compatível (`equipadoEm` = uid da arma), com marquinha
  da mesma cor nos dois. 1 mira + 1 coronha por arma. Modificador de acerto: a definir pelo mestre.
- Ervas (proposta do mestre): verde 1 dado de vida, vermelha ½ + tira a dor, amarela ½ + pulso de adrenalina; misturas somam; 3 ervas = vida toda. **Ovos fora.** Spray de primeiros socorros é raro.
- Facas **não quebram** (sem durabilidade).

## Regras

- Não edite nada em `assets/` à mão: altere `data/` ou o script e rode `python tools/make_icons.py`
  (e depois `python tools/build_prototipo.py` para atualizar o protótipo).
- `source-images/` são os originais — não sobrescrever.
- Tamanhos incertos (ver `docs/verificacao-tamanhos.md`): Striker (2x5 vs 2x4), consumíveis sem fonte do remake, Bolts (suposição).
- As imagens são da Capcom; uso só entre os amigos. Se o projeto for publicado, trocar por arte própria.

## Referências do jogo

- Maleta inicial 10×7 (70); expansões 12×7, 12×8, 13×8, até 13×9 (117).
- Print de referência: `docs/referencia-maleta-jogo.png`.
