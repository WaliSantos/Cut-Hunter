## Etapa 1: Preparação do terreno (Ambiente e Chave da IA)
Antes de escrever lógica, vamos deixar a oficina pronta e leve.

Criar a pasta do projeto: Montar a estrutura básica (backend e frontend) no seu computador.

Gerar a chave da API: Criar sua conta gratuita no Google AI Studio e pegar sua GEMINI_API_KEY (sem precisar cadastrar cartão de crédito).

Configurar o Python: Criar um ambiente virtual (venv) — boa prática essencial de engenharia de software para isolar bibliotecas — e instalar apenas quatro pacotes leves: fastapi, uvicorn, youtube-transcript-api e google-genai.

## Etapa 2: O motor em Python (Backend + IA)
Aqui você vai perder o medo de backend fazendo tudo funcionar primeiro sem interface gráfica.

Extrair a legenda: Fazer uma função que recebe o link de uma live pós-jogo do Canto Rubro-Negro e puxa o texto com os segundos exatos.

Calibrar o prompt e o JSON: Ensinar o Gemini a agir como um editor de cortes de futebol, adicionando um mini-glossário do Vitória (para a IA não confundir nomes de jogadores ou "Barradão") e obrigando a resposta a voltar em JSON estruturado (minuto inicial, título chamativo, categoria e resumo).

Subir o servidor local: Colocar isso dentro do FastAPI e testar pelo navegador usando o painel automático que o próprio FastAPI cria (/docs), vendo os cortes aparecerem na tela antes mesmo de criar o frontend.

## Etapa 3: A vitrine rubro-negra (Frontend)
É a hora de usar o que você já sabe de web para transformar aqueles dados brutos em um produto de verdade.

Estrutura e visual: Criar o index.html e o style.css com tema escuro, identidade discreta em vermelho e preto, campo para colar o link do YouTube e player embutido.

Conexão com o Python: No app.js, usar o fetch() para mandar o link para o seu backend, mostrar uma animação de "Analisando live..." e desenhar os cards dos cortes na tela.

Interatividade no player: Programar o clique no card para fazer o vídeo do YouTube pular automaticamente para o segundo exato do corte sugerido, além de um botão para copiar o título pronto.

## Etapa 4: Colocando no ar (GitHub e Deploy Gratuito)
Um projeto local não dá para mandar por e-mail. Vamos publicar tudo de graça na nuvem.

Segurança e Git: Configurar o arquivo .gitignore (para nunca vazar sua chave da API) e subir o código organizado para um repositório no seu GitHub.

Hospedagem gratuita: Subir o backend em Python no Render (ou Railway) e o frontend na Vercel (ou GitHub Pages), gerando um link público oficial que abre de qualquer celular ou computador.

## Etapa 5: Portfólio e abordagem ao canal
Com o link funcionando, transformamos o código em oportunidade profissional.

Documentação de engenheiro: Escrever um README.md caprichado no GitHub explicando o problema resolvido, a arquitetura e prints da tela funcionando — isso brilha aos olhos de recrutadores de estágio.

O e-mail para o Canto Rubro-Negro: Mandar uma mensagem curta e direta para eles com o link da ferramenta no ar e já anexando 3 ou 4 cortes prontos que o seu sistema encontrou na última live deles.