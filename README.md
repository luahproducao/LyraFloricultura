# Lyra Floricultura: catálogo, encomendas e cuidados

Site de uma página só (`index.html`) com o catálogo de plantas, encomenda pelo WhatsApp e fichas de cuidados. Não precisa de servidor nem de instalação.

## Colocar no ar com o GitHub Pages
1. No GitHub, crie um repositório **público** chamado `lyra-floricultura`.
2. Em **Add file > Upload files**, envie `index.html` e `README.md` e confirme (**Commit changes**).
3. Vá em **Settings > Pages**. Em **Branch**, escolha `main` e a pasta `/ (root)`, e salve.
4. Em 1 a 2 minutos o site abre em `https://SEU-USUARIO.github.io/lyra-floricultura/`.

## Como atualizar
Abra `index.html` no GitHub e toque no lápis (Edit). Procure por:
- `var ZAP=` : número do WhatsApp da Lyra.
- `var P=[` : lista de plantas (nome, tipo, preço, frase, foto, luz, água, dica, aviso de pets).
- `var FR=` : frete por região.
- `var X=[` : fichas completas (nome científico, benefícios, simbolismo, cuidados, presente, pets).

Depois de editar, toque em **Commit changes**. O site atualiza sozinho em poucos minutos.

## Observações
- As fotos estão dentro do `index.html`. Para trocar por fotos melhores, peça ajuda para gerar um novo arquivo.
- A consulta pela foto funciona aqui como atalho para o WhatsApp: a cliente descreve a planta e envia a foto para a Lyra.
- O site não guarda dados das clientes. O pedido só existe na mensagem enviada ao WhatsApp.
- Para usar um endereço próprio (ex.: `lyraflores.com.br`), compre o domínio e configure em **Settings > Pages > Custom domain**.
