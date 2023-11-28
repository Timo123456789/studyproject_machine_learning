import cv2

# Lese das Bild
image = cv2.imread('D:/SP_ML4IM/insects/train/images/img_001_000001.png')

# Konvertiere das Bild in Graustufen
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gehe durch jede Zeile
for i in range(1000, 1500):
    # Gebe die Zeilennummer und den Pixelwert aus
    print(f'Zeile {i}: {gray[i, 0]}')