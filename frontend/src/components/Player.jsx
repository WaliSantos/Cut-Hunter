function Player({playerSrc}) {
    return (
        <div className="lg:col-span-7 lg:sticky lg:top-6">
              <div className="relative w-full aspect-video rounded-xl overflow-hidden border border-zinc-800 bg-black shadow-2xl">
                <iframe
                  src={playerSrc}
                  title="YouTube video player"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="absolute inset-0 w-full h-full border-0"
                />
              </div>
              <p className="mt-3 text-sm text-zinc-400">
                Clique em qualquer cartão ao lado para saltar direto para o segundo exato no vídeo.
              </p>
            </div>
    )
}

export default Player;