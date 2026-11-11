# Agentes Video Lab

Kit para **fazer vídeos de produto com um agente de código (Claude Code)**: você manda um **vídeo de referência**, o kit analisa o estilo dele, e o agente produz o seu vídeo em cima disso (motion em código com Remotion, telas do produto, cenas de IA e som), parando nas decisões que são suas.

Serve para qualquer empresa ou produto. Nada aqui é específico de uma marca: as cores e a fonte ficam em um arquivo (`motor/src/marca.json`) e tudo o que é de um vídeo específico fica fora do repositório (`projetos/`, no `.gitignore`).

```
video-maker/
├── README.md              ← você está aqui
├── guia/                  ← o fluxo, as regras, as dicas e os prompts (o agente lê isto)
├── modelo/                ← documentos em branco de um projeto (fatos, direções, roteiro, estado…)
├── motor/                 ← projeto Remotion base: tema da marca, fundos, texto cinético, cursor, câmera, legendas
├── ferramentas/           ← scripts: analisar referência, exportar, verificar, novo projeto, legendas, voz
└── projetos/              ← (ignorado pelo git) um vídeo por pasta: seus fatos, mídia, prévias e entregas
```

## O que você precisa

| Ferramenta | Para quê | Como instalar |
|---|---|---|
| **Node 22+** | Remotion | https://nodejs.org |
| **ffmpeg completo** | analisar, exportar e checar vídeo (o que vem dentro do Remotion é reduzido) | Windows: `winget install -e --id Gyan.FFmpeg` · Mac: `brew install ffmpeg` · Linux: `apt install ffmpeg` |
| **Python 3.10+** | as ferramentas (só biblioteca padrão; `numpy` é opcional) | https://python.org |
| **Claude Code** | o agente que produz | https://claude.com/claude-code |
| *opcional:* `faster-whisper` | transcrever a fala da referência e do vídeo final | `pip install faster-whisper` |
| *opcional:* gerador de IA | voz, música, imagem e vídeo gerados (Artlist, ElevenLabs, Higgsfield…) | com o **ok de quem aprova antes de gastar** |

Se o `ffmpeg` não estiver no PATH, aponte para ele: `export FFMPEG=/caminho/ffmpeg` (Windows PowerShell: `$env:FFMPEG="C:\...\ffmpeg.exe"`).

> Sobre a licença do Remotion: é gratuito para pessoas e times pequenos, mas empresas maiores precisam de licença. Confira em https://www.remotion.dev/license antes de usar comercialmente.

## Passo a passo: do vídeo de referência ao seu vídeo

### 1. Crie o projeto
```bash
python ferramentas/novo-video.py meu-video
cd projetos/meu-video/motion && npm install     # uma vez
```
Isso cria `projetos/meu-video/` com os documentos do `modelo/`, as pastas de trabalho e uma cópia do `motor/`.

### 2. Dê um vídeo de referência e gere a análise
Ponha o vídeo que você quer imitar (um vídeo de produto de que você gostou) em `projetos/meu-video/referencias/` e rode:
```bash
python ferramentas/analisar-referencia.py projetos/meu-video/referencias/ref.mp4 \
       --saida projetos/meu-video/referencias/ref-analise
```
Sai uma pasta com:
- `analise.md`: duração, formato, quantos cortes e de quanto em quanto tempo, volume (LUFS), quadros parados e pretos, paleta de cores e, se tiver `faster-whisper`, a fala e o ritmo em palavras por segundo;
- `folha.png`: 30 quadros do vídeo numa imagem só; `abertura.png` e `fechamento.png`: os 3 primeiros e os 3 últimos segundos; `cortes.png`: o começo de cada cena.

Depois **o agente lê a folha e preenche a seção "Leitura" do `analise.md`**: qual o molde (metáfora, carrossel ou história), como é o gancho, quando vira para o produto, como são os blocos, o texto na tela e as passagens. É isso que vira o roteiro do seu vídeo. Detalhes em [`guia/03-referencias.md`](guia/03-referencias.md).

### 3. Abra o Claude Code na pasta do projeto e peça
```bash
cd projetos/meu-video && claude
```
Cole algo como:
> Leia `../../guia/01-fluxo.md` e `../../guia/02-regras.md`. Quero um vídeo do produto **<nome>** no estilo da referência `referencias/ref-analise/analise.md`. Comece pelo passo 0 (fatos) e pare onde o guia mandar.

O agente conduz o fluxo e **para em quatro decisões suas**: a direção, o roteiro, o estilo e o corte final. Em nenhuma gasta crédito sem o seu ok.

### 4. Produza e revise
O agente escreve as cenas em `motion/src/`, gera prévias e as folhas de contato e mostra para você. Peça os ajustes em linguagem normal; ele aplica e mostra de novo.

### 5. Exporte e confira
```bash
python ferramentas/exportar.py render-bruto.mp4 projetos/meu-video/entrega --nome meu-video \
       --vertical render-vertical.mp4           # --vertical é opcional
python ferramentas/verificar-entrega.py projetos/meu-video/entrega/meu-video-mestre.mp4
```
Sai o mestre (H.264, −14 LUFS, BT.709), a versão leve de 720p, a capa e a versão vertical 9:16, com a checagem técnica.

## Versão vertical (9:16) de verdade
Não é uma faixa de vídeo no meio da tela: a **mesma composição** é filmada por uma câmera que segue a ação (`motor/src/pecas/Camera.tsx`), e as cenas de texto se reorganizam quando o contexto `FormatoVertical` está ligado. Veja `ExemploVertical` no motor (`npm run dev`) e a seção de vertical em [`guia/04-producao.md`](guia/04-producao.md).

## Comandos do motor
```bash
cd projetos/meu-video/motion
npm run dev                  # abre o estúdio do Remotion para ver e ajustar
npx remotion still Exemplo out/q.png --frame=60
npx remotion render Exemplo out/video.mp4 --color-space=bt709      # sempre com bt709
npm run lint                 # eslint + tsc
```

## O que NÃO vai para o repositório
Tudo que é de um vídeo: `projetos/`, mídia (`.mp4`, `.wav`, `.mp3`, `.srt`), `node_modules`, renders (`out/`), segredos (`.env`). Está tudo no `.gitignore`. Só entram o guia, o modelo, o motor e as ferramentas.

## Contribuindo
Melhorou uma peça do motor ou uma ferramenta? Mantenha tudo **genérico** (cores vindas de `marca.json`, nenhum nome de empresa no código) e atualize o guia.
