# tests/test_intents.py
from chatbot.intent_classifier import predict_intent_with_confidence

cases = [
    ("Who is Nikola Tesla?", "wiki_search"),
    ("What's the weather in London?", "weather"),
    ("Add buy groceries to my list", "task_add"),
    ("Show my tasks", "task_show"),
    ("Calculate 12 * (5+3)", "calculator"),
    ("Hello, how are you?", "chitchat"),
]

for text, expected in cases:
    pred, conf = predict_intent_with_confidence(text)
    print(f"Input: {text}\n Pred: {pred} (conf={conf:.2f})  Expected: {expected}\n")
