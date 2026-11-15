# Verificação dos tamanhos (14/11/2026)

A lista original (`lista-original-deepseek.md`) foi gerada pelo DeepSeek e foi conferida com guias do RE4 Remake.
Os valores finais em uso estão em `data/item-sizes.json` (campo `status` de cada item).

## Corrigidos

| Item | Lista original | Valor usado | Fontes |
|---|---|---|---|
| LE 5 | 2x3 | **2x6** | Game8 ("12 (6x2)"), NamuWiki |
| Fighting Knife | 1x3 | **1x4** | GamertagMythras ("4 (1x4)"), NamuWiki |
| Kitchen Knife | 1x3 | **1x2** | Game8 ("2 (1x2)"), NamuWiki, Sportskeeda |
| Boot Knife | 1x3 | **1x2** | Game8 ("2 (1x2)"), NamuWiki, Sportskeeda |

## Em disputa

- **Striker**: usando **2x5**. NamuWiki diz 2x5; Sportskeeda e GamertagMythras dizem 10 slots; Game8 diz 8 (2x4).

## Confirmados (batem com a lista)

Todas as pistolas (SG-09 R, Punisher, Red9, Matilda, Sentinel Nine 2x3; Blacktail 2x2), magnums (Broken Butterfly e Killer7 2x3; Handcannon 2x4),
espingardas (W-870 e Riot Gun 2x8; Skull Shaker 1x5), rifles (SR M1903 1x9; Stingray e CQBR 2x7), TMP 2x3, Chicago Sweeper 3x7,
Bolt Thrower 2x4, Rocket Launcher e Rocket Launcher (Special) 2x8, Combat e Primal Knife 1x3, Hand Grenade 1x1, Flash/Heavy Grenade 1x2,
Laser Sight 1x1, Scope 1x2, High-Power Scope 1x3, Biosensor Scope 2x2, Red9 Stock 1x4, Matilda Stock 1x3, TMP Stock 2x3.

## Sem fonte do remake (mantido da lista)

Ervas (simples e misturadas), First Aid Spray, ovos, todas as munições e Attachable Mines.
O print `referencia-maleta-jogo.png` é consistente com erva e munição ocupando 2 quadradinhos.

## Suposição

- **Bolts**: não estava na lista; assumido **2x1** igual às outras munições.

## Fontes

- Game8 — páginas de cada arma do RE4 Remake (campo "Inventory Slots"): https://game8.co/games/Resident-Evil-4-Remake
- NamuWiki — Resident Evil RE:4 / Weapons and Equipment: https://en.namu.wiki/w/바이오하자드%20RE:4/무기%20및%20장비
- GamertagMythras — RE4 Remake Best Knife: https://gamertagmythras.com/blog/resident-evil-4/resident-evil-4-remake-best-knife
- Sportskeeda — Striker / Boot Knife: https://sportskeeda.com/esports/how-get-striker-resident-evil-4-remake
- Imagens de origem: Evil Resource — https://www.evilresource.com/resident-evil-4-remake/weaponry e /items

## Ajustes feitos para economizar espaço (15/11/2026)

O desenho de alguns itens é bem mais curto que o retângulo que eles ocupavam no jogo, e sobrava muito espaço vazio na maleta.
Esses itens foram diminuídos para o tamanho do desenho. O tamanho original fica guardado em `tamanhoJogo` no `data/item-sizes.json`,
caso queiram voltar.

| Item | Antes (jogo) | Agora |
|---|---|---|
| SR M1903 | 9×1 | 8×2 (era 4×1; ganhou 2 linhas para parecer arma longa) |
| CQBR Assault Rifle | 7×2 | 5×2 |
| LE 5 | 6×2 | 4×2 |
| Skull Shaker | 5×1 | 5×2 (era 3×1; ganhou 2 linhas para parecer espingarda) |
| Killer7 | 3×2 | 2×2 |
| Scope | 2×1 | 1×1 |
| Shotgun Shells | 2×1 | 2×1 (voltou ao padrão das munições; o desenho mostra duas caixas lado a lado) |

Também foram endireitados (estavam inclinados na foto): as três granadas, os virotes e os frascos de erva misturada.

Obs.: com 1 linha só, o desenho dessas armas ficava pequeno e elas não pareciam grandes. Com 2 linhas o desenho cabe inteiro
e a arma ocupa um espaço coerente com o tamanho dela (perto das espingardas e do Stingray).
