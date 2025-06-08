import hashlib
import json
from ecdsa import VerifyingKey, SigningKey, SECP256k1, BadSignatureError

class Transaction:
    def __init__(self, inputs, outputs, fee=0.0):
        self.inputs = inputs  # [{ txid, index, signature }]
        self.outputs = outputs  # [{ direccion, cantidad }]
        self.fee = fee
        self.txid = self._calculate_txid()

    def _calculate_txid(self):
        tx_copy = {
            "inputs": self.inputs,
            "outputs": self.outputs,
            "fee": self.fee
        }
        tx_string = json.dumps(tx_copy, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign_input(self, index, private_key_hex):
        """Firma una entrada específica usando la clave privada"""
        sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
        message = self._message_to_sign(index)
        signature = sk.sign(message.encode()).hex()
        self.inputs[index]["signature"] = signature
        self.txid = self._calculate_txid() 

    def _message_to_sign(self, index):
        """Mensaje único a firmar por input[index] (sin la firma incluida)"""
        input_copy = self.inputs[index].copy()
        input_copy.pop("signature", None)

        tx_part = {
            "input": input_copy,
            "outputs": self.outputs,
            "fee": self.fee
        }
        return json.dumps(tx_part, sort_keys=True)

    def verify_input(self, index, public_key_hex):
        """Verifica la firma de una entrada usando la clave pública"""
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
            message = self._message_to_sign(index)
            signature = bytes.fromhex(self.inputs[index]["signature"])
            return vk.verify(signature, message.encode())
        except (BadSignatureError, KeyError, Exception):
            return False
        
class UTXOManager:
    def __init__(self):
        self.utxos = {}  # key = txid:index, value = {direccion, cantidad}

    def add_utxo(self, txid, index, direccion, cantidad):
        self.utxos[f"{txid}:{index}"] = {
            "direccion": direccion,
            "cantidad": cantidad
        }

    def remove_utxo(self, txid, index):
        self.utxos.pop(f"{txid}:{index}", None)

    def get_utxos_for_address(self, direccion):
        return {k: v for k, v in self.utxos.items() if v["direccion"] == direccion}