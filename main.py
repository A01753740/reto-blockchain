from utils.install_requirements import install_requirements
# install_requirements()
from utils.delete_cache import delete_pycache
from utils.logger import log_info
from blockchain.wallet import Wallet
from blockchain.transaction import Transaction, UTXOManager

def test_transaction_flow():
    log_info("=== Simulación de Transacción ===")

    # Simular creación de wallets
    sender = Wallet()
    receiver = Wallet()

    log_info(f"Dirección remitente: {sender.address}")
    log_info(f"Dirección receptor: {receiver.address}")

    # Crear gestor de UTXOs
    utxo_manager = UTXOManager()

    # Agregar un UTXO simulado al remitente (10 monedas)
    utxo_manager.add_utxo("abc123", 0, sender.address, 10)
    log_info("UTXO inicial agregado: 10 monedas para el remitente")

    # Crear transacción: enviar 7 monedas al receptor, 2 de cambio, 1 de comisión
    inputs = [{"txid": "abc123", "index": 0}]
    outputs = [
        {"direccion": receiver.address, "cantidad": 7},
        {"direccion": sender.address, "cantidad": 2}
    ]
    tx = Transaction(inputs, outputs, fee=1.0)

    # Firmar la entrada con la clave privada del remitente
    sender_keys = sender.get_keys()
    tx.sign_input(0, sender_keys["private_key"])
    log_info(f"Transacción firmada. txid: {tx.txid}")

    # Verificar la firma con la clave pública del remitente
    if tx.verify_input(0, sender_keys["public_key"]):
        log_info("Firma válida")
        
        # Actualizar UTXO: eliminar el usado, agregar nuevas salidas
        utxo_manager.remove_utxo("abc123", 0)
        for i, output in enumerate(tx.outputs):
            utxo_manager.add_utxo(tx.txid, i, output["direccion"], output["cantidad"])
        log_info("UTXO actualizado correctamente")
    else:
        log_info("Firma inválida. Transacción rechazada.")

    delete_pycache()  # Limpiar caché de Python

if __name__ == "__main__":
    test_transaction_flow()