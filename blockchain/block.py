"""
block.py

Este módulo define la clase Block, que representa un bloque individual en la cadena de bloques.
Cada bloque contiene una lista de transacciones, un hash del bloque anterior, un nonce, y su propio hash,
calculado mediante SHA-256. También incluye un mecanismo de minería basado en Prueba de Trabajo (PoW).
"""

import hashlib
import json
import time

class Block:
    """
    Representa un bloque en una blockchain.

    Atributos:
        index (int): Índice del bloque en la cadena.
        timestamp (str): Marca de tiempo en formato "YYYY-MM-DD HH:MM:SS".
        transactions (list): Lista de transacciones incluidas en el bloque.
        prev_hash (str): Hash del bloque anterior.
        nonce (int): Número utilizado para PoW. Se ajusta hasta cumplir la dificultad.
        hash (str): Hash SHA-256 del contenido del bloque.
    """

    def __init__(self, index, transactions, prev_hash, nonce=0, timestamp=None):
        """
        Inicializa un nuevo bloque.

        Args:
            index (int): Índice del bloque.
            transactions (list): Lista de transacciones (dicts) a incluir en el bloque.
            prev_hash (str): Hash del bloque anterior.
            nonce (int, opcional): Valor inicial del nonce. Por defecto es 0.
            timestamp (str, opcional): Timestamp del bloque. Si no se proporciona, se genera automáticamente.
        """
        self.index = index
        self.timestamp = timestamp or time.strftime("%Y-%m-%d %H:%M:%S")
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calcula el hash SHA-256 del bloque a partir de su contenido.

        Returns:
            str: Hash SHA-256 del bloque como string hexadecimal.
        """
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty_prefix="000"):
        """
        Ejecuta Prueba de Trabajo (PoW) buscando un nonce tal que el hash comience con un prefijo determinado.

        Args:
            difficulty_prefix (str): Prefijo que el hash debe cumplir (por defecto "000").
        """
        while not self.hash.startswith(difficulty_prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()
