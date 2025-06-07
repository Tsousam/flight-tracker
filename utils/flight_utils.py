import re

def extract_airport_shorten(airport):
    if not airport:
        return None

    match = re.search(r"\((\w{3})\)", airport)
    if match:
        return match.group(1)
    return None
