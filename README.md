# 🧱 Reto Blockchain

Este es un proyecto integrador que simula una blockchain, incluyendo creación de wallets, transacciones firmadas, modelo UTXO, minería con PoW y una interfaz visual en Streamlit para interacción.

---

## 🚀 Funcionalidades

- 🔐 Generación de claves y direcciones (ECDSA + SHA-256)
- 💸 Envío de transacciones firmadas entre usuarios
- 📦 Minado de bloques con prueba de trabajo (PoW con 3 ceros)
- 🧾 Modelo UTXO (salidas no gastadas)
- 🧍 Gestión de múltiples usuarios
- 🧰 Interfaz web con [Streamlit](https://streamlit.io/)
- 💾 Persistencia en archivos JSON (blockchain, UTXOs, usuarios)
- ✅ Verificación de firmas digitales

---

## 📁 Estructura del proyecto

```
reto-blockchain/
│   .DS_Store
│   .gitignore
│   debug.log
│   prueba.py
│   README.md
│   requirements.txt
│   
├───blockchain
│   │   block.py
│   │   blockchain.py
│   │   system.py
│   │   transaction.py
│   │   wallet.py
│   │   __init__.py
│
├───data
│       blockchain.json
│       usuarios.json
│       utxos.json
│       
├───docs
│   │   make.bat
│   │   Makefile
│   │   Presentación proyecto integrador.pdf
│   │   
│   ├───build
│   │   │   
│   │   ├───html
│   │   └───latex
│   │
│   └───source
│       │   blockchain.rst
│       │   conf.py
│       │   index.rst
│       │
│       ├───_static
│       └───_templates
├───interface
│       app.py
│       __init__.py
│
├───logs
│       ejecucion.log
│
└───utils
    │   delete_cache.py
    │   install_requirements.py
    │   logger.py
    │   __init__.py
```

---

## 📦 Requisitos

Python 3.10 o superior. Instala las dependencias con:

```bash
pip install -r requirements.txt
```

---
## Ejecución Local
Para iniciar el proyecto:

```bash
streamlit run interface/app.py
```

---

## Funcionalidades en la interfaz

| Sección           | Descripción                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| **Inicio**        | Información general del sistema                                          |
| **Usuarios**      | Crear nuevos usuarios y mostrar direcciones                              |
| **Transacciones** | Enviar monedas de un usuario a otro con firma digital                    |
| **Minería**       | Ejecutar Prueba de Trabajo (PoW) y minar un bloque con recompensa + fees |
| **Saldos**        | Visualizar el saldo actual por dirección de usuario                      |
| **Blockchain**    | Visualizar la cadena de bloques (hashes, transacciones, nonce, etc.)     |
| **Reiniciar**     | Borra todos los datos JSON y regenera el bloque génesis                  |
