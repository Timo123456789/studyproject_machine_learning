import os
import cv2
import numpy as np

def background_Sub(vid, name, output_path):
    output = os.path.join(output_path, name)
    cap = cv2.VideoCapture(vid)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(output, fourcc, fps, size, isColor=False)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= total_frames:
            break

        sub = fgbg.apply(frame)
        video.write(sub)

        prev_frame = frame
        frame_count += 1
        print(str(frame_count) + " / " + str(total_frames))
    cap.release()

def rgbToHsv(vid, name, output_path):
    output = os.path.join(output_path, name)
    cap = cv2.VideoCapture(vid)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(output, fourcc, fps, size)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= total_frames:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = 179
        video.write(hsv)

        frame_count += 1
        print(str(frame_count) + " / " + str(total_frames))
    cap.release()


def substract(vid, name, output_path):
    output = os.path.join(output_path, name)
    cap = cv2.VideoCapture(vid)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(output, fourcc, fps, size)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= total_frames:
            break

        if prev_frame is not None:
            sub = cv2.subtract(frame, prev_frame)
            video.write(sub)

        prev_frame = frame
        frame_count += 1
        print(str(frame_count) + " / " + str(total_frames))
    cap.release()

def time_offset_by1(vid, name, output_path):
    output = os.path.join(output_path, name)
    cap = cv2.VideoCapture(vid)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(output, fourcc, fps, size)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    frame_minus1 = None
    frame_minus2 = None

    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= total_frames:
            break

        if frame_minus2 is not None:
            # Combine the frames into a single image where each frame is a different color channel
            frame[:, :, 2] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # red
            frame[:, :, 1] = cv2.cvtColor(frame_minus1, cv2.COLOR_BGR2GRAY) # green
            frame[:, :, 0] = cv2.cvtColor(frame_minus2, cv2.COLOR_BGR2GRAY) # blue
            video.write(frame)

        # Shift the frames
        frame_minus2 = frame_minus1
        frame_minus1 = frame

        frame_count += 1
        print(str(frame_count) + " / " + str(total_frames))
    
    cap.release()

def time_offset_by10(vid, name, output_path):
    output = os.path.join(output_path, name)
    cap = cv2.VideoCapture(vid)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(output, fourcc, fps, size)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0

    frames = [None] * 20  # Initialize a list with 20 None elements

    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= total_frames:
            break

        frames[frame_count % 20] = frame  # Store the current frame in the list

        if frame_count >= 19:  # Start writing to the video after 20 frames have been read
            frame_minus10 = frames[(frame_count - 10) % 20]  # Get the frame from 10 frames ago
            frame_minus20 = frames[(frame_count - 20) % 20]  # Get the frame from 20 frames ago

            # Combine the frames into a single image where each frame is a different color channel
            frame[:, :, 2] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # red
            frame[:, :, 1] = cv2.cvtColor(frame_minus10, cv2.COLOR_BGR2GRAY)  # green
            frame[:, :, 0] = cv2.cvtColor(frame_minus20, cv2.COLOR_BGR2GRAY)  # blue
            video.write(frame)

        frame_count += 1
        print(str(frame_count) + " / " + str(total_frames))

    cap.release()



if __name__ == "__main__":
    # Setup
    video_dir = '/scratch/tmp/t_liet02/videos_dez_new'
    output_dir = '/scratch/tmp/t_liet02/videos_output_backSub'
    # video_dir = "../../videos_new_cutted/"
    # output_dir = '../../videos_new_test/'


    # Erstelle den Ordner "videos_rgb", falls er noch nicht existiert
    os.makedirs(output_dir, exist_ok=True)

    # Für jede Datei im Ordner "videos"
    for video in os.listdir(video_dir):
        # DS_Store ignorieren
        if video == '.DS_Store':
            continue

        # Zusammensetzen des Pfades
        video_dir_deep = os.path.join(video_dir, video)
        output_dir_deep = os.path.join(output_dir, video)

        os.makedirs(output_dir_deep, exist_ok=True)
        # Für jede Datei im Ordner
        for video_file in os.listdir(video_dir_deep):
            vid_file = os.path.join(video_dir_deep, video_file)
            background_Sub(vid_file, video_file, output_dir_deep)



    # # Setup 2
    # video_path = '../../../../scratch/tmp/melfers/videos_backSub/'
    # out_path = '../../../../scratch/tmp/melfers/videos_backSubPlusSub/'
    

    # # Erstelle den Ordner "videos_rgb", falls er noch nicht existiert
    # os.makedirs(out_path, exist_ok=True)

    # # Für jede Datei im Ordner "videos"
    # for video in os.listdir(video_dir):
    #     # DS_Store ignorieren
    #     if video == '.DS_Store':
    #         continue
        
    #     if video == "2023-10-10-botanical_garden":
    #         continue

    #     # Zusammensetzen des Pfades
    #     video_dir_deep = os.path.join(video_dir, video)
    #     output_dir_deep = os.path.join(output_dir, video)

    #     os.makedirs(output_dir_deep, exist_ok=True)

    #     # Für jede Datei im Ordner
    #     for video_file in os.listdir(video_dir_deep):
    #         vid_file = os.path.join(video_dir_deep, video_file)
    #         substract(vid_file, video_file, output_dir_deep)
