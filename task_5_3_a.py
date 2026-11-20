"""Задание 5.3, сценарий А — чат-бот поддержки с историей."""
import json
import os

from hf_client import APIError, call_model, log

CHAT_MODEL = "microsoft/DialoGPT-medium"
HISTORY_FILE = "support_chat.json"
EOS = "<|endoftext|>"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def bot_reply(history, user_text):
    # DialoGPT ждёт реплики, разделённые EOS-токеном; берём последние 6
    turns = [m["text"] for m in history[-6:]] + [user_text]
    prompt = EOS.join(turns) + EOS
    data, _ = call_model(CHAT_MODEL, {"inputs": prompt})
    text = data[0]["generated_text"] if isinstance(data, list) else data["generated_text"]
    return text[len(prompt):].strip() or text.strip()


def main():
    history = load_history()
    print("Чат поддержки. Напишите «оператор», чтобы позвать менеджера, «выход» — завершить.")
    while True:
        user_text = input("Вы: ").strip()
        if not user_text:
            continue
        if user_text.lower() == "выход":
            break

        history.append({"role": "user", "text": user_text})

        if user_text.lower() == "оператор":
            reply = "Передаю старшему менеджеру"
            log.info("Клиент запросил оператора")
        else:
            try:
                reply = bot_reply(history[:-1], user_text)
            except APIError as e:
                reply = "Сейчас бот недоступен, попробуйте позже."
                log.error("Ошибка бота: %s", e)

        history.append({"role": "bot", "text": reply})
        save_history(history)
        print("Бот:", reply)


if __name__ == "__main__":
    main()
