from random import randint


def hash_message(length: int = 25) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

    return "".join(map(lambda i: chars[randint(0, len(chars) - 1)], range(length)))
