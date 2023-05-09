import random
import string


def generate_random_string(length: int, *, include_punctuation: bool = False) -> str:
    """ Generates a random string using lower & upper case characters, as well as numbers. Punctuation characters can be optionally included as well. """
    if length <= 0:
        raise ValueError("Length must be positive.")
    return ''.join(random.choice(string.ascii_letters + string.digits + (string.punctuation if include_punctuation else '')) for i in range(length))
