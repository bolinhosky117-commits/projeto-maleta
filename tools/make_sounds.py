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
# tiros e explosões: volume pela "fantasia" da arma (loudness integrada, LUFS). Pistola mais contida,
# espingarda/magnum/rifle mais encorpados, bazuca e granada no topo. Submetralhadora mais baixa porque a rajada soma.
ALVO_LUFS = {"pistola": -23.0, "submetralhadora": -25.0, "espingarda": -20.5, "magnum": -19.5, "rifle": -20.5,
             "especial": -18.5, "arremessável": -18.5, "munição especial": -18.5, "faca": -24.0}
TETO_TIRO_DB = -4.0


def tabelas(cfg):
    """Todas as tabelas {acao: nome} do sons.json."""
    return list(cfg["armas"].values()) + list(cfg.get("tipos", {}).values()) + [cfg.get("padrao", {})]


def nomes_de(v):
    """Um valor do sons.json é um nome ou uma lista de {som, em, ganho} (sons em sequência)."""
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        return [x["som"] for x in v]
    return []


def classe_tiro(nome, cfg, tipos_item):
    """Se 'nome' é tiro/explosão de alguma arma, devolve o tipo da arma (pistola, espingarda...)."""
    achados = []
    for arma, sons in cfg["armas"].items():
        for acao in ("atirar", "atacar"):
            if nome in nomes_de(sons.get(acao)):
                achados.append(tipos_item.get(arma))
    for tipo, sons in cfg.get("tipos", {}).items():
        if nome in nomes_de(sons.get("atacar")):
            achados.append(tipo)
    achados = [a for a in achados if a in ALVO_LUFS]
    return max(achados, key=lambda a: ALVO_LUFS[a]) if achados else None


def lufs(arquivo):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", arquivo, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    linhas = [l for l in out.splitlines() if l.strip().startswith("I:")]
    return float(linhas[-1].split()[1]) if linhas else -70.0


def tipo_de(nome, cfg):
    m = cfg.get("maleta", {})
    if nome == m.get("deslocar"):
        return "tique"
    if nome in m.values():
        return "maleta"
    for sons in tabelas(cfg):
        for acao, v in sons.items():
            if nome in nomes_de(v) and acao in ALVO_DB:
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
        for v in sons.values():
            usados.update(nomes_de(v))
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
    itens = json.load(open(os.path.join(ROOT, "assets", "items.json"), encoding="utf-8"))["items"]
    tipos_item = {it["id"]: (it.get("rpg") or {}).get("tipo") for it in itens}
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
        classe = classe_tiro(nome, cfg, tipos_item)
        g = ganho_db(tmp, ALVO_DB[tipo_de(nome, cfg)])
        if classe:
            i = lufs(tmp)
            if i > -60:   # som curto demais para medir a loudness: fica no método do trecho mais forte
                pico = ganho_db(tmp, 100.0)  # só o limite de pico (alvo absurdo → sobra o teto)
                g = min(ALVO_LUFS[classe] - i, pico + (TETO_TIRO_DB - TETO_DB))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={g:.2f}dB",
                        "-c:a", "libvorbis", "-q:a", "3", os.path.join(OUT, nome.replace("/", "__") + ".ogg")], check=True)
        os.remove(tmp)
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"{len(os.listdir(OUT))} sons em assets/sounds ({total // 1024} KB)")


if __name__ == "__main__":
    main()
