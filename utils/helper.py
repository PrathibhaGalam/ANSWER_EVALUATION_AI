import re

# Clean text extracted from PDF
def clean_text(text):

    text = text.replace("\n", " ")
    text = text.replace("  ", " ")

    return text


# Limit large answers
def trim_text(text, limit=2000):

    if len(text) > limit:
        return text[:limit]

    return text


# Extract marks from LLM output

def extract_marks(response):

    match = re.search(r"(\d+)/(\d+)", response)

    if match:
        return int(match.group(1))

    return "Not Found"