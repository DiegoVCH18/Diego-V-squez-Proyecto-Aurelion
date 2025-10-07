"""
Programa principal del proyecto Minimarket Aurelion
Con logging básico incorporado
"""

import os
import logging
from datetime import datetime

# ---------------- CONFIGURACIÓN DE LOGGING ---------------- #
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, f"pipeline_{datetime.now().strftime('%Y%m%d')}.log")

# Crear carpeta de logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # también muestra en consola
    ]
)

# ---------------- INFORMACIÓN DEL PROYECTO ---------------- #
PROYECTO = "Minimarket Aurelion"

INFO = {
    "nombre": PROYECTO,
    "descripcion": "Análisis avanzado de ventas en Minimarket Aurelion, integrando datos de clientes, productos y transacciones para detección de productos estrella, estacionalidad y segmentación ABC.",
    "carpeta": [
        "Diego Vásquez - Proyecto Aurelion/"
    ],
    "archivos_clave": [
        "1. Documentación.md",
        "3. Instrucciones.md",
        "4. simulador_datos_comerciales.py"
    ],
    "datasets": [
        "clientes.xlsx",
        "productos.xlsx",
        "ventas.xlsx",
        "detalle_ventas.xlsx"
    ]
}

PROYECTO_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_PRINCIPAL = os.path.join(PROYECTO_DIR)
CARPETA_DATASETS = os.path.join(PROYECTO_DIR, "datasets")


# ---------------- FUNCIONES PRINCIPALES ---------------- #
def mostrar_info():
    logging.info("Mostrando información del proyecto.")
    print(f"\n📊 Proyecto: {INFO['nombre']}")
    print(f"🧾 Descripción: {INFO['descripcion']}")
    print("\n📁 Carpeta principal:")
    print("  - Diego Vásquez - Proyecto Aurelion/")
    print("\n📄 Archivos clave:")
    for archivo in INFO["archivos_clave"]:
        print(f"  - {archivo}")
    print("\n📊 Datasets:")
    for dataset in INFO["datasets"]:
        print(f"  - {dataset}")


def verificar_estructura():
    """
    Verifica la existencia de carpetas y archivos básicos del proyecto.
    """
    logging.info("Verificando estructura de carpetas y archivos del proyecto...")
    faltantes = []
    # Verificar carpetas
    carpetas_relativas = [CARPETA_DATASETS, LOG_DIR]
    for carpeta in carpetas_relativas:
        if not os.path.exists(carpeta):
            faltantes.append(carpeta)
            logging.warning(f"Carpeta faltante: {carpeta}")
    # Verificar archivos clave en la raíz del proyecto
    for archivo in INFO["archivos_clave"]:
        ruta_archivo = os.path.join(CARPETA_PRINCIPAL, archivo)
        if not os.path.exists(ruta_archivo):
            faltantes.append(ruta_archivo)
            logging.warning(f"Archivo faltante: {ruta_archivo}")
    # Verificar datasets en carpeta datasets
    for archivo in INFO["datasets"]:
        ruta_archivo = os.path.join(CARPETA_DATASETS, archivo)
        if not os.path.exists(ruta_archivo):
            faltantes.append(ruta_archivo)
            logging.warning(f"Archivo faltante: {ruta_archivo}")
    if faltantes:
        logging.warning(f"⚠️ Se detectaron {len(faltantes)} elementos faltantes.")
    else:
        logging.info("✅ Estructura del proyecto verificada correctamente.")


def iniciar_pipeline():
    """
    Simula el inicio del pipeline analítico completo.
    (Aquí podrías conectar con tus scripts de análisis reales)
    """
    try:
        logging.info("🚀 Iniciando ejecución del pipeline Aurelion.")
        # Aquí se llamarían tus scripts reales:
        # os.system("python simulador_datos_comerciales.py")
        logging.info("✅ Pipeline ejecutado exitosamente.")
    except Exception as e:
        logging.error(f"❌ Error durante la ejecución del pipeline: {e}")


# ---------------- EJECUCIÓN PRINCIPAL ---------------- #
if __name__ == "__main__":
    logging.info("===== INICIO DEL PROGRAMA MINIMARKET AURELION =====")
    mostrar_info()
    verificar_estructura()
    iniciar_pipeline()
    logging.info("===== FIN DEL PROGRAMA =====")
