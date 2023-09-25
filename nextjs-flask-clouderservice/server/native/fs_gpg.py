#!/usr/bin/env python3
import os
import fs
import gnupg
import subprocess
from fs import open_fs


gpg = gnupg.GPG(homedir="/home/redmoon/.gnupg")
home_fs = open_fs(".")

debug_mail = "test.test@mail.ru"
debug_phrase = "123"

if os.path.exists("signatures/"):
    print("Signatures directory already created")
else:
    home_fs.makedir(u"signatures")
    print("Created signatures directory")


def generate_key(first_name, last_name, domain, passphrase=None):
    "Generate a key"
    params = {
        'Key-Type': 'DSA',
        'Key-Length': 1024,
        'Subkey-Type': 'ELG-E',
        'Subkey-Length': 2048,
        'Name-Comment': 'A test user',
        'Expire-Date': 0,
    }
    params['Name-Real'] = '%s %s' % (first_name, last_name)
    params['Name-Email'] = ("%s.%s@%s" %
                            (first_name, last_name, domain)).lower()
    params['Passphrase'] = passphrase
    cmd = gpg.gen_key_input(**params)
    return gpg.gen_key(cmd)


def encrypt():
    open('my-unencrypted.txt', 'w').write('You need to Google Venn diagram.')
    recipient = debug_mail
    subprocess.run(['gpg', '--recipient', recipient, '--encrypt', "my-unencrypted.txt", "-y"])

def decrypt():
    # Укажите путь к файлу, который нужно расшифровать
    input_file = 'my-unencrypted.txt.gpg'
    # Укажите путь для сохранения расшифрованного файла
    output_file = 'file.txt'
    # Запустите команду gpg в терминале
    password = '123'
    result = subprocess.run(['gpg', '--batch', '--passphrase', password, '--output', output_file, '--decrypt', input_file])

    if result.returncode == 0:
        # Расшифровка прошла успешно
        with open(output_file, 'r') as f:
            decrypted_text = f.read()
        print(decrypted_text)
    else:
        # Произошла ошибка при расшифровке
        print('Ошибка расшифровки файла')


        
if __name__ == '__main__':
    pass
