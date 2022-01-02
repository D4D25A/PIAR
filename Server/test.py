import string, random
def generate_random_id():
    legal_chars = string.ascii_letters + string.digits
    return "".join(random.choice(legal_chars) for _ in range(40))



print(generate_random_id())