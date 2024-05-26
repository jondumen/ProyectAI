import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import subprocess
import threading
import random
import os
import pygame

size = 825, 500  # Tamaño inicial
aspect_ratio = size[0] / size[1]

def iniciar_juego(command):
    # Mostrar la barra de progreso
    progress_bar.place(relx=0.5, rely=0.9, anchor="center", relwidth=0.8)
    loading_label.place(relx=0.5, rely=0.75, anchor="center")
    progress_bar.start()

    # Ejecutar el juego en un hilo separado
    def run_game():

        subprocess.run(command)
        # Detener la barra de progreso cuando el juego se inicia
        progress_bar.stop()
        progress_bar.place_forget()  # Ocultar la barra de progreso
        loading_label.place_forget()  # Ocultar el texto de carga

    threading.Thread(target=run_game).start()

def iniciar_juego1():
    iniciar_juego(["python", "snake.py"])

def iniciar_juego2():
    iniciar_juego(["python", "pong.py"])

def iniciar_juego3():
    iniciar_juego(["python", "paint.py"])

def check_window_size(event):
    if root.state() == "normal":
        loading_label.config(font=("Bowhouse Black", 18))
    elif root.state() == "zoomed":
        loading_label.config(font=("Bowhouse Black", 24))

def actualizar_fondo(event):
    # Solo procesar cambios de tamaño una vez por evento
    nuevo_ancho = root.winfo_width()
    nuevo_alto = root.winfo_height()

    # Calcular nueva altura basada en el ancho para mantener la proporción
    esperado_alto = int(nuevo_ancho / aspect_ratio)

    # Si la altura actual no es la esperada, ajustarla
    if nuevo_alto != esperado_alto:
        root.geometry(f"{nuevo_ancho}x{esperado_alto}")
        nuevo_alto = esperado_alto

    # Redimensionar la imagen de fondo
    imagen_redimensionada = background_image.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(imagen_redimensionada)
    background_label.config(image=background_photo)
    background_label.image = background_photo

    # Actualizar tamaño de fuente del texto
    check_window_size(event)

def restore_window_size(event):
    global size
    root.geometry(f"{size[0]}x{size[1]}")

def salir():
    pygame.mixer.quit()  # Detener la reproducción de música
    root.destroy()

def mostrar_menu():
    global background_image, background_label, root, button_juego1_img, button_juego2_img, button_juego3_img, progress_bar, loading_label, size

    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry(f"{size[0]}x{size[1]}")
    root.minsize(size[0], size[1])

    # Almacenar el tamaño original de la ventana
    size = (root.winfo_width(), root.winfo_height())

    # Vincular la función restore_window_size al evento de maximizar
    root.bind("<Map>", restore_window_size)

    # Cargar imagen de fondo
    background_image = Image.open("fondo.jpg")

    # Mostrar imagen de fondo
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Redimensionar imagen de fondo cuando cambie el tamaño de la ventana
    root.bind("<Configure>", actualizar_fondo)

    # Cargar imágenes para los botones
    button_juego1_img = ImageTk.PhotoImage(Image.open("mhl.png").resize((100, 70), Image.Resampling.LANCZOS))
    button_juego2_img = ImageTk.PhotoImage(Image.open("mhl.png").resize((100, 70), Image.Resampling.LANCZOS))
    button_juego3_img = ImageTk.PhotoImage(Image.open("mhl.png").resize((100, 70), Image.Resampling.LANCZOS))

    # Botón para iniciar Snake
    button_juego1 = tk.Button(root, image=button_juego1_img, command=iniciar_juego1, bg="lightgreen")
    button_juego1.place(relx=0.237, rely=0.5, anchor="center")

    # Botón para iniciar Pong
    button_juego2 = tk.Button(root, image=button_juego2_img, command=iniciar_juego2, bg="lightgray")
    button_juego2.place(relx=0.5, rely=0.5, anchor="center")

    # Botón para iniciar Paint
    button_juego3 = tk.Button(root, image=button_juego3_img, command=iniciar_juego3, bg="lightyellow")
    button_juego3.place(relx=0.762, rely=0.5, anchor="center")

    # Añadir barra de progreso en la parte inferior, pero oculta inicialmente
    progress_bar = ttk.Progressbar(root, mode="indeterminate")
    loading_label = tk.Label(root, text="Cargando el juego...\nPor favor espera 🥺", font=("Bowhouse Black", 18), bg="#6b7cc5")
    #loading_label.pack()

    root.mainloop()

if __name__ == "__main__":
    pygame.mixer.init()  # Inicializar Pygame para reproducir música
    # Ruta completa al directorio de canciones
    directorio_canciones = r"C:\Users\Jon Hatsune\Documents\TEC II - Trabajos\4.- Inteligencia Artificial\Music"  
    # Lista de canciones MP3
    canciones = ["1.mp3", "2.mp3", "3.mp3", "4.mp3", "5.mp3", "6.mp3", "7.mp3", "8.mp3"]
    # Reproducir música aleatoria
    pygame.mixer.music.load(os.path.join(directorio_canciones, random.choice(canciones)))
    pygame.mixer.music.play(-1)  # Reproducir en bucle infinito
    mostrar_menu()
