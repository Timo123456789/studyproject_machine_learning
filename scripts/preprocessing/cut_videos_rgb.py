import cv2
import os

# this script cuts the rgb stream off the dvs stream

def cut_video(video_dir, output_dir):
    # Öffne das Video
    video = cv2.VideoCapture(video_dir)
    filename = os.path.basename(video_dir)
    
    # Erhalte die Framegröße
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Berechne die Hälfte der Höhe
    cut_height = 1080
    print(f"Frame height: {cut_height}")
    
    # Definiere den Codec und erstelle ein VideoWriter-Objekt
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 

    # Erstelle den Ausgabepfad mit dem gleichen Dateinamen
    output_path = os.path.join(output_dir, filename)

    out = cv2.VideoWriter(output_path, fourcc, 100.0, (frame_width, (frame_height-cut_height)))
    
    while(video.isOpened()):
        ret, frame = video.read()
        if ret == True:
            # Schneide den Frame in der Mitte durch und behalte den unteren Teil
            cut_frame = frame[cut_height:, :]
            
            # Schreibe den bearbeiteten Frame in das neue Video
            out.write(cut_frame)
            print('Frame processed')
        else:
            break

    # Schließe das Video und das VideoWriter-Objekt
    video.release()
    out.release()

    # Gebe den Pfad des neuen Videos zurück
    return os.path.abspath(output_path)


if __name__ == "__main__":
    # Setup
    video_dir = 'path/to/raw/video'
    output_dir = 'path/to/video/rgb'

    # Liste alle Dateien im Ordner "videos"
    video_files = os.listdir(video_dir)

    # Erstelle den Ordner "videos_rgb", falls er noch nicht existiert
    os.makedirs(output_dir, exist_ok=True)

    # Für jede Datei im Ordner
    for video_file in video_files:
        # Schneide das Video
        cut_video(os.path.join(video_dir, video_file), output_dir)

        print(f'Video {video_file} processed')