import { interpolate, useCurrentFrame } from "remotion";
import { cor, curva, fonte } from "../tema";

const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/**
 * Texto cinético: cada palavra entra no quadro dado em `inicios` (um por palavra, em quadros).
 * Dica do fluxo: 2–6 palavras por linha, até 2 linhas, uma palavra destacada (`destaque` = índice).
 * Os `inicios` devem cair nas palavras da voz (use o tempo de cada palavra da transcrição).
 */
export const TextoCinetico: React.FC<{
  frase: string;
  inicios: number[];
  destaque?: number;
  tamanho?: number;
  escuro?: boolean;
}> = ({ frase, inicios, destaque, tamanho = 96, escuro = true }) => {
  const f = useCurrentFrame();
  const palavras = frase.split(" ");
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: `0 ${tamanho * 0.28}px`, fontFamily: fonte, fontSize: tamanho, fontWeight: 800, letterSpacing: -tamanho * 0.02, lineHeight: 1.12 }}>
      {palavras.map((p, i) => {
        const t = interpolate(f, [inicios[i] ?? 0, (inicios[i] ?? 0) + 14], [0, 1], { ...cl, easing: curva.saida });
        const base = escuro ? cor.branco : cor.texto;
        return (
          <span key={i} style={{ opacity: t, transform: `translateY(${(1 - t) * 28}px)`, color: i === destaque ? (escuro ? cor.destaqueNoEscuro : cor.destaque) : base }}>
            {p}
          </span>
        );
      })}
    </div>
  );
};
