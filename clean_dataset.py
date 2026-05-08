import re

def clean_sentence(s):
    s = s.strip()

    # Too short
    if len(s) < 40:
        return None

    # Remove junk text
    junk_patterns = [
        r"subscribe", r"advertisement", r"copyright",
        r"follow us", r"login", r"sign in", r"newsletter",
        r"cookie policy", r"privacy policy", r"terms of",
        r"©", r"all rights reserved", r"breaking news"
    ]

    for p in junk_patterns:
        if re.search(p, s, re.IGNORECASE):
            return None

    # Remove crime, violence, politics
    bad_topics = [
        "murder", "killed", "dead", "shot", "arrested", "police",
        "court", "crime", "violence", "rape", "assault", "battery",
        "politics", "election", "minister", "bjp", "congress", "trump"
    ]

    for p in bad_topics:
        if p in s.lower():
            return None

    # Remove weird characters
    s = re.sub(r"[\n\r\t]+", " ", s)

    return s


def clean_text(text):
    sentences = re.split(r"[.!?]", text)
    clean = []

    for s in sentences:
        s = clean_sentence(s)
        if s:
            clean.append(s.strip())

    return clean
