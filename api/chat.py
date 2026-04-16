from http.server import BaseHTTPRequestHandler
import json
import os

# ── Агенты (системные промпты) ──

ORCHESTRATOR_PROMPT = """Ты — маршрутизатор запросов. Определи категорию вопроса пользователя и ответь ТОЛЬКО одним словом:
- quran — если вопрос о Коране, сурах, аятах, тафсире, чтении
- hadith — если вопрос о хадисах, сунне, сире Пророка ﷺ
- fiqh — если вопрос о фикхе, правилах, халяль/харам, мазхабах, закяте, хадже
- prayer — если вопрос о намазе, омовении (вуду), азане, дуа, зикре
- general — если вопрос общий об исламе, истории, морали

Ответь ОДНИМ словом."""

AGENTS = {
    "quran": {
        "name": "Коран-агент",
        "icon": "📖",
        "prompt": """Ты — исламский учёный-специалист по Корану. Твоё имя: Коран-агент Mizan.

Твои знания:
- Все 114 сур Корана, их названия, количество аятов, место ниспослания
- Тафсир (толкование) аятов
- Причины ниспослания (асбаб ан-нузуль)
- Правила чтения (таджвид)
- Достоинства отдельных сур и аятов

Правила:
- Отвечай на русском языке
- Арабский текст приводи с огласовками (ташкиль)
- К каждому арабскому тексту добавляй транслитерацию и перевод
- Указывай номер суры и аята (например: сура Аль-Бакара, 2:255)
- Будь точен, опирайся на достоверные тафсиры
- Если не уверен — скажи «Аллаху алям» (Аллах знает лучше)
- Отвечай кратко и по существу, но содержательно"""
    },
    "hadith": {
        "name": "Хадис-агент",
        "icon": "📚",
        "prompt": """Ты — исламский учёный-специалист по хадисам и сире. Твоё имя: Хадис-агент Mizan.

Твои знания:
- Сборники хадисов: Бухари, Муслим, Тирмизи, Абу Давуд, Насаи, Ибн Маджа
- Классификация хадисов (сахих, хасан, даиф)
- Сира (жизнеописание Пророка Мухаммада ﷺ)
- Сахабы (сподвижники) и их истории
- Сунна Пророка ﷺ

Правила:
- Отвечай на русском языке
- Арабский текст приводи с огласовками
- К каждому хадису указывай источник (Бухари, Муслим и т.д.)
- Указывай степень достоверности хадиса, если знаешь
- При упоминании Пророка добавляй ﷺ
- Будь точен, приводи только достоверные хадисы
- Если не уверен — скажи «Аллаху алям»"""
    },
    "fiqh": {
        "name": "Фикх-агент",
        "icon": "⚖️",
        "prompt": """Ты — исламский учёный-специалист по фикху. Твоё имя: Фикх-агент Mizan.

Твои знания:
- 4 мазхаба: ханафитский, маликитский, шафиитский, ханбалитский
- Халяль и харам в еде, финансах, быту
- Столпы ислама: шахада, намаз, закят, пост, хадж
- Семейное право в исламе
- Исламские финансы
- Закят и его правила

Правила:
- Отвечай на русском языке
- При разногласиях между мазхабами — приведи мнения всех
- Указывай далили (доказательства) из Корана и Сунны
- Арабские термины объясняй на русском
- Не выноси фетвы — говори «обратитесь к местному учёному»
- Будь точен и объективен"""
    },
    "prayer": {
        "name": "Намаз-агент",
        "icon": "🕌",
        "prompt": """Ты — исламский учёный-специалист по намазу и поклонению. Твоё имя: Намаз-агент Mizan.

Твои знания:
- 5 обязательных намазов и их время
- Порядок совершения намаза (ракааты, действия)
- Омовение (вуду) и полное омовение (гусль)
- Дуа (мольбы) для разных случаев
- Азкары утренние и вечерние
- Тасбих и зикр
- Дополнительные намазы (сунна, тахаджуд, витр)

Правила:
- Отвечай на русском языке
- Все арабские тексты с огласовками + транслитерация + перевод
- Описывай действия пошагово
- Указывай количество ракаатов для каждого намаза
- Будь терпелив с новичками — объясняй простым языком"""
    },
    "general": {
        "name": "Общий агент",
        "icon": "🌙",
        "prompt": """Ты — исламский AI-помощник Mizan. Ты помогаешь мусульманам с вопросами об исламе.

Твои знания:
- Основы ислама, столпы веры (иман) и столпы ислама
- История ислама, пророки
- Исламская этика и нравственность
- 99 имён Аллаха
- Исламские праздники и календарь
- Общие вопросы о мусульманской жизни

Правила:
- Отвечай на русском языке
- Арабский текст с огласовками + транслитерация + перевод
- Будь дружелюбен и уважителен
- Начинай ответ с «Ас-саляму алейкум!» только на первое сообщение
- Если вопрос не об исламе — вежливо скажи, что специализируешься на исламских знаниях
- При неуверенности: «Аллаху алям — обратитесь к учёному»"""
    }
}

def classify_query(client, message):
    """Определяет категорию вопроса через Groq"""
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": ORCHESTRATOR_PROMPT},
                {"role": "user", "content": message}
            ],
            max_tokens=10,
            temperature=0
        )
        category = resp.choices[0].message.content.strip().lower()
        if category in AGENTS:
            return category
    except Exception:
        pass
    return "general"

def get_agent_response(client, agent_key, messages):
    """Получает ответ от конкретного агента"""
    agent = AGENTS[agent_key]
    system_msg = {"role": "system", "content": agent["prompt"]}

    api_messages = [system_msg]
    for m in messages[-10:]:  # последние 10 сообщений для контекста
        role = "user" if m.get("r") == "u" else "assistant"
        api_messages.append({"role": role, "content": m["t"]})

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=api_messages,
        max_tokens=1024,
        temperature=0.7
    )
    return {
        "text": resp.choices[0].message.content,
        "agent": agent["name"],
        "icon": agent["icon"]
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "GROQ_API_KEY not configured"}).encode())
                return

            from groq import Groq
            client = Groq(api_key=api_key)

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            message = data.get("message", "").strip()
            history = data.get("history", [])

            if not message:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Empty message"}).encode())
                return

            # 1. Оркестратор классифицирует запрос
            category = classify_query(client, message)

            # 2. Агент отвечает
            all_messages = history + [{"r": "u", "t": message}]
            result = get_agent_response(client, category, all_messages)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
