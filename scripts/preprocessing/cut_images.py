import cv2
import os

# this script is for cutting single images

# setup
image_dir = 'D:/studyproject_machine_learning/insects/train/images'
image_rgb_dir = 'D:/studyproject_machine_learning/insects/train/images_rgb'

# Liste alle Dateien im Ordner "images"
image_files = os.listdir(image_dir)

# Erstelle den Ordner "images_rgb", falls er noch nicht existiert
os.makedirs(image_rgb_dir, exist_ok=True)

# Für jede Datei im Ordner
for image_file in image_files:
    # Lese das Bild
    image = cv2.imread(os.path.join(image_dir, image_file))
    
    # Bestimme die Höhe und Breite des Bildes
    h, w = image.shape[:2]

    # Schneide die untere Hälfte des Bildes aus
    cropped_image = image[1080:, :]
    
    # Speichere das halbierte Bild im Ordner "images_rgb" mit dem gleichen Namen
    cv2.imwrite(os.path.join(image_rgb_dir, image_file), cropped_image)

    print(f'Image {image_file} processed')