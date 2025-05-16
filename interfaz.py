import tkinter as tk

# Diccionario de food trucks con emojis
food_trucks = {
    "USA": "🍔",
    "Italia": "🍕",
    "España": "🥘",
    "Asia": "🍜",
    "Francia": "🍷",
    "México": "🌮"
}

estado_labels = {}
contador_labels = {}
cola_puntos = {}
puntos_frames = {}

def crear_food_truck(parent, nombre, emoji):
    frame = tk.Frame(parent)
    frame.pack(side=tk.LEFT, padx=40, pady=40)

    camion_frame = tk.Frame(frame, bg="lightblue", width=240, height=120, bd=4, relief=tk.SOLID)
    camion_frame.pack()
    camion_frame.pack_propagate(False)

    label_nombre = tk.Label(camion_frame, text=f"{emoji} {nombre}", font=("Arial", 22, "bold"), bg="lightblue", fg="white")
    label_nombre.pack(expand=True)

    contador = tk.Label(frame, text="0 servidos | 0 en cola", font=("Arial", 18))
    contador.pack(pady=10)
    contador_labels[nombre] = contador

    puntos_frame = tk.Frame(frame)
    puntos_frame.pack(pady=10)
    puntos_frames[nombre] = puntos_frame
    cola_puntos[nombre] = []

def actualizar_contador(nombre, servidos, en_cola):
    if nombre in contador_labels:
        contador_labels[nombre].config(text=f"{servidos} servidos | {en_cola} en cola")

def actualizar_puntos_cola(nombre, estados):
    if nombre not in puntos_frames:
        return

    frame = puntos_frames[nombre]

    for widget in frame.winfo_children():
        widget.destroy()

    cola_puntos[nombre] = []

    for estado in estados:
        color = {
            'esperando': 'gray',
            'atendiendo': 'orange',
            'servido': 'green',
            'rechazado': 'red'
        }.get(estado, 'black')

        punto = tk.Canvas(frame, width=24, height=24, highlightthickness=0)
        punto_id = punto.create_oval(4, 4, 20, 20, fill=color)
        punto.pack(pady=4)
        cola_puntos[nombre].append((punto, punto_id))

def lanzar_interfaz(shared_estado_queue=None):
    root = tk.Tk()
    root.title("Food Truck Festival")
    root.configure(bg="#222222")  # fondo oscuro para mejor contraste

    fila_superior = tk.Frame(root, bg="#222222")
    fila_superior.pack()
    fila_inferior = tk.Frame(root, bg="#222222")
    fila_inferior.pack()

    for i, (nombre, emoji) in enumerate(food_trucks.items()):
        fila = fila_superior if i < 3 else fila_inferior
        crear_food_truck(fila, nombre, emoji)

    def revisar_actualizaciones():
        if shared_estado_queue:
            while not shared_estado_queue.empty():
                try:
                    nombre, estado, servidos, cola = shared_estado_queue.get_nowait()
                    actualizar_contador(nombre, servidos, len(cola))
                    actualizar_puntos_cola(nombre, cola)
                except Exception as e:
                    print("Error al actualizar interfaz:", e)
        root.after(500, revisar_actualizaciones)

    revisar_actualizaciones()
    root.mainloop()
