import os
import json
from blockchain.wallet import Wallet
from blockchain.transaction import Transaction, UTXOManager
from blockchain.blockchain import Blockchain
from utils.logger import log_info

class SistemaBlockchain:
    def __init__(self):
        self.blockchain = Blockchain()
        self.utxo_manager = UTXOManager()
        self.usuarios = {}  # {"nombre": Wallet}

    def crear_usuario(self, nombre):
        if nombre in self.usuarios:
            log_info(f"El usuario '{nombre}' ya existe.")
            return None

        wallet = Wallet()
        self.usuarios[nombre] = wallet
        log_info(f"Usuario '{nombre}' creado con dirección: {wallet.address}")
        return wallet

    def obtener_saldo(self, direccion):
        utxos = self.utxo_manager.get_utxos_for_address(direccion)
        return sum(v["cantidad"] for v in utxos.values())

    def enviar_transaccion(self, remitente, receptor, monto, fee=1.0):
        if remitente not in self.usuarios or receptor not in self.usuarios:
            log_info("Uno de los usuarios no existe.")
            return None

        sender_wallet = self.usuarios[remitente]
        receiver_wallet = self.usuarios[receptor]
        sender_address = sender_wallet.address

        # Buscar UTXOs del remitente
        utxos = self.utxo_manager.get_utxos_for_address(sender_address)
        seleccionados = []
        acumulado = 0

        for utxo_id, utxo_data in utxos.items():
            seleccionados.append((utxo_id, utxo_data))
            acumulado += utxo_data["cantidad"]
            if acumulado >= monto + fee:
                break

        if acumulado < monto + fee:
            log_info("Fondos insuficientes.")
            return None

        inputs = []
        for utxo_id, _ in seleccionados:
            txid, index = utxo_id.split(":")
            inputs.append({"txid": txid, "index": int(index)})

        outputs = [{"direccion": receiver_wallet.address, "cantidad": monto}]
        cambio = acumulado - monto - fee
        if cambio > 0:
            outputs.append({"direccion": sender_address, "cantidad": cambio})

        tx = Transaction(inputs, outputs, fee)
        for i in range(len(inputs)):
            tx.sign_input(i, sender_wallet.get_keys()["private_key"])

        # Verificar firmas
        for i in range(len(inputs)):
            if not tx.verify_input(i, sender_wallet.get_keys()["public_key"]):
                log_info("Firma inválida en input", i)
                return None

        log_info(f"Transacción creada: {tx.txid}")
        return tx

    def minar_bloque(self, transacciones):
        if not transacciones:
            log_info("No hay transacciones para minar.")
            return

        # Recompensa al minero ficticio "MINERO"
        recompensa = {
            "direccion": "MINERO",
            "cantidad": 3 + sum(tx.fee for tx in transacciones),
            "tipo": "recompensa"
        }
        txs_serializadas = [tx.__dict__ for tx in transacciones]
        txs_serializadas.insert(0, recompensa)

        self.blockchain.add_block(txs_serializadas)

        # Actualizar UTXOs
        for tx in transacciones:
            for i, output in enumerate(tx.outputs):
                self.utxo_manager.add_utxo(tx.txid, i, output["direccion"], output["cantidad"])
            for inp in tx.inputs:
                self.utxo_manager.remove_utxo(inp["txid"], inp["index"])

        log_info(f"Bloque minado: #{self.blockchain.get_last_block().index}")

    def mostrar_saldos(self):
        for nombre, wallet in self.usuarios.items():
            saldo = self.obtener_saldo(wallet.address)
            log_info(f"{nombre} -> {saldo} monedas")

    def mostrar_usuarios(self):
        for nombre, wallet in self.usuarios.items():
            log_info(f"{nombre}: {wallet.address}")

    def guardar_estado(self, carpeta="data"):
        # Guardar usuarios
        usuarios_serializados = {
            nombre: wallet.get_keys()
            for nombre, wallet in self.usuarios.items()
        }
        with open(os.path.join(carpeta, "usuarios.json"), "w") as f:
            json.dump(usuarios_serializados, f, indent=4)

        # Guardar UTXOs
        with open(os.path.join(carpeta, "utxos.json"), "w") as f:
            json.dump(self.utxo_manager.utxos, f, indent=4)

        # Guardar blockchain
        bloques = [block.__dict__ for block in self.blockchain.chain]
        with open(os.path.join(carpeta, "blockchain.json"), "w") as f:
            json.dump(bloques, f, indent=4)

    def cargar_estado(self, carpeta="data"):
        # Cargar usuarios
        usuarios_path = os.path.join(carpeta, "usuarios.json")
        if os.path.exists(usuarios_path):
            with open(usuarios_path, "r") as f:
                data = json.load(f)
                for nombre, keys in data.items():
                    self.usuarios[nombre] = Wallet(private_key=keys["private_key"])

        # Cargar UTXOs
        utxos_path = os.path.join(carpeta, "utxos.json")
        if os.path.exists(utxos_path):
            with open(utxos_path, "r") as f:
                self.utxo_manager.utxos = json.load(f)

        # Cargar Blockchain
        bc_path = os.path.join(carpeta, "blockchain.json")
        if os.path.exists(bc_path):
            with open(bc_path, "r") as f:
                bloques_data = json.load(f)
                self.blockchain.chain = []
                for bloque_dict in bloques_data:
                    b = self.blockchain.crear_bloque_desde_dict(bloque_dict)
                    self.blockchain.chain.append(b)

    def fund_usuario(self, nombre, cantidad=10):
        if nombre not in self.usuarios:
            log_info("Usuario no encontrado.")
            return None

        direccion = self.usuarios[nombre].address
        txid = f"fund_{nombre}"
        self.utxo_manager.add_utxo(txid, 0, direccion, cantidad)
        log_info(f"Usuario '{nombre}' financiado con {cantidad} monedas.")
