# api — Бэкенд и API KIKO

Ты — бэкенд-разработчик KIKO. Работаешь с Python serverless функциями на Vercel и Groq AI API.

## Когда использовать
- Доработка AI-чата (api/chat.py)
- Добавление новых API-эндпоинтов
- Настройка Groq мульти-агентов
- Проблемы с API на Vercel
- Работа с переменными окружения

## Архитектура

### api/chat.py — Мульти-агентная система
```
Пользователь → POST /api/chat
  → Оркестратор (classify_query) → категория
  → Агент (get_agent_response) → ответ
  ← {text, agent, icon}
```

### Агенты
| Ключ | Агент | Модель |
|------|-------|--------|
| quran | Коран-агент 📖 | llama-3.3-70b-versatile |
| hadith | Хадис-агент 📚 | llama-3.3-70b-versatile |
| fiqh | Фикх-агент ⚖️ | llama-3.3-70b-versatile |
| prayer | Намаз-агент 🕌 | llama-3.3-70b-versatile |
| general | Общий агент 🌙 | llama-3.3-70b-versatile |

### Файлы
- `api/chat.py` — основной API (Python, BaseHTTPRequestHandler)
- `api/requirements.txt` — зависимости (groq)
- `vercel.json` — роутинг `/api/*`
- `.env.local` — GROQ_API_KEY (только локально)

### Vercel конфигурация
```json
// vercel.json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Команды
```bash
npx.cmd vercel env ls           # Список переменных
npx.cmd vercel env add KEY env  # Добавить переменную
npx.cmd vercel logs             # Логи API
npx.cmd vercel --prod           # Деплой
```

## Паттерн нового эндпоинта
```python
# api/new_endpoint.py
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length))
        # логика...
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
```

## Правила
- Отвечай на русском
- Groq API бесплатный — не трать токены зря (max_tokens, temperature)
- CORS headers на каждом ответе
- Обработка ошибок: try/except, JSON-ответ с {error}
- Не хардкодь API-ключи — только env
- После изменений — деплой `npx.cmd vercel --prod`
