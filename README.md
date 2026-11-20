# День 5 — Интеграция AI-сервисов через API

Анализ тональности отзывов через Hugging Face Inference API.

## Запуск
1. `python -m venv .venv` и активировать
2. `pip install -r requirements.txt`
3. Скопировать `.env.example` в `.env` и вписать свой `HF_API_KEY`
4. `python task_5_1.py`, `python task_5_3_b.py`, `python task_5_4.py`

## Файлы
- `task_5_1.py` — ask_ai, проверка на трёх отзывах
- `hf_client.py` — retry, обработка 401/429/503, логирование (5.2)
- `task_5_3_a.py` — чат-бот с историей (сценарий А)
- `task_5_3_b.py` — автоответы на отзывы (сценарий Б)
- `task_5_4.py` — статистика, `support_results.json`
