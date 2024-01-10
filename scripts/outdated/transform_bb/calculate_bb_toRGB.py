import os, cv2

# this script is for testing the bounding box calculation

# Setup
width = 1920
height = 1200

# bounding-box data can be found in export-result.ndjson
dict = {"left": 849.9052631578948, "top": 790.1578947368421, "width": 101, "height": 90}

old_box = f"{0} {dict['left']} {dict['top']} {dict['width']} {dict['height']}"
    

# shrink factor
factor_x = 0.97
factor_y = 0.89

center_x = dict["left"] + (dict["width"] /2)
center_y = dict["top"] + (dict["height"] /2)

display_old_box = f"{0} {center_x} {center_y} {dict['width']} {dict['height']}"

# berechne neue höhe da rgb (1200) größer als dvs (1080)
#center_y *= 1.11111111111111

# Berechne die Mitte des Bildes
img_center_x = width / 2
img_center_y = height / 2

# Berechne die Differenz zwischen der Bounding-Box-Mitte und der Bildmitte
diff_x = center_x - img_center_x
diff_y = center_y - img_center_y

# Skaliere die Differenz
diff_x *= factor_x
diff_y *= factor_y

# Addiere die skalierte Differenz zur Bildmitte, um die neue Bounding-Box-Mitte zu erhalten
new_center_x = img_center_x + diff_x
new_center_y = img_center_y + diff_y

# Skaliere die Breite und Höhe der Bounding-Box
new_width = dict["width"] / width * factor_x
new_height = dict["height"] / height * factor_y


# Berechne die neuen Bounding-Box-Koordinaten
center_x = new_center_x - (new_width / 2)
center_y = new_center_y - (new_height / 2)
    
center_x /= width
center_y /= height

box = f"{0} {center_x} {center_y} {new_width} {new_height}"
    
print(box)



#-------------------------------------------------------------
# input
image_dir = 'path/to/frame/with/bounding/box'

# Bild laden
image = cv2.imread(image_dir)
h, w = image.shape[:2]

# old Bounding-Boxen zeichnen
t, x, y, w_box, h_box = map(float, display_old_box.strip().split())
x1 = int((x - w_box / 2))
y1 = int((y - h_box / 2))
x2 = int((x + w_box / 2))
y2 = int((y + h_box / 2))
print(f'old: {x1}, {y1}, {x2}, {y2}')
cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# new Bounding-Boxen zeichnen
t, x, y, w_box, h_box = map(float, box.strip().split())
x1 = int((x - w_box / 2) * w)
y1 = int((y - h_box / 2) * h)
x2 = int((x + w_box / 2) * w)
y2 = int((y + h_box / 2) * h)
print(f'new: {x1}, {y1}, {x2}, {y2}')
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