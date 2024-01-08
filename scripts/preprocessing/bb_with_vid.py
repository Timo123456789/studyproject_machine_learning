import cv2
import glob
import os

# Ordnerpfade
img_folder = '../../insects/train/images'
bbox_folder = '../../insects/train/labels'

# Videoparameter
fps = 100
frame_size = (1920, 1200)

# VideoWriter-Objekt erstellen
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

i = 1
# Durchlaufe alle Bilder im Ordner
for img_path in sorted(glob.glob(os.path.join(img_folder, '*.png'))):
    if i > 3000:
        break
    
    # Lade das Bild
    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    # Lade die zugehörige Bounding-Box-Datei
    bbox_path = os.path.join(bbox_folder, os.path.splitext(os.path.basename(img_path))[0] + '.txt')
    if os.path.exists(bbox_path):
        with open(bbox_path, 'r') as f:
            bbox = f.readlines()

        # Zeichne die Bounding-Box auf das Bild
        for box in bbox:
            t, x, y, w_box, h_box = map(float, box.strip().split())
            x1 = int((x - w_box / 2) * w)
            y1 = int((y - h_box / 2) * h)
            x2 = int((x + w_box / 2) * w)
            y2 = int((y + h_box / 2) * h)
            print(f"[{x1}, {y1}, {x2}, {y2}]. Frame {i}.")
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    else:
        print(f"No bounding box file for {img_path}. Frame {i}")

    # Füge das Bild zum Video hinzu
    out.write(img)
    i += 1

# Schließe den VideoWriter
out.release()