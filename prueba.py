from utils.delete_cache import delete_pycache

from blockchain.system import SistemaBlockchain

def test_sistema():
    sistema = SistemaBlockchain()

    sistema.crear_usuario("Alice")
    sistema.crear_usuario("Bob")

    sistema.utxo_manager.add_utxo("GENESIS", 0, sistema.usuarios["Alice"].address, 10)

    tx = sistema.enviar_transaccion("Alice", "Bob", monto=7, fee=1)
    if tx:
        sistema.minar_bloque([tx])

    sistema.mostrar_saldos()

    delete_pycache()  # Limpiar caché de Python

if __name__ == "__main__":
    test_sistema()
