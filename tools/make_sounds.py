"""
Prepara os sons das armas para o protótipo.

Uso (na raiz do projeto):
    python tools/make_sounds.py

Lê:   data/sons.json + source-sounds/wep/*.ogg (originais, não mexer)
Gera: assets/sounds/<nome>.ogg  — pares "-L"/"-R" (ou ".L"/".R") viram um arquivo estéreo,
      o silêncio do começo é cortado (para o tiro não sair atrasado) e o volume é igualado.
Precisa do ffmpeg instalado.
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-sounds", "wep")
OUT = os.path.join(ROOT, "assets", "sounds")

# corta o silêncio inicial e iguala o pico em -1 dB
FILTRO = "silenceremove=start_periods=1:start_threshold=-50dB,dynaudnorm=f=500:g=31:p=0.89"


def nomes_usados(cfg):
    usados = set(cfg.get("padrao", {}).values())
    for sons in cfg["armas"].values():
        usados.update(v for k, v in sons.items() if isinstance(v, str))
    return sorted(usados)


def fontes(nome):
    for e, d in (("-L", "-R"), (".L", ".R")):
        l, r = os.path.join(SRC, nome + e + ".ogg"), os.path.join(SRC, nome + d + ".ogg")
        if os.path.exists(l) and os.path.exists(r):
            return [l, r]
    p = os.path.join(SRC, nome + ".ogg")
    return [p] if os.path.exists(p) else []


def main():
    cfg = json.load(open(os.path.join(ROOT, "data", "sons.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".ogg"):
            os.remove(os.path.join(OUT, f))
    for nome in nomes_usados(cfg):
        src = fontes(nome)
        if not src:
            print("SEM ARQUIVO:", nome)
            continue
        cmd = ["ffmpeg", "-v", "error", "-y"]
        for s in src:
            cmd += ["-i", s]
        filtro = ("[0:a][1:a]amerge=inputs=2," if len(src) == 2 else "") + FILTRO
        cmd += ["-filter_complex", filtro, "-c:a", "libvorbis", "-q:a", "3", os.path.join(OUT, nome + ".ogg")]
        subprocess.run(cmd, check=True)
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"{len(os.listdir(OUT))} sons em assets/sounds ({total // 1024} KB)")


if __name__ == "__main__":
    main()
