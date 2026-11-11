import { createContext, useContext } from "react";

// Formato da montagem. No vertical (9:16) a composição de 1920×1080 é filmada por uma câmera (VideoVertical.tsx);
// as cenas que precisam de outro arranjo leem este contexto. No 16:9 nada muda.
export const FormatoVertical = createContext(false);
export const useVertical = () => useContext(FormatoVertical);

/** Retângulo (em coordenadas do quadro 1920×1080) que a câmera vertical mostra com o foco em (960, 540) e escala 1. */
export const JANELA_V = { x: 420, y: -420, w: 1080, h: 1920 };
