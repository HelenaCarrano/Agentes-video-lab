# Trabalhando com o Claude Code

## Como conduzir
- **Uma conversa só, com subagentes.** Quem aprova fala só com o agente principal. O que precisa de olhar limpo vai para um subagente com briefing curto: leitor cego, revisores, análise de muitas imagens. O briefing é por **caminho de arquivo**, sem colar conteúdo; o subagente devolve só a conclusão.
- **Conversa longa custa mais que modelo caro.** Cada resposta relê a conversa inteira, imagens incluídas. Olhe folhas de contato, não dezenas de stills; deixe análises grandes para subagentes; mantenha resumos curtos; guarde o estado em disco (`estado.md`), não na conversa.
- **Retomar ou chamar de novo.** Para ajuste pequeno logo depois da entrega (poucos minutos), retome o mesmo subagente (contexto em cache, sai barato). Depois de uma pausa maior, chame um novo com briefing curto.
- **Subagente trava em pedido de permissão.** Libere em `.claude/settings.json` só os comandos de rotina, cada um pelo nome (`npx remotion`, `ffmpeg`, os scripts de `ferramentas/` pelo caminho). Não libere `node` nem `python` inteiros. **Nunca libere nada que gere com custo** (geradores de voz, imagem ou vídeo).
- **Agente editado no meio da sessão não muda.** O Claude Code carrega `.claude/agents/*.md` no começo; se editar, mande o agente ler o arquivo.
- Antes de chamar a pessoa por um bloqueio, tente o caminho que já funcionou e diga o que tentou.

## Prompts dos subagentes

**Leitor cego** (passo 02):
> Você nunca ouviu falar deste produto nem desta empresa. Leia só o arquivo `<caminho>/leitura-cega.txt`: o vídeo batida a batida, com o que aparece na tela, o texto escrito e a fala. A linha "imagem" é a descrição de quem escreveu e pode ter nomes internos; conte como visto só o que ela diz que aparece. Não abra mais nada. Devolva, curto:
> 1. **O que entendi:** em duas ou três frases, do que é o vídeo e o que ele quer que eu faça. Se não der para dizer em uma frase, diga isso.
> 2. **Onde me perdi:** cada ponto com o tempo e o porquê (palavra que não conheço, imagem que não bate com a fala, salto sem ligação, coisa citada antes de aparecer), ou "nenhum".
> 3. **Primeiros três segundos:** eu continuaria assistindo? Por quê, em uma linha.
>
> Não sugira texto novo.

**Revisor de plano de IA** (antes de gerar os quadros e antes de gerar o vídeo):
> Você só aponta erros e não muda arquivos. Leia `ia/<id>/plano.md` e, se já existirem, olhe `<id>-inicio.png` e `<id>-fim.png`. Confira: todo objeto usado na ação já está no primeiro quadro; entre os quadros só muda o que deve mudar; esquerda e direita batem com o prompt; a ação cabe na duração (no máximo duas ações principais); não há nada do que a IA erra (mãos com objeto pequeno, texto, reflexo, pessoas se cruzando, luz mudando, pessoa falando); o prompt está no positivo, com a ordem das ações, as direções na tela e as quantidades; não há interface, logo ou texto gerado por IA. Responda "passou" ou "não passou", com a lista do que corrigir em ordem de gravidade.

**Revisor final** (passo 09):
> Você revisa um vídeo que não ajudou a fazer, e não corrige nada.
> 1. Antes de qualquer outro arquivo, olhe `<folha.png>` e `<passagens.png>` e leia `<transcricao.txt>`. Escreva em duas ou três frases a história que entendeu, e o que não entendeu.
> 2. Só então leia `roteiro.md` e `fatos.md`, e confira: cada fala sobre o produto bate com os fatos; não aparece dado real, URL interna nem recurso não lançado; não há texto cortado, errado ou ilegível no tamanho do celular; não há defeito de IA (mãos, rostos, objetos que mudam, salto de cor ou luz, boca mexendo); não há trecho de mais de ~3 s sem nada novo; a cartela e o botão se leem.
> 3. Separe os **graves** (o espectador não entende, fato errado, algo proibido aparece) dos **pequenos**, cada um com o tempo e a etapa dona: roteiro, telas, motion, IA, som ou montagem.
> 4. Diga o que não consegue avaliar: o movimento entre os quadros, o ritmo, a música, a voz.

## Armadilhas já encontradas
- Voz estranha "por baixo" do vídeo: era a **música** (textura de voz na faixa), não a locução. Isole cada faixa e ouça antes de regerar qualquer coisa paga.
- Palavras soltas na voz sintética saem em inglês: use frases completas.
- Frase longa cortada em pedaços para dividir por tela perde a pronúncia: prefira uma frase por tela.
- Emendas de música soam como pulo: repita uma frase de 4 compassos num ponto de compassos gêmeos.
- Mudar a versão que já foi aprovada sem pedirem: congele (regra 13).
