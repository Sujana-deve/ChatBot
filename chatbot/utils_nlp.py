# chatbot/utils_nlp.py
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_gpe(text, top_k=1):
    """
    Extract GPE (geopolitical entity) tokens (cities/countries).
    Returns a list (may be empty).
    """
    doc = nlp(text)
    gpes = [ent.text for ent in doc.ents if ent.label_ in ("GPE","LOC")]
    # fallback: naive 'in' search for 'in <city>'
    if not gpes:
        # try pattern "in <word...>"
        import re
        m = re.search(r"\bin\s+([A-Za-z \-]+)", text)
        if m:
            candidate = m.group(1).strip()
            # trim at common words
            candidate = candidate.split(" for ")[0].split(" tomorrow")[0]
            gpes = [candidate]
    return gpes[:top_k]
