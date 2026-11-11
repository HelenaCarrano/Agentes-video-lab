# O fluxo

```
referência → 00 fatos → 01 direções → [decide] → 02 roteiro e storyboard → [aprova]
    → 03 quadros de estilo → [aprova]
    → 04 telas · 05 IA · 06 motion · 07 som   (em paralelo; cada geração paga com o ok)
    → 08 montagem → 09 revisão → [assiste: aprova, ajusta ou rejeita] → 10 entrega e retrospectiva
```
As quatro **paradas** (entre colchetes) são de quem aprova o vídeo. O agente nunca escolhe nem aprova por essa pessoa.

## Pastas de um projeto (`projetos/<nome>/`)
```
fatos.md  direcoes.md  roteiro.md  leitura-cega.txt
estado.md  pedidos.md  decisoes.md  gastos.md  licencas.md
referencias/   vídeos de referência + <nome>-analise/ (saída do analisar-referencia.py)
estilo/        quadros de estilo e paleta.md
telas/         prints e gravações do produto; telas.md diz o que cada uma mostra
ia/            <id>/ plano.md, quadros e versões de cada plano gerado
motion/        o projeto Remotion (cópia do motor/)
som/           voz, música, efeitos
montagem/      prévias, folhas de contato
entrega/       mestre, versão leve, legenda, capa, vertical
anteriores/    versões substituídas, com data e hora
```

## 00 · Fatos
Leia site, documentação, README, changelog, material de marketing, apresentações, guia de marca e o código (se houver), para conferir que o recurso existe e como se chama na tela. Preencha `fatos.md` (veja o modelo). Pergunte no máximo **três** coisas, cada uma com sugestão ("Onde vai passar e com quanto tempo? Sugiro 45–60 s").

## 01 · Direções (parada 1)
Três direções **diferentes de verdade**. Se há referência, ela indica o molde; ofereça mesmo assim uma alternativa.

| Molde | Como é | Planos de IA |
|---|---|---|
| **Metáfora** | uma persona e uma imagem para a dor, que volta no ganho | 1–3 |
| **Carrossel** | a dor em uma linha → entra na tela → 3 a 5 recursos, cada um com cor e rótulo → cartela | 0–1 |
| **História** | uma pessoa num momento real tem o problema, usa o produto e o final é a emoção | 5–10 |

Cada direção traz: a espinha (uma frase com "mas"/"portanto"), os 3 primeiros segundos (o que se entende **sem som**), o gancho em 3 versões (resultado, pergunta, contraste), os blocos com tempo, a mistura motion/tela/IA com créditos estimados, a voz e os riscos. **Pare.**

## 02 · Roteiro e storyboard (parada 2)
Uma tabela, uma linha por batida (modelo em `roteiro.md`). Regras:
- A fala acrescenta o porquê, o sentimento ou o contexto; não descreve o que a imagem já mostra.
- O texto na tela é a frase-chave da fala, encurtada (2–6 palavras), nunca a fala inteira.
- Entre um bloco e o próximo algo muda ("mas", "portanto"), não "e então".
- Números por extenso na fala (o alinhamento erra com algarismos).
- **A duração quem dá é a voz:** palavras ÷ ritmo medido, +~10% de pausas, + a cartela. Para caber, corte palavras, não o tempo das batidas.
- Nenhum trecho de mais de ~3 s sem algo novo na tela.
- Cada fala sobre o produto cita a linha do `fatos.md` que a sustenta.

**Leitura cega antes de mostrar:** escreva `leitura-cega.txt` só com o que o espectador vê e ouve (tempo, imagem sem nomes internos, texto, fala) e peça a um subagente novo, com o prompt de `05-claude-code.md`, para dizer o que entendeu e onde se perdeu. Corrija o que não muda o sentido; o que muda vira pergunta. **Pare.**

## 03 · Quadros de estilo (parada 3)
Antes de gastar com vídeo, mostre o visual: um still de motion, um still da interface tratada (janela, gradiente, cursor), um ou dois quadros de IA (modelo barato, com ok do gasto) e `paleta.md`. Antes de mostrar faça o **teste do cinza** (o assunto se separa do fundo?) e o **do celular** (640 px de largura, o texto ainda se lê?). **Pare.**

## 04–07 · Produção
Veja `04-producao.md`: telas, motion, IA e som.

## 08 · Montagem
Uma composição Remotion só junta as cenas. Mude o corte mudando dados (JSON/constantes), não os componentes. Render sempre com `--color-space=bt709`. A cada versão gere prévia em meia resolução (`--scale=0.5`), folha de contato de 30 quadros, folha das passagens (antes/depois de cada transição) e confira: nada parado por mais de ~0,6 s sem querer, nenhum quadro preto fora do lugar, texto inteiro e legível no celular, cursor em cima do que a fala cita, passagens que casam a posição dos objetos.

## 09 · Revisão
1. **Técnica, por script:** `ferramentas/verificar-entrega.py`.
2. **Revisor novo** (subagente sem contexto) com o prompt de `05-claude-code.md`: começa só com folha, passagens e transcrição, escreve a história que entendeu, só depois confere fatos, dado real na tela, texto errado, defeitos de IA, leitura no celular e marca.

Quem aprova assiste ao vídeo inteiro: "aprova", "ajusta: …" (aplique e mostre, sem perguntas novas; se pedir geração paga, ok do gasto antes) ou "rejeita" (anote o motivo e pergunte se volta à direção ou ao roteiro).

## 10 · Entrega e retrospectiva
`ferramentas/exportar.py` gera mestre, leve, capa e vertical. Acrescente o `.srt` e a `retrospectiva.md` (estilo, prompts que funcionaram e os que não, créditos por plano, o que mudar no próximo).
