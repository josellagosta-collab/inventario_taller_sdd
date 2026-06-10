from decimal import Decimal
from datetime import date

from inventario.models import Categoria, Subcategoria, Proveedor, Material


# Opcional: borrar materiales de prueba anteriores
Material.objects.all().delete()

proveedor, _ = Proveedor.objects.get_or_create(
    nombre="Proveedor de prueba",
    defaults={
        "telefono": "900 123 456",
        "email": "proveedor@ejemplo.com",
        "web": "https://www.ejemplo.com",
        "observaciones": "Proveedor creado automáticamente para pruebas.",
    }
)

datos_categorias = {
    "Redes": ["Routers", "Switches", "Puntos de acceso", "Cableado"],
    "Componentes": ["Memoria RAM", "Fuentes de alimentación", "Tarjetas de red"],
    "Almacenamiento": ["Discos SSD", "Discos HDD", "Pendrives"],
    "IoT": ["ESP32", "Raspberry Pi", "Sensores"],
    "Periféricos": ["Monitores", "Teclados", "Ratones"],
}

subcategorias = []

for nombre_categoria, lista_subcategorias in datos_categorias.items():
    categoria, _ = Categoria.objects.get_or_create(
        nombre=nombre_categoria,
        defaults={"descripcion": f"Categoría de {nombre_categoria.lower()}."}
    )

    for nombre_subcategoria in lista_subcategorias:
        subcategoria, _ = Subcategoria.objects.get_or_create(
            categoria=categoria,
            nombre=nombre_subcategoria,
            defaults={"descripcion": f"Subcategoría {nombre_subcategoria}."}
        )
        subcategorias.append(subcategoria)


nombres_materiales = [
    "Router Cisco 1841",
    "Switch Cisco Catalyst 2960",
    "Punto de acceso TP-Link AC1200",
    "Cable de red UTP Cat 6",
    "Patch panel 24 puertos",
    "Memoria RAM DDR4 8GB",
    "Memoria RAM DDR4 16GB",
    "Fuente de alimentación ATX 650W",
    "Tarjeta de red Gigabit PCIe",
    "Tarjeta WiFi PCIe",
    "Disco SSD SATA 500GB",
    "Disco SSD NVMe 1TB",
    "Disco duro HDD 2TB",
    "Pendrive USB 64GB",
    "Adaptador USB SATA",
    "ESP32-S3 DevKit",
    "ESP8266 NodeMCU",
    "Sensor BME280",
    "Sensor ultrasónico HC-SR04",
    "Módulo relé 5V",
    "Raspberry Pi 4 Model B",
    "Raspberry Pi Pico W",
    "Cámara Raspberry Pi",
    "Fuente USB-C Raspberry Pi",
    "Protoboard 830 puntos",
    "Monitor LCD 24 pulgadas",
    "Teclado USB Logitech",
    "Ratón óptico USB",
    "Webcam Full HD",
    "Auriculares con micrófono",
    "Arduino Uno R3",
    "Arduino Mega 2560",
    "Módulo Bluetooth HC-05",
    "Módulo GPS NEO-6M",
    "Sensor de temperatura DS18B20",
    "Crimpadora RJ45",
    "Tester de cable de red",
    "Latiguillo RJ45 1 metro",
    "Latiguillo RJ45 3 metros",
    "Bobina cable UTP Cat 6",
    "Switch pequeño 8 puertos",
    "Router doméstico WiFi",
    "Adaptador USB Ethernet",
    "Disco externo USB 1TB",
    "Docking station USB-C",
    "Hub USB 3.0",
    "Lector de tarjetas SD",
    "Kit tornillos PC",
    "Pasta térmica",
    "Multímetro digital",
]

estados = [
    "disponible",
    "prestado",
    "reservado",
    "averiado",
    "en_reparacion",
    "fuera_servicio",
]

for i, nombre in enumerate(nombres_materiales, start=1):
    subcategoria = subcategorias[i % len(subcategorias)]

    Material.objects.create(
        codigo_inventario=f"MAT-{i:04d}",
        nombre=nombre,
        descripcion=f"Material de prueba {i} para comprobar el listado y la paginación en Django.",
        categoria=subcategoria.categoria,
        subcategoria=subcategoria,
        proveedor=proveedor,
        marca=f"Marca {i}",
        modelo=f"Modelo {i}",
        numero_serie=f"SN-TEST-{i:05d}",
        cantidad=(i % 10) + 1,
        stock_minimo=i % 3,
        precio_compra=Decimal(f"{10 + i * 2}.50"),
        fecha_compra=date(2025, ((i - 1) % 12) + 1, 10),
        garantia_hasta=date(2027, ((i - 1) % 12) + 1, 10),
        estado=estados[i % len(estados)],
        observaciones="Registro creado automáticamente desde Django shell.",
    )

print("Se han creado 50 materiales de prueba correctamente.")