import tkinter as tk
from PIL import ImageTk, Image
import subprocess

size = 400, 300

def iniciar_juego1():
    subprocess.run(["python", "main.py"])

def mostrar_menu():
    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry("400x300")

    # Cargar imagen de fondo
    background_image = Image.open("fondo.jpg")
    background_image = background_image.resize(size, Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Mostrar imagen de fondo
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Botón para iniciar juego 1
    button_juego1 = tk.Button(root, text="Snake", command=iniciar_juego1, bg="lightblue")
    button_juego1.place(relx=0.5, rely=0.4, anchor="center")

    '''# Botón para iniciar juego 2
    button_juego2 = tk.Button(root, text="Juego 2", command=iniciar_juego2, bg="lightgreen")
    button_juego2.place(relx=0.5, rely=0.5, anchor="center")'''

    root.mainloop()

if __name__ == "__main__":
    mostrar_menu()
