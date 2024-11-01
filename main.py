import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import getpass



def derive_key_from_password(password: str, salt: bytes) -> bytes:
    # Generate a key from a password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(file_path: str, password: str) -> None:
    # Encrypt a file with a password
    salt = os.urandom(16)  # Generate a new salt
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        data = file.read()

    encrypted_data = fernet.encrypt(data)

    with open(file_path + ".enc", 'wb') as file:
        file.write(salt + encrypted_data)  # Save salt and encrypted data together

def decrypt_file(encrypted_file_path: str, password: str, output_file_path: str) -> None:
    # Decrypt a file with a password
    with open(encrypted_file_path, 'rb') as file:
        salt = file.read(16)  # Extract salt
        encrypted_data = file.read()  # Read the encrypted data

    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)


menu = \
"""
1 - encrypt file
2 - decrypt file
0 - exit
"""

while True:
    print(menu)
    r = input('> ')
    r.strip()
    if r.isdigit():
        if r == '0':
            break

        elif r == '1':
            while True:
                filepath = input('file name > ')
                if not os.path.exists(filepath):
                    print('file not found, enter it again')
                else:
                    break
            password = getpass.getpass("enter your password > ")
            encrypt_file(filepath, password)

        elif r == '2':
            while True:
                filepath = input('file name > ')
                if not os.path.exists(filepath):
                    print('file not found, enter it again')
                else:
                    break
            password = getpass.getpass("enter your password > ")
            if filepath[-4:] == '.enc':
                decrypt_file(filepath, password, filepath[:-4])
            else:
                output_file_path = input('output file name > ')
                decrypt_file(filepath, password, output_file_path)

        else:
            print('not a valid input')

    else:
        print('not a valid input')