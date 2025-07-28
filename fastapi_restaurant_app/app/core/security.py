from passlib.hash import pbkdf2_sha256 as hash


def hash_password(password: str):
    return hash.hash(password)

def verify_password(plain: str, hashed: str):
    return hash.verify(plain, hashed)
