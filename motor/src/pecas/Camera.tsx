import { interpolate, useCurrentFrame } from "remotion";
import { curva } from "../tema";

const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** Ponto-chave da câmera: [quadro, foco x, foco y, escala], com x e y em coordenadas da composição original. */
export type KeyframeCamera = [number, number, number, number];

const valor = (cam: KeyframeCamera[], f: number, i: 1 | 2 | 3) => {
  if (f <= cam[0][0]) return cam[0][i];
  for (let k = 1; k < cam.length; k++) {
    if (f <= cam[k][0]) {
      const p = interpolate(f, [cam[k - 1][0], cam[k][0]], [0, 1], { ...cl, easing: curva.suave });
      return cam[k - 1][i] + (cam[k][i] - cam[k - 1][i]) * p;
    }
  }
  return cam[cam.length - 1][i];
};

/**
 * Filma uma composição pronta (por ex. 1920×1080) com uma câmera que segue a ação, dentro de um quadro de outro
 * tamanho (por ex. 1080×1920 para Reels/Shorts). É assim que sai uma versão vertical que não é só uma faixa no meio:
 * a câmera vai para onde a ação está em cada cena. Como tudo é vetor, a interface continua nítida.
 *
 *   <Camera origem={{ w: 1920, h: 1080 }} destino={{ w: 1080, h: 1920 }} keyframes={[[0, 960, 540, 1], [90, 1300, 540, 1.2]]}>
 *     <MinhaComposicao />
 *   </Camera>
 */
export const Camera: React.FC<{
  origem: { w: number; h: number };
  destino: { w: number; h: number };
  keyframes: KeyframeCamera[];
  children: React.ReactNode;
}> = ({ origem, destino, keyframes, children }) => {
  const f = useCurrentFrame();
  const s = valor(keyframes, f, 3);
  const tx = destino.w / 2 - valor(keyframes, f, 1) * s;
  const ty = destino.h / 2 - valor(keyframes, f, 2) * s;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: origem.w, height: origem.h, transformOrigin: "0 0", transform: `translate(${tx}px, ${ty}px) scale(${s})` }}>
      {children}
    </div>
  );
};
