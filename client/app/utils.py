def undo_slug(text: str):
    return " ".join([x.capitalize() for x in text.split("-")])
