# FizzBuzz Microservices

Система из четырёх микросервисов на FastAPI, совместно
решающих задачу FizzBuzz. Сервисы общаются друг с другом по протоколу HTTP.

Пользователь отправляет число в сервис `main`, тот опрашивает `fizz` и
`buzz`, передаёт их результаты в `concat` и возвращает итог.

- `fizz` - если число делится на 3
- `buzz` - если число делится на 5
- `fizzbuzz` - если делится и на 3, и на 5
- иначе - исходное число строкой

## Порты

| Сервис | Порт | Endpoint                      |
| ------ | ---- | ----------------------------- |
| main   | 8000 | `POST /fizzbuzz`              |
| fizz   | 8001 | `GET /fizz?value=...`         |
| buzz   | 8002 | `GET /buzz?value=...`         |
| concat | 8003 | `GET /concat?lhs=...&rhs=...` |

Формат ответа у всех сервисов идентичный: `{"result": "..."}`.

## Запуск

### Способ 1. Локально

Подготовка окружения:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install fastapi "uvicorn[standard]" httpx pydantic
```

Затем в каждом терминале запустить свой сервис (сначала
fizz/buzz/concat, потом main):

```bash
# fizz
cd fizz
uvicorn main:app --reload --port 8001

# buzz
cd buzz
uvicorn main:app --reload --port 8002

# concat
cd concat
uvicorn main:app --reload --port 8003

# main (последним)
cd main
uvicorn main:app --reload --port 8000
```

### Способ 2. Docker

Из корневой папки:

```bash
docker compose up --build
```

## Документация и интерфейсы

После запуска для каждого сервиса доступны:
- Swagger UI: `http://localhost:<порт>/docs`
- ReDoc: `http://localhost:<порт>/redoc`

## Примеры запросов

```bash
curl -X POST http://localhost:8000/fizzbuzz -H "Content-Type: application/json" -d "{\"value\": 15}"
# {"result": "fizzbuzz"}

curl -X POST http://localhost:8000/fizzbuzz -H "Content-Type: application/json" -d "{\"value\": 9}"
# {"result": "fizz"}

curl -X POST http://localhost:8000/fizzbuzz -H "Content-Type: application/json" -d "{\"value\": 10}"
# {"result": "buzz"}

curl -X POST http://localhost:8000/fizzbuzz -H "Content-Type: application/json" -d "{\"value\": 7}"
# {"result": "7"}
```

Проверка состояния:

```bash
curl http://localhost:8000/health
# {"status": "ok", "dependencies": {"fizz": "up", "buzz": "up", "concat": "up"}}
```

## Реализация

- Андрей - сервис fizz
- Михаил - сервисы buzz и concat
- Игорь - сервис main 