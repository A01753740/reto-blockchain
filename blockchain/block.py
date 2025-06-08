import hashlib
import json
import time

class Block:
    def __init__(self, index, transactions, prev_hash, nonce=0, timestamp=None):
        self.index = index
        self.timestamp = timestamp or time.strftime("%Y-%m-%d %H:%M:%S")
        self.transactions = transactions  # lista de dicts con transacciones
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
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
        while not self.hash.startswith(difficulty_prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()
