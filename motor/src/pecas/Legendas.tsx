import { interpolate, useCurrentFrame } from "remotion";
import { cor, curva, fonte } from "../tema";

const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export type Legenda = { ini: number; fim: number; texto: string };

/**
 * Legenda grande para versão de celular (maioria assiste sem som). `ini` e `fim` em quadros.
 * Gere o JSON a partir do .srt com `ferramentas/srt-para-json.py`.
 * `top` põe a legenda fora das áreas onde Reels/Shorts/Stories colocam botões (nada importante nos 250 px de cima
 * nem nos 380 px de baixo de um quadro 1080×1920).
 */
export const Legendas: React.FC<{ legendas: Legenda[]; top?: number; claro?: boolean; tamanho?: number }> = ({ legendas, top = 1565, claro = false, tamanho = 50 }) => {
  const f = useCurrentFrame();
  const L = legendas.find((l) => f >= l.ini - 2 && f < l.fim + 4);
  if (!L) return null;
  const o = interpolate(f, [L.ini - 2, L.ini + 5, L.fim - 2, L.fim + 4], [0, 1, 1, 0], cl);
  const y = interpolate(f, [L.ini - 2, L.ini + 8], [14, 0], { ...cl, easing: curva.saida });
  return (
    <div style={{ position: "absolute", left: 70, right: 70, top, display: "flex", justifyContent: "center", opacity: o, transform: `translateY(${y}px)` }}>
      <div style={{ textAlign: "center", fontFamily: fonte, fontSize: tamanho, fontWeight: 700, lineHeight: 1.25, letterSpacing: -0.5, color: claro ? cor.texto : cor.branco, textWrap: "balance" } as React.CSSProperties}>{L.texto}</div>
    </div>
  );
};
