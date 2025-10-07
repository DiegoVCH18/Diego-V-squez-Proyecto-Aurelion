import pandas as pd
import random
from datetime import datetime, timedelta
import json

"""
Simulador de Datos Comerciales
------------------------------

Este script genera y valida datos simulados para un entorno comercial, creando los siguientes archivos en la carpeta Datasets:

- productos.xlsx
- clientes.xlsx
- ventas.xlsx
- detalle_ventas.xlsx

Reglas de integridad y coherencia:
- Los productos tienen categoría lógica y precios base.
- Los detalles de ventas respetan la integridad referencial y precios de venta (+1% a +5% sobre el base).
- Los clientes se generan con nombres y apellidos permitidos, email único y ciudad aleatoria.
- Las ventas respetan la relación con clientes y medios/canales válidos.
- Regla nueva: si medio_pago = "transferencia" entonces canal = "web", caso contrario "local".
"""

# ------------------ Listas base ------------------
nombres = [
    "Mateo","Benjamín","Felipe","Valentino","Bautista","Julián","Lorenzo","Joaquín","Tomás","Benicio",
    "Franco","Lautaro","Agustín","Lucas","Nicolás","Santiago","Matías","Juan","José","Luis",
    "Carlos","Jorge","Daniel","Ricardo","Roberto","Olivia","Sofía","Emma","Emilia","Isabella",
    "Catalina","Martina","Valentina","Renata","Delfina","Victoria","Lucía","María","Ana","Laura",
    "Claudia","Silvia","Patricia","Sandra","Marcela","Andrea","Mónica","Gabriela","Julieta","Florencia","Diego","Armando","Lionel"
]

apellidos = [
    "González","Rodríguez","Gómez","Fernández","López","Martínez","Díaz","Pérez","Sánchez","Romero",
    "García","Sosa","Benítez","Ramírez","Ruiz","Torres","Flores","Álvarez","Acosta","Rojas","Molina",
    "Castro","Peralta","Aguirre","Ojeda","Giménez","Medina","Pereyra","Godoy","Núñez","Ferreyra",
    "Ríos","Mendoza","Suárez","Vega","Ponce","Guillén","Herrera","Domínguez","Cabrera","Campos",
    "Vázquez","Bravo","Morales","Cordero","Figueroa","Duarte","Villalba","Cardozo","Silva", "Messi","Vasquez","Chávez"
]

ciudades = ["Buenos Aires","Córdoba","Rosario","Mendoza","La Plata",
            "Mar del Plata","Salta","Santa Fe","San Juan","Neuquén"]

categorias_productos = {
    "Bebidas": [
        "Coca-Cola","Pepsi","Fanta","Sprite","Agua Mineral","Quilmes","Heineken","Cerveza Andes",
        "Red Bull","Monster","Jugo de Naranja","Jugo de Manzana","Agua con gas","Té frío","Mate",
        "Cerveza Brahma","Sidra","Energizante","Agua saborizada","Jugo de Piña","Té verde",
        "Agua sabor limón","Agua sabor naranja","Ginger Ale","Seven Up"
    ],
    "Limpieza": [
        "Lavandina","Detergente","Jabón Líquido","Desinfectante","Limpiavidrios","Esponja","Trapo de Piso",
        "Cepillo","Balde","Guantes","Paño de Microfibra","Limpiador multiusos","Limpiador de baño","Fregona",
        "Escoba","Recolector de polvo","Amoniaco","Toallas de papel","Ambientador","Limpiador de cocina",
        "Limpiador de horno","Limpiador de pisos","Limpiador de vidrios","Limpiador de muebles","Limpiador de acero"
    ],
    "Alimentos": [
        "Arroz","Fideos","Aceite","Azúcar","Harina","Sal","Yerba","Café","Leche","Galletitas",
        "Alfajores","Pan","Mantequilla","Queso","Yogur","Huevos","Pollo","Carne de res","Carne de cerdo",
        "Verduras","Frutas","Legumbres","Salsa de tomate","Mayonesa","Mermelada"
    ],
    "Higiene": [
        "Shampoo","Acondicionador","Jabón","Pasta Dental","Desodorante","Toalla","Papel Higiénico",
        "Algodón","Hisopos","Crema Corporal","Cepillo de dientes","Enjuague bucal","Rastrillo de afeitar",
        "Crema de afeitar","Hilo dental","Protector solar","Toallitas húmedas","Gel antibacterial","Esponja de baño",
        "Cortaúñas","Loción corporal","Crema facial","Mascarilla facial","Peine","Spray desodorante"
    ],
    "Electrónica": [
        "Auriculares","Mouse","Teclado","Lámpara LED","Cargador","Cable USB","Parlante","Smartwatch",
        "USB","Powerbank","Hub USB","Soporte para celular","Linterna LED","Audífonos Bluetooth",
        "Adaptador de corriente","Memoria SD","Cable HDMI","Base para laptop","Soporte para auriculares",
        "Mini ventilador USB","Mouse pad","Cámara web","Cargador inalámbrico","Teclado mecánico","Teclado inalámbrico"
    ]
}


# ------------------ Funciones ------------------

def generar_productos(path, total=125):
    productos = []
    id = 1
    categorias = list(categorias_productos.keys())
    nombres_categorias = [ (cat, nombre) for cat in categorias for nombre in categorias_productos[cat] ]
    random.shuffle(nombres_categorias)
    usados = set()
    i = 0
    while len(productos) < total and i < len(nombres_categorias):
        cat, nombre = nombres_categorias[i]
        clave = (nombre, cat)
        if clave not in usados:
            usados.add(clave)
            precio = round(random.uniform(100, 5000), 2)
            productos.append({
                "id_producto": id,
                "nombre_producto": nombre,
                "categoria": cat,
                "precio_unitario": precio
            })
            id += 1
        i += 1
    # Si no hay suficientes combinaciones únicas, rellena cíclicamente
    while len(productos) < total:
        cat, nombre = random.choice(nombres_categorias)
        precio = round(random.uniform(100, 5000), 2)
        productos.append({
            "id_producto": id,
            "nombre_producto": nombre,
            "categoria": cat,
            "precio_unitario": precio
        })
        id += 1
    df = pd.DataFrame(productos)
    df.to_excel(path, index=False)
    return df

def ampliar_clientes(path, minimo=1000):
    clientes = set()
    contador_emails = {}
    registros = []
    fecha_inicio = datetime.strptime("2024-01-01", "%Y-%m-%d")
    fecha_fin = datetime.today()
    rango_dias = (fecha_fin - fecha_inicio).days
    for idx in range(minimo):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        nombre_cliente = f"{nombre} {apellido}"
        email_base = f"{nombre.lower()}.{apellido.lower()}"
        email = f"{email_base}@mail.com"
        if email in contador_emails:
            contador_emails[email] += 1
            email = f"{email_base}{contador_emails[email]}@mail.com"
        else:
            contador_emails[email] = 1
        ciudad = random.choice(ciudades)
        # Fecha de alta más antigua para id_cliente menor
        # Distribuir fechas de alta de forma creciente
        dias_offset = int(idx * rango_dias / (minimo - 1)) if minimo > 1 else 0
        fecha_alta = fecha_inicio + timedelta(days=dias_offset)
        clave = (nombre_cliente, email)
        if clave not in clientes:
            clientes.add(clave)
            registros.append({
                "id_cliente": idx + 1,
                "nombre_cliente": nombre_cliente,
                "email": email,
                "ciudad": ciudad,
                "fecha_alta": fecha_alta.date().isoformat()
            })
    df = pd.DataFrame(registros)
    df.to_excel(path, index=False)
    return df

def generar_ventas(path, clientes_df, total=10000):
    medios_pago = ["tarjeta", "qr", "efectivo", "transferencia"]
    ventas_por_cliente = []
    fecha_fin = datetime.today()
    fechas_ventas = []
    # Primero, aseguramos al menos una venta por cliente, ordenada por id_cliente
    for idx, row in clientes_df.sort_values("id_cliente").iterrows():
        id_cliente = row["id_cliente"]
        fecha_alta_dt = datetime.strptime(row["fecha_alta"], "%Y-%m-%d")
        rango_dias = (fecha_fin - fecha_alta_dt).days
        if rango_dias > 0:
            fecha_venta = fecha_alta_dt + timedelta(days=random.randint(0, rango_dias))
        else:
            fecha_venta = fecha_alta_dt
        fechas_ventas.append(fecha_venta)
        medio_pago = random.choice(medios_pago)
        canal = "web" if medio_pago == "transferencia" else "local"
        ventas_por_cliente.append({
            "id_venta": len(ventas_por_cliente) + 1,
            "fecha": fecha_venta.date().isoformat(),
            "id_cliente": id_cliente,
            "medio_pago": medio_pago,
            "canal": canal
        })
    # Generar el resto de ventas aleatorias, manteniendo la relación y orden
    restantes = total - len(ventas_por_cliente)
    for i in range(restantes):
        id_cliente = random.choice(clientes_df["id_cliente"].tolist())
        fecha_alta_cliente = clientes_df.loc[clientes_df["id_cliente"] == id_cliente, "fecha_alta"].values[0]
        fecha_alta_dt = datetime.strptime(fecha_alta_cliente, "%Y-%m-%d")
        rango_dias = (fecha_fin - fecha_alta_dt).days
        if rango_dias > 0:
            fecha_venta = fecha_alta_dt + timedelta(days=random.randint(0, rango_dias))
        else:
            fecha_venta = fecha_alta_dt
        fechas_ventas.append(fecha_venta)
        medio_pago = random.choice(medios_pago)
        canal = "web" if medio_pago == "transferencia" else "local"
        ventas_por_cliente.append({
            "id_venta": len(ventas_por_cliente) + 1,
            "fecha": fecha_venta.date().isoformat(),
            "id_cliente": id_cliente,
            "medio_pago": medio_pago,
            "canal": canal
        })
    # Ordenar ventas por fecha de menor a mayor y reasignar id_venta
    ventas_df = pd.DataFrame(ventas_por_cliente)
    ventas_df["fecha_dt"] = pd.to_datetime(ventas_df["fecha"])
    ventas_df = ventas_df.sort_values("fecha_dt").reset_index(drop=True)
    ventas_df["id_venta"] = ventas_df.index + 1
    ventas_df = ventas_df.drop(columns=["fecha_dt"])
    ventas_df.to_excel(path, index=False)
    return ventas_df

def generar_detalle_ventas(path, ventas_df, productos_df, total=10000):
    detalles = []
    # Aseguramos que id_venta comience en 1 y corresponda a ventas válidas
    id_ventas_validos = ventas_df["id_venta"].tolist()
    for i in range(total):
        id_venta = id_ventas_validos[i % len(id_ventas_validos)]
        venta = ventas_df.loc[ventas_df["id_venta"] == id_venta].iloc[0]
        producto = productos_df.iloc[random.randint(0, len(productos_df) - 1)]
        cantidad = random.randint(1, 10)
        precio_base = producto["precio_unitario"]
        precio_venta = round(precio_base * random.uniform(1.01, 1.05), 2)
        importe = round(cantidad * precio_venta, 2)
        detalles.append({
            "id_venta": id_venta,
            "id_producto": producto["id_producto"],
            "nombre_producto": producto["nombre_producto"],
            "cantidad": cantidad,
            "precio_unitario": precio_venta,
            "importe": importe
        })
    df = pd.DataFrame(detalles)
    df.to_excel(path, index=False)
    return df

def validar_integridad(productos_df, detalle_df, clientes_df, ventas_df):
    assert productos_df["id_producto"].is_unique,"id_producto no es único"
    assert clientes_df["id_cliente"].is_unique,"id_cliente no es único"
    assert set(detalle_df["id_producto"]).issubset(set(productos_df["id_producto"])),"id_producto en detalle_ventas no existe en productos"
    assert set(detalle_df["nombre_producto"]).issubset(set(productos_df["nombre_producto"])),"nombre_producto en detalle_ventas no existe en productos"
    assert set(ventas_df["id_cliente"]).issubset(set(clientes_df["id_cliente"])),"id_cliente en ventas no existe en clientes"
    for _,row in detalle_df.iterrows():
        prod_base = productos_df.loc[productos_df["id_producto"]==row["id_producto"]]
        assert not prod_base.empty,"Producto inexistente"
        base = prod_base["precio_unitario"].values[0]
        assert row["nombre_producto"] == prod_base["nombre_producto"].values[0], f"Inconsistencia nombre/id en detalle_ventas (id={row['id_producto']})"
        assert base <= row["precio_unitario"] <= base*1.05,"precio_unitario en detalle_ventas fuera de rango"
        assert row["importe"] == round(row["cantidad"]*row["precio_unitario"],2),"importe incorrecto"
    print("✔️ Validación OK")

def agregar_canal_tabla_ventas(ruta_ventas):
    """
    Asigna la columna 'canal' en ventas.xlsx según el medio de pago:
    - Si medio_pago = 'transferencia' => canal = 'web'
    - Otro medio => canal = 'local'
    Sobrescribe el archivo ventas.xlsx.
    """
    import pandas as pd
    df = pd.read_excel(ruta_ventas)
    df['canal'] = df['medio_pago'].apply(lambda x: 'web' if str(x).lower() == 'transferencia' else 'local')
    df.to_excel(ruta_ventas, index=False)
    print("Columna 'canal' asignada y archivo sobrescrito correctamente.")

# ------------------ Rutas absolutas (seguras) ------------------
# Leer configuración desde 5. config.json
with open("5. config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

ruta_productos = config["rutas"]["productos"]
ruta_clientes = config["rutas"]["clientes"]
ruta_ventas = config["rutas"]["ventas"]
ruta_detalle = config["rutas"]["detalle_ventas"]

size_productos = config["tamaños"]["productos"]
size_clientes = config["tamaños"]["clientes"]
size_ventas = config["tamaños"]["ventas"]
size_detalle = config["tamaños"]["detalle_ventas"]

# ------------------ Ejecución principal ------------------
if __name__ == "__main__":
    productos_df = generar_productos(ruta_productos, size_productos)
    clientes_df = ampliar_clientes(ruta_clientes, size_clientes)
    ventas_df = generar_ventas(ruta_ventas, clientes_df, size_ventas)
    detalle_df = generar_detalle_ventas(ruta_detalle, ventas_df, productos_df, size_detalle)
    validar_integridad(productos_df, detalle_df, clientes_df, ventas_df)
    agregar_canal_tabla_ventas(ruta_ventas)
    print(f"✔️ Productos generados: {len(productos_df)}")
    print(f"✔️ Clientes generados: {len(clientes_df)}")
    print(f"✔️ Ventas generadas: {len(ventas_df)}")
    print(f"✔️ Detalles de ventas generados: {len(detalle_df)}")