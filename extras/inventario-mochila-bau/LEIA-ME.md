# Sistema de Inventário: Catálogo, Armário, Mochila e Baú

> **Pacote anterior do Ez.** Foi a primeira ideia de inventário (mochila por número de espaços).
> Na proposta atual, a **maleta em grade** (pasta principal deste projeto) substitui a mochila daqui.
> Catálogo, Armário e Baú continuam valendo e já estão no protótipo da maleta.
> O protótipo deste pacote se chama `inventario.html`.


Pacote independente para levar para outro site de RPG. Tem duas partes:

- **`LEIA-ME.md`** (este arquivo): as regras e como encaixar no site.
- **`inventario.html`**: uma página que funciona sozinha (abre no navegador, sem login e sem banco). Serve para testar a mecânica e como referência de código.

> **Para o Claude que vai ler isto:** este pacote foi feito fora do seu projeto. Não copie o protótipo inteiro para dentro do site. Use as **regras** (seção 2) e o bloco `Regras` do protótipo como especificação, e reconstrua tudo com a tecnologia, o banco, os componentes e o visual que o site já usa. Antes de criar tabelas, veja como o site guarda personagens e usuários hoje e adapte os nomes. Na dúvida sobre uma regra, pergunte ao mestre.

---

## 1. As quatro peças

| Peça | De quem é | O que guarda | Limite |
|---|---|---|---|
| **Catálogo de Itens** | do mestre | A ficha de cada item que existe no jogo: nome, categoria, dano, espaço, descrição e campos extras livres. É o "molde" e não está em lugar nenhum. | nenhum |
| **Armário de armas** | do grupo (um só) | Armas, anexos, munição e explosivos disponíveis para pegar. | estoque por item; pode ser **∞** |
| **Mochila** | de cada personagem | O que ele leva consigo. | **espaços** (padrão 10, o mestre ajusta por personagem) |
| **Baú** | de cada personagem | O que ele guarda e não leva. | sem limite |

Categorias do protótipo: Arma, Anexo, Munição, Explosivo, Consumível, Equipamento. O mestre pode mudar a lista.

## 2. Regras

1. **O mestre cria os itens no Catálogo.** Campos fixos: nome, categoria, dano (opcional, texto livre como `2d6`), espaço por unidade (aceita 0,5) e descrição. Campos extras são pares livres de "campo: valor" (ex.: `Alcance: Curto`, `Pente: 15 tiros`).
2. **Itens do Catálogo só existem no jogo quando o mestre coloca:** no Armário (com quantidade ou ∞), na mochila ou no baú de alguém.
3. **O jogador pega o que quiser do Armário para a mochila, desde que caiba.** Espaço usado = soma de (espaço do item × quantidade) de tudo na mochila. Se passar da capacidade, a ação é recusada e a mensagem diz quanto falta.
4. **O jogador move livremente entre mochila, baú e armário**, sempre só as próprias coisas. Devolver ao Armário um item que lá é ∞ não muda o estoque.
5. **Regra da base (liga e desliga):** com ela ligada, quando o grupo está **em missão** o jogador só mexe na mochila. Armário e baú ficam fechados até o mestre marcar que o grupo voltou à **base**. É isso que dá peso à escolha do que levar.
6. **Consumíveis** têm o botão "Usar", que gasta 1 unidade, e só funcionam se estiverem na mochila.
7. **O mestre pode tudo:** mexer em qualquer inventário (respeitando o espaço da mochila), colocar itens em jogo, descartar itens e excluir do Catálogo (o que tira o item de todos os lugares).
8. **Tudo vai para um histórico** (quem, o quê, de onde para onde), visível para o mestre.

### Decisões tomadas no protótipo (o mestre pode mudar)
- Espaço é por unidade, sem peso separado.
- O baú não tem limite.
- O estoque infinito só existe no Armário.
- Anexos são itens comuns: ainda não "encaixam" numa arma.

## 3. Quem pode o quê

| Ação | Jogador | Mestre |
|---|---|---|
| Ver o Catálogo inteiro / criar e editar itens | não | sim |
| Ver o Armário | sim (se aberto) | sim |
| Mover itens das próprias coisas | sim | sim, de qualquer um |
| Abrir armário e baú em missão | não (com a regra da base ligada) | sim |
| Usar consumível | o próprio | qualquer um |
| Colocar em jogo / descartar / excluir | não | sim |
| Ligar "na base / em missão" | não | sim |

## 4. Modelo de dados (sugestão para Supabase/Postgres)

Os nomes são sugestão. **Adapte à tabela de personagens que o site já tem.**

```sql
-- Catálogo
create table itens (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  categoria text not null,
  dano text,
  espaco numeric(5,1) not null default 1 check (espaco >= 0),
  descricao text,
  extras jsonb not null default '[]',   -- [{ "campo": "Alcance", "valor": "Curto" }]
  criado_em timestamptz not null default now()
);

-- Armário do grupo (qtd null = infinito)
create table armario (
  item_id uuid primary key references itens(id) on delete cascade,
  qtd int check (qtd is null or qtd > 0)
);

-- Capacidade da mochila fica no personagem
alter table personagens add column capacidade_mochila numeric(5,1) not null default 10;

-- Mochila e baú de cada personagem
create table inventario (
  personagem_id uuid not null references personagens(id) on delete cascade,
  local text not null check (local in ('mochila', 'bau')),
  item_id uuid not null references itens(id) on delete cascade,
  qtd int not null check (qtd > 0),
  primary key (personagem_id, local, item_id)
);

-- Estado da mesa (uma linha só)
create table inventario_config (
  id int primary key default 1 check (id = 1),
  acesso_so_na_base boolean not null default true,
  grupo_na_base boolean not null default true
);

-- Histórico
create table inventario_historico (
  id bigint generated always as identity primary key,
  quando timestamptz not null default now(),
  autor text not null,
  texto text not null
);
```

### Ponto importante: mover tem que ser uma operação só no servidor
Dois jogadores podem clicar ao mesmo tempo na última pistola. Por isso, **mover, usar e colocar em jogo devem ser uma função no banco** (ex.: `mover_item(item, de, para, qtd)` via `rpc`) que, dentro de uma única transação:

1. confere se quem chamou é o dono do personagem ou o mestre;
2. confere a regra da base;
3. trava a linha de origem (`select ... for update`) e confere a quantidade;
4. se o destino for a mochila, soma o espaço e confere a capacidade;
5. tira de um lado, põe no outro (`insert ... on conflict do update`) e apaga linhas que zerarem;
6. grava no histórico.

O navegador nunca escreve direto nas tabelas `armario` e `inventario`. Com RLS: o jogador **lê** só o próprio inventário e o armário, o mestre lê tudo, e as escritas passam só pelas funções.

Se o site tiver tempo real (Supabase Realtime), vale assinar `armario` e `inventario` para todo mundo ver o estoque mudar na hora.

## 5. Como o protótipo está organizado

O `<script>` do `inventario.html` tem três partes, marcadas com comentários:

1. **PARTE 1, REGRAS:** o objeto `Regras` com `mover`, `usar`, `descartar`, `colocarEmJogo`, `excluirDoCatalogo`, `espacoUsado` e `temAcesso`. Cada função devolve `{ ok: true }` ou `{ erro: "mensagem para o jogador" }`. **É a especificação viva:** no site real, essa lógica vira as funções do banco da seção 4.
2. **PARTE 2, DADOS:** os dados de exemplo e o salvamento no navegador (só para o protótipo).
3. **PARTE 3, TELA:** desenha as telas e chama as Regras. Pode ser refeita do zero no estilo do site.

No protótipo, o seletor "Ver como" no topo troca entre Mestre e cada jogador, para testar os dois lados.

## 6. Ideias para depois (fora deste pacote)
- Anexos que encaixam numa arma específica (mira, silenciador) e mudam os números dela.
- Munição gasta tiro a tiro, ligada à arma.
- Itens que aumentam a mochila (colete com bolsos, mochila maior).
- Passar item direto de um jogador para outro em missão.
- Baú com limite, ou baú do grupo além do pessoal.
