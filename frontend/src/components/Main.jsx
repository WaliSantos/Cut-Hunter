import Section from "./Section";

function Main({
    loading,
    erro,
    cortes,
    segundoAtivo,
    setSegundoAtivo,
    copiarTitulo,
    copiadoIndex,
    playerSrc,
    formatarTempo
}){
    return (

        <main className="max-w-6xl mx-auto px-6">
        {loading && (
          <div className="text-center py-12 px-4 bg-zinc-900 border border-zinc-800 rounded-xl text-zinc-400">
            <div className="w-9 h-9 border-3 border-zinc-800 border-t-red-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p>Lendo a transcrição e analisando os melhores momentos com IA... (cerca de 15s)</p>
          </div>
        )}

        {erro && (
          <div className="text-center py-8 px-4 bg-red-950/30 border border-red-600 rounded-xl text-red-300">
            {erro}
          </div>
        )}

        {cortes.length > 0 && (
          <Section
            segundoAtivo={segundoAtivo}
            setSegundoAtivo={setSegundoAtivo}
            copiarTitulo={copiarTitulo}
            copiadoIndex={copiadoIndex}
            playerSrc={playerSrc}
            cortes={cortes}
            formatarTempo={formatarTempo}
          />
        )}
      </main>
    )
}

export default Main;