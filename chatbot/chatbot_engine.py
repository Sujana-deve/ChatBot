# chatbot/chatbot_engine.py
import re
from datetime import datetime

from chatbot.intent_classifier import predict_intent_with_confidence
from chatbot.modules.weather_module import get_weather_by_place
from chatbot.modules.calculator_module import calculate
from chatbot.modules.wiki_module import search_wiki
from chatbot.modules.task_manager import init_db, add_task, show_tasks

CONFIDENCE_THRESHOLD = 0.65  # slightly stricter

init_db()

def get_response(user_input, session_context=None):
    """
    Returns a chatbot response string.
    session_context can be used later for memory/personalization.
    """
    # 1) Quick rule-based math detection
    if re.search(r"[\d\.\+\-\*\/\^\(\)=]|solve|integrate|differentiate|derivative", user_input.lower()):
        return calculate(user_input)

    # 2) Predict intent
    intent, conf = predict_intent_with_confidence(user_input)

    # 3) Handle low-confidence fallback
    if conf < CONFIDENCE_THRESHOLD:
        # Check weather keywords first
        low = user_input.lower()
        weather_keywords = ["weather", "temperature", "forecast", "rain", "snow", "cloud"]
        if any(k in low for k in weather_keywords):
            tokens = user_input.split()
            place = tokens[-1] if len(tokens) > 1 else None
            if place:
                geo, msg = get_weather_by_place(place)
                if geo:
                    return msg
        # Otherwise fallback to Wikipedia
        wiki_ans = search_wiki(user_input)
        return f"(fallback) {wiki_ans}"

    # 4) Route according to intent
    if intent == "greeting":
        return "Hello! How can I help you today?"
    elif intent == "goodbye":
        return "Goodbye! Have a great day!"
    elif intent == "thanks":
        return "You're welcome!"
    elif intent == "joke":
        return "Why don’t scientists trust atoms? Because they make up everything!"
    elif intent == "capabilities":
        return "I can tell you the weather, solve math problems, manage tasks, tell jokes, and fetch info from Wikipedia."
    elif intent == "weather":
        # Try to extract place
        m = re.search(r"in\s+([A-Za-z \-]+)", user_input)
        if m:
            place = m.group(1).strip()
            geo, msg = get_weather_by_place(place)
            return msg
        return "Please tell me the city (e.g., 'What's the weather in Tokyo?')."
    elif intent == "task_add":
        task = user_input
        for s in ["add task", "remind me to", "remind me", "add"]:
            task = task.replace(s, "")
        task = task.strip(" .")
        return add_task(task)
    elif intent == "task_show":
        return show_tasks()
    elif intent == "calculator":
        return calculate(user_input)
    elif intent == "time_date":
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')} and today is {now.strftime('%A, %B %d, %Y')}."
    elif intent == "wiki_search":
        return search_wiki(user_input)

    # Default fallback
    return search_wiki(user_input)
