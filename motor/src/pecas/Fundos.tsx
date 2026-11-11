import { AbsoluteFill, useCurrentFrame } from "remotion";
import { cor } from "../tema";

/** Fundo escuro da marca: dois brilhos que derivam devagar. */
export const FundoEscuro: React.FC = () => {
  const f = useCurrentFrame();
  const x1 = 28 + Math.sin(f / 90) * 4;
  const y1 = 30 + Math.cos(f / 110) * 3;
  const x2 = 78 + Math.cos(f / 100) * 4;
  const y2 = 78 + Math.sin(f / 120) * 3;
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(60% 70% at ${x1}% ${y1}%, ${cor.principal} 0%, transparent 70%),
          radial-gradient(45% 55% at ${x2}% ${y2}%, ${cor.destaque}2a 0%, transparent 70%),
          linear-gradient(160deg, ${cor.principalEscuro} 0%, ${cor.principalProfundo} 100%)`,
      }}
    />
  );
};

/** Fundo claro (dentro do produto): bolhas muito desfocadas nas cores da marca. */
export const FundoClaro: React.FC = () => {
  const f = useCurrentFrame();
  const bolha = (x: number, y: number, tam: number, c: string, fase: number): React.CSSProperties => ({
    position: "absolute",
    left: `${x + Math.sin(f / 80 + fase) * 2}%`,
    top: `${y + Math.cos(f / 95 + fase) * 2}%`,
    width: tam,
    height: tam,
    borderRadius: "50%",
    background: c,
    filter: "blur(120px)",
    transform: "translate(-50%, -50%)",
  });
  return (
    <AbsoluteFill style={{ background: cor.fundoClaro, overflow: "hidden" }}>
      <div style={bolha(8, 12, 700, `${cor.principal}38`, 0)} />
      <div style={bolha(94, 88, 760, `${cor.destaque}1f`, 2)} />
      <div style={bolha(88, 6, 520, "rgba(90, 110, 200, 0.16)", 4)} />
    </AbsoluteFill>
  );
};
