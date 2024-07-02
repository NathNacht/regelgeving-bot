import re


def make_safe_filename(filename):
    # Characters not allowed on Linux and Windows
    invalid_chars = r'[\/:*?"<>|\\]'
    safe_filename = re.sub(invalid_chars, '_', filename)
    return safe_filename