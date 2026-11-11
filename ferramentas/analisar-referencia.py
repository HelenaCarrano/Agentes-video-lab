#!/usr/bin/env python3
"""Analisa um vídeo de referência e gera, numa pasta, tudo o que o fluxo precisa para copiar o *molde* dele.

Uso:
    python ferramentas/analisar-referencia.py caminho/do/video.mp4 [--saida pasta] [--nome slug]
    python ferramentas/analisar-referencia.py https://link-do-video [--saida pasta]      # baixa com yt-dlp e analisa

Com um LINK, o vídeo é baixado (até 1080p) para <saida>/fonte/, junto com as legendas automáticas/oficiais do próprio
vídeo (.srt), que viram a transcrição (sem precisar do whisper), e um fonte.md com título, canal, data e a URL.
Precisa de `pip install yt-dlp`. Baixe só vídeos que você tem direito de analisar; a referência serve de MOLDE
(estrutura, ritmo, passagens), nunca para copiar marca, texto, música, imagem ou voz.

Saída (por padrão em projetos/<projeto>/referencias/<nome>/ se existir, senão ./analise-<nome>/):
    analise.md        números medidos (duração, ritmo de cortes, volume, quadros pretos/parados, cores, fala)
    folha.png         30 quadros igualmente espaçados (6x5) — leia isto primeiro
    cortes.png        o primeiro quadro de cada cena detectada (até 24)
    abertura.png      os 3 primeiros segundos (6 quadros)
    fechamento.png    os 3 últimos segundos (6 quadros)
    cortes.json       tempos dos cortes e dos intervalos sem novidade (para reaproveitar em scripts)

Precisa só de um ffmpeg COMPLETO no PATH (ou na variável FFMPEG). Opcional: numpy (paleta de cores) e
faster-whisper (transcrição e palavras por segundo). Nada é enviado para fora: tudo roda local.
"""
import argparse, json, os, re, shutil, subprocess, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def achar_ffmpeg():
    cand = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if not cand:
        sys.exit("ffmpeg não encontrado. Instale o build completo (winget install -e --id Gyan.FFmpeg | brew install ffmpeg) "
                 "ou aponte a variável FFMPEG para ele.")
    return cand


FF = achar_ffmpeg()


def rodar(args, **kw):
    return subprocess.run([FF, "-hide_banner", "-nostdin", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def eh_link(x):
    return re.match(r"^https?://", x or "") is not None


def baixar(url, pasta):
    """Baixa o vídeo e as legendas com yt-dlp; devolve (caminho do mp4, dict com metadados, caminho do srt ou None)."""
    os.makedirs(pasta, exist_ok=True)
    cmd = [sys.executable, "-m", "yt_dlp"]
    if subprocess.run(cmd + ["--version"], capture_output=True).returncode:
        if shutil.which("yt-dlp"):
            cmd = ["yt-dlp"]
        else:
            sys.exit("yt-dlp não encontrado. Instale com: pip install yt-dlp")
    args = cmd + ["--no-playlist", "-f", "bv*[height<=1080]+ba/b[height<=1080]/b", "--merge-output-format", "mp4",
                  "--write-info-json", "--write-subs", "--write-auto-subs", "--sub-langs", "pt.*,en.*", "--convert-subs", "srt",
                  "--ffmpeg-location", os.path.dirname(FF) or ".", "-o", os.path.join(pasta, "referencia.%(ext)s"), url]
    print("→ baixando a referência…")
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    mp4 = os.path.join(pasta, "referencia.mp4")
    if r.returncode or not os.path.exists(mp4):
        sys.exit("Não consegui baixar o vídeo (link privado, restrito ou indisponível?):\n" + r.stderr[-800:])
    meta = {}
    try:
        meta = json.load(open(os.path.join(pasta, "referencia.info.json"), encoding="utf-8"))
    except Exception:
        pass
    srt = None
    for f in sorted(os.listdir(pasta)):
        if f.endswith(".srt"):
            srt = os.path.join(pasta, f)
            if ".pt" in f:
                break
    info_md = ["# Fonte da referência", "", f"- URL: {url}", f"- Título: {meta.get('title', '—')}", f"- Canal: {meta.get('uploader', '—')}",
               f"- Publicado em: {meta.get('upload_date', '—')}", f"- Baixado em: {__import__('datetime').date.today()}", "",
               "> Uso: análise de molde (estrutura, ritmo, passagens). Não copiar marca, texto, música, imagem ou voz.", ""]
    open(os.path.join(pasta, "fonte.md"), "w", encoding="utf-8").write("\n".join(info_md))
    return mp4, meta, srt


def fala_do_srt(srt):
    """Transcrição a partir de um .srt (legendas do próprio vídeo): devolve o mesmo formato de transcrever()."""
    texto, palavras, ini, fim = [], 0, None, 0.0
    for bloco in re.split(r"\n\s*\n", open(srt, encoding="utf-8", errors="replace").read().strip()):
        ls = bloco.strip().splitlines()
        if len(ls) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", ls[1])
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        t = re.sub(r"<[^>]+>", "", " ".join(ls[2:])).strip()
        if not t or (texto and texto[-1].endswith(t)):
            continue
        ini = a if ini is None else ini
        fim = b
        palavras += len(t.split())
        texto.append(f"[{a:6.1f}s] {t}")
    return {"idioma": "legenda do vídeo", "texto": texto, "palavras": palavras, "span": (fim - ini) if ini is not None else 0}


def info(video):
    t = rodar(["-i", video]).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", t)
    dur_s = int(dur[1]) * 3600 + int(dur[2]) * 60 + float(dur[3]) if dur else 0.0
    v = re.search(r"Stream #[^:]+:[^:]*: Video: ([^\n]+)", t)
    a = re.search(r"Stream #[^:]+:[^:]*: Audio: ([^\n]+)", t)
    res = re.search(r"(\d{3,5})x(\d{3,5})", v[1]) if v else None
    fps = re.search(r"([\d.]+) fps", v[1]) if v else None
    return {
        "duracao": dur_s,
        "largura": int(res[1]) if res else 0,
        "altura": int(res[2]) if res else 0,
        "fps": float(fps[1]) if fps else 0.0,
        "video": v[1].split(",")[0] if v else "—",
        "cor": re.search(r"\((tv|pc)[^)]*\)", v[1])[0] if v and re.search(r"\((tv|pc)[^)]*\)", v[1]) else "sem marcação",
        "audio": a[1] if a else None,
    }


def cortes(video, limiar=0.25):
    t = rodar(["-i", video, "-vf", f"scale=480:-2,select='gt(scene,{limiar})',showinfo", "-an", "-f", "null", "-"]).stderr
    return [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", t)]


def volume(video):
    t = rodar(["-i", video, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"]).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", t)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", t)
    r = re.findall(r"LRA:\s+(-?[\d.]+) LU", t)
    return {"lufs": float(i[-1]) if i else None, "pico_dbfs": float(p[-1]) if p else None, "lra": float(r[-1]) if r else None}


def intervalos(video, filtro, padrao_ini, padrao_fim):
    t = rodar(["-i", video, "-vf", filtro, "-an", "-f", "null", "-"]).stderr
    ini = [float(x) for x in re.findall(padrao_ini, t)]
    fim = [float(x) for x in re.findall(padrao_fim, t)]
    return list(zip(ini, fim + [None] * (len(ini) - len(fim))))


def folha(video, dur, saida, colunas, linhas, largura=384):
    n = colunas * linhas
    rodar(["-y", "-i", video, "-vf", f"fps={n}/{max(dur, 0.1):.3f},scale={largura}:-2,tile={colunas}x{linhas}:padding=4:color=white",
           "-frames:v", "1", saida])


def trecho(video, ini, saida, qtd=6, janela=3.0):
    rodar(["-y", "-ss", f"{max(ini, 0):.2f}", "-i", video, "-t", f"{janela}", "-vf", f"fps={qtd}/{janela},scale=480:-2,tile={qtd}x1:padding=4:color=white",
           "-frames:v", "1", saida])


def quadros_dos_cortes(video, tempos, saida, maximo=24):
    if not tempos:
        return False
    pasta = saida + "_tmp"
    os.makedirs(pasta, exist_ok=True)
    escolhidos = [0.0] + tempos
    if len(escolhidos) > maximo:
        passo = len(escolhidos) / maximo
        escolhidos = [escolhidos[int(i * passo)] for i in range(maximo)]
    arqs = []
    for k, tt in enumerate(escolhidos):
        a = os.path.join(pasta, f"{k:03d}.png")
        rodar(["-y", "-ss", f"{tt + 0.08:.2f}", "-i", video, "-frames:v", "1", "-vf", "scale=320:-2", a])
        if os.path.exists(a):
            arqs.append(a)
    if arqs:
        entradas = []
        for a in arqs:
            entradas += ["-i", a]
        col = min(6, len(arqs))
        lin = (len(arqs) + col - 1) // col
        # preenche com quadros vazios no fim para fechar a grade
        rodar(["-y", *entradas, "-filter_complex", f"concat=n={len(arqs)}:v=1:a=0,tile={col}x{lin}:padding=4:color=white", "-frames:v", "1", saida])
    shutil.rmtree(pasta, ignore_errors=True)
    return os.path.exists(saida)


def paleta(video, dur):
    try:
        import numpy as np
    except Exception:
        return None
    p = subprocess.run([FF, "-hide_banner", "-nostdin", "-v", "error", "-i", video, "-vf", "fps=1,scale=48:27", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    if not p:
        return None
    px = np.frombuffer(p, np.uint8).reshape(-1, 3).astype(np.float32)
    # k-means simples, 6 cores
    rng = np.random.default_rng(1)
    c = px[rng.choice(len(px), 6, replace=False)]
    for _ in range(12):
        d = ((px[:, None, :] - c[None]) ** 2).sum(2)
        lab = d.argmin(1)
        for k in range(6):
            if (lab == k).any():
                c[k] = px[lab == k].mean(0)
    pesos = np.bincount(lab, minlength=6) / len(lab)
    ordem = pesos.argsort()[::-1]
    return [("#%02x%02x%02x" % tuple(int(v) for v in c[k]), round(float(pesos[k]) * 100)) for k in ordem]


def transcrever(video):
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return None
    m = WhisperModel("small", device="auto", compute_type="auto")
    segs, lang = m.transcribe(video, word_timestamps=True)
    palavras, texto = [], []
    for s in segs:
        texto.append(f"[{s.start:6.1f}s] {s.text.strip()}")
        palavras += [w for w in (s.words or [])]
    return {"idioma": lang.language, "texto": texto, "palavras": len(palavras),
            "span": (palavras[-1].end - palavras[0].start) if palavras else 0}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", help="arquivo de vídeo OU link (https://…)")
    ap.add_argument("--saida")
    ap.add_argument("--nome")
    ap.add_argument("--limiar", type=float, default=0.25, help="sensibilidade dos cortes (0.1 pega mais, 0.4 só os secos)")
    ap.add_argument("--sem-fala", action="store_true", help="não tenta transcrever")
    a = ap.parse_args()

    srt_fonte = None
    if eh_link(a.video):
        base = os.path.abspath(a.saida or f"analise-{a.nome or 'referencia'}")
        video, meta, srt_fonte = baixar(a.video, os.path.join(base, "fonte"))
        nome = a.nome or re.sub(r"[^a-z0-9]+", "-", (meta.get("title") or "referencia").lower()).strip("-")[:50] or "referencia"
        saida = base
    else:
        video = os.path.abspath(a.video)
        if not os.path.exists(video):
            sys.exit(f"Não achei {video}")
        nome = a.nome or re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(video))[0].lower()).strip("-")
        saida = os.path.abspath(a.saida or f"analise-{nome}")
    os.makedirs(saida, exist_ok=True)

    print("→ lendo o arquivo…")
    inf = info(video)
    D = inf["duracao"]
    print("→ detectando cortes…")
    cs = cortes(video, a.limiar)
    if len(cs) < 3 and a.limiar > 0.1:  # vídeo de motion: as passagens são suaves, não cortes secos
        print("  poucos cortes secos; tentando de novo com sensibilidade maior…")
        cs = cortes(video, 0.1)
    print("→ medindo volume…")
    vol = volume(video) if inf["audio"] else None
    print("→ quadros pretos e parados…")
    pretos = intervalos(video, "blackdetect=d=0.1:pix_th=0.1", r"black_start:([\d.]+)", r"black_end:([\d.]+)")
    parados = intervalos(video, "freezedetect=n=-55dB:d=0.6", r"freeze_start: ([\d.]+)", r"freeze_end: ([\d.]+)")
    print("→ folhas de contato…")
    folha(video, D, os.path.join(saida, "folha.png"), 6, 5)
    trecho(video, 0, os.path.join(saida, "abertura.png"))
    trecho(video, D - 3.0, os.path.join(saida, "fechamento.png"))
    tem_cortes = quadros_dos_cortes(video, cs, os.path.join(saida, "cortes.png"))
    print("→ paleta…")
    pal = paleta(video, D)
    fala = None
    if srt_fonte:
        fala = fala_do_srt(srt_fonte)
    elif inf["audio"] and not a.sem_fala:
        print("→ transcrevendo (se o faster-whisper estiver instalado)…")
        fala = transcrever(video)

    pts = [0.0] + cs + [D]
    duracoes = [round(pts[i + 1] - pts[i], 2) for i in range(len(pts) - 1)]
    maior = max(duracoes) if duracoes else D
    media = sum(duracoes) / len(duracoes) if duracoes else D
    json.dump({"duracao": D, "cortes": cs, "duracoes_das_cenas": duracoes, "pretos": pretos, "parados": parados}, open(os.path.join(saida, "cortes.json"), "w"), indent=1)

    L = []
    L += [f"# Análise de referência: {nome}", "", f"Arquivo: `{os.path.basename(video)}` · gerado por `ferramentas/analisar-referencia.py`", ""]
    L += ["## Formato", "", "| Item | Valor |", "|---|---|",
          f"| Duração | {D:.1f} s |", f"| Quadro | {inf['largura']}×{inf['altura']} a {inf['fps']:g} q/s |",
          f"| Vídeo | {inf['video']} · cor: {inf['cor']} |", f"| Áudio | {inf['audio'] or 'sem áudio'} |", ""]
    L += ["## Ritmo", "", "| Item | Valor | Referência do fluxo |", "|---|---|---|",
          f"| Cortes secos detectados | {len(cs)} | — |", f"| Cena média | {media:.1f} s | algo novo a cada 2–3 s |",
          f"| Maior cena sem corte | {maior:.1f} s | (pode ter movimento dentro: confira na folha) |",
          f"| Quadros parados > 0,6 s | {len(parados)} | no máximo ~0,6 s, fora o de propósito |",
          f"| Quadros pretos | {len(pretos)} | nenhum fora do lugar |", ""]
    if cs:
        L += ["Cortes (s): " + ", ".join(f"{c:g}" for c in cs), ""]
    if parados:
        L += ["Trechos parados (s): " + ", ".join(f"{i:.1f}→{(f or D):.1f}" for i, f in parados), ""]
    if vol:
        L += ["## Som", "", "| Item | Valor | Alvo |", "|---|---|---|", f"| Volume integrado | {vol['lufs']} LUFS | −14 |",
              f"| Pico | {vol['pico_dbfs']} dBFS | ≤ −1 |", f"| Variação (LRA) | {vol['lra']} LU | — |", ""]
    if fala:
        ritmo = fala["palavras"] / fala["span"] if fala["span"] else 0
        L += ["## Fala", "", f"Idioma: {fala['idioma']} · {fala['palavras']} palavras · ritmo {ritmo:.2f} palavras/s", "", "```", *fala["texto"], "```", ""]
    elif inf["audio"]:
        L += ["## Fala", "", "Não transcrita (instale `pip install faster-whisper` ou transcreva à mão).", ""]
    if pal:
        L += ["## Paleta dominante", "", " · ".join(f"`{h}` {p}%" for h, p in pal), ""]
    L += ["## Arquivos", "", "- `folha.png`: 30 quadros — comece por aqui", "- `abertura.png`: os 3 primeiros segundos (o gancho)", "- `fechamento.png`: os 3 últimos (a cartela)"]
    if tem_cortes:
        L += ["- `cortes.png`: o começo de cada cena"]
    L += ["", "## Leitura (preencha olhando a folha — o Claude faz isso no passo 2 do README)", "",
          "- **Molde:** metáfora / carrossel / história / outro?", "- **Gancho (0–3 s):** o que se vê e o que se entende sem som:",
          "- **Virada para o produto:** em que segundo e como:", "- **Blocos:** (tempo, o que muda de um para o outro)",
          "- **Texto na tela:** quantas palavras, que posição, que animação:", "- **Passagens entre cenas:** cortes secos ou movimentos?",
          "- **Cartela final:** duração, o que aparece:", "- **O que copiar:** …", "- **O que não copiar:** …", ""]
    open(os.path.join(saida, "analise.md"), "w", encoding="utf-8").write("\n".join(L))
    print(f"\nPronto: {os.path.join(saida, 'analise.md')}")


if __name__ == "__main__":
    main()
