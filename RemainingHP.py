import device
import cv2
import numpy as np

def SeleccionarCapturadora(recuento):

    mensaje = "Select a camera (0 to " + str(recuento) + "): "
    try:
        valor = int(input(mensaje))
        # select = int(select)
    except Exception:
        print("It's not a number!")
        return SeleccionarCapturadora(recuento)

    if valor > recuento:
        print("Invalid number! Retry!")
        return SeleccionarCapturadora(recuento)

    return valor

def main():
    # print OpenCV version
    print("OpenCV version: " + cv2.__version__)

    # Get camera list
    device_list = device.getDeviceList()
    etiqueta = 0

    for name in device_list:
        print(str(etiqueta) + ': ' + name)
        etiqueta += 1

    recuento = etiqueta - 1

    if recuento < 0:
        print("No device is connected")
        return

    # Select a camera
    NumeroCapturadora = SeleccionarCapturadora(recuento)

    return NumeroCapturadora


capture = cv2.VideoCapture(main())
capture.set(3, 1280)
capture.set(4, 720)

# Definir colores
gris_min = np.array([0, 0, 0])        # Promedio del rango mínimo de color gris con 3 capturadoras diferentes
gris_max = np.array([177, 255, 125])        # Promedio del rango maximo de color gris con 3 capturadoras diferentes
verde_min = np.array([25, 156, 35])
verde_max = np.array([76, 255, 255])

# Funcion para detectar punto control
def NumberHP1(x):
    contornos, hierarchy = cv2.findContours(x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if contornos == [] and checkpoint(CheckHP1) == True:
        cv2.putText(frame, r'100%',
                    (710, 120),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)
    for cnt in contornos:
        # area = cv2.contourArea(cnt)
        # if area>50:
        # cv2.drawContours(frame, cnt, -1, (255, 0, 0), 3)
        perimetro = cv2.arcLength(cnt, True)
        vertices = cv2.approxPolyDP(cnt,0.02*perimetro, True)
        x, y, w, h = cv2.boundingRect(vertices)

        porcentaje = 100*(1 - (w/266))

        # Use putText() method for inserting text on video
        cv2.putText(frame, str(round(porcentaje,2)) + r'%',
                    (710, 120),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)


def NumberHP2(x):
    contornos, hierarchy = cv2.findContours(x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if contornos == [] and checkpoint(CheckHP2) == True:
        cv2.putText(frame, r'100%',
                    (1050, 120),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)
    for cnt in contornos:
        # area = cv2.contourArea(cnt)
        # if area>50:
        # cv2.drawContours(frame, cnt, -1, (255, 0, 0), 3)
        perimetro = cv2.arcLength(cnt, True)
        vertices = cv2.approxPolyDP(cnt, 0.02 * perimetro, True)
        x, y, w, h = cv2.boundingRect(vertices)

        porcentaje = 100 * (1 - (w / 266))

        # Use putText() method for inserting text on video
        cv2.putText(frame, str(round(porcentaje, 2)) + r'%',
                    (1050, 120),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)

def checkpoint(x):
    contornos, hierarchy = cv2.findContours(x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area > 30:
            # cv2.drawContours(frame, cnt, -1, (255, 0, 0), 3)
            return True
        else:
            return False


# Bucle de ejecucion del programa

while True:

    # Leer la capturadora
    success, frame = capture.read()
    clean = frame.copy()

    # Transformación y manipulación del frame
    FrameBlur = cv2.GaussianBlur(frame, (7, 7), 1)                   # Difuminar el Frame
    FrameHSV = cv2.cvtColor(FrameBlur, cv2.COLOR_BGR2HSV)            # Conversión de color del Frame a gama de color HSV

    # Crear mascara de color
    maskGrey = cv2.inRange(FrameHSV, gris_min, gris_max)        # White tone detection mask  - for ALL
    maskGreen = cv2.inRange(FrameHSV, verde_min, verde_max)
    # Definir puntos de deteccion
    HP1 = maskGrey[65:70, 636:902]
    CheckHP1 = maskGreen[65:70, 700:750]
    HP2 = maskGrey[65:70, 978:1244]
    CheckHP2 = maskGreen[65:70, 1000:1050]

    # LLAMADA DE FUNCIONES

    NumberHP1(HP1)
    NumberHP2(HP2)

# Mostrar ventanas


    cv2.imshow("frame", frame)              # SHOW HIDE VGC INFO window
    # cv2.imshow("clean", clean)              # SHOW CLEANFEED window

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
