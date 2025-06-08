import sys
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
from blockchain.system import SistemaBlockchain

# Inicializar sistema global
if "sistema" not in st.session_state:
    sistema = SistemaBlockchain()
    sistema.cargar_estado()
    st.session_state.sistema = sistema
if "transacciones_pendientes" not in st.session_state:
    st.session_state.transacciones_pendientes = []

sistema = st.session_state.sistema

# --- Sidebar ---
st.sidebar.title("Menú")
seccion = st.sidebar.radio("Navegación", ["Inicio", "Usuarios", "Transacciones", "Minería", "Saldos", "Blockchain", "Reiniciar Sistema"])


# --- Inicio ---
if seccion == "Inicio":
    st.title("Blockchain Demo 🧱")
    st.markdown("""
        Proyecto integrador en Python con wallets, transacciones, PoW y Streamlit.
        - Crea usuarios
        - Realiza transacciones firmadas
        - Mina bloques con prueba de trabajo
        - Visualiza el estado de la cadena
    """)

# --- Usuarios ---
elif seccion == "Usuarios":
    st.header("👤 Crear Usuario")
    nuevo_nombre = st.text_input("Nombre del usuario")
    if st.button("Crear"):
        if nuevo_nombre:
            sistema.crear_usuario(nuevo_nombre)
            sistema.guardar_estado()
        else:
            st.warning("Escribe un nombre válido.")
    
    st.subheader("Usuarios registrados:")
    for nombre, wallet in sistema.usuarios.items():
        st.write(f"- {nombre}: `{wallet.address}`")

    st.subheader("💰 Financiar usuario (dev mode)")
    usuario_seleccionado = st.selectbox("Seleccionar usuario para financiar", list(sistema.usuarios.keys()))
    monto = st.number_input("Monto a asignar", min_value=1, value=10)

    if st.button("Asignar fondos"):
        sistema.fund_usuario(usuario_seleccionado, cantidad=monto)
        sistema.guardar_estado()
        st.success(f"Fondos asignados a {usuario_seleccionado}")

# --- Transacciones ---
elif seccion == "Transacciones":
    st.header("💸 Enviar Transacción")

    if len(sistema.usuarios) < 2:
        st.warning("Debes tener al menos 2 usuarios.")
    else:
        usuarios = list(sistema.usuarios.keys())
        remitente = st.selectbox("Remitente", usuarios)
        receptor = st.selectbox("Receptor", [u for u in usuarios if u != remitente])
        monto = st.number_input("Monto", min_value=0.0, step=0.1)
        fee = st.number_input("Comisión (fee)", min_value=0.0, step=0.1, value=1.0)

        if st.button("Enviar"):
            tx = sistema.enviar_transaccion(remitente, receptor, monto, fee)
            if tx:
                st.session_state.transacciones_pendientes.append(tx)
                st.success(f"Transacción agregada a la cola: {tx.txid}")
            else:
                st.error("Transacción fallida.")


# --- Minería ---
elif seccion == "Minería":
    st.header("⛏️ Minar Bloque")
    
    if st.session_state.transacciones_pendientes:
        st.subheader("Transacciones pendientes")
        for tx in st.session_state.transacciones_pendientes:
            st.json(tx.__dict__)
    else:
        st.info("No hay transacciones en la cola.")

    if st.button("Minar"):
        txs = st.session_state.transacciones_pendientes
        if txs:
            sistema.minar_bloque(txs)
            bloque = sistema.blockchain.get_last_block() 
            st.success(f"✅ Bloque #{bloque.index} minado con hash: `{bloque.hash}`")
            st.session_state.transacciones_pendientes = []
            sistema.guardar_estado()
        else:
            st.warning("No hay transacciones pendientes.")


# --- Saldos ---
elif seccion == "Saldos":
    st.header("💰 Saldos actuales")
    for nombre, wallet in sistema.usuarios.items():
        saldo = sistema.obtener_saldo(wallet.address)
        st.write(f"{nombre}: **{saldo} monedas**")

# --- Blockchain ---
elif seccion == "Blockchain":
    st.header("📦 Cadena de bloques")
    for bloque in sistema.blockchain.chain:
        with st.expander(f"Bloque #{bloque.index}"):
            st.json({
                "index": bloque.index,
                "timestamp": bloque.timestamp,
                "hash": bloque.hash,
                "prev_hash": bloque.prev_hash,
                "nonce": bloque.nonce,
                "transacciones": bloque.transactions
            })



elif seccion == "Reiniciar Sistema":
    st.header("⚠️ Reiniciar Sistema Blockchain")

    if st.button("Eliminar estado y reiniciar"):
        # Eliminar archivos de data/
        for archivo in ["usuarios.json", "utxos.json", "blockchain.json"]:
            ruta = os.path.join("data", archivo)
            if os.path.exists(ruta):
                os.remove(ruta)

        # Reiniciar estado interno
        st.session_state.sistema = SistemaBlockchain()
        st.session_state.transacciones_pendientes = []
        st.success("Sistema reiniciado con éxito. Se generó un nuevo bloque génesis.")