# .hash_password.py
import bcrypt
import sys

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # encode the password
    return hashed.decode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(hash_password(sys.argv[1]))
    else:
        print("No password provided")
