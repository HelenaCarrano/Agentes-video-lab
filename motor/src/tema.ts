import { Easing } from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";
import marca from "./marca.json";

// Tema da marca. Para outra marca: edite marca.json (cores) e, se a fonte não for a Inter, troque o import acima
// por outra de @remotion/google-fonts/<Fonte>. Nenhum componente usa cor fixa.
const { fontFamily } = loadFont("normal", {
  weights: ["400", "500", "600", "700", "800"],
  subsets: ["latin", "latin-ext"],
});

const c = marca.cores;
export const cor = {
  principal: c.principal,
  principalEscuro: c.principalEscuro,
  principalProfundo: c.principalProfundo,
  destaque: c.destaque,
  // destaque para texto sobre o fundo escuro: o vermelho/escuro some no teste de cinza
  destaqueNoEscuro: c.destaqueNoEscuro,
  sucesso: c.sucesso,
  alerta: c.alerta,
  fundoClaro: c.fundoClaro,
  superficie: c.superficie,
  superficieAlta: c.superficieAlta,
  borda: c.borda,
  texto: c.texto,
  textoSuave: c.textoSuave,
  branco: c.branco,
};

export const fonte = fontFamily;
export const raio = { cartao: 18, janela: 22, pilula: 999 };
export const sombra = {
  cartao: "0 24px 60px rgba(0, 0, 0, 0.16), 0 6px 16px rgba(0, 0, 0, 0.08)",
  janela: "0 40px 100px rgba(0, 0, 0, 0.28), 0 10px 30px rgba(0, 0, 0, 0.12)",
};

export const curva = {
  // câmera e janelas
  suave: Easing.bezier(0.65, 0, 0.35, 1),
  // entradas
  saida: Easing.bezier(0.16, 1, 0.3, 1),
};
export const mola = { damping: 16, stiffness: 140, mass: 0.8 };

export const VIDEO = marca.video;
export const NOME_MARCA = marca.nome;
