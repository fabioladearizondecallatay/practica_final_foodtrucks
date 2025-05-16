import json

def inicializar_stock():
    with open('datos/ingredientes.json', 'r', encoding='utf-8') as f:
        return json.load(f)['stock']

def cargar_recetas():
    with open('datos/ingredientes.json', 'r', encoding='utf-8') as f:
        return json.load(f)['recetas']
