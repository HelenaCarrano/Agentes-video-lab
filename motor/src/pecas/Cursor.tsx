import { interpolate, useCurrentFrame } from "remotion";
import { cor } from "../tema";

/** Cursor desenhado: seta com sombra; uma onda a cada clique; encolhe um pouco enquanto segura. */
export const Cursor: React.FC<{ x: number; y: number; cliques: number[]; segurando?: boolean }> = ({ x, y, cliques, segurando }) => {
  const f = useCurrentFrame();
  const ondas = cliques
    .map((c) => f - c)
    .filter((d) => d >= 0 && d < 16)
    .map((d) => d / 16);
  const aperto = cliques.some((c) => f - c >= 0 && f - c < 4) || segurando ? 0.88 : 1;
  return (
    <div style={{ position: "absolute", left: x, top: y, pointerEvents: "none", zIndex: 50 }}>
      {ondas.map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: -28 * (0.4 + p),
            top: -28 * (0.4 + p),
            width: 56 * (0.4 + p),
            height: 56 * (0.4 + p),
            borderRadius: "50%",
            border: `3px solid ${cor.destaque}`,
            opacity: interpolate(p, [0, 1], [0.9, 0]),
          }}
        />
      ))}
      <svg width="40" height="48" viewBox="0 0 20 24" style={{ transform: `scale(${aperto})`, transformOrigin: "0 0", filter: "drop-shadow(0 4px 6px rgba(0,0,0,0.35))" }}>
        <path d="M1 1 L1 19 L6 14.5 L9.5 22 L12.5 20.7 L9 13.3 L15.5 13.3 Z" fill="#fff" stroke={cor.principalEscuro} strokeWidth="1.4" strokeLinejoin="round" />
      </svg>
    </div>
  );
};
