# Partir de um vídeo de referência

A forma mais rápida de acertar o estilo é imitar o **molde** de um vídeo de que se gostou, não o conteúdo. Este passo transforma o vídeo em medidas e em uma leitura escrita que o roteiro usa.

## 1. Gere as medidas
```bash
python ferramentas/analisar-referencia.py projetos/<nome>/referencias/ref.mp4 --saida projetos/<nome>/referencias/ref-analise
```
Para vários vídeos, rode um por vez com `--nome` e compare os `analise.md`. Se o vídeo tem fala e há `faster-whisper`, a transcrição e o ritmo (palavras/s) saem juntos. Sem ele, use `--sem-fala` ou transcreva à mão.

## 2. Leia a folha (o agente faz isto)
Abra `folha.png` **primeiro**, depois `abertura.png`, `fechamento.png` e `cortes.png`. Não abra dezenas de quadros soltos: cada imagem custa contexto. Se precisar olhar uma passagem de perto, extraia 6 quadros em volta dela (veja `comandos-ffmpeg.md`).

Preencha a seção **Leitura** do `analise.md`:

| Pergunta | O que olhar |
|---|---|
| **Molde** | metáfora (persona + imagem da dor), carrossel (recursos trocados por clique) ou história (pessoa real)? |
| **Gancho (0–3 s)** | o que aparece e o que se entende sem som; texto, rosto, interface ou pergunta? |
| **Virada para o produto** | em que segundo a interface aparece e como é a passagem |
| **Blocos** | tempo de cada um e o que muda de um para o outro |
| **Texto na tela** | palavras por linha, posição, animação, qual palavra é destacada |
| **Passagens** | corte seco ou movimento que leva à cena seguinte (o logo vira cabeçalho, a janela vira tela cheia…) |
| **Cartela final** | duração, o que aparece (logo, slogan, chamada) |
| **Som** | música contida na dor, sobe na virada? há efeitos de clique? a voz domina? |
| **Cor** | paleta dominante (o `analise.md` já lista), fundo claro ou escuro |

## 3. Converta em alvos
Copie os números para o seu briefing como alvos de partida (o fluxo traz os valores gerais em `04-producao.md`):
- duração e ritmo (cena média, algo novo a cada quantos segundos);
- quando vira para o produto (% da duração);
- palavras por segundo da narração;
- volume (−14 LUFS é o padrão das redes) e relação voz/música.

## 4. Separe o que copiar do que não copiar
- **Copie:** a estrutura, o ritmo, o tipo de passagem, o tamanho e a posição do texto, a duração da cartela.
- **Não copie:** marca, logo, texto, música, imagens, voz ou qualquer trecho. A referência é um molde; o vídeo é do seu produto, com a sua marca e os seus fatos (`fatos.md`).

## 5. Uma referência é suficiente, três é melhor
Com várias, procure o que **se repete** entre elas (é a convenção do gênero) e o que **só uma** faz (é o diferencial dela). Registre os dois lados em `direcoes.md` para escolher de propósito.
