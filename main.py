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

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGameClass:
    def __init__(self):
        self.points = []    # Lista de puntos de la serpiente
        self.lenghts = []   # Lista de longitudes de la serpiente
        self.currentLength = 0  # Longitud actual de la serpiente
        self.allowedLength = 150 # Longitud maxima de la serpiente
        self.previousHead = 0, 0    # Posicion anterior de la cabeza de la serpiente

        self.imgFood = cv2.imread('donut.png', cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoints = 0, 0
        self.randomFoodLoc()

        self.score = 0

    def randomFoodLoc(self):
        self.foodPoints = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        px, py = self.previousHead
        cx, cy = currentHead

        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lenghts.append(distance)
        self.currentLength += distance
        self.previousHead = cx, cy

        # Lenght reduction
        if self.currentLength > self.allowedLength:
            for i, lenght in enumerate(self.lenghts):
                self.currentLength -= lenght
                self.lenghts.pop(i)
                self.points.pop(i)
                if self.currentLength < self.allowedLength:
                    break

        # Comer comida
        rx, ry = self.foodPoints
        if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
            self.randomFoodLoc()
            self.allowedLength += 50
            self.score += 1
            print("Score:", self.score)

        # Dibujar serpiente
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    cv2.line(imgMain, self.points[i-1], self.points[i], (0, 0, 250), 20)
            cv2.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

        # Dibujar comida
        imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))
    
        return imgMain

game = SnakeGameClass()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        # cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)
        img = game.update(img, pointIndex)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF  # Obtener los bits menos significativos
    if key == ord('q') or key == 27:  # Presionar 'q' o la tecla ESC para salir
        break

    # Verificar si la ventana ha sido cerrada
    if cv2.getWindowProperty("Image", cv2.WND_PROP_AUTOSIZE) < 1:
        break

cap.release()
cv2.destroyAllWindows()