import hashlib
import unidecode
from models import Employee


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_login_variants(full_name: str):
    parts = full_name.strip().split()

    surname = unidecode.unidecode(parts[0].lower()).replace("'", "")
    name = unidecode.unidecode(parts[1].lower()).replace("'", "")
    patronymic = unidecode.unidecode(parts[2].lower()).replace("'", "")

    variants = []

    for i in range(1, len(name) + 1):
        for j in range(1, len(patronymic) + 1):
            variants.append(f"{name[:i]}.{patronymic[:j]}.{surname}")

    return variants


def generate_login(db, full_name: str, current_employee_id: int = None):
    variants = generate_login_variants(full_name)

    for login in variants:
        query = db.query(Employee).filter(Employee.login == login)

        if current_employee_id:
            query = query.filter(Employee.id != current_employee_id)
        existing = query.first()

        if not existing:
            return login

    parts = full_name.strip().split()

    surname = unidecode.unidecode(parts[0].lower()).replace("'", "")
    name = unidecode.unidecode(parts[1].lower()).replace("'", "")
    patronymic = unidecode.unidecode(parts[2].lower()).replace("'", "")

    return f"{name}.{patronymic}.{surname}"
