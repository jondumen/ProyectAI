# Proyecto Juego con camara web
# Materia: Inteligencia Artificial
# Profesor: Arturo Legarda Saens
# Alumnos:  Jonathan Duran Mendoza
#           Pablo Pizarro Chalup    20550431

# Descripcion: Este programa es un juego que hace uso de la camara web para detectar la posicion de la mano del jugador y asi poder mover un objeto en la pantalla.
import math
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
        self.allowedLength = 50 # Longitud maxima de la serpiente
        self.previousHead = 0, 0    # Posicion anterior de la cabeza de la serpiente

    def update(self, img, currentHead):
        px, py = self.previousHead
        cx, cy = currentHead

        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lenghts.append(distance)
        self.currentLength += distance
        self.previousHead = cx, cy

while True:
    success, img = cap.read()
    # img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)