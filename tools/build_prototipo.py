"""
Monta o protótipo da maleta num arquivo único, que abre com dois cliques (sem servidor).

Uso (na raiz do projeto, depois de rodar make_icons.py):
    python tools/build_prototipo.py

Lê:   prototipo/maleta.src.html  (código da página — edite aqui)
      assets/items.json + assets/icons/*.png
      data/sons.json + assets/sounds/*.ogg (gerados por tools/make_sounds.py)
Gera: prototipo/maleta.html      (página pronta, com ícones embutidos — não editar à mão)
"""
import base64
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
SRC = os.path.join(ROOT, "prototipo", "maleta.src.html")
OUT = os.path.join(ROOT, "prototipo", "maleta.html")


def main():
    data = json.load(open(os.path.join(ASSETS, "items.json"), encoding="utf-8"))
    for it in data["items"]:
        raw = open(os.path.join(ASSETS, it["file"]), "rb").read()
        it["icon"] = "data:image/png;base64," + base64.b64encode(raw).decode()
    # sons das armas (tools/make_sounds.py gera assets/sounds a partir de data/sons.json)
    mapa = json.load(open(os.path.join(ROOT, "data", "sons.json"), encoding="utf-8"))
    pasta = os.path.join(ASSETS, "sounds")
    arquivos = {}
    if os.path.isdir(pasta):
        for f in sorted(os.listdir(pasta)):
            if f.endswith(".ogg"):
                raw = open(os.path.join(pasta, f), "rb").read()
                arquivos[f[:-4]] = "data:audio/ogg;base64," + base64.b64encode(raw).decode()
    data["sons"] = {"mapa": {"padrao": mapa.get("padrao", {}), "armas": mapa["armas"]}, "arquivos": arquivos}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = open(SRC, encoding="utf-8").read().replace("__DADOS__", payload)
    open(OUT, "w", encoding="utf-8").write(html)
    print("Protótipo gerado:", OUT, f"({os.path.getsize(OUT) // 1024} KB)")


if __name__ == "__main__":
    main()
