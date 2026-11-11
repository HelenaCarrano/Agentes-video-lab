# Comandos úteis

Todos usam um ffmpeg **completo** (o que vem dentro do Remotion não tem `tile`, `select`, `ebur128`, `blend`, `drawtext`).
No Windows, escape os dois-pontos do caminho de fonte em `drawtext`: `fontfile='C\:/Windows/Fonts/arialbd.ttf'`.

```bash
# Folha de 30 quadros de um vídeo de D segundos (6 colunas x 5 linhas)
ffmpeg -i video.mp4 -vf "fps=30/D,scale=384:-2,tile=6x5:padding=4:color=white" -frames:v 1 folha.png

# Cortes secos detectados (segundos)
ffmpeg -i video.mp4 -vf "scale=480:-2,select='gt(scene,0.25)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"

# Seis quadros em volta de uma passagem em T segundos (3 antes, 3 depois, a 30 q/s)
ffmpeg -ss T-0.1 -i video.mp4 -t 0.25 -vf "fps=30,scale=480:-2,tile=6x1" -frames:v 1 passagem.png

# Still de uma peça do Remotion no quadro N (repita para 10, 30, 50, 70 e 90% da duração)
npx remotion still MinhaPeca out/peca-10.png --frame=N

# Cinco stills lado a lado, numa folha só
ffmpeg -i a.png -i b.png -i c.png -i d.png -i e.png -filter_complex "[0][1][2][3][4]hstack=inputs=5,scale=2400:-2" folha.png

# Volume integrado e pico
ffmpeg -i video.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12

# Marcação de cor de um clipe
ffprobe -v error -select_streams v:0 -show_entries stream=color_space,color_transfer,color_primaries,color_range -of default=nw=1 clipe.mp4

# O que muda entre o primeiro e o último quadro (claro = mudou)
ffmpeg -i inicio.png -i fim.png -filter_complex "blend=all_mode=difference" diferenca.png

# Teste de cinza e teste do celular
ffmpeg -i quadro.png -vf format=gray cinza.png
ffmpeg -i quadro.png -vf scale=640:-2 celular.png

# Quadros pretos e trechos parados
ffmpeg -i video.mp4 -vf "blackdetect=d=0.1:pix_th=0.1,freezedetect=n=-55dB:d=0.6" -an -f null - 2>&1 | grep -E "black_start|freeze_start"

# Prévia em meia resolução do Remotion
npx remotion render MinhaComposicao out/previa.mp4 --scale=0.5 --color-space=bt709
```

Troque `T-0.1` pelo número já calculado (para T = 12, use `11.9`) e `D` pela duração em segundos.
