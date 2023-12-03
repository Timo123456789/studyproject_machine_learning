import cv2

# this script was for finding the exact cut line between rgb and dvs

# Lese das Bild
image = cv2.imread('path/to/raw/image')

# Konvertiere das Bild in Graustufen
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gehe durch jede Zeile
for i in range(1000, 1500):
    # Gebe die Zeilennummer und den Pixelwert aus
    print(f'Zeile {i}: {gray[i, 0]}')