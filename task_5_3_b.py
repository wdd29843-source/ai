"""Задание 5.3, сценарий Б — автоответы на отзывы."""
import pandas as pd

from hf_client import APIError, ask_ai, log

NEGATIVE_REPLY = "Здравствуйте! Приносим извинения за доставленные неудобства. Свяжемся с вами в течение 24 часов."
POSITIVE_REPLY = "Спасибо за отзыв! Рады, что вам понравилось."

df = pd.read_csv("reviews.csv", encoding="utf-8")

sentiments, replies = [], []
for review in df["review"]:
    try:
        label = ask_ai(review)["label"]
    except APIError as e:
        log.error("Отзыв пропущен: %s", e)
        label = "ERROR"
    sentiments.append(label)
    if label == "NEGATIVE":
        replies.append(NEGATIVE_REPLY)
    elif label == "POSITIVE":
        replies.append(POSITIVE_REPLY)
    else:
        replies.append("")

df["sentiment"] = sentiments
df["reply"] = replies
df.to_csv("reviews_with_replies.csv", index=False, encoding="utf-8-sig")
print(f"Готово: {len(df)} отзывов -> reviews_with_replies.csv")
