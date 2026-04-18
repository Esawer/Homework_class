import random, re


def generate_code():
    final_code = ""

    while len(final_code) < 6:
        character = chr(random.randint(45, 175))
        if re.findall(r"[a-zA-Z0-9]", character):
            final_code += character

    return final_code
