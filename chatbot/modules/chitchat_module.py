import random

responses = {
    "hello": ["Hi!", "Hello there!", "Hey 👋"],
    "how are you": ["I’m doing great!", "All good, thanks!", "Awesome!"],
    "bye": ["Goodbye!", "See you!", "Take care!"]
}

def chat(query):
    for key in responses:
        if key in query.lower():
            return random.choice(responses[key])
    return "I'm not sure what to say 🤔"
