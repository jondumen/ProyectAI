# Proyecto Juego con camara web
# Materia: Inteligencia Artificial
# Profesor: Arturo Legarda Saens
# Alumnos:  Jonathan Duran Mendoza  20550401
#           Pablo Pizarro Chalup    20550431

# Descripcion: Este programa es un juego que hace uso de la camara web para detectar la posicion de la mano del jugador y asi poder mover un objeto en la pantalla.

import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)   # Iniciar la camara web
cap.set(3, 1280)    # Ancho de la camara
cap.set(4, 720) # Alto de la camara

detector = HandDetector(detectionCon=0.8, maxHands=1)   # Detector de manos

color_blue = (255, 0, 0)    # Color azul
color_green = (0, 255, 0)   # Color verde
color_red = (0, 0, 255) # Color rojo
color_yellow = (0, 255, 255)   # Color amarillo
color_purple = (255, 0, 255)   # Color morado
color_orange = (0, 140, 255)   # Color naranja
color_white = (255, 255, 255)  # Color blanco
color_black = (0, 0, 0)    # Color negro
sky_blue = (235, 206, 135)   # Color azul cielo


# Clase del modo de juego Ping Pong
class PingPong:
    def __init__(self, pos, color):
        self.pos = pos  # Posicion de la pelota
        self.color = color  # Color de la pelota
        self.radius = 20    # Radio de la pelota
        self.direccion = [
            random.randint(-5, -1),
            random.randint(-5, 5)
        ] 

    # Dibujar la pelota
    def draw(self, img): # Dibujar la pelota
        cv2.circle(img, self.pos, self.radius, self.color, cv2.FILLED) # el circulo
        cv2.circle(img, self.pos, self.radius, color_black, 2)
        self.mover()

    # Mover la pelota
    def mover(self):
        self.pos[0] += self.direccion[0]*9
        self.pos[1] += self.direccion[1]*9
        
        # Detectar colision con la ventana
        #   Deteccion en lo horizontal
        if (self.pos[0] < 10 or self.pos[0] > 1270):
            self.direccion[0] = self.direccion[0] * -1
        
        #   deteccion en lo vertical
        if (self.pos[1] < 10 or self.pos[1] > 710):
            self.direccion[1] = self.direccion[1] * -1


juego = PingPong([640, 360], sky_blue)    # Initialize the game

while True:
    success, img = cap.read()  # Leer la imagen de la camara
    img = cv2.flip(img, 1)  # Voltear la imagen horizontalmente
    hands, img = detector.findHands(img, flipType=False)    # Detectar las manos en la imagen
    grosor = 15 # Grosor de la linea
    
    # Dibujar la pelota
    juego.draw(img)

    if hands:
        lmList = hands[0]['lmList']   # Lista de puntos de la mano
        centerPoint = hands[0]['center']   # Punto central de la mano
        punto1 = (centerPoint[0] - grosor, centerPoint[1] - 100)
        punto2 = (centerPoint[0] + grosor, centerPoint[1] + 100)

        # dibujar un punto en el centro de la mano
        cv2.rectangle(img, punto1, punto2, color_green, cv2.FILLED) # el rectangulo
        cv2.rectangle(img, punto1, punto2, color_black, 2) # el borde del rectangulo
        
        

    cv2.imshow("Image", img)    # Mostrar la imagen

    # Cerrar juego
    key = cv2.waitKey(1) & 0xFF  # Obtener los bits menos significativos
    if key == ord('q') or key == 27:  # Presionar 'q' o la tecla ESC para salir
        break
    if key == ord('r'):
        juego = PingPong([640, 360], sky_blue)    # Reiniciar el juego
    
    # Verificar si la ventana ha sido cerrada
    if cv2.getWindowProperty("Image", cv2.WND_PROP_AUTOSIZE) < 1:
        break

cap.release()
cv2.destroyAllWindows()