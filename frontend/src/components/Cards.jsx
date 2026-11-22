function Cards({
    segundoAtivo,
    setSegundoAtivo,
    copiarTitulo,
    copiadoIndex,
    cortes,
    formatarTempo
}){
    return (

        <div className="lg:col-span-5">
              <h2 className="text-xl font-bold mb-4">
                Cortes Sugeridos ({cortes.length})
              </h2>
              <div className="flex flex-col gap-4">
                {cortes.map((corte, index) => {
                  const ativo = segundoAtivo === corte.segundo_inicio; 
                  return (
                    <div
                      key={index}
                      onClick={() => setSegundoAtivo(corte.segundo_inicio)}
                      className={`p-5 rounded-xl border cursor-pointer transition-all ${
                        ativo
                          ? "border-red-600 bg-red-950/20"
                          : "border-zinc-800 bg-zinc-900 hover:bg-zinc-800/80 hover:border-zinc-700 hover:-translate-y-0.5"
                      }`}
                    >
                      <div className="flex justify-between items-center mb-2.5">
                        <span className="bg-red-600 text-white font-bold text-xs px-2.5 py-1 rounded-md">
                          ▶ {formatarTempo(corte.segundo_inicio)}
                        </span>
                        <span className="text-xs font-semibold text-zinc-400 bg-zinc-800 px-2.5 py-1 rounded-md">
                          {corte.categoria}
                        </span>
                      </div>

                      <h3 className="text-base font-bold text-zinc-100 mb-1.5 leading-snug">
                        {corte.titulo_sugerido}
                      </h3>
                      <p className="text-sm text-zinc-400 mb-4 leading-relaxed">
                        {corte.motivo}
                      </p>

                      <button
                        type="button"
                        onClick={(e) => copiarTitulo(e, corte.titulo_sugerido, index)}
                        className="text-xs font-medium text-zinc-200 border border-zinc-700 hover:border-zinc-500 px-3 py-1.5 rounded-md transition-colors cursor-pointer"
                      >
                        {copiadoIndex === index ? "Título copiado!" : "Copiar título sugerido"}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
    )
}

export default Cards;