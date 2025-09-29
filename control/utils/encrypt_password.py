from argon2 import PasswordHasher

def encrypt_password(password):
    ph = PasswordHasher()
    return ph.hash(password)

def verify_password(hashed_password, password):
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
        return True
    except:
        return False