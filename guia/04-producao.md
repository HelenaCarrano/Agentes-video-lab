# Produção: números-alvo, telas, motion, IA, som e vertical

## Números-alvo (ajuste com a análise da referência)
| Item | Alvo |
|---|---|
| Quadro | 1920×1080, 30 q/s (25 se a marca já usa) |
| Duração | curto 20–35 s · médio 45–60 s · longo 60–95 s. Quem aprova escolhe na direção |
| Narração | ~2,0–2,4 palavras/s em português; **meça a voz real** e recalcule |
| Virada para o produto | até ~30% da duração |
| Algo novo na tela | a cada 2–3 s |
| Quadro parado | no máximo ~0,6 s, fora o de propósito |
| Texto | 2–6 palavras por linha, até 2 linhas, uma palavra destacada |
| Cartela final | 3–6 s |
| Volume | −14 LUFS integrado, pico até −1 dBTP; música ~10 dB abaixo da voz |
| Cor | BT.709 marcado no arquivo (sem isso cada app mostra uma cor) |
| Margem do texto | ao menos 5% das bordas |

## Telas (o produto de verdade)
- Capture com uma conta de **demonstração com dados fictícios** (regra 5).
- Ou recrie a interface em código (React) a partir das capturas: fica nítida em qualquer tamanho, permite cursor, cliques e zoom, e é o que permite a versão vertical. Simplificar pode; inventar recurso não.
- Trate com janela, sombra, gradiente de fundo da marca, cursor e destaque do que a fala cita.
- `telas/telas.md` diz o que cada tela mostra e de onde veio.

## Motion (Remotion)
- Cada peça é uma composição própria para conferir sozinha (`npx remotion still <Peça> out/x.png --frame=N`); a montagem final junta todas numa só.
- Cores e fonte vêm só de `motor/src/marca.json`. Nenhum componente usa cor fixa.
- Peças prontas no motor: `FundoEscuro`/`FundoClaro`, `TextoCinetico`, `Cursor` (com ondas de clique), `Camera`, `Legendas`, `util/homografia` (encaixa uma interface numa tela de celular/notebook filmada).
- Anime com `interpolate` e as curvas de `tema.ts` (`curva.suave` para câmera e janelas, `curva.saida` para entradas). Animações do produto mais **lentas** do que parecem certas no estúdio: a pessoa precisa ler.
- A mídia precisa estar em `motion/public/` (o `staticFile()` só enxerga ali). Copie lá a mídia aprovada; o original fica na pasta da etapa.
- Faça os tempos virarem dados (`linha.json`, constantes no topo) para mudar o corte sem tocar nos componentes.

## Cenas de IA (vídeo e imagem)
Use IA para o que só a IA faz (pessoas, lugares, metáforas), nunca para interface, logo ou número.
- Cada plano tem uma pasta com `plano.md`: intenção, primeiro e último quadro, ação, prompt, duração.
- Um **revisor** (subagente, prompt em `05-claude-code.md`) confere o plano antes de gerar e o resultado depois.
- Gere primeiro os **quadros** (barato), aprove, só então o vídeo. Prompt no positivo, com ordem das ações, direções na tela e quantidades; no máximo duas ações principais.
- O que a IA erra: mãos com objeto pequeno, texto, reflexo, pessoas que se cruzam, luz que muda, pessoa falando. Evite no roteiro do plano.
- **Tela real dentro de cena de IA:** peça um aparelho com a tela lisa de uma cor, rastreie os 4 cantos quadro a quadro e encaixe a interface com `util/homografia.ts`. Se o rosto/mãos cobrem a tela, use um matte.
- **Pós de cada clipe:** corrija cor para casar com a marca; teste de cinza e de celular.
- Divulgação: confira os termos do gerador para uso comercial e as regras de conteúdo sintético da plataforma onde vai passar. Registre em `licencas.md`.

## Som
**Música**
- Só com licença (biblioteca da empresa, Artlist, Epidemic Sound…), registrada em `licencas.md`.
- Energia segue a estrutura: contida na dor, sobe na virada, constante nos recursos, resolve na cartela.
- Ouça **a faixa inteira** antes de usar: já aconteceu de uma música gerada ter textura de voz humana no meio. Para música gerada por IA peça explicitamente *"no human voice of any kind"* e gere uma faixa só para conferir antes de gastar mais.
- Para esticar ou encurtar sem pulo, repita **uma frase musical inteira** (4 compassos) num ponto onde os compassos são "gêmeos" (`ferramentas/musica-compassos.py` ajuda a achar).
- **Duck:** abaixe a música quando a voz fala (curva de volume ligada às falas).

**Voz**
- Pode ser de uma pessoa, da empresa ou sintética (ElevenLabs etc., com ok do gasto).
- **Gere o áudio primeiro, avalie, só depois ponha no vídeo.** É barato errar no áudio e caro no render.
- Modelos de voz sintética tendem a ler **palavra isolada** ("E-mail.", "Agenda.") como inglês: gere **frases completas em português**, e escreva termos estrangeiros como se pronunciam ("imêil").
- Use frase com problema só para refazer a frase, não o texto todo; emende no silêncio e ouça a emenda.
- Transcreva (`faster-whisper`), compare com o roteiro (≥ 95% das palavras iguais, nenhuma palavra do roteiro faltando, exceto nome próprio) e use o **tempo de cada palavra do whisper**, não o alinhamento do provedor.
- Meça o ritmo real (palavras/s) e recalcule a duração do roteiro.
- Clonagem de voz: só da própria pessoa, com autorização (regra 12).
- **A montagem segue a voz:** cortes e entradas caem nas palavras, não o contrário. `ferramentas/envelope-voz.py` extrai a energia da voz por quadro para animar uma onda que reage de verdade à fala.

**Efeitos**
- Um clique no clique do cursor, um sopro nas passagens, um "pop" leve nos cartões; ~10 dB abaixo da voz, cada um preso ao quadro do evento. Todos com licença.

**Final:** −14 LUFS e pico ≤ −1 dBTP. `ferramentas/exportar.py` mede, aplica o ganho exato e um limitador.

**Sem som:** muita gente assiste mudo. O texto na tela conta a história sozinho e a entrega leva `.srt`.

## Versão vertical (9:16) de verdade
Uma faixa de vídeo no meio da tela **não é** versão vertical. Faça assim:
1. Mantenha a composição horizontal como está (é a aprovada).
2. Crie uma composição 1080×1920 que a **filma com uma câmera** (`pecas/Camera.tsx`): pontos-chave `[quadro, foco x, foco y, escala]` que levam a câmera para onde a ação está em cada cena (rosto, cartão, cursor, tabela).
3. Para cenas que não funcionam estreitas (texto largo, grades, constelações), leia o contexto `FormatoVertical` (`useVertical()`) e reorganize só nesse modo; no 16:9 nada muda.
4. Estenda os fundos para cima e para baixo (a câmera enxerga além do palco: `JANELA_V` em `formato.ts`).
5. Faixa de cima: a marca. Faixa de baixo: legendas grandes (`Legendas`), pois quase todo mundo assiste mudo. Não repita em legenda o que já está escrito na imagem.
6. **Áreas seguras de Reels/Shorts/Stories:** nada importante nos ~250 px de cima nem nos ~380 px de baixo.
7. Confira por folha de contato, quadro a quadro das trocas de cena, e leia o texto em 640 px.
`ExemploVertical` no motor mostra o padrão completo.
