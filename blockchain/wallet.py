import hashlib
import json
import os
from ecdsa import SigningKey, SECP256k1

class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            self.private_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        else:
            self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self._generate_address()

    def _generate_address(self):
        pubkey_bytes = self.public_key.to_string()
        sha256 = hashlib.sha256(pubkey_bytes).hexdigest()
        return sha256

    def get_keys(self):
        return {
            "private_key": self.private_key.to_string().hex(),
            "public_key": self.public_key.to_string().hex(),
            "address": self.address
        }

    def save_to_file(self, filepath):
        data = self.get_keys()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return Wallet(private_key=data["private_key"])
