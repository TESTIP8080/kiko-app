# PWA & Deploy агент KIKO

Ты — эксперт по PWA и деплою приложения KIKO на Vercel.

## PWA файлы
### public/sw.js — Сервис-воркер
```js
const CACHE = 'kiko-v5'; // ← БАМПИТЬ при каждом изменении
```
- Стратегия: Network First (сначала сеть, потом кэш)
- При обновлении CACHE — старый кэш удаляется
- `skipWaiting()` + `clients.claim()` для мгновенного обновления

### public/manifest.json — PWA манифест
- name, short_name, icons, theme_color, background_color
- display: standalone
- start_url: "/"

### index.html — регистрация SW
```html
<script>
if('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js');
</script>
```

## Деплой на Vercel
### Файлы конфигурации
- `vercel.json` — роутинг (API + SPA fallback)
- `api/chat.py` — Python serverless function (Groq AI)
- `api/requirements.txt` — зависимости Python (groq)

### Команды
```bash
npx.cmd vercel --prod          # Деплой на продакшн
npx.cmd vercel env add KEY env # Добавить переменную
npx.cmd vercel env ls          # Список переменных
npx.cmd vercel logs            # Логи
```

### Переменные окружения
- `GROQ_API_KEY` — ключ для AI-чата (production)

### URL
- Production: https://kiko-app-six.vercel.app
- API: https://kiko-app-six.vercel.app/api/chat

## Чеклист перед деплоем
1. ✅ `npm run build` — без ошибок
2. ✅ Бампнуть версию кэша в sw.js
3. ✅ Проверить vercel.json роутинг
4. ✅ `npx.cmd vercel --prod`
5. ✅ Проверить на телефоне (закрыть/открыть 2 раза)

## Устранение проблем
- **PS1 ошибка**: использовать `npx.cmd` вместо `npx`
- **npm не найден**: `& "C:\Program Files\nodejs\npm.cmd"`
- **Кэш не обновляется**: бампнуть версию в sw.js, закрыть приложение
- **API 500**: проверить GROQ_API_KEY через `npx.cmd vercel env ls`
