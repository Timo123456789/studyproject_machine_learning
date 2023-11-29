import cv2

# input
image_dir = 'insects/train/images_rgb/img_001_003923.png'
label_dir = 'insects/train/labels_rgb/img_001_003923.txt' 

# Bild laden
image = cv2.imread(image_dir)
h, w = image.shape[:2]

# Bounding-Boxen aus txt-Datei lesen
with open(label_dir, 'r') as f:
    boxes = f.readlines()

# Bounding-Boxen zeichnen
for box in boxes:
    t, x, y, w_box, h_box = map(float, box.strip().split())
    x1 = int((x - w_box / 2) * w)
    y1 = int((y - h_box / 2) * h)
    x2 = int((x + w_box / 2) * w)
    y2 = int((y + h_box / 2) * h)
    print(x1, y1, x2, y2)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Bild skalieren
max_height = 600
max_width = 600
# Höhe und Breite des skalierten Bildes berechnen
scaling_factor = min(max_width / w, max_height / h)
image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

# Bild anzeigen
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()