
def get_legal_chars(string):
    if not string:
        return string
    return ''.join(c for c in string if c == ' ' or c == '-' or c.isalnum())
