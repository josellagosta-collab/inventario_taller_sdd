print("Iniciando carga de categorías...")
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_taller.settings")
django.setup()

from inventario.models import Categoria, Subcategoria


datos = {
    "Equipos informáticos": [
        "Ordenadores de sobremesa",
        "Portátiles",
        "Servidores",
        "Mini PC",
        "Thin Clients",
        "Raspberry Pi",
    ],
    "Componentes hardware": [
        "Placas base",
        "Procesadores",
        "Memorias RAM",
        "Discos SSD",
        "Discos HDD",
        "Tarjetas gráficas",
        "Fuentes de alimentación",
        "Ventiladores",
    ],
    "Redes": [
        "Switches",
        "Routers",
        "Firewalls",
        "Puntos de acceso WiFi",
        "Módulos SFP",
        "Conversores de medios",
    ],
    "Cableado y conectividad": [
        "Cable UTP",
        "Cable FTP",
        "Fibra óptica",
        "Latiguillos",
        "Conectores RJ45",
        "Keystone",
        "Patch panels",
    ],
    "Electrónica e IoT": [
        "ESP32",
        "ESP8266",
        "Arduino",
        "Sensores",
        "Relés",
        "Displays",
        "Módulos GPS",
        "Módulos Bluetooth",
    ],
    "Automatización industrial": [
        "PLC",
        "Módulos de entradas/salidas",
        "Variadores",
        "HMI",
        "Sensores industriales",
        "Actuadores",
    ],
    "Robótica": [
        "Robots colaborativos",
        "Pinzas",
        "Cámaras de visión",
        "Accesorios UR3",
        "Cintas transportadoras",
    ],
    "Instrumentación y medida": [
        "Multímetros",
        "Osciloscopios",
        "Fuentes de alimentación",
        "Calibres",
        "Básculas",
        "Analizadores de red",
    ],
    "Herramientas": [
        "Destornilladores",
        "Crimpadoras",
        "Pelacables",
        "Alicates",
        "Kits de reparación",
    ],
    "Periféricos": [
        "Monitores",
        "Teclados",
        "Ratones",
        "Impresoras",
        "Escáneres",
        "Webcams",
    ],
}


for nombre_categoria, subcategorias in datos.items():
    categoria, creada = Categoria.objects.get_or_create(
        nombre=nombre_categoria,
        defaults={
            "descripcion": f"Categoría de {nombre_categoria.lower()}"
        }
    )

    if creada:
        print(f"Categoría creada: {categoria.nombre}")
    else:
        print(f"Categoría ya existía: {categoria.nombre}")

    for nombre_subcategoria in subcategorias:
        subcategoria, creada = Subcategoria.objects.get_or_create(
            categoria=categoria,
            nombre=nombre_subcategoria,
            defaults={
                "descripcion": f"Subcategoría de {nombre_subcategoria.lower()}"
            }
        )

        if creada:
            print(f"  Subcategoría creada: {subcategoria.nombre}")
        else:
            print(f"  Subcategoría ya existía: {subcategoria.nombre}")

print("Proceso terminado.")