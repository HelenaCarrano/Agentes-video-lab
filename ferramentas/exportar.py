#!/usr/bin/env python3
"""Gera as entregas a partir do render bruto do Remotion, com os padrões do fluxo.

Uso:
    python ferramentas/exportar.py render-bruto.mp4 pasta-de-entrega [--nome meu-video] [--vertical render-9x16.mp4]

Cria na pasta de entrega:
    <nome>-mestre.mp4        H.264 High, CRF 17, yuv420p, BT.709 marcado, AAC 48 kHz, +faststart, −14 LUFS / pico ≤ −1 dBTP
    <nome>-mestre.mp4.sha256
    <nome>-leve-720p.mp4     1280×720, CRF 28 (para mandar no celular)
    <nome>-capa.png          um quadro (use --capa SEGUNDOS para escolher; padrão: 40% da duração)
    <nome>-vertical-9x16.mp4 (só com --vertical) mesmo tratamento de som, CRF 20

O volume é ajustado em duas passadas (mede, depois aplica o ganho exato e um limitador). Precisa de um ffmpeg completo.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or sys.exit("ffmpeg não encontrado (instale o build completo ou defina FFMPEG).")


def ff(args):
    r = subprocess.run([FF, "-hide_banner", "-nostdin", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r


def medir(arq):
    t = ff(["-i", arq, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"]).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", t)
    return float(i[-1]) if i else None


def duracao(arq):
    t = ff(["-i", arq]).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", t)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0


def codificar(entrada, saida, crf, escala=None, ganho=0.0):
    af = f"aresample=192000,volume={ganho:.2f}dB,alimiter=limit=0.8:attack=2:release=60:level=disabled,aresample=48000"
    vf = f"scale={escala}:flags=lanczos," if escala else ""
    vf += "format=yuv420p"
    r = ff(["-y", "-i", entrada, "-vf", vf, "-af", af,
            "-c:v", "libx264", "-profile:v", "high", "-crf", str(crf), "-preset", "slow", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", saida])
    if r.returncode:
        sys.exit("ffmpeg falhou:\n" + r.stderr[-1500:])


def sha(arq):
    h = hashlib.sha256()
    with open(arq, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def com_som(entrada, saida, crf, escala=None):
    # 1ª passada: aplica um ganho de teste e mede; 2ª: aplica o ganho que falta para chegar a −14 LUFS
    teste = saida + ".medida.wav"
    ff(["-y", "-i", entrada, "-vn", "-ac", "2", "-ar", "48000", teste])
    atual = medir(teste)
    os.remove(teste)
    ganho = -14.0 - atual if atual is not None else 0.0
    codificar(entrada, saida, crf, escala, ganho)
    return medir(saida)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("render")
    ap.add_argument("pasta")
    ap.add_argument("--nome", default="video")
    ap.add_argument("--vertical")
    ap.add_argument("--capa", type=float)
    a = ap.parse_args()
    os.makedirs(a.pasta, exist_ok=True)
    out = lambda s: os.path.join(a.pasta, f"{a.nome}-{s}")

    print("→ mestre…")
    l = com_som(a.render, out("mestre.mp4"), 17)
    open(out("mestre.mp4.sha256"), "w").write(f"{sha(out('mestre.mp4'))}  {a.nome}-mestre.mp4\n")
    print(f"  {l} LUFS")
    print("→ versão leve…")
    codificar(out("mestre.mp4"), out("leve-720p.mp4"), 28, "1280:720", 0.0)
    print("→ capa…")
    t = a.capa if a.capa is not None else duracao(a.render) * 0.4
    ff(["-y", "-ss", f"{t:.2f}", "-i", a.render, "-frames:v", "1", out("capa.png")])
    if a.vertical:
        print("→ vertical…")
        l = com_som(a.vertical, out("vertical-9x16.mp4"), 20)
        print(f"  {l} LUFS")
    print("Pronto em", a.pasta, "— rode ferramentas/verificar-entrega.py para conferir.")


if __name__ == "__main__":
    main()
