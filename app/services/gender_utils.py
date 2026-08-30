import re

def normalise_gender(value):
    if not value:
        return None

    value = value.lower()

    if re.search(
        r"\b(women|female|girls?|girl)\b",
        value
    ):
        return "Female"

    if re.search(
        r"\b(men|male|boys?|boy)\b",
        value
    ):
        return "Male"

    return None