 function Header(
    { handleBuscarCortes, url, setUrl, loading }
 ) {
    return(
        <header className="bg-gradient-to-b from-red-950/40 to-zinc-950 border-b border-zinc-800 py-10 mb-8">
        <div className="max-w-6xl mx-auto px-6">
          <span className="inline-block bg-red-600/15 text-red-500 border border-red-600/40 text-xs font-bold px-3 py-1 rounded-full tracking-wider mb-3">
            FERRAMENTA DE INDICAÇÃO DE CORTES BASEADA EM IA
          </span>
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-2">
            Caçador de Cortes - <span className="text-red-600">IA</span>
          </h1>
          <p className="text-zinc-400 mb-6 max-w-2xl">
            Cole o link de uma live ou pós-jogo do Canto Rubro-Negro para identificar os melhores momentos automaticamente.
          </p>

          <form onSubmit={handleBuscarCortes} className="flex flex-col sm:flex-row gap-3 max-w-2xl">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Ex: https://www.youtube.com/watch?v=DTqaqRj7BNHY"
              required
              className="flex-1 px-4 py-3 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-red-600 transition-colors"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 rounded-lg bg-red-600 hover:bg-red-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold transition-colors cursor-pointer"
            >
              {loading ? "Analisando..." : "Buscar Cortes"}
            </button>
          </form>
        </div>
      </header>
    )
}

export default Header;