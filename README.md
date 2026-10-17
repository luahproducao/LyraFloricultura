# Site da Lyra Floricultura, atualizado pelo Notion

O site é uma página (`index.html`) que lê o catálogo de `plants.json`. Um robô do GitHub busca o banco **Catálogo do site (estoque)** no Notion a cada 30 minutos, atualiza o `plants.json` e as fotos, e publica o site de novo. Quem cuida do estoque só mexe no Notion.

## Colocar no ar (uma vez só)

1. **Repositório:** no GitHub, crie um repositório público chamado `lyra-floricultura` e envie TODOS os arquivos desta pasta, inclusive as pastas `fotos/` e `.github/workflows/`. Pelo computador, é só arrastar a pasta. Pelo celular, use **Add file > Create new file** e digite o caminho (ex.: `.github/workflows/atualizar-site.yml`) para criar as pastas.
2. **Pages:** em **Settings > Pages**, em **Source**, escolha **GitHub Actions**.
3. **Integração do Notion:** em https://www.notion.so/profile/integrations, crie uma integração interna e copie o **Internal Integration Secret**. Depois abra o banco **Catálogo do site (estoque)**, toque em **...** > **Connections** e adicione a integração (sem isso o robô não enxerga o banco).
4. **ID do banco:** `226b52841d404bd18852d631535cea65`
5. **Segredos:** no GitHub, em **Settings > Secrets and variables > Actions > New repository secret**, crie:
   - `NOTION_TOKEN`: o secret copiado no passo 3.
   - `NOTION_DB_ID`: o ID do passo 4.
6. **Primeira publicação:** em **Actions > Atualizar site a partir do Notion > Run workflow**. Quando terminar, o site abre em `https://SEU-USUARIO.github.io/lyra-floricultura/`.

## Dia a dia no Notion

| Campo | O que faz no site |
|---|---|
| Publicar | Só aparece no site se estiver marcado. Desmarque para esconder. |
| Disponível hoje | Mostra o selo "Disponível hoje" no card. |
| Estoque | Com 0, mostra "Esgotada". Vazio, não mostra nada. |
| Preço / Faixa de preço | Preço do card. A faixa (texto) é para itens sob encomenda. |
| Categoria | Define o filtro. Use "Sob encomenda" para itens sem preço fixo. |
| Foto | Envie uma foto: o robô baixa, reduz e publica. |
| Frase, Nome científico, Sobre, Benefícios, Simbolismo e crenças, Luz, Água, Dica de cuidado, Bom para presentear, Aviso de pets | Textos da ficha. Se ficar vazio em uma planta que já existe, vale o texto padrão do site. |
| Tóxica para pets | Mostra o aviso de toxicidade. |
| Ordem | Posição no catálogo. |

Para uma planta nova: crie a linha, marque **Publicar**, preencha nome, categoria, preço e foto. Em até 30 minutos ela aparece. Para atualizar na hora, rode o fluxo em **Actions > Run workflow**.

## Observações
- O robô só lê linhas com **Publicar** marcado e só as colunas listadas acima. Mesmo assim, não coloque no banco informações internas, porque o preço e o texto ficam públicos.
- Fotos de iPhone (HEIC) são convertidas para JPEG e reduzidas para até 900 px.
- Nunca coloque o token do Notion dentro dos arquivos. Ele fica só em **Secrets**.
- O GitHub pode atrasar os agendamentos e pausar fluxos agendados em repositórios sem atividade por 60 dias. O robô registra uma atualização a cada 20 dias para manter ativo. Se o fluxo for pausado, é só reativar na aba **Actions**.
- A consulta pela foto funciona aqui como atalho: a cliente descreve a planta e envia a foto pelo WhatsApp da Lyra.
