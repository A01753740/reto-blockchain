"""
wallet.py

Este módulo define la clase Wallet, encargada de generar claves privadas y públicas usando ECDSA
(curva secp256k1), y derivar direcciones SHA-256. También permite guardar y cargar las claves desde archivo.
"""

import hashlib
import json
import os
from ecdsa import SigningKey, SECP256k1

class Wallet:
    """
    Representa una wallet criptográfica basada en ECDSA.

    Atributos:
        private_key (SigningKey): Clave privada ECDSA.
        public_key (VerifyingKey): Clave pública derivada de la privada.
        address (str): Dirección derivada aplicando SHA-256 a la clave pública.
    """

    def __init__(self, private_key=None):
        """
        Inicializa una nueva wallet. Si se proporciona una clave privada, la utiliza;
        de lo contrario, genera una nueva.

        Args:
            private_key (str, opcional): Clave privada en formato hexadecimal.
        """
        if private_key:
            self.private_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        else:
            self.private_key = SigningKey.generate(curve=SECP256k1)

        self.public_key = self.private_key.get_verifying_key()
        self.address = self._generate_address()

    def _generate_address(self):
        """
        Genera la dirección de la wallet aplicando SHA-256 a la clave pública.

        Returns:
            str: Dirección de la wallet en formato hexadecimal.
        """
        pubkey_bytes = self.public_key.to_string()
        sha256 = hashlib.sha256(pubkey_bytes).hexdigest()
        return sha256

    def get_keys(self):
        """
        Devuelve las claves y dirección de la wallet.

        Returns:
            dict: Diccionario con 'private_key', 'public_key' y 'address'.
        """
        return {
            "private_key": self.private_key.to_string().hex(),
            "public_key": self.public_key.to_string().hex(),
            "address": self.address
        }

    def save_to_file(self, filepath):
        """
        Guarda las claves de la wallet en un archivo JSON.

        Args:
            filepath (str): Ruta al archivo de salida.
        """
        data = self.get_keys()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_file(filepath):
        """
        Carga una wallet desde un archivo JSON que contiene la clave privada.

        Args:
            filepath (str): Ruta al archivo con las claves.

        Returns:
            Wallet: Instancia de Wallet reconstruida desde archivo.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        return Wallet(private_key=data["private_key"])
