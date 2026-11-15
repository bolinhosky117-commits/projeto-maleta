"""
Prepara os sons das armas para o protótipo.

Uso (na raiz do projeto):
    python tools/make_sounds.py

Lê:   data/sons.json + source-sounds/<pasta>/*.ogg|wav (originais, não mexer)
Gera: assets/sounds/<pasta>__<nome>.ogg  — pares "-L"/"-R" (ou ".L"/".R") viram um arquivo estéreo,
      o silêncio do começo é cortado (para o tiro não sair atrasado) e o volume é igualado por tipo
      (ALVO_DB: tiros iguais entre si; recarga e clique vazio mais baixos).
Precisa do ffmpeg instalado.
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-sounds")
OUT = os.path.join(ROOT, "assets", "sounds")

import numpy as np

# corta o silêncio inicial
FILTRO = "silenceremove=start_periods=1:start_threshold=-50dB"
# volume de cada tipo de som: o trecho mais forte (janela de 50 ms) fica neste nível, em dB.
# Assim todos os tiros soam parecidos entre si, e a recarga e o clique vazio ficam abaixo do tiro.
ALVO_DB = {"atirar": -16.0, "atacar": -16.0, "recarregar": -24.0, "vazio": -26.0, "usar": -24.0, "maleta": -27.0, "tique": -32.0}
TETO_DB = -3.0   # nenhum pico passa disto (evita estourar)


def tabelas(cfg):
    """Todas as tabelas {acao: nome} do sons.json."""
    return list(cfg["armas"].values()) + list(cfg.get("tipos", {}).values()) + [cfg.get("padrao", {})]


def tipo_de(nome, cfg):
    m = cfg.get("maleta", {})
    if nome == m.get("deslocar"):
        return "tique"
    if nome in m.values():
        return "maleta"
    for sons in tabelas(cfg):
        for acao, v in sons.items():
            if v == nome and acao in ALVO_DB:
                return acao
    return "recarregar"


def ganho_db(arquivo, alvo):
    """Lê o som e calcula quanto subir/baixar para o trecho mais forte ficar no alvo."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", arquivo, "-ac", "1", "-ar", "32000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    if not len(x):
        return 0.0
    w = 1600  # 50 ms
    pot = np.convolve(x.astype(np.float64) ** 2, np.ones(w) / w, mode="valid") if len(x) > w else np.array([np.mean(x ** 2)])
    forte = 10 * np.log10(max(pot.max(), 1e-12))
    pico = 20 * np.log10(max(np.abs(x).max(), 1e-9))
    return min(alvo - forte, TETO_DB - pico)


def nomes_usados(cfg):
    usados = set(cfg.get("maleta", {}).values())
    for sons in tabelas(cfg):
        usados.update(v for k, v in sons.items() if isinstance(v, str))
    return sorted(usados)


def fontes(nome):
    """'nome' é pasta/arquivo sem extensão; sem pasta, procura em wep/."""
    if "/" not in nome:
        nome = "wep/" + nome
    base = os.path.join(SRC, *nome.split("/"))
    for ext in (".ogg", ".wav"):
        for e, d in (("-L", "-R"), (".L", ".R")):
            l, r = base + e + ext, base + d + ext
            if os.path.exists(l) and os.path.exists(r):
                return [l, r]
        if os.path.exists(base + ext):
            return [base + ext]
    return []


def main():
    cfg = json.load(open(os.path.join(ROOT, "data", "sons.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".ogg", ".wav")):
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
        tmp = os.path.join(OUT, "_tmp.wav")
        subprocess.run(cmd + ["-filter_complex", filtro, tmp], check=True)
        g = ganho_db(tmp, ALVO_DB[tipo_de(nome, cfg)])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={g:.2f}dB",
                        "-c:a", "libvorbis", "-q:a", "3", os.path.join(OUT, nome.replace("/", "__") + ".ogg")], check=True)
        os.remove(tmp)
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"{len(os.listdir(OUT))} sons em assets/sounds ({total // 1024} KB)")


if __name__ == "__main__":
    main()
