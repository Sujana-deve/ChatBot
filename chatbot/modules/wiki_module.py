# chatbot/modules/wiki_module.py
import wikipedia

def search_wiki(query):
    try:
        # attempt to find the best page
        results = wikipedia.search(query, results=3)
        if not results:
            return "I couldn't find information on that. Try rephrasing."
        page = results[0]
        summary = wikipedia.summary(page, sentences=2)
        return f"{summary}\n\n(Topic: {page})"
    except Exception as e:
        return "Sorry, couldn't fetch info right now."
