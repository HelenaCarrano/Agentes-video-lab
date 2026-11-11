# A equipe de agentes

Cada etapa do fluxo tem um **subagente** com uma responsabilidade só, definido em `agentes/<nome>.md` (frontmatter do Claude Code). `ferramentas/novo-video.py` copia todos para `projetos/<nome>/.claude/agents/`, e o `CLAUDE.md` do projeto transforma o agente principal em **diretor**, que coordena os outros.

```
                      ┌──────────── diretor (agente principal) ────────────┐
     você ⇄ perguntas │  estado · pedidos · decisões · gastos · paradas    │
                      └───┬───────┬────────┬────────┬────────┬───────┬─────┘
                          ▼       ▼        ▼        ▼        ▼       ▼
                  analista-de-  pesquisador  roteirista  designer  diretor  produtor
                  referência    -de-fatos        │       -de-motion  -de-ia  -de-som
                          │                 leitor-cego                          │
                          └────────────► molde.md ──► roteiro ──► cenas ──► montador ──► revisor-final
```

| Agente | Responsabilidade | Lê | Escreve |
|---|---|---|---|
| `analista-de-referencia` | engenharia reversa do vídeo de referência (link ou arquivo) | vídeo, folha, transcrição | `analise.md`, `molde.md` |
| `pesquisador-de-fatos` | verdade sobre o produto, com fonte | código, docs, site | `fatos.md` |
| `roteirista` | direções, roteiro, duração pela voz | `molde.md`, `fatos.md` | `direcoes.md`, `roteiro.md`, `leitura-cega.txt` |
| `leitor-cego` | testa se o roteiro se entende sem contexto | só `leitura-cega.txt` | resposta curta |
| `designer-de-motion` | cenas em Remotion com a marca | roteiro, capturas | `motion/src/` |
| `diretor-de-ia` | planos de IA e revisão | roteiro | `ia/<id>/plano.md` |
| `produtor-de-som` | voz, música, efeitos, volume | roteiro, áudios | plano de som, `licencas.md` |
| `montador` | montagem, vertical, exportação | tudo acima | prévias, entrega |
| `revisor-final` | revisão sem contexto | folha, passagens, transcrição | lista de problemas |

## Por que subagentes
- **Olhar limpo:** o leitor cego e o revisor final começam sem o contexto de quem escreveu; por isso acham o que o autor não vê.
- **Contexto barato:** análise de muitas imagens e leitura de código ficam fora da conversa principal; volta só a conclusão.
- **Responsabilidade única:** cada agente tem um critério claro de "pronto" e regras próprias.

## Regras da equipe
- Só o **diretor** fala com a pessoa e só ele gera coisas pagas (com o ok).
- O briefing vai **por caminho de arquivo**, sem colar conteúdo.
- Subagentes que rodam sozinhos travam em pedido de permissão: libere em `.claude/settings.json` só comandos de rotina (`npx remotion`, `ffmpeg`, os scripts de `ferramentas/` pelo caminho). **Nunca libere nada que gere com custo.**
- O Claude Code carrega `.claude/agents/` no começo da sessão; se editar um agente, reinicie ou mande o agente ler o arquivo.
- Para ajuste pequeno logo depois, retome o mesmo subagente (contexto em cache); depois de uma pausa, chame um novo com briefing curto.

## Criar um agente novo
Copie um arquivo de `agentes/`, mude `name`, `description` (diga **quando** usar) e `tools` (o mínimo necessário) e escreva as instruções como um briefing: entrada, o que fazer, regras e o que devolver.
