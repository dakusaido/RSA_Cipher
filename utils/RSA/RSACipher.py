import sys

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import new as Random

from Crypto.PublicKey.RSA import RsaKey
from Crypto.Math.Numbers import Integer

from base64 import b64encode
from base64 import b64decode

from utils.Exceptions.LenErrorException import LenError


class RSACipher:
    def __init__(self, private_key=None):
        self.key = private_key

    def generate_key(self, key_length: int) -> None:
        if key_length % 1024:
            raise LenError(f"key_length cannot be {key_length}")

        rng = Random().read
        self.key = RSA.generate(key_length, rng)

    def encrypt(self, data: str, private_key: RSA = None) -> str:
        plaintext = b64encode(data.encode())
        rsa_encryption_cipher = PKCS1_v1_5.new(private_key or self.key)
        ciphertext = rsa_encryption_cipher.encrypt(plaintext)
        return b64encode(ciphertext).decode()

    def decrypt(self, data: str, private_key: RSA = None) -> str:
        ciphertext = b64decode(data.encode())
        rsa_decryption_cipher = PKCS1_v1_5.new(private_key or self.key)
        plaintext = rsa_decryption_cipher.decrypt(ciphertext, 16)
        return b64decode(plaintext).decode()

    def save_private_key(self, path):
        components = ['n', 'e', 'd', 'p', 'q', 'u']

        try:
            with open(path, mode='w', encoding='utf-8') as file:
                for component in components:
                    file.write(component + '\t=\t' + self.key.__dict__.get('_' + component).__str__() + '\n')

        except Exception as e:
            print(e)


if __name__ == '__main__':
    from config.projectPath.getProjectPath import get_project_path
    project_path = get_project_path()

    with open(project_path + r'result.env', mode='r', encoding='utf-8') as result:
        encrypted = result.readline().split()[-1]

    with open(project_path + r'config\personKey\personKey.env', mode='r', encoding='utf-8') as file:
        data = list(map(lambda number: Integer(int(number)), map(lambda x: x[4:], file.readlines())))

        decrypted = RSACipher().decrypt(encrypted, RsaKey(
            n=data[0],
            e=data[1],
            d=data[2],
            p=data[3],
            q=data[4],
            u=data[5]
        ))

        print(decrypted)
