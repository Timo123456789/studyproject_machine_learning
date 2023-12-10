import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def background_Sub(vid, name, output_path):
    os.chdir(output_path)
    cap = cv2.VideoCapture(vid)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(name, fourcc, fps, size, isColor=False)
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

    # if typ == "colorManipu":
    #     img = Image.open('../insects/train/images_rgb/img_001_002910.png')
    #     M = np.asarray(img)
    #     blue = M[:, :, 0]
    #     green = M[:, :, 1]
    #     red = M[:, :, 2]
    #
    #     cv2.imwrite("red.jpg", red)
    #     cv2.imwrite("green.jpg", green)
    #     cv2.imwrite("blue.jpg", blue)
    #
    #     img2 = Image.open("../resultsPreprocessing/subtraction.jpg")
    #     M2 = np.asarray(img2)
    #     blue2 = M2[:, :, 0]
    #     enhanced_image = np.stack((red, green, blue2), axis=-1).astype(np.uint8)
    #     enhanced_image = Image.fromarray(enhanced_image)
    #     enhanced_image.save("combi channels.jpg")


def substract(vid, name, output_path):
    os.chdir(output_path)
    cap = cv2.VideoCapture(vid)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(name, fourcc, fps, size)
    fgbg = cv2.createBackgroundSubtractorMOG2()
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


def optical_flow(vid, name, output_path):
    os.chdir(output_path)

    # Get a VideoCapture object from video and store it in vс
    vc = cv2.VideoCapture(vid)
    size = (int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = vc.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the input video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(name, fourcc, fps, size)

    # Read first frame
    _, first_frame = vc.read()
    # Convert to gray scale 
    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    # Create mask
    mask = np.zeros_like(first_frame)
    # Set image saturation to maximum value as we do not need it
    mask[..., 1] = 255
    while(vc.isOpened()):
        # Read a frame from video
        _, frame = vc.read()

        # Convert new frame format`s to gray scale and resize gray frame obtained
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate dense optical flow by Farneback method
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
        # Compute the magnitude and angle of the 2D vectors
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        # Set image hue according to the optical flow direction
        mask[..., 0] = angle * 180 / np.pi / 2
        # Set image value according to the optical flow magnitude (normalized)
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        # Convert HSV to RGB (BGR) color representation
        rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        # Open a new window and displays the output frame
        dense_flow = cv2.addWeighted(frame, 1,rgb, 2, 0)
        cv2.imshow("Dense optical flow", rgb)
        # Update previous frame
        prev_gray = gray
        video.write(rgb)
        # Frame are read by intervals of 10 millisecond. The programs breaks out of the while loop when the user presses the ‘q’ key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    vc.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    # Setup
    video_path = "/Users/melfers/Documents/Uni/Master 1.Semster/Studyproject/yolov7/videos/rgb/"
    out_path = "/Users/melfers/Documents/Uni/Master 1.Semster/Studyproject/yolov7/videos/processed"
    
    # Liste alle Dateien im Ordner "videos/rgb"
    video_files = os.listdir(video_path)

    # Erstelle den Ordner "videos_rgb", falls er noch nicht existiert
    os.makedirs(out_path, exist_ok=True)

    # Für jede Datei im Ordner
    for video_file in video_files:
        video_dir = os.path.join(video_path, video_file)
        filename = os.path.basename(video_dir)
        background_Sub(video_dir, filename, out_path)



    # Setup 2
    video_path = "/Users/melfers/Documents/Uni/Master 1.Semster/Studyproject/yolov7/videos/processed/"
    out_path = "/Users/melfers/Documents/Uni/Master 1.Semster/Studyproject/yolov7/videos/processed/secondIteration"
    
    # Liste alle Dateien im Ordner "videos/rgb"
    video_files = os.listdir(video_path)

    # Erstelle den Ordner "videos_rgb", falls er noch nicht existiert
    os.makedirs(out_path, exist_ok=True)

    # Für jede Datei im Ordner
    for video_file in video_files:
        video_dir = os.path.join(video_path, video_file)
        filename = os.path.basename(video_dir)
        substract(video_dir, filename, out_path)
