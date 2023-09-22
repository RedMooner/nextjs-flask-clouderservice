#!/usr/bin/env python3
import os
import fs
import gnupg
from fs import open_fs
gpg = gnupg.GPG(homedir="/home/redmoon/.gnupg")
home_fs = open_fs(".")
if os.path.exists("signatures/"):
    print("Signatures directory already created")
else:
    home_fs.makedir(u"signatures")
    print("Created signatures directory")


def generate_key( first_name, last_name, domain, passphrase=None):
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

def encrypt(key_name):
    pass


def decrypt(key_name):
    pass


if __name__ == '__main__':
    pass
