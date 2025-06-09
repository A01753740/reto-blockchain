"""
transaction.py

Este módulo define las clases Transaction y UTXOManager.

- La clase Transaction representa una transacción basada en el modelo UTXO,
  incluyendo entradas firmadas, salidas y comisiones.
- La clase UTXOManager se encarga de mantener el conjunto actual de salidas no gastadas (UTXOs).
"""

import hashlib
import json
from ecdsa import VerifyingKey, SigningKey, SECP256k1, BadSignatureError

class Transaction:
    """
    Representa una transacción en el modelo UTXO.

    Atributos:
        inputs (list): Lista de entradas, cada una con txid, index y firma.
        outputs (list): Lista de salidas con dirección y cantidad.
        fee (float): Comisión asignada al minero.
        txid (str): Identificador único de la transacción (SHA-256).
    """

    def __init__(self, inputs, outputs, fee=0.0):
        """
        Inicializa una transacción con entradas, salidas y comisión.

        Args:
            inputs (list): Lista de entradas (dicts con txid, index).
            outputs (list): Lista de salidas (dicts con direccion y cantidad).
            fee (float): Comisión opcional (por defecto 0.0).
        """
        self.inputs = inputs
        self.outputs = outputs
        self.fee = fee
        self.txid = self._calculate_txid()

    def _calculate_txid(self):
        """
        Calcula el hash único de la transacción usando SHA-256.

        Returns:
            str: Hash hexadecimal como identificador de la transacción.
        """
        tx_copy = {
            "inputs": self.inputs,
            "outputs": self.outputs,
            "fee": self.fee
        }
        tx_string = json.dumps(tx_copy, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign_input(self, index, private_key_hex):
        """
        Firma una entrada específica usando la clave privada del remitente.

        Args:
            index (int): Índice de la entrada a firmar.
            private_key_hex (str): Clave privada en formato hexadecimal.
        """
        sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
        message = self._message_to_sign(index)
        signature = sk.sign(message.encode()).hex()
        self.inputs[index]["signature"] = signature
        self.txid = self._calculate_txid()

    def _message_to_sign(self, index):
        """
        Construye el mensaje que debe firmarse para una entrada.

        Args:
            index (int): Índice de la entrada.

        Returns:
            str: Mensaje serializado a firmar.
        """
        input_copy = self.inputs[index].copy()
        input_copy.pop("signature", None)

        tx_part = {
            "input": input_copy,
            "outputs": self.outputs,
            "fee": self.fee
        }
        return json.dumps(tx_part, sort_keys=True)

    def verify_input(self, index, public_key_hex):
        """
        Verifica la firma de una entrada utilizando la clave pública.

        Args:
            index (int): Índice de la entrada a verificar.
            public_key_hex (str): Clave pública en formato hexadecimal.

        Returns:
            bool: True si la firma es válida, False en caso contrario.
        """
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
            message = self._message_to_sign(index)
            signature = bytes.fromhex(self.inputs[index]["signature"])
            return vk.verify(signature, message.encode())
        except (BadSignatureError, KeyError, Exception):
            return False


class UTXOManager:
    """
    Manejador del conjunto de salidas no gastadas (UTXO).

    Atributos:
        utxos (dict): Diccionario con claves 'txid:index' y valores con dirección y cantidad.
    """

    def __init__(self):
        """
        Inicializa el conjunto de UTXOs como un diccionario vacío.
        """
        self.utxos = {}

    def add_utxo(self, txid, index, direccion, cantidad):
        """
        Agrega un nuevo UTXO al conjunto.

        Args:
            txid (str): ID de la transacción.
            index (int): Índice de la salida.
            direccion (str): Dirección del beneficiario.
            cantidad (float): Valor de la salida.
        """
        self.utxos[f"{txid}:{index}"] = {
            "direccion": direccion,
            "cantidad": cantidad
        }

    def remove_utxo(self, txid, index):
        """
        Elimina un UTXO gastado del conjunto.

        Args:
            txid (str): ID de la transacción.
            index (int): Índice de la salida.
        """
        self.utxos.pop(f"{txid}:{index}", None)

    def get_utxos_for_address(self, direccion):
        """
        Recupera todos los UTXOs asociados a una dirección específica.

        Args:
            direccion (str): Dirección del usuario.

        Returns:
            dict: Subconjunto de UTXOs propiedad de la dirección.
        """
        return {k: v for k, v in self.utxos.items() if v["direccion"] == direccion}
