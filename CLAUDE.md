# Agentes Video Lab: instruções para o agente

Você produz vídeos de produto seguindo o fluxo deste repositório. Antes de qualquer coisa, leia:

1. `guia/02-regras.md`: regras que não mudam (paradas, créditos, fatos com fonte, nada de dado real, nunca `git push`).
2. `guia/01-fluxo.md`: o fluxo passo a passo e onde parar.
3. `guia/03-referencias.md`: como partir de um vídeo de referência (`ferramentas/analisar-referencia.py`).
4. `guia/04-producao.md` e `guia/05-claude-code.md` quando chegar na produção e na revisão.

Estrutura: `motor/` é o Remotion base (genérico, cores em `motor/src/marca.json`); `ferramentas/` são os scripts; `modelo/` são os documentos em branco; `projetos/<nome>/` é cada vídeo (fora do git). Crie um projeto novo com `python ferramentas/novo-video.py <nome>`.

Mantenha o código e o guia **genéricos**: nenhum nome de empresa, cor fixa ou dado de cliente em `motor/`, `ferramentas/`, `guia/` ou `modelo/`. O que é de um vídeo específico vai só em `projetos/`.

Responda a quem aprova em português, curto, e sempre diga o que você não consegue avaliar (ritmo, música, timbre).
