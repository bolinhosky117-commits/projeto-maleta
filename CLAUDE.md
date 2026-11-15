# CLAUDE.md — Projeto Maleta

> **Origem:** este projeto foi feito pelo **Ez** (um dos jogadores) e enviado ao mestre do RPG. Nas seções abaixo,
> "o usuário" é o Ez. Se quem está te usando agora é o mestre, trate tudo aqui como **proposta do Ez**:
> pode adaptar, juntar com o site Mesa Sigilosa ou descartar partes. O acerto e o modificador dos anexos são decisão do mestre.

Contexto para o Claude (extensão do VS Code). Responda em português do Brasil.

## Objetivo

Sistema de inventário em grade inspirado na maleta do Resident Evil 4 Remake: itens ocupam retângulos de N×M
quadradinhos, giram (facas em 4 posições, o resto deitado ou em pé) e encaixam como Tetris. Feito para o RPG de um grupo de amigos.
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
- **Sons**: `source-sounds/` (originais, não mexer): `wep/` (armas, RE4 2005), `maleta/` (Attache Case & UI, RE4 Ultimate HD),
  `itens/` (Pickup and Radio, RE4 UHD), `zeebo/` (faca e granadas, RE4 Zeebo Edition) — todos do The Sounds Resource.
  `data/sons.json` (`armas`: atirar/recarregar/vazio/atacar e `cadencia` da rajada, com a tabela wepNN → arma; `tipos`: faca, granada, cura;
  `maleta`: pegar, soltar, girar, bloqueado, equipar, descartar, misturar, juntar, bau),
  `python tools/make_sounds.py` gera `assets/sounds/*.ogg` (junta os pares L/R em estéreo, corta o silêncio inicial; precisa do ffmpeg).
  O `build_prototipo.py` embute os sons. No protótipo: Atirar toca o tiro (repetido na rajada), Recarregar toca a recarga, sem bala faz o clique vazio; botão "Som" e o controle de Volume no topo (padrão 50%). O volume de cada tipo de som é igualado no make_sounds.py (`ALVO_DB`: tiro mais alto, recarga e clique vazio mais baixos).
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
  abre se houver um Baú na cena. Só o mestre muda o tamanho da maleta. O mestre apaga um item arrastando-o da maleta/baú para o Catálogo.
- **Anexos** não fundem nem saem da grade: ficam equipados na arma compatível (`equipadoEm` = uid da arma), com marquinha
  da mesma cor nos dois. 1 mira + 1 coronha por arma. Modificador de acerto: a definir pelo mestre.
- Ervas (proposta do mestre; "dado de vida" = o dado de cura do personagem, `dadoVida` por jogador no protótipo): verde 1 dado de vida, vermelha ½ + tira a dor, amarela ½ + pulso de adrenalina; misturas somam; 3 ervas = vida toda. **Ovos fora.** Spray de primeiros socorros é raro.
- Facas **não quebram** (sem durabilidade).
- O **baú** é uma lista no painel da direita (a versão em grade embaixo da maleta foi testada e descartada). Arrasta-se entre maleta e baú; Shift + clique troca o item de lugar. Girar só com R (ou botão direito durante o arrasto); a rodinha do mouse não gira.
- 15/11: em tela larga a página não rola: cada coluna (catálogo, maleta, painel da direita com o baú) rola sozinha e a maleta fica sempre no lugar, encolhendo as células para caber na altura (`medirC`).
- 15/11: clique esquerdo num item abre os detalhes no painel da direita; botão direito abre um menu de contexto com todas as ações do item (`acoesDe()` alimenta os dois).
- 15/11: itens com muito espaço vazio foram ajustados ao desenho (CQBR, LE 5, Killer7, Scope e Biosensor Scope (2×1) diminuíram; Shotgun Shells ficou 2×1 com `esticaMax` 1.4 (desenho esticado um pouco mais que o padrão); SR M1903 virou 8×2 e Skull Shaker 5×2, com 2 linhas, para continuarem parecendo armas grandes). O tamanho do jogo fica em `tamanhoJogo`. Ver `docs/verificacao-tamanhos.md`.

## Regras

- Não edite nada em `assets/` à mão: altere `data/` ou o script e rode `python tools/make_icons.py`
  (e depois `python tools/build_prototipo.py` para atualizar o protótipo).
- `source-images/` são os originais — não sobrescrever.
  Exceção: `recovery/red-herb.png` é a erva verde recolorida de vermelho (mesmo modelo das três ervas); a foto original ficou em `source-images/recovery/_original/`.
  `weaponry/biosensor-scope.png` foi trocada por uma foto melhor mandada pelo Ez (fundo branco, `fundoLimite` 120); a antiga ficou em `source-images/weaponry/_original/`.
- Tamanhos incertos (ver `docs/verificacao-tamanhos.md`): Striker (2x5 vs 2x4), consumíveis sem fonte do remake, Bolts (suposição).
- As imagens e os sons são da Capcom; uso só entre os amigos. Se o projeto for publicado, trocar por arte própria.

## Referências do jogo

- Maleta inicial 10×7 (70); expansões 12×7, 12×8, 13×8, até 13×9 (117).
- Print de referência: `docs/referencia-maleta-jogo.png`.
