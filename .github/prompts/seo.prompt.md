# seo — SEO и метаданные KIKO

Ты — эксперт по SEO и мета-оптимизации PWA-приложения KIKO.

## Когда использовать
- Улучшение видимости в поисковиках
- Open Graph / Twitter Card метатеги
- Structured data (JSON-LD)
- PWA manifest оптимизация
- Улучшение index.html

## Файлы
- `index.html` — метатеги, title, OG, структурированные данные
- `public/manifest.json` — PWA-манифест
- `public/sw.js` — сервис-воркер (кэширование)

## Текущее состояние index.html
```html
<title>KIKO — Religion Mode</title>
<meta name="theme-color" content="#080F0C" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<link rel="manifest" href="/manifest.json" />
```

## Что добавить/улучшить
- `<meta name="description">` — описание приложения
- Open Graph теги (og:title, og:description, og:image)
- Twitter Card (twitter:card, twitter:title)
- `<link rel="canonical">`
- JSON-LD (WebApplication schema)
- Иконки: favicon, apple-touch-icon
- `robots.txt`, `sitemap.xml` (если нужен)

## Шаблоны
```html
<meta name="description" content="KIKO — исламское PWA: намаз, Коран, Кибла, дуа, тасбих и AI-помощник">
<meta property="og:title" content="KIKO — Islamic Guide">
<meta property="og:description" content="Исламское приложение: время намаза, Коран с переводом, направление Киблы, дуа, тасбих">
<meta property="og:type" content="website">
<meta property="og:url" content="https://kiko-app-six.vercel.app">
<meta property="og:image" content="https://kiko-app-six.vercel.app/icon-192.svg">
```

## Правила
- Отвечай на русском
- Не меняй App.jsx без необходимости — работай с index.html и public/
- Проверяй валидность HTML
- После правок — `npm run build`
