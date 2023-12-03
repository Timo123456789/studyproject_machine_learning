import os

# Setup
input_dir = 'insects/train/labels'
output_dir = 'insects/train/labels_rgb'

# Liste alle Dateien im Eingabeordner
input_files = os.listdir(input_dir)

# Gehe durch jede Datei
for filename in input_files:
    # Öffne die Datei zum Lesen
    with open(os.path.join(input_dir, filename), 'r') as f:
        # Lese die Werte
        values = list(map(float, f.read().strip().split()))

    # x
    values[1] += 0.02
    # y
    values[2] *= 2
    values[2] -= 0.075
    # height bbox
    values[4] *= 2
    

    # Öffne eine neue Datei im Ausgabeordner zum Schreiben
    with open(os.path.join(output_dir, filename), 'w') as f:
        # Schreibe die verarbeiteten Werte in die Datei
        f.write(' '.join(map(str, values)))
    
    print(f'File {filename} processed')