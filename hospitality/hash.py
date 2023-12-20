import hashlib


def generate_md5(user_string, user_id):
    hashed_string = hashlib.md5(user_string.encode("UTF-8"))
    return "{}_{}".format(hashed_string.hexdigest(), user_id)
