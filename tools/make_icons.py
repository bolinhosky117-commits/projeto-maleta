"""
Gera os ícones da maleta (estilo RE4 Remake) a partir das imagens de origem.

Uso (na raiz do projeto):
    pip install -r tools/requirements.txt
    python tools/make_icons.py

Lê:   data/item-sizes.json           (tamanhos, descrições e receitas — edite aqui)
      data/rpg-stats.json            (números do RPG — edite aqui)
      source-images/<categoria>/*.png (fundo preto, branco ou xadrez claro — o script detecta)
Gera: assets/icons/<id>.png  (PNG transparente, cols*cell x rows*cell)
      assets/items.json      (manifesto para o sistema de inventário)
      assets/preview.png     (todos os ícones encaixados numa grade, para conferir)
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "item-sizes.json")
RPG = os.path.join(ROOT, "data", "rpg-stats.json")
SRC = os.path.join(ROOT, "source-images")
OUT = os.path.join(ROOT, "assets")
ESTICA_MAX = 1.2  # quanto um lado pode ser esticado além da proporção original (1 = nunca distorce)


def cutout(img, limite=232):
    """Remove o fundo: flood fill a partir das bordas.
    Detecta sozinho se o fundo é escuro (renders do Evil Resource, fundo preto) ou claro
    (fundo branco, ou o xadrez cinza/branco de "transparência falsa")."""
    if img.mode == "RGBA" and np.asarray(img)[:, :, 3].min() < 255:
        return img  # já tem transparência de verdade
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    lum, low = a.max(axis=2), a.min(axis=2)
    borda = np.concatenate([lum[0], lum[-1], lum[:, 0], lum[:, -1]])
    claro = np.median(borda) > 128
    xadrez = False
    if claro:
        sat = lum - low
        bl = np.concatenate([low[0], low[-1], low[:, 0], low[:, -1]])
        xadrez = np.mean((bl >= 190) & (bl <= 220)) > 0.2   # fundo de "transparência falsa"
        if xadrez:
            cand = (sat <= 14) & ((low >= 235) | ((low >= 190) & (lum <= 220)))
        else:
            cand = (sat <= 20) & (low >= limite)   # branco; 'fundoLimite' no item baixa isso para engolir sombras
    else:
        cand = lum <= 12                           # quase preto
    lab, _ = ndimage.label(cand)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    if claro and xadrez:  # tira restos claros do xadrez e rebarbas finas grudadas no contorno
        bg = bg | ((low >= 150) & (sat <= 20))
        bg = ~ndimage.binary_opening(~bg, structure=np.ones((3, 3)), iterations=2)
    if claro:  # sujeira solta (pontinhos do xadrez/JPEG): fica só o objeto e pedaços grandes
        lab2, n = ndimage.label(~bg)
        if n > 1:
            tam = ndimage.sum(np.ones_like(lab2), lab2, range(1, n + 1))
            manter = np.flatnonzero(tam >= 0.02 * tam.max()) + 1
            bg = bg | ~np.isin(lab2, manter)
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    edge = ndimage.binary_dilation(bg, iterations=1) & ~bg
    if claro:
        alpha[edge] = np.clip((255 - low[edge]) * 255 // 90, 0, 255).astype(np.uint8)
    else:
        alpha[edge] = np.clip(lum[edge] * 255 // 40, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")


def main_axis(im):
    """Ângulo do eixo principal do objeto (PCA na máscara) e o quão alongado ele é."""
    m = np.asarray(im)[:, :, 3] > 128
    ys, xs = np.nonzero(m)
    pts = np.stack([xs - xs.mean(), ys - ys.mean()])
    evals, evecs = np.linalg.eigh(np.cov(pts))
    v = evecs[:, np.argmax(evals)]
    ang = np.degrees(np.arctan2(v[1], v[0]))
    if ang > 90:
        ang -= 180
    if ang <= -90:
        ang += 180
    return ang, evals.max() / max(evals.min(), 1e-6)


def find_source(item_id, category):
    p = os.path.join(SRC, category, f"{item_id}.png")
    return p if os.path.exists(p) else None


def main():
    cfg = json.load(open(DATA, encoding="utf-8"))
    CELL, PAD = cfg["cellSize"], cfg.get("padding", 4)
    rpg = json.load(open(RPG, encoding="utf-8"))["items"] if os.path.exists(RPG) else {}
    os.makedirs(os.path.join(OUT, "icons"), exist_ok=True)

    manifest = []
    for it in cfg["items"]:
        slug, cat = it["id"], it["category"]
        src = find_source(slug, cat)
        if not src:
            print("SEM IMAGEM:", slug)
            continue
        long_c, short_c = it["size"]
        im = cutout(Image.open(src), it.get("fundoLimite", 232))
        ang, elong = main_axis(im)
        rotated = 0.0
        # itens compridos, facas e os marcados com "endireitar" no data/ vêm inclinados na foto: endireita
        if ((long_c / short_c >= 3 or "knife" in slug) and elong > 4 or it.get("endireitar")) and abs(ang) > 3:
            im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
            rotated = round(float(ang), 1)
        im = im.crop(im.getbbox())
        w, h = im.size
        if long_c == short_c:
            cols = rows = long_c
        elif it.get("forceHorizontal") or w >= h:
            cols, rows = long_c, short_c
        else:
            cols, rows = short_c, long_c
        W, H = cols * CELL, rows * CELL
        # preenche o retângulo: encaixa sem distorcer e depois estica cada lado até ESTICA_MAX para tirar as faixas vazias
        s = min((W - 2 * PAD) / w, (H - 2 * PAD) / h)
        nw = min(W - 2 * PAD, w * s * ESTICA_MAX)
        nh = min(H - 2 * PAD, h * s * ESTICA_MAX)
        im = im.resize((max(1, round(nw)), max(1, round(nh))), Image.LANCZOS)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2))
        canvas.save(os.path.join(OUT, "icons", f"{slug}.png"))
        manifest.append({
            "id": slug, "name": it["name"], "file": f"icons/{slug}.png", "category": cat,
            "cols": cols, "rows": rows, "slots": cols * rows,
            "sizeStatus": it.get("status", ""), "rotatedDeg": rotated,
            "description": it.get("description", ""),
            "rpg": rpg.get(slug, {}),
        })

    json.dump({"cellSize": CELL, "items": manifest, "recipes": cfg.get("recipes", [])},
              open(os.path.join(OUT, "items.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    make_preview(manifest, CELL)
    print(len(manifest), "ícones gerados em", OUT)


def make_preview(manifest, CELL, GW=20):
    order = sorted(manifest, key=lambda m: -m["slots"])
    occ = np.zeros((300, GW), bool)
    place = []
    for m in order:
        c, r = m["cols"], m["rows"]
        for y in range(300):
            xs = [x for x in range(GW - c + 1) if not occ[y:y + r, x:x + c].any()]
            if xs:
                occ[y:y + r, xs[0]:xs[0] + c] = True
                place.append((m, xs[0], y))
                break
    GH = max(y + m["rows"] for m, x, y in place)
    sheet = Image.new("RGBA", (GW * CELL, GH * CELL), (22, 22, 24, 255))
    d = ImageDraw.Draw(sheet)
    for x in range(GW + 1):
        d.line([(x * CELL, 0), (x * CELL, GH * CELL)], fill=(55, 55, 60))
    for y in range(GH + 1):
        d.line([(0, y * CELL), (GW * CELL, y * CELL)], fill=(55, 55, 60))
    for m, x, y in place:
        box = [x * CELL, y * CELL, (x + m["cols"]) * CELL - 1, (y + m["rows"]) * CELL - 1]
        d.rectangle(box, fill=(38, 38, 42))
        sheet.alpha_composite(Image.open(os.path.join(OUT, m["file"])), (x * CELL, y * CELL))
        d.rectangle(box, outline=(150, 150, 150))
    sheet.convert("RGB").save(os.path.join(OUT, "preview.png"))


if __name__ == "__main__":
    main()
