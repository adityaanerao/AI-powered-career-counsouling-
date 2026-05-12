def analyze_emotion(text):
    text = text.lower()

    if "confused" in text:
        return "Needs Guidance"

    if "interested" in text:
        return "Highly Motivated"

    return "Neutral"