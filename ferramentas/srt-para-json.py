#!/usr/bin/env python3
"""Converte um .srt em JSON de legendas em QUADROS, para o componente `Legendas` do motor.

Uso:
    python ferramentas/srt-para-json.py legendas.srt motion/src/legendas.json [--fps 30]
"""
import argparse, json, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("srt")
ap.add_argument("saida")
ap.add_argument("--fps", type=float, default=30)
a = ap.parse_args()

t = lambda s: (int(s[0]) * 3600 + int(s[1]) * 60 + int(s[2]) + int(s[3]) / 1000)
saida = []
for bloco in re.split(r"\n\s*\n", open(a.srt, encoding="utf-8").read().strip()):
    linhas = bloco.strip().splitlines()
    if len(linhas) < 3:
        continue
    m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", linhas[1])
    if not m:
        continue
    g = m.groups()
    saida.append({"ini": round(t(g[:4]) * a.fps), "fim": round(t(g[4:]) * a.fps), "texto": " ".join(linhas[2:])})
json.dump(saida, open(a.saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(saida)} legendas → {a.saida}")
