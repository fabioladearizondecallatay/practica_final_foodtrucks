import time
import random
from cocina import cargar_recetas

recetas = cargar_recetas()

def food_truck_process(nombre, cola_pedidos, stock, queue_actualizaciones, recetas):
    pedidos_servidos = 0

    while True:
        if not cola_pedidos.empty():
            pedido = cola_pedidos.get()
            cliente = pedido['cliente']
            plato = pedido['plato']

            print(f"[{nombre}] 🍽️ Pedido recibido: {plato} para {cliente}")
            queue_actualizaciones.put((nombre, "atendiendo", cliente))

            time.sleep(random.uniform(8, 10))  # Simula cocina

            if puede_cocinar(plato, stock):
                cocinar(plato, stock)
                pedidos_servidos += 1
                print(f"[{nombre}] ✅ {plato} servido a {cliente}")
                queue_actualizaciones.put((nombre, "servido", cliente))
            else:
                print(f"[{nombre}] ❌ Sin stock para {plato}")
                queue_actualizaciones.put((nombre, "rechazado", cliente))
        else:
            time.sleep(0.5)

def puede_cocinar(plato, stock):
    if plato not in recetas:
        return False
    for ing, cant in recetas[plato].items():
        if stock.get(ing, 0) < cant:
            return False
    return True

def cocinar(plato, stock):
    for ing, cant in recetas[plato].items():
        stock[ing] -= cant