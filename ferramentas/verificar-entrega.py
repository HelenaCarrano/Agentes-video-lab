#!/usr/bin/env python3
"""Revisão técnica de um vídeo final (passo 09 do fluxo). Mostra OK / ATENÇÃO por item.

Uso:
    python ferramentas/verificar-entrega.py video.mp4 [--largura 1920 --altura 1080 --fps 30]

Confere: tamanho e q/s, H.264 yuv420p com BT.709 marcado, áudio AAC 48 kHz, volume (−14 LUFS ±1) e pico (≤ −1 dBFS),
quadros pretos e parados, e se tem faststart. Sai com código 1 se algo exigir atenção.
"""
import argparse, os, re, shutil, subprocess, sys

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or sys.exit("ffmpeg não encontrado (defina FFMPEG).")


def ff(args):
    return subprocess.run([FF, "-hide_banner", "-nostdin", *args], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--largura", type=int, default=1920)
    ap.add_argument("--altura", type=int, default=1080)
    ap.add_argument("--fps", type=float, default=30)
    a = ap.parse_args()
    t = ff(["-i", a.video])
    ruim = 0

    def item(ok, texto):
        nonlocal ruim
        print(("OK       " if ok else "ATENÇÃO  ") + texto)
        ruim += 0 if ok else 1

    v = re.search(r"Video: ([^\n]+)", t)
    res = re.search(r"(\d{3,5})x(\d{3,5})", v[1]) if v else None
    fps = re.search(r"([\d.]+) fps", v[1]) if v else None
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", t)
    item(bool(dur), f"duração {int(dur[1])*3600+int(dur[2])*60+float(dur[3]):.1f} s" if dur else "sem duração")
    item(bool(res) and (int(res[1]), int(res[2])) == (a.largura, a.altura), f"quadro {res[1]}x{res[2]}" if res else "sem vídeo")
    item(bool(fps) and abs(float(fps[1]) - a.fps) < 0.05, f"{fps[1]} q/s" if fps else "q/s desconhecido")
    item(bool(v) and "h264" in v[1] and "yuv420p" in v[1], "H.264 yuv420p" if v else "—")
    item(bool(v) and "bt709" in v[1], "cor BT.709 marcada" if v and "bt709" in v[1] else "cor SEM marcação BT.709 (rode o render com --color-space=bt709)")
    au = re.search(r"Audio: ([^\n]+)", t)
    item(bool(au) and "aac" in au[1] and "48000" in au[1], f"áudio {au[1][:40]}" if au else "SEM áudio")
    if au:
        m = ff(["-i", a.video, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"])
        i = re.findall(r"I:\s+(-?[\d.]+) LUFS", m)
        p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", m)
        if i:
            item(abs(float(i[-1]) + 14) <= 1, f"volume {i[-1]} LUFS (alvo −14 ±1)")
        if p:
            item(float(p[-1]) <= -1.0, f"pico {p[-1]} dBFS (limite −1)")
    s = ff(["-i", a.video, "-vf", "blackdetect=d=0.1:pix_th=0.1,freezedetect=n=-55dB:d=1.0", "-an", "-f", "null", "-"])
    pretos = re.findall(r"black_start:([\d.]+)", s)
    parados = re.findall(r"freeze_start: ([\d.]+)", s)
    item(len(pretos) <= 1, f"quadros pretos: {len(pretos)}" + (f" em {', '.join(pretos[:6])} s" if pretos else ""))
    item(len(parados) == 0, f"trechos parados > 1 s: {len(parados)}" + (f" em {', '.join(parados[:6])} s" if parados else ""))
    with open(a.video, "rb") as f:
        cab = f.read(65536)
    item(cab.find(b"moov") != -1, "faststart (começa a tocar antes de baixar tudo)")
    print("\nTudo certo." if not ruim else f"\n{ruim} item(ns) pedem atenção.")
    sys.exit(1 if ruim else 0)


if __name__ == "__main__":
    main()
