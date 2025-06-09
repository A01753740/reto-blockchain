"""
blockchain.py

Este módulo define la clase Blockchain, responsable de mantener la cadena de bloques.
Incluye la creación del bloque génesis, validación de la cadena, adición de nuevos bloques
y mecanismos de minería basados en dificultad por prefijo.
"""

from blockchain.block import Block

class Blockchain:
    """
    Representa una cadena de bloques.

    Atributos:
        chain (list): Lista de bloques en la cadena.
        difficulty (str): Prefijo de dificultad para minería (e.g. '000').
    """

    def __init__(self):
        """
        Inicializa la blockchain con un bloque génesis.
        """
        self.chain = []
        self.difficulty = "000"
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Crea el bloque génesis con una transacción coinbase inicial.
        """
        genesis_block = Block(
            index=0,
            transactions=[{"tipo": "coinbase", "direccion": "GENESIS", "cantidad": 1000}],
            prev_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_last_block(self):
        """
        Retorna el último bloque de la cadena.

        Returns:
            Block: Último bloque en la cadena.
        """
        return self.chain[-1]

    def add_block(self, transactions):
        """
        Agrega un nuevo bloque a la cadena con las transacciones proporcionadas.

        Args:
            transactions (list): Lista de transacciones a incluir en el nuevo bloque.
        """
        prev_block = self.get_last_block()
        new_block = Block(
            index=prev_block.index + 1,
            transactions=transactions,
            prev_hash=prev_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_valid_chain(self):
        """
        Verifica la validez de toda la cadena.

        Returns:
            bool: True si la cadena es válida, False si hay una inconsistencia.
        """
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Verificar hash actual
            if curr.hash != curr.calculate_hash():
                return False
            # Verificar enlace con bloque anterior
            if curr.prev_hash != prev.hash:
                return False
            # Verificar cumplimiento de PoW
            if not curr.hash.startswith(self.difficulty):
                return False

        return True

    @staticmethod
    def crear_bloque_desde_dict(data):
        """
        Crea un objeto Block a partir de un diccionario serializado (usado en carga desde JSON).

        Args:
            data (dict): Diccionario con los datos del bloque.

        Returns:
            Block: Objeto de tipo Block recreado con sus atributos.
        """
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
