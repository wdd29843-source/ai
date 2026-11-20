"""Задание 5.1 — AI-помощник поддержки: определяем тональность отзыва."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()  # читает файл .env и кладёт HF_API_KEY в переменные окружения

API_KEY = os.getenv("HF_API_KEY")
MODEL = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"


def ask_ai(prompt):
    """POST-запрос к модели. Возвращает (метка, уверенность)."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
    response.raise_for_status()
    data = response.json()
    # Ответ приходит как [[{label, score}, {label, score}]]
    items = data[0] if isinstance(data[0], list) else data
    best = max(items, key=lambda x: x["score"])
    return best["label"], best["score"]


if __name__ == "__main__":
    reviews = [
        "Доставили быстро, всё супер!",
        "Товар пришёл разбитым, ужас.",
        "Нормально, но могло быть лучше.",
    ]
    for review in reviews:
        label, score = ask_ai(review)
        print(f"'{review}' -> {label} ({score:.3f})")
