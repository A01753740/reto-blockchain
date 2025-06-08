from blockchain.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = "000"
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            transactions=[{"tipo": "coinbase", "direccion": "GENESIS", "cantidad": 1000}],
            prev_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        prev_block = self.get_last_block()
        new_block = Block(
            index=prev_block.index + 1,
            transactions=transactions,
            prev_hash=prev_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Validar hash y conexión con el anterior
            if curr.hash != curr.calculate_hash():
                return False
            if curr.prev_hash != prev.hash:
                return False
            if not curr.hash.startswith(self.difficulty):
                return False
        return True
    
    @staticmethod
    def crear_bloque_desde_dict(data):
        from blockchain.block import Block
        b = Block(
            index=data["index"],
            transactions=data["transactions"],
            prev_hash=data["prev_hash"],
            nonce=data["nonce"],
            timestamp=data["timestamp"]
        )
        b.hash = data["hash"]
        return b