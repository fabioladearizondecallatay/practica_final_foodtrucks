# 🍽️ Simulación Concurrente de un Festival de Food Trucks

Este proyecto simula un festival de food trucks, donde múltiples camiones atienden pedidos de clientes en paralelo, gestionan ingredientes limitados y muestran en tiempo real el estado de los pedidos en una interfaz visual.

---

## Objetivo

Demostrar el uso práctico de conceptos de **concurrencia, paralelismo y sincronización** en Python, a través de un sistema distribuido y visualmente interactivo.

---

## Estructura del proyecto

foodtruck/

├── cliente.py # Proceso generador de clientes

├── food_truck.py # Lógica concurrente de cada food truck

├── cocina.py # Recetas y control de stock

├── interfaz.py # Interfaz gráfica con Tkinter

├── main.py # Orquestador principal del sistema

├── shared.py # Menús y datos comunes

├── ingredientes.json # Stock inicial de ingredientes

└── nombres_clientes.txt # Lista de nombres aleatorios

---

## ¿Cómo se ejecuta?

1. Clona el proyecto o descarga todos los archivos.
2. Ejecuta el programa desde el terminal:

```bash
python main.py
