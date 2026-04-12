import hashlib
import unidecode


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_login(full_name: str):
    parts = full_name.strip().split()
    i, o, f = parts[1][0], parts[2][0], parts[0]
    login = f"{i}.{o}.{f}"
    return unidecode.unidecode(login.lower()).replace("'", "")
