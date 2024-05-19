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
from main import mostrar_menu

def iniciar_juego1():
    # Lógica del juego 3
    print("¡Iniciando Snake Game!")

cap = cv2.VideoCapture(0)   # Iniciar la camara web
cap.set(3, 1280)    # Ancho de la camara
cap.set(4, 720) # Alto de la camara

detector = HandDetector(detectionCon=0.8, maxHands=1)   # Detector de manos

# Clase del juego de la serpiente
class SnakeGameClass:
    def __init__(self):
        self.points = []    # Lista de puntos de la serpiente
        self.lenghts = []   # Lista de longitudes de la serpiente
        self.currentLength = 0  # Longitud actual de la serpiente
        self.allowedLength = 150 # Longitud maxima de la serpiente
        self.previousHead = 0, 0    # Posicion anterior de la cabeza de la serpiente

        self.imgFood = cv2.imread('donut.png', cv2.IMREAD_UNCHANGED)    # Cargar imagen de la comida
        self.hFood, self.wFood, _ = self.imgFood.shape  # Obtener dimensiones de la comida
        self.foodPoints = 0, 0  # Posicion de la comida
        self.randomFoodLoc()    # Posicion aleatoria de la comida

        self.score = 0  # Puntaje
        self.scoreFinal = 0  # Puntaje
        self.gameOver = False   # Juego terminado

    # Posicion aleatoria de la comida
    def randomFoodLoc(self):
        self.foodPoints = random.randint(100, 1000), random.randint(100, 600)

    # Actualizar el juego
    def update(self, imgMain, currentHead):
        if self.gameOver:   # Verificar si el juego ha terminado
            cvzone.putTextRect(imgMain, "GAME OVER", (500, 300), scale=7, offset=20, thickness=5, border=2)    # Imprimir GAME OVER
            cvzone.putTextRect(imgMain, "SCORE: " + str(self.scoreFinal), (500, 500), scale=5, offset=20, thickness=5, border=2)
        else:
            px, py = self.previousHead  # Posicion anterior de la cabeza
            cx, cy = currentHead    # Posicion actual de la cabeza

            self.points.append([cx, cy])    # Agregar la posicion actual de la cabeza a la lista de puntos
            distance = math.hypot(cx - px, cy - py)   # Distancia entre la posicion anterior y la actual de la cabeza
            self.lenghts.append(distance)   # Agregar la distancia a la lista de longitudes
            self.currentLength += distance  # Aumentar la longitud actual
            self.previousHead = cx, cy  # Actualizar la posicion anterior de la cabeza

            # Verificar si la serpiente ha alcanzado la longitud maxima
            if self.currentLength > self.allowedLength:
                for i, lenght in enumerate(self.lenghts):
                    self.currentLength -= lenght    # Disminuir la longitud actual
                    self.lenghts.pop(i) # Eliminar la longitud de la lista
                    self.points.pop(i)  # Eliminar el punto de la lista
                    # Verificar si la longitud actual es menor a la longitud maxima
                    if self.currentLength < self.allowedLength:
                        break

            # Comer comida
            rx, ry = self.foodPoints   # Posicion de la comida

            # Verificar si la cabeza de la serpiente esta en la posicion de la comida
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLoc()
                self.allowedLength += 50    # Aumentar la longitud maxima
                self.score += 1 # Aumentar el puntaje
                self.scoreFinal = self.score    # Aumentar el puntaje final
                print("Score:", self.score) # Imprimir el puntaje

            # Dibujar serpiente
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i-1], self.points[i], (0, 0, 250), 20)   # Dibujar la serpiente
                cv2.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)  # Dibujar la cabeza de la serpiente

            # Dibujar comida
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))

            # Dibujar puntaje
            cvzone.putTextRect(imgMain, "SCORE: " + str(self.score), [50, 50], scale=3, offset=10, thickness=3, border=2)

            # Colisiones con la cola de la serpiente
            pts = np.array(self.points[:-2], np.int32)  # Puntos de la serpiente
            pts = pts.reshape((-1, 1, 2))   # Redimensionar los puntos
            cv2.polylines(imgMain, [pts], False, (0, 200, 0), 3)    # Dibujar la serpiente
            minDistance = cv2.pointPolygonTest(pts, (cx, cy), True)  # Verificar si la cabeza de la serpiente colisiona con la cola
            # print(minDistance)  # Imprimir la distancia minima

            if -1 <= minDistance <= 1:  # Verificar si la distancia minima es menor o igual a 1
                print("COLLISION")  # Imprimir COLISION
                self.gameOver = True    # Juego terminado

                # Limpiar la serpiente
                self.points = []
                self.lenghts = []
                self.currentLength = 0
                self.allowedLength = 150
                self.previousHead = 0, 0

                # Reiniciar la comida
                self.randomFoodLoc()

                # Reiniciar el puntaje
                self.score = 0
    
        return imgMain

game = SnakeGameClass()

while True:
    success, img = cap.read()  # Leer la imagen de la camara
    img = cv2.flip(img, 1)  # Voltear la imagen horizontalmente
    hands, img = detector.findHands(img, flipType=False)    # Detectar las manos en la imagen

    if hands:
        lmList = hands[0]['lmList']   # Lista de puntos de la mano
        pointIndex = lmList[8][0:2]  # Punto de la punta del dedo indice
        # cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)
        img = game.update(img, pointIndex)  # Actualizar el juego

    cv2.imshow("Image", img)    # Mostrar la imagen

    # Cerrar juego
    key = cv2.waitKey(1) & 0xFF  # Obtener los bits menos significativos
    if key == ord('q') or key == 27:  # Presionar 'q' o la tecla ESC para salir
        break
    if key == ord('r'):
        game.gameOver = False

    # Verificar si la ventana ha sido cerrada
    if cv2.getWindowProperty("Image", cv2.WND_PROP_AUTOSIZE) < 1:
        break

cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    mostrar_menu()
    iniciar_juego1()  # Llamada a la función del juego 3