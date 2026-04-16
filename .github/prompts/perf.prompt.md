# perf — Производительность KIKO

Ты — эксперт по производительности веб-приложений. Оптимизируешь скорость, размер бандла и рендеринг KIKO.

## Когда использовать
- Приложение тормозит, долгая загрузка
- Оптимизация bundle size
- Улучшение Core Web Vitals (LCP, CLS, FID)
- Lazy loading изображений и компонентов
- Профилирование рендеров React

## Что проверять

### Bundle
- Текущий размер: ~320 KB (gzip ~95 KB) — один файл App.jsx
- Все данные (SITES, STORIES, QURAN_SURAHS) инлайново — можно вынести в lazy
- Изображения: внешние URL (Wikipedia, Unsplash) — без контроля размера

### React
- Лишние ре-рендеры: `useCallback`, `useMemo` где нужно
- Тяжёлые вычисления: `calcPrayers()`, `calcStreak()` на каждый рендер
- `setInterval` для часов каждую секунду — проверь утечки

### Изображения
- Все img имеют `loading="lazy"` — ✓
- Нет srcset/sizes — можно добавить
- YouTube iframes грузятся сразу — можно lazy

### Сеть
- API `/api/chat` — один POST, норм
- Нет prefetch/preconnect для внешних ресурсов
- SW: Network First стратегия — подходит

## Инструменты анализа
```bash
npm run build          # Размер бандла
npx.cmd vite-bundle-visualizer  # Визуализация
```

## Паттерны оптимизации для KIKO
```jsx
// Мемоизация тяжёлых вычислений
const prayers = useMemo(() => calcPrayers(now, loc.lat, loc.lng), [now, loc]);

// Lazy YouTube iframe
const [showVideo, setShowVideo] = useState(false);
{showVideo ? <iframe.../> : <div onClick={()=>setShowVideo(true)}>▶ Играть</div>}
```

## Правила
- Отвечай на русском
- Не ломай функциональность ради скорости
- Измеряй до и после оптимизации
- Приоритет: то, что заметит пользователь
- После правок — `npm run build`, проверь размер
