import Player from "./Player";
import Cards from "./Cards"

function Section({
    segundoAtivo,
    setSegundoAtivo,
    copiarTitulo,
    copiadoIndex,
    playerSrc,
    cortes,
    formatarTempo
}) {
  return (
    <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Coluna do Player */}
            <Player playerSrc={playerSrc} />

            {/* Coluna dos Cartões */}
            <Cards
              segundoAtivo={segundoAtivo}
              setSegundoAtivo={setSegundoAtivo}
              copiarTitulo={copiarTitulo}
              copiadoIndex={copiadoIndex}
              cortes={cortes}
              formatarTempo={formatarTempo}
            />
    </section>
  );
}

export default Section;