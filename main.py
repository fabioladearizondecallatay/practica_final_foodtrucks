from multiprocessing import Process, Queue
from cliente import generar_clientes
from food_truck import food_truck_process
from interfaz import lanzar_interfaz
from shared import FOOD_TRUCK_MENUS
from cocina import inicializar_stock, cargar_recetas
from collections import defaultdict
import time
import threading

if __name__ == '__main__':
    # Colas para pedidos y para la interfaz
    queue_pedidos = {ft: Queue() for ft in FOOD_TRUCK_MENUS}
    queue_eventos = Queue()       # comunicación desde cliente/food_truck
    queue_interfaz = Queue()      # comunicación hacia la interfaz

    stock = inicializar_stock()
    recetas = cargar_recetas()

    # 🧠 Estado local por food truck
    estado_en_memoria = defaultdict(list)
    servidos_por_truck = defaultdict(int)

    def procesar_eventos():
        def loop():
            while True:
                while not queue_eventos.empty():
                    try:
                        truck, tipo, cliente = queue_eventos.get_nowait()

                        if tipo == "nuevo":
                            estado_en_memoria[truck].append({
                                "cliente": cliente,
                                "estado": "esperando"
                            })

                        elif tipo == "atendiendo":
                            for pedido in estado_en_memoria[truck]:
                                if pedido["cliente"] == cliente:
                                    pedido["estado"] = "atendiendo"
                                    break

                        elif tipo == "servido":
                            for pedido in estado_en_memoria[truck]:
                                if pedido["cliente"] == cliente:
                                    pedido["estado"] = "servido"
                                    pedido["fin"] = time.time()
                                    break
                            servidos_por_truck[truck] += 1

                        elif tipo == "rechazado":
                            encontrado = False
                            for pedido in estado_en_memoria[truck]:
                                if pedido["cliente"] == cliente:
                                    pedido["estado"] = "rechazado"
                                    pedido["fin"] = time.time()
                                    encontrado = True
                                    break
                            if not encontrado:
                                estado_en_memoria[truck].append({
                                    "cliente": cliente,
                                    "estado": "rechazado",
                                    "fin": time.time()
                                })

                    except Exception as e:
                        print("❌ Error procesando evento:", e)

                # Eliminar servidos/rechazados que hayan estado visibles > 2 segundos
                tiempo_actual = time.time()
                for truck in list(estado_en_memoria):
                    estado_en_memoria[truck] = [
                        p for p in estado_en_memoria[truck]
                        if not (p["estado"] in ("servido", "rechazado") and tiempo_actual - p.get("fin", 0) > 2)
                    ]

                # Enviar resumen a la interfaz
                for truck, pedidos in estado_en_memoria.items():
                    estados = [p["estado"] for p in pedidos]
                    servidos = servidos_por_truck[truck]
                    queue_interfaz.put((truck, "", servidos, estados))

                time.sleep(0.5)

        threading.Thread(target=loop, daemon=True).start()

    # Lanzar food trucks
    procesos = []
    for nombre in FOOD_TRUCK_MENUS:
        p = Process(target=food_truck_process, args=(
            nombre, queue_pedidos[nombre], stock, queue_eventos, recetas
        ))
        p.start()
        procesos.append(p)

    # Lanzar proceso de clientes
    p_clientes = Process(target=generar_clientes, args=(queue_pedidos, queue_eventos))
    p_clientes.start()

    # Iniciar procesador de eventos y lanzar la interfaz
    procesar_eventos()
    lanzar_interfaz(queue_interfaz)
