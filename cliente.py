import time
import random
from shared import FOOD_TRUCK_MENUS
import os

def cargar_nombres(path='datos/nombres_clientes.txt'):
    if not os.path.exists(path):
        return ['Cliente']
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def generar_clientes(queues_pedidos, queue_actualizaciones):
    nombres = cargar_nombres()
    usados = set()

    while True:
        nombre = random.choice(nombres)
        while nombre in usados and len(usados) < len(nombres):
            nombre = random.choice(nombres)
        usados.add(nombre)
        if len(usados) > len(nombres) * 0.8:
            usados.clear()

        truck = random.choice(list(FOOD_TRUCK_MENUS.keys()))
        plato = random.choice(FOOD_TRUCK_MENUS[truck])

        pedido = {
            'cliente': nombre,
            'plato': plato
        }

        queues_pedidos[truck].put(pedido)

        # ✅ Enviamos evento a main.py (formato fijo: truck, tipo, cliente)
        queue_actualizaciones.put((truck, "nuevo", nombre))

        print(f"[Cliente] {nombre} se ha puesto en la cola de {truck} y ha pedido {plato}")
        time.sleep(random.uniform(1, 2))