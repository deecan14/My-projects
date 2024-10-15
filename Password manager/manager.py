from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

# Function to write a new key to a file (uncomment if you need to generate a new key)
"""
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
"""


def load_key():
    with open("key.key", "rb") as file:
        key = file.read()
    return key


def derive_key(master_pwd, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_pwd))


boss_pwd = input("What is the master password? ")
salt = b'\x00'*16
key = derive_key(boss_pwd.encode(), salt)
fer = Fernet(key)


def view():
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            if "|" in data:  # Check if the line contains the "|" separator
                try:
                    user, passw = data.split("|")
                    print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())
                except ValueError:
                    print("Error decrypting password for", user)
            else:
                print("Invalid line format:", data)



def add():
    name = input("Account Name: ")
    pwd = input("Password: ")

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")


while True:
    mode = input("Would you like to add a new password or view the existing ones (view, or add), press q to quit? ").lower()
    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")

