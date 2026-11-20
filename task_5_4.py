"""Задание 5.4 — статистика работы поддержки."""
import json
from datetime import datetime

import pandas as pd

from hf_client import APIError, ask_ai, log

df = pd.read_csv("reviews.csv", encoding="utf-8")

results = []
for review in df["review"]:
    try:
        r = ask_ai(review)
    except APIError as e:
        log.error("Отзыв пропущен: %s", e)
        continue
    results.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "review": review,
        "sentiment": r["label"],
        "score": r["score"],
        "elapsed_sec": r["elapsed_sec"],
    })

with open("support_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

total = len(results)
if total == 0:
    print("Нет ни одного обработанного отзыва — проверьте ключ и лог support.log")
else:
    negatives = [r for r in results if r["sentiment"] == "NEGATIVE"]
    avg_time = sum(r["elapsed_sec"] for r in results) / total
    print(f"Обработано: {total} отзывов")
    print(f"Негативных: {len(negatives)} ({len(negatives) / total:.0%})")
    print(f"Среднее время: {avg_time:.2f} с")
    if negatives:
        worst = max(negatives, key=lambda r: r["score"])  # самая уверенная NEGATIVE
        print(f"Самый негативный: '{worst['review']}' ({worst['sentiment']}, {worst['score']})")
