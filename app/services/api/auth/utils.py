import hashlib


def hash_password(password: str) -> str:
    """Hash a password."""
    pw_bytes = password.encode("utf-8")
    hashed_pw = hashlib.sha256(pw_bytes).hexdigest()
    return hashed_pw


def verify_password(password: str, password_in_db: str) -> bool:
    """Verify a password."""
    pw = bytes(password, "utf-8")
    return hashlib.sha256(pw).hexdigest() == password_in_db
