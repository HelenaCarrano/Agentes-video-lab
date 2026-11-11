import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { cor, curva, fonte, NOME_MARCA, raio, sombra } from "./tema";
import { FundoClaro, FundoEscuro } from "./pecas/Fundos";
import { TextoCinetico } from "./pecas/TextoCinetico";
import { Cursor } from "./pecas/Cursor";
import { Camera } from "./pecas/Camera";
import { FormatoVertical, JANELA_V, useVertical } from "./formato";

const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const DURACAO_EXEMPLO = 240; // 8 s a 30 q/s

/**
 * Composição de EXEMPLO: abertura com texto cinético sobre o fundo da marca, depois uma "janela de produto" com
 * cursor clicando num cartão. Serve de ponto de partida: copie, renomeie e troque as cenas pelas do roteiro.
 */
export const Exemplo: React.FC = () => {
  const f = useCurrentFrame();
  // no vertical, cenas de texto se reorganizam (coluna estreita); a câmera cuida do resto
  const vertical = useVertical();
  const claro = interpolate(f, [100, 130], [0, 1], cl);
  const janela = interpolate(f, [110, 150], [0, 1], { ...cl, easing: curva.saida });
  return (
    <AbsoluteFill style={{ fontFamily: fonte }}>
      {/* no vertical a câmera enxerga além do palco (JANELA_V em formato.ts): estenda os fundos para cima e para baixo */}
      <AbsoluteFill style={{ top: vertical ? JANELA_V.y : 0, height: vertical ? JANELA_V.h : "100%" }}>
        <FundoEscuro />
        <AbsoluteFill style={{ opacity: claro }}>
          <FundoClaro />
        </AbsoluteFill>
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: 1 - claro, padding: vertical ? "0 480px" : 160 }}>
        <TextoCinetico frase="Escreva aqui a frase do gancho" inicios={[8, 16, 24, 32, 40, 48]} destaque={4} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 360, top: 190, width: 1200, height: 700, borderRadius: raio.janela, background: cor.superficie, boxShadow: sombra.janela, opacity: janela, transform: `translateY(${(1 - janela) * 40}px)`, padding: 40 }}>
        <div style={{ fontSize: 30, fontWeight: 700, color: cor.texto }}>{NOME_MARCA}</div>
        <div style={{ marginTop: 30, display: "flex", gap: 24 }}>
          {["Indicador A", "Indicador B", "Indicador C"].map((t, i) => (
            <div key={t} style={{ flex: 1, height: 220, borderRadius: raio.cartao, background: cor.superficieAlta, border: `2px solid ${i === 1 ? cor.destaque : cor.borda}`, padding: 24, fontSize: 24, color: cor.textoSuave }}>
              {t}
            </div>
          ))}
        </div>
      </div>
      <div style={{ opacity: janela }}>
        <Cursor x={interpolate(f, [150, 190], [1400, 960], { ...cl, easing: curva.suave })} y={interpolate(f, [150, 190], [800, 420], { ...cl, easing: curva.suave })} cliques={[194]} />
      </div>
    </AbsoluteFill>
  );
};

/** A mesma composição filmada por uma câmera num quadro vertical 1080×1920. */
export const ExemploVertical: React.FC = () => (
  <AbsoluteFill style={{ background: cor.principalProfundo }}>
    <Camera
      origem={{ w: 1920, h: 1080 }}
      destino={{ w: 1080, h: 1920 }}
      keyframes={[
        [0, 960, 540, 1],
        [110, 960, 540, 1],
        [150, 960, 520, 0.88],
        [200, 960, 420, 0.88],
        [240, 960, 420, 0.88],
      ]}
    >
      <FormatoVertical.Provider value={true}>
        <Exemplo />
      </FormatoVertical.Provider>
    </Camera>
  </AbsoluteFill>
);
