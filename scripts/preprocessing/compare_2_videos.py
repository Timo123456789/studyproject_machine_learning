import cv2

# this script is for testing the shift of the dvs and the rgb stream

#setup
video1_dir = 'D:/studyproject_machine_learning/videos_dvs/2023-09-28-botanical_garden/2023-09-28_12-16-27.479006981_combined_000_4000.mp4'
video2_dir = 'D:/studyproject_machine_learning/videos/2023-09-28-botanical_garden/2023-09-28_12-16-27.479006981_combined_000_4000.mp4'

# Öffne die beiden Videos
video1 = cv2.VideoCapture(video1_dir)
video2 = cv2.VideoCapture(video2_dir)

video1_shape = video1.get(cv2.CAP_PROP_FRAME_WIDTH), video1.get(cv2.CAP_PROP_FRAME_HEIGHT)
video2_shape = video2.get(cv2.CAP_PROP_FRAME_WIDTH), video2.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(f"Video 1 shape: {video1_shape}")
print(f"Video 2 shape: {video2_shape}")



# Springe zu Frame 3016 in beiden Videos ----------------------------------------------------
frame_id = 2001
video1.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
video2.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

# Lese Frame 3016 aus jedem Video
ret1, frame1 = video1.read()
ret2, frame2 = video2.read()

# Überprüfe, ob beide Frames erfolgreich gelesen wurden
if not ret1 or not ret2:
    print(f"Can't receive frame {frame_id} (stream end?). Exiting ...")
else:
    # Speichere Frame 3016 als Bild
    cv2.imwrite(f'frame_{frame_id}_video1.png', frame1)
    cv2.imwrite(f'frame_{frame_id}_video2.png', frame2)
# -------------------------------------------------------------------------------------------



while True:
    # Lese einen Frame aus jedem Video
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    # Überprüfe, ob beide Frames erfolgreich gelesen wurden
    if not ret1 or not ret2:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Skaliere das Bild so, dass die Höhe 1200 beträgt
    new_height = 1200
    scale_ratio = 1.05
    new_width = int(frame1.shape[1] * scale_ratio)
    resized_frame1 = cv2.resize(frame1, (new_width, new_height))

    # Finde die Mitte des Bildes
    mid_x = resized_frame1.shape[1] // 2

    # Schneide die Seiten des Bildes ab, um die Breite auf 1920 zu reduzieren
    start_x = mid_x - 960
    end_x = mid_x + 960
    cropped_frame1 = resized_frame1[:, start_x:end_x]

    # Ändere die Größe beider Frames auf 1000x1000
    frame1_final = cv2.resize(cropped_frame1, (1000,1000))
    frame2_final = cv2.resize(frame2, (1000,1000))



    # Stelle sicher, dass beide Frames die gleiche Größe haben
    if frame1_final.shape != frame2_final.shape:
        print(f"Frame 1 shape: {frame1_final.shape}")
        print(f"Frame 2 shape: {frame2_final.shape}")
        print("Frames have different shapes. Exiting ...")
        break

    # Berechne die gewichtete Summe der beiden Frames
    blended_frame = cv2.addWeighted(frame1_final, 0.5, frame2_final, 0.5, 0)

    # Zeige das resultierende Bild an
    cv2.imshow('Blended Video', blended_frame)

    # Beende die Schleife, wenn die 'q'-Taste gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Schließe die Fenster und gebe die Ressourcen frei
video1.release()
video2.release()
cv2.destroyAllWindows()