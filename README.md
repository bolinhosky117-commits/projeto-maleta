# Projeto Maleta

> **Este projeto foi feito pelo Ez** (com a ajuda do Claude dele) e enviado para o mestre do RPG.
> Não é uma parte do site Mesa Sigilosa: é uma ideia do Ez, entregue para o mestre avaliar e adaptar como quiser.
>
> - **Para ver funcionando:** abra `prototipo/maleta.html` com dois cliques.
> - **A ideia:** a maleta em grade (estilo Resident Evil 4) substitui a "mochila" do pacote de inventário anterior do Ez
>   (está junto, em `extras/inventario-mochila-bau/`). O Catálogo, o Armário e o Baú daquele pacote continuam valendo,
>   e já estão neste protótipo também.
> - **Números do RPG** (dano, cura, pente…): são uma proposta do Ez, em `docs/conversao-rpg.md`.
>   O **acerto** e o **modificador dos anexos** ficaram para o mestre decidir.
> - **Imagens:** os ícones são renders da Capcom (RE4 Remake), só para uso entre os amigos. Se o site for aberto ao público, trocar por arte própria.

Sistema de inventário em grade no estilo da maleta (attaché case) do Resident Evil 4 Remake.

## O que já está pronto

- **55 ícones** em `assets/icons/` (44 armas/peças/munição + 11 itens de cura), PNG com fundo transparente,
  cada um no tamanho exato da área que ocupa na grade (64px por quadradinho; ex.: pistola 3x2 → 192x128).
- **`assets/items.json`**: tudo de cada item num arquivo só: `id`, `name`, `file`, `category`, `cols`, `rows`, `slots`,
  `description` e `rpg` (dano, pente, cura, anexos…), mais as `recipes` (misturas de ervas). É o arquivo que o sistema deve ler.
- **`prototipo/maleta.html`**: a maleta funcionando (ver abaixo).
- **`assets/preview.png`**: todos os ícones encaixados numa grade, para conferir visualmente.

## Protótipo da maleta

Abra `prototipo/maleta.html` com dois cliques (não precisa de servidor). No topo, **Ver como** troca entre Mestre e cada jogador.

- **Mestre:** vê o **Catálogo** com todos os itens. O **+** de cada item põe 1 no armário aberto; a seta dá o item direto para a maleta
  do jogador escolhido em "Maleta de". No painel **Cena**, coloca e tira objetos: **Armários** (com estoque que ele define: −, +, ∞, ✕)
  e o **Baú**. Também é o único que muda o tamanho da maleta.
- **Jogador:** vê só a própria maleta e o que está **na cena**. Pega itens do armário (arrastando ou no +), devolve arrastando de volta.
  O baú é de cada jogador (só os itens dele) e só abre se o mestre tiver posto um Baú na cena. Ele aparece como uma
  **segunda grade logo abaixo da maleta** (mesma largura, cresce conforme enche): arraste itens direto entre as duas.
- **Dado de vida** (o dado de cura do personagem): o mestre escolhe por jogador no topo; as ervas rolam esse dado ao usar.
- **Botão direito** num item (na maleta, no armário, no catálogo ou no baú) abre os detalhes; o clique esquerdo só seleciona.
- **Enter** com uma cura selecionada usa o item (o botão Usar também fica nos detalhes do botão direito).
- **Delete** no teclado com um item selecionado abre uma janela: "Mover para o baú" ou "Deletar" (Esc cancela).
- Na maleta: arrastar, girar (R ou botão direito durante o arrasto; facas em 4 posições, o resto deitado ou em pé), misturar ervas, equipar anexos,
  atirar e recarregar (munição contada em balas; juntar caixas soltando uma na outra), usar itens e organizar.

O código fica em `prototipo/maleta.src.html`; depois de mexer nele ou nos itens, rode `python tools/build_prototipo.py`
(ele embute o `items.json` e os ícones e gera o `maleta.html`).

## Estrutura

```
assets/            saída gerada (ícones, manifesto, preview) — não editar à mão
data/item-sizes.json   FONTE DE VERDADE dos tamanhos, descrições e receitas — edite aqui
data/rpg-stats.json    números do RPG (dano, pente, cura) — edite aqui
source-images/     imagens originais (fundo preto, branco ou xadrez) — só servem para gerar os ícones de novo
  weaponry/        44 itens da página Weaponry
  recovery/        14 itens da seção Recovery items
prototipo/
  maleta.src.html   código do protótipo — edite aqui
  maleta.html       protótipo pronto (gerado) — não editar à mão
tools/
  build_prototipo.py       gera prototipo/maleta.html
  make_icons.py            gera assets/ a partir de data/ + source-images/
  download_evilresource.js script de navegador para baixar mais imagens do site
  requirements.txt
extras/
  inventario-mochila-bau/  pacote anterior do Ez (regras do Catálogo, Armário, Mochila e Baú + protótipo simples)
docs/
  verificacao-tamanhos.md  o que foi conferido/corrigido e com quais fontes
  conversao-rpg.md         como os itens viraram números de RPG
  lista-original-deepseek.md   lista original de tamanhos
  referencia-maleta-jogo.png   print da maleta no jogo (referência visual)
```

## Como regenerar os ícones

```bash
pip install -r tools/requirements.txt
python tools/make_icons.py
```

Para mudar o tamanho de um item, edite `size` em `data/item-sizes.json` (`[lado maior, lado menor]`) e rode de novo.
Para mudar o tamanho do quadradinho, edite `cellSize` no mesmo arquivo.

## Como adicionar itens novos

1. Abra a página de listagem no Evil Resource, rode `tools/download_evilresource.js` no console do navegador (instruções no arquivo).
2. Coloque os PNGs em `source-images/<categoria>/` (o nome do arquivo deve ser o `id`).
3. Adicione o item em `data/item-sizes.json` e rode `python tools/make_icons.py`.

## Próximos passos

- **Mestre:** decidir como fica o acerto de cada arma (`precisaoJogo` ajuda), o modificador de cada anexo e o que o "pulso de adrenalina" faz nas regras dele.
- **Levar para o site:** guardar maleta, baú e armários no banco; cada jogador vê só a própria tela; mestre controla a cena.
- Conferir no jogo os tamanhos marcados como incertos (ver `docs/verificacao-tamanhos.md`): Striker, consumíveis e Bolts.
