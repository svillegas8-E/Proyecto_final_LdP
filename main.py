import os
import re
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO


# Funciones para el análisis lexicográfico
def cargar_palabras(letra):
    ruta = f'{letra}.txt'
    palabras = set()
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for palabra in archivo:
            palabras.add(palabra.strip())
    return palabras


def identificar_emoticones(cadena):
    emoticones_encontrados = re.findall(
        r':\)|:\(|:D|;\)|xD|:-\)|:-\(|\(y\)|\(n\)|:-O|:O|>:\(|:-\]', cadena)
    return emoticones_encontrados


def analizador_lexicografico(cadena):
    diccionario_espanol = {}
    for letra in 'abcdefghijklmnñopqrstuvwxyz':
        palabras_letra = cargar_palabras(letra)
        diccionario_espanol[letra] = palabras_letra
    palabras_encontradas = re.findall(r'\b\w+\b', cadena)
    palabras_espanol = sum(1 for palabra in palabras_encontradas if any(
        palabra.lower() in diccionario_letra for diccionario_letra in diccionario_espanol.values()))
    emoticones = identificar_emoticones(cadena)
    return palabras_encontradas, palabras_espanol, emoticones


def cargar_imagenes_emoticones():
    ruta_emoticones = {
        ":)": "003-feliz.png",
        ":(": "009-triste.png",
        ":D": "005-sonriente.png",
        ";)": "018-guino.png",
        "xD": "058-riendo.png",
        ":-)": "014-sonrisa.png",
        ":-(": "029-triste-1.png",
        "(y)": "031-me-gusta-1.png",
        "(n)": "028-pulgares-abajo.png",
        ":-O": "055-sorpresa.png",
        ":O": "004-conmocionado.png",
        ">:(": "051-enojado-2.png",
        ":-]": "047-feliz-2.png",
    }
    imagenes_emoticones = {}
    for emoticon, ruta in ruta_emoticones.items():
        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize((30, 30))
            imagen = ImageTk.PhotoImage(imagen)
            imagenes_emoticones[emoticon] = imagen
        except FileNotFoundError:
            print(f"No se encontró el archivo para el emoticón: {emoticon}")
    return imagenes_emoticones


# Funciones para la interfaz gráfica
def procesar_cadena():
    cadena = texto_entrada.get("1.0", "end-1c")
    palabras, palabras_espanol, emoticones = analizador_lexicografico(cadena)
    # Cargar las imágenes de los emoticones
    imagenes_emoticones = cargar_imagenes_emoticones()
    # Mostrar la cadena ingresada y los resultados del análisis en la interfaz
    texto_salida.delete(1.0, tk.END)
    texto_salida.insert(tk.END, f"Cadena ingresada: {cadena}\n\n")
    for emoticon in emoticones:
        if emoticon in imagenes_emoticones:
            imagen = imagenes_emoticones[emoticon]
            texto_salida.image_create(tk.END, image=imagen)
        else:
            texto_salida.insert(tk.END, f"{emoticon} ")  # Mostrar emoticones no encontrados como texto
    texto_salida.insert(tk.END, "\n\n")
    texto_salida.insert(tk.END, f"Palabras encontradas: {palabras}\n")
    texto_salida.insert(tk.END, f"Palabras en español: {palabras_espanol}\n")
    texto_salida.insert(tk.END, f"Emoticones encontrados: {emoticones}\n")


# Creación de la interfaz gráfica
root = tk.Tk()
root.title("Analizador Lexicográfico")
# Cargar la imagen del logo
ruta_logo = "logo_eafit_completo.png"
imagen = Image.open(ruta_logo)
imagen = imagen.resize((200, 100))
imagen = ImageTk.PhotoImage(imagen)
# Mostrar la imagen en un widget de la interfaz
panel_logo = tk.Label(root, image=imagen)
panel_logo.pack(side="top", anchor="nw")
etiqueta = tk.Label(root, text="Ingrese la cadena:")
etiqueta.pack()
texto_entrada = tk.Text(root, height=10, width=50)
texto_entrada.pack()
boton_procesar = tk.Button(root, text="Procesar", command=procesar_cadena)
boton_procesar.pack()
texto_salida = tk.Text(root, height=50, width=100, bg="white")
texto_salida.pack()
root.mainloop()
