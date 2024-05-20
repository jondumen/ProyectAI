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

while True:
    success, img = cap.read()  # Leer la imagen de la camara
    img = cv2.flip(img, 1)  # Voltear la imagen horizontalmente
    hands, img = detector.findHands(img, flipType=False)    # Detectar las manos en la imagen

    if hands:
        lmList = hands[0]['lmList']   # Lista de puntos de la mano
        pointIndex = lmList[8][0:2]  # Punto de la punta del dedo indice
        # cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)
    cv2.imshow("Image", img)    # Mostrar la imagen

    # Cerrar juego
    key = cv2.waitKey(1) & 0xFF  # Obtener los bits menos significativos
    if key == ord('q') or key == 27:  # Presionar 'q' o la tecla ESC para salir
        break

    # Verificar si la ventana ha sido cerrada
    if cv2.getWindowProperty("Image", cv2.WND_PROP_AUTOSIZE) < 1:
        break

cap.release()
cv2.destroyAllWindows()