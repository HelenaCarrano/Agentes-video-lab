#!/usr/bin/env python3
"""Cria um projeto de vídeo novo a partir de `modelo/` e do `motor/`.

Uso:
    python ferramentas/novo-video.py nome-do-video

Cria `projetos/<nome>/` (que o .gitignore deixa de fora do repositório) com:
    fatos.md, direcoes.md, roteiro.md, estado.md, pedidos.md, decisoes.md, gastos.md, licencas.md  (do modelo)
    referencias/   ← ponha aqui os vídeos de referência e rode analisar-referencia.py
    telas/  ia/  som/  montagem/  entrega/  anteriores/
    motion/        ← cópia do motor Remotion (rode `npm install` dentro dela uma vez)
"""
import os, re, shutil, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    nome = re.sub(r"[^a-z0-9]+", "-", sys.argv[1].lower()).strip("-")
    destino = os.path.join(RAIZ, "projetos", nome)
    if os.path.exists(destino):
        sys.exit(f"Já existe {destino}. Escolha outro nome (nada é sobrescrito).")
    os.makedirs(destino)
    for f in os.listdir(os.path.join(RAIZ, "modelo")):
        shutil.copy(os.path.join(RAIZ, "modelo", f), os.path.join(destino, f))
    for p in ["referencias", "telas", "ia", "som", "montagem", "entrega", "anteriores"]:
        os.makedirs(os.path.join(destino, p))
    shutil.copytree(os.path.join(RAIZ, "motor"), os.path.join(destino, "motion"), ignore=shutil.ignore_patterns("node_modules", "out", "dist"))
    print(f"Projeto criado em {destino}\n\nPróximos passos:\n"
          f"  1. cd projetos/{nome}/motion && npm install\n"
          f"  2. coloque o vídeo de referência em projetos/{nome}/referencias/\n"
          f"  3. python ferramentas/analisar-referencia.py projetos/{nome}/referencias/<video>.mp4 --saida projetos/{nome}/referencias/<video>-analise\n"
          f"  4. abra o Claude Code na pasta do projeto e siga o README (passo 2).")


if __name__ == "__main__":
    main()
