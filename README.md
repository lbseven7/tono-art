# Tono — Escala de Cinzas e Valores Tonais para Artistas

Plataforma web interativa de estudo de **valores tonais** e **escala de cinzas** para artistas. Oferece ferramentas para treinar o olhar, preparar referências (converter, posterizar, risco linear, quadricular) e analisar luz e sombra.

- Site: https://tono.art.br
- Autor: Leo Barbosa

## Funcionalidades

### Ferramentas livres
- **Início** — visão geral e acesso rápido
- **TonoCast** — aulas de teoria em áudio
- **Escala** — escala de cinzas interativa com guia de misturas e pigmentos
- **Treino** — treino de leitura de valores
- **Risco** — risco linear a partir de uma foto

### Ferramentas PRO
- **Converter** — converte a foto para escala de cinzas
- **Posterizar** — reduz a imagem a zonas de valor
- **Janela** — simulador de janela física para isolar detalhes
- **Quadricular** — transferência com grade
- **Ilusão** — estudo de ilusões de óptica
- **Localizar Valor** — identifica o valor de uma região da imagem
- **Extrair Paleta** — extrai paleta de cores de uma foto
- **Exercícios** — 8 semanas de exercícios progressivos
- **Análise de Luz** — direção e zonas de luz
- **Dica de Mestre** — passo a passo comentado de um exercício real

## Estrutura do projeto

```
├── index.html          # Dashboard principal (com área PRO bloqueada)
├── open.html           # Versão aberta/free (sem trava PRO)
├── sales-page.html     # Página de vendas (Hotmart)
├── apresentacao-tono.html
├── og-banner.html      # Banner para Open Graph
├── thumb.html
├── css/
│   ├── input.css             # Entrada Tailwind (tema claro/escuro)
│   ├── tailwind-output.css   # CSS compilado
│   └── tutorial.css
├── js/
│   ├── dashboard.js          # Lógica principal e renderização das telas
│   └── tono-chat-widget.js   # Widget de chat
├── ensino/             # Conteúdo das aulas do TonoCast (markdown)
├── audio/              # Áudios das aulas e comentários
├── images/             # Imagens do site e ilustrações
├── knowledge_base/     # Base de conhecimento
├── docs/               # Textos de vendas, scripts e descrições
├── pdf/
├── scripts/
├── fonts/
└── tailwind.config.js  # Configuração Tailwind (darkMode: class)
```

## Tecnologias

- HTML5, CSS3 e JavaScript vanilla (sem frameworks)
- [Tailwind CSS](https://tailwindcss.com) v3
- Tema claro/escuro via classe `.light` no `<html>` (padrão: claro)
- Internacionalização pt-BR / en / es (chave `tono_lang` em `localStorage`)
- Zero dependências em runtime

## Como rodar

O projeto é estático — basta servir a pasta. Por exemplo:

```bash
# com um servidor simples
npx serve .
```

### Build do CSS (opcional)

```bash
npm install
npm run build:css        # build de produção
npm run watch:css        # watch durante desenvolvimento
```

O HTML carrega `css/tailwind-output.css`, então recompile sempre que alterar `css/input.css` ou adicionar classes novas.

## Personalização

### Tema
O tema é controlado pela classe `.light` na raiz e salvo em `localStorage` (`tono_theme`). O padrão — sem preferência salva — é o tema claro.

### Idiomas
A página detecta `tono_lang` em `localStorage` (padrão `pt`) e troca os textos via `[data-i18n]`.

### Modo PRO
- `index.html` mostra as ferramentas PRO com trava e popup de venda (Hotmart).
- `open.html` é a versão aberta e libera todas as ferramentas (`tono_pro = true`).

## SEO

- Meta tags Open Graph e Twitter Card em todas as páginas
- `hreflang` para pt-br, en-us e es-es
- Dados estruturados `SoftwareApplication` + `Product` com oferta Hotmart
- `sitemap.xml`, `robots.txt` e domínio canônico `https://tono.art.br`

## Scripts de vendas e conteúdo

Os textos comerciais e scripts de vídeo ficam em `docs/`:

- `hotmart-descricao.md` — descrição do produto
- `hotmart-modulos.md` — módulos do curso
- `hotmart-planos.md` — planos e precificação
- `script-apresentacao-tono.md` — roteiro da apresentação
- `script-video-venda.md` — roteiro do vídeo de vendas
