import tkinter as tk
from tkinter import ttk
import re

# Definir patrones de expresiones regulares
palabras_reservadas = {'if', 'else', 'while', 'for', 'return', 'void', 'static'}
patron_cadenas = r'\".*?\"|\'.*?\''
patron_identificadores = r'\b(?!(?:' + '|'.join(palabras_reservadas) + r')\b)[a-zA-Z_]\w*\b'
patron_simbolos = r'[+\-*/=,;(){}[\]]'

# Diccionario para mapear símbolos a sus descripciones
descripcion_simbolos = {
    '+': 'Operador de suma',
    '-': 'Operador de resta',
    '*': 'Operador de multiplicación',
    '/': 'Operador de división',
    '=': 'Operador de asignación',
    ',': 'Coma',
    ';': 'Punto y coma',
    '(': 'Paréntesis de apertura',
    ')': 'Paréntesis de cierre',
    '{': 'Llave de apertura',
    '}': 'Llave de cierre',
    '[': 'Corchete de apertura',
    ']': 'Corchete de cierre'
}

def analizar_codigo(codigo):
    tokens = []

    # Buscar palabras reservadas y añadir la palabra misma
    for palabra in palabras_reservadas:
        for match in re.finditer(r'\b{}\b'.format(palabra), codigo):
            tokens.append((palabra, "Palabra reservada"))

    # Buscar cadenas
    tokens += [(cadena, "Cadena") for cadena in re.findall(patron_cadenas, codigo)]

    # Buscar identificadores y añadir la leyenda "Identificador"
    for identificador in re.finditer(patron_identificadores, codigo):
        tokens.append((identificador.group(), "Identificador"))

    # Buscar símbolos y añadir descripción en lugar del símbolo
    for simbolo in re.findall(patron_simbolos, codigo):
        if simbolo in descripcion_simbolos:
            tokens.append((descripcion_simbolos[simbolo], simbolo))
        else:
            tokens.append((simbolo, simbolo))

    return tokens

def analizar():
    codigo = texto_codigo.get("1.0", "end-1c")
    tokens = analizar_codigo(codigo)
    # Limpiar árbol existente
    for item in tree.get_children():
        tree.delete(item)
    # Mostrar resultados en el Treeview
    for token in tokens:
        tree.insert("", "end", values=(token[0], token[1]))

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico")

frame_codigo = ttk.Frame(root)
frame_codigo.pack(fill=tk.BOTH, expand=True)

texto_codigo = tk.Text(frame_codigo)
texto_codigo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll = ttk.Scrollbar(frame_codigo, orient=tk.VERTICAL, command=texto_codigo.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
texto_codigo['yscrollcommand'] = scroll.set

boton_analizar = ttk.Button(root, text="Analizar", command=analizar)
boton_analizar.pack()

tree = ttk.Treeview(root, columns=('Token', 'Tipo'))
tree.heading('#1', text='Token')
tree.heading('#2', text='Tipo')



tree.pack(fill=tk.BOTH, expand=True)

root.mainloop()

