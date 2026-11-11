import { Composition } from "remotion";
import { VIDEO } from "./tema";
import { DURACAO_EXEMPLO, Exemplo, ExemploVertical } from "./Exemplo";

// Registre aqui cada composição do vídeo. A montagem final é UMA composição que junta as cenas.
export const RemotionRoot: React.FC = () => {
  const base = { fps: VIDEO.fps };
  return (
    <>
      <Composition id="Exemplo" component={Exemplo} durationInFrames={DURACAO_EXEMPLO} width={VIDEO.largura} height={VIDEO.altura} {...base} />
      <Composition id="ExemploVertical" component={ExemploVertical} durationInFrames={DURACAO_EXEMPLO} width={1080} height={1920} {...base} />
    </>
  );
};
