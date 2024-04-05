
import bcrypt


def hash_password(password) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt).decode("utf-8")
    return hashed_password


def verify_password(plain_password, hashed_password) -> bool:
    hashed_password = hashed_password.encode("utf-8")
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

