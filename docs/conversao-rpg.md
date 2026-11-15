# Conversão dos itens para o RPG (rascunho do Ez com ajustes do mestre, 14/11/2026)

Proposta do Ez para levar os itens da maleta para o RPG do amigo. Os números ficam em `data/rpg-stats.json` e entram no `assets/items.json` (campo `rpg`) quando se roda `python tools/make_icons.py`.

## A régua
- Um humano tem **até 12 de vida**.
- A pistola inicial (**SG-09 R**) causa **1d8** (mínimo 1, máximo 8).
- As outras armas foram escaladas pelo **Power** do jogo com todas as melhorias, comprimido (raiz quadrada) para não explodir: uma arma 4× mais forte que a SG-09 R causa cerca do dobro do dano, não o quádruplo.
- O **acerto fica com o mestre**. Cada arma guarda `precisaoJogo` (o Precision do jogo, de 1,8 a 5,4) para ele converter no sistema dele.

## Dano das armas

| Arma | Dano | Mín–máx | Chance de derrubar 12 PV num golpe |
|---|---|---|---|
| Kitchen Knife, Boot Knife | 1d4 | 1–4 | 0% |
| Combat Knife, Primal Knife | 1d6 | 1–6 | 0% |
| Fighting Knife, Bolt Thrower | 1d8 | 1–8 | 0% |
| Punisher | 1d6 | 1–6 | 0% |
| SG-09 R, Sentinel Nine | 1d8 | 1–8 | 0% |
| Blacktail | 1d8+1 | 2–9 | 0% |
| Red9 | 1d10 | 1–10 | 0% |
| TMP (rajada) | 2d4 | 2–8 | 0% |
| Matilda, LE 5, Chicago Sweeper, CQBR (rajada) | 2d6 | 2–12 | 3% |
| Stingray, Skull Shaker | 2d6 | 2–12 | 3% |
| SR M1903, W-870, Striker | 2d8 | 2–16 | 23% |
| Riot Gun | 2d10 | 2–20 | 45% |
| Granada de mão, mina da besta | 3d6 | 3–18 | 38% |
| Broken Butterfly, Killer7 | 2d12 | 2–24 | 62% |
| Granada pesada | 4d6 | 4–24 | 76% |
| Handcannon | 3d10 | 3–30 | 84% |
| Lança-foguetes | 6d10 | 6–60 | 100% |

## Regras que os números supõem
- **Rajada** (Matilda, submetralhadoras, CQBR): um ataque gasta 1 do pente (várias balas) e o dano da tabela já é o da rajada.
- **Pente**: quantos disparos (ou rajadas) antes de recarregar. **Recarga** rápida, normal ou lenta vem do Reload Speed do jogo; o mestre decide quanto cada uma custa em ação.
- **Munição em balas**: cada caixa guarda balas (pistola 15, espingarda 8, submetralhadora 50, rifle 5, magnum 6, virotes 5).
  A arma guarda quantas balas tem carregadas (pente × balas por rajada). **Atirar** gasta 1 tiro (ou 1 rajada);
  **Recarregar** puxa só as balas que faltam, começando pelas caixas mais vazias. Caixas do mesmo tipo se juntam soltando uma na outra.
  Virotes: depois do combate, recupera metade dos disparados.
- **Perfurante**: o tiro pode acertar também quem está logo atrás, na mesma linha.
- **Espalha** (espingardas): dano cheio de perto, metade a média distância.
- **Crítico ampliado** (SG-09 R, Sentinel Nine, Killer7): critica mais fácil que as outras armas.
- **Facas**: não quebram no RPG (não há mecânica de durabilidade).

## Anexos
- Não se fundem com a arma: continuam ocupando o lugar deles na maleta e ficam **equipados** nela. A arma e o anexo ganham uma marquinha da mesma cor no canto (cada dupla com uma cor).
- Guardar a arma no baú leva junto os anexos equipados; ao voltar para a maleta, eles voltam equipados.
- Só encaixam nas armas feitas para eles (`encaixa` em `data/rpg-stats.json`). Cada arma aceita **1 mira e 1 coronha**.
- O efeito em regra (modificador de acerto) fica **a definir pelo mestre**. `efeitoNoJogo` mostra o que o anexo faz no RE4.

| Anexo | Encaixa em | No jogo |
|---|---|---|
| Laser Sight | SG-09 R, Punisher, Sentinel Nine | Precision +0,5 |
| Scope, High Power Scope, Biosensor Scope | LE 5, SR M1903, Stingray, CQBR | zoom; o Biosensor revela parasitas |
| Red9 Stock | Red9 | Precision 3,0 → 4,8 |
| Matilda Stock | Matilda | Precision 3,5 → 4,6 |
| TMP Stock | TMP | Precision 2,0 → 3,5 |

## Cura (proposta do mestre)

A cura usa o **dado de vida** do sistema do mestre (ou 10 PV, se preferir um número fixo).
Cada erva soma: **verde = 1 dado de vida**, **vermelha = ½ dado + tira a dor**, **amarela = ½ dado + pulso de adrenalina**.
Mistura de 3 ervas cura a vida toda e mantém os efeitos das ervas que tem.

| Item | Cura | Efeitos |
|---|---|---|
| Erva verde | 1 dado de vida | |
| Erva vermelha | ½ dado de vida | tira a dor (remove desvantagens por dor) |
| Erva amarela | ½ dado de vida | pulso de adrenalina |
| Verde + verde | 2 dados de vida | |
| Verde + vermelha | 1½ dado de vida | tira a dor |
| Verde + amarela | 1½ dado de vida | pulso de adrenalina |
| Vermelha + amarela | 1 dado de vida | tira a dor + adrenalina |
| Verde + verde + verde | vida toda | |
| Verde + verde + amarela | vida toda | adrenalina |
| Verde + vermelha + amarela | vida toda | tira a dor + adrenalina |
| Spray de primeiros socorros | vida toda | **raro**: o mestre põe pouco no armário |

Os ovos saíram do jogo.

## Craft
Só as misturas de ervas (lista em `recipes`, no `data/item-sizes.json`).

## Fontes dos números do jogo
- Stats máximos de todas as armas: https://steamcommunity.com/sharedfiles/filedetails/?id=2959791533
- Power base das armas: https://game8.co/games/Resident-Evil-4-Remake/archives/408811
- Itens de cura: https://game8.co/games/Resident-Evil-4-Remake/archives/408061 e https://gameluster.com/?p=78444
