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
color_light_gray = (192, 192, 192)   # Color gris claro


# Clase del modo de juego galaga
class Galaga:
    def __init__(self, score):
        self.score = score  # Posicion del objeto
        self.lifes = 3  # Numero de vidas inicial
        self.color = color_orange  # Color del objeto
        self.radius = 20    # Radio del objeto
        self.pos = [
            1300,   # Horizontal
            random.randint(1, 35) * self.radius # Vertical
        ]
        self.velocidad = random.randint(3, 7) * 5

    # Obtener la puntuación
    def get_score(self):
        return self.score
    
    # Obtener las vidas
    def get_lifes(self):
        return self.lifes

    # Dibujar el objeto
    def draw(self, img):
        cv2.circle(img, self.pos, self.radius, self.color, cv2.FILLED) # el circulo
        cv2.circle(img, self.pos, self.radius, color_black, 2)

        self.mover()

    # Mostrar informacion en pantalla
    def info(self, img):
        # Escribir la puntuacion en pantalla 
        cv2.putText(img, "Score: " + str(juego.get_score()), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color_black, 2, cv2.LINE_AA)
        # Escribir el numero de vidas en pantalla
        cv2.putText(img, "Lives: " + str(juego.get_lifes()), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, color_black, 2, cv2.LINE_AA)


    # Mover la pelota
    def mover(self):
        self.pos[0] -= self.velocidad

        if self.pos[0] < 0:
            self.pos = self.random_pos()
            self.velocidad = random.randint(1, 5) * 10
            self.score += 1

    # Posicion aleatoria
    def random_pos(self):
        return [
            1300,
            random.randint(1, 35) * self.radius # Vertical
        ]

    # Colision con la nave con la pelota
    def colision(self, nave):
        # if the position of the ball is touching the rectangle of the ship, then lose a life
        if (
            (nave[0] + 55 > self.pos[0] - self.radius) and 
            (nave[0] - 55 < self.pos[0] + self.radius) and 
            (nave[1] + 55 > self.pos[1] - self.radius) and 
            (nave[1] - 55 < self.pos[1] + self.radius)
            ):
            self.lifes -= 1
            self.pos = self.random_pos()
            self.velocidad = random.randint(1, 5) * 10


# Inicializar el juego
juego = Galaga(0)

while True:
    success, img = cap.read()  # Leer la imagen de la camara
    img = cv2.flip(img, 1)  # Voltear la imagen horizontalmente
    hands, img = detector.findHands(img, False, False)    # Detectar las manos en la imagen
    nave = cv2.imread('nave.png', cv2.IMREAD_UNCHANGED) # Leer la imagen de la nave

    # en caso de que el jugador pierda
    if juego.get_lifes() <= 0:
        cv2.putText(img, "GAME OVER", (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, color_black, 8, cv2.LINE_AA)
        cv2.putText(img, "GAME OVER", (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, color_white, 2, cv2.LINE_AA)

        cv2.putText(img, "Press 'r' to restart", (530, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, color_black, 8, cv2.LINE_AA)
        cv2.putText(img, "Press 'r' to restart", (530, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, color_white, 2, cv2.LINE_AA)

        cv2.putText(img, "Press 'q' to quit", (530, 390), cv2.FONT_HERSHEY_SIMPLEX, 1, color_black, 8, cv2.LINE_AA)
        cv2.putText(img, "Press 'q' to quit", (530, 390), cv2.FONT_HERSHEY_SIMPLEX, 1, color_white, 2, cv2.LINE_AA)
    else:
        # Dibujar la pelota
        juego.draw(img)
        juego.info(img)

    # Dibujar la mano
    if hands:
        lmList = hands[0]['lmList']   # Lista de puntos de la mano
        centerPoint = hands[0]['center']   # Punto central de la mano

        # colocar imagen de nave en el centro de la mano
        nave = cv2.resize(nave, (130, 130)) # Cambiar el tamaño de la imagen
        nave = cv2.rotate(nave, cv2.ROTATE_90_CLOCKWISE) # Rotar la imagen
        img = cvzone.overlayPNG(img, nave, [centerPoint[0] - 70, centerPoint[1] - 62]) # Superponer la imagen en la pantalla

        # Detectar la colision con la nave
        juego.colision(centerPoint)

        # Dibujar coliision box de la nave
        cv2.rectangle(img, (centerPoint[0] - 55, centerPoint[1] - 55), (centerPoint[0] + 55, centerPoint[1] + 55), color_black, 2)
        

    cv2.imshow("Handlaga", img)    # Mostrar la imagen

    # Cerrar juego
    key = cv2.waitKey(1) & 0xFF  # Obtener los bits menos significativos
    if key == ord('q') or key == 27:  # Presionar 'q' o la tecla ESC para salir
        break
    if key == ord('r'):
        juego = Galaga(juego.get_score())    # Reiniciar el juego
    
    # Verificar si la ventana ha sido cerrada
    if cv2.getWindowProperty("Handlaga", cv2.WND_PROP_AUTOSIZE) < 1:
        break

cap.release()
cv2.destroyAllWindows()