import json
import numpy as np
import cv2
import os
import subprocess
import ffmpeg

def read_ndjson(path):
    return [json.loads(line) for line in open(path, 'r')]

def adjust_string_length(input_str, length, fill_char):
    """
    Adjusts the length of the input string by appending characters from the left side if needed.

    Args:
    input_str (str): The input string.
    length (int): The desired length of the string.
    fill_char (str): The character to append to the left side if needed.

    Returns:
    str: The adjusted string.

    Raises:
    ValueError: If the length of the string is greater than the specified length.
    """
    if len(input_str) < length:
        return fill_char * (length - len(input_str)) + input_str
    elif len(input_str) == length:
        return input_str
    else:
        raise ValueError(f"Invalid input: Length of the string '{input_str}' is greater than the specified length {length}.")

def get_video_location(base_dir: str, json_row:dict) -> str:
    dir_name = json_row["data_row"]["details"]["dataset_name"]
    file_name = json_row["data_row"]["external_id"]
    return f"{base_dir}/{dir_name}/{file_name}"

class BoundingBox:
    
    x: float
    y: float
    w: float
    h: float
    
    def __init__(self,x,y,w,h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.w} {self.h}"
    

class Annotation:
    name: str
    bounding_box: BoundingBox

    def __init__(self, name, bounding_box) -> None:
        self.name = name
        self.bounding_box = bounding_box

    def __str__(self) -> str:
        return "0 "+self.bounding_box.__str__()
        
class AnnotationsVideo:

    frame:str
    annotations: [Annotation]

    def __init__(self,frame) -> None:
        self.frame = frame
        self.annotations = []

    def add_annotation(self, annotation):
        self.annotations.append(annotation)
    
    def save_to_file(self, dir: str,video_id: str) -> str:
        file_path = dir + f"img_{video_id}_{self.frame}.txt"
        with open(file_path, 'w') as f:
            f.write(self.__str__())    
        return file_path    
    def __str__(self) -> str:
        res = ""
        for bb in self.annotations:
            res += bb.__str__() +"\n"
        return res
    
def labelbox_bb_to_yolo(dict, imageWidth, imageHeight):

    homogeneity_matrix = np.array([[1.4162952571336898e+00, -1.0272416855624227e-02, 5.6968813544405364e+01], 
                                   [1.4842921663035491e-02, 1.3935753508359128e+00, 1.0792638259289236e+01],
                                   [1.2498370634317314e-05, -6.2418078407251730e-07, 1.] ])
    homogeneity_matrix = np.linalg.inv(homogeneity_matrix)


    bb  = np.array([dict["left"],
                    dict["top"], #y
                    dict["width"], #width
                    dict["height"]]) #height

    # mirror bounding box vertical
    bb[0] = imageWidth - bb[0]


    # transform coordinates with homogeneity matrix ---------------------------------------------------------------------------------------------
    # substract half width and height
    bb[0] -= round(imageWidth / 2) #x
    bb[1] -= round(imageHeight / 2) #y

    # Convert to 4 point coordinates
    bb_coords = np.array([[bb[0], bb[1], 1], 
                         [bb[0] + bb[2], bb[1], 1], 
                         [bb[0], bb[1] + bb[3], 1], 
                         [bb[0] + bb[2], bb[1] + bb[3], 1]], dtype=np.float32)
    
    # Transform the corner points
    bb_transform = np.array([np.dot(homogeneity_matrix,bb_coords[0]),
                        np.dot(homogeneity_matrix,bb_coords[1]),
                        np.dot(homogeneity_matrix,bb_coords[2]),
                        np.dot(homogeneity_matrix,bb_coords[3])])
    
    # normalize
    bb_transform = bb_transform / bb_transform[:, 2].reshape(-1, 1)

    # cut third dimension
    bb_transform = bb_transform[:, :2]

    # Calculate minimum and maximum values for x and y
    min_x, min_y = np.min(bb_transform, axis=0)
    max_x, max_y = np.max(bb_transform, axis=0)
    new_width = max_x - min_x
    new_height = max_y - min_y

    
    # New Bounding Box coordinates in the format (x, y, w, h)
    bb = np.array([min_x, min_y, new_width, new_height])

    # scale coordinates
    
    bb[0] *= 1.325
    bb[1] *= 1.3

    #add half width and height
    bb[0] += round(imageWidth / 2)
    bb[1] += round(imageHeight / 2)

    # -------------------------------------------------------------------------------------------------------------------------------------------
    # convert center-based bounding-box
    bb[0] += bb[2] / 2
    bb[1] += bb[3] / 2

    # Convert to percentages
    bb[0] /= imageWidth
    bb[1] /= imageHeight
    bb[2] /= imageWidth
    bb[3] /= imageHeight

    return BoundingBox(bb[0], bb[1], bb[2], bb[3])


def convert_to_coco_format(json_data) -> [AnnotationsVideo]:
    #width, height = json_data["media_attributes"]["width"],json_data["media_attributes"]["height"]
    width, height = 1920,1200
    frames = json_data["projects"]['clor41l0i03gi07znfo8051e3']["labels"][0]["annotations"]["frames"]
    annotations = []
    for frame in frames:
        annotations_frame = AnnotationsVideo(adjust_string_length(frame, 6, "0"))
        objects = frames[frame]["objects"]
        for objectKey in objects:
            a = Annotation(objects[objectKey]["name"],labelbox_bb_to_yolo(objects[objectKey]["bounding_box"],width,height))        
            annotations_frame.add_annotation(a)
            
        annotations.append(annotations_frame)
    return annotations

def extract_frames(input_file, output_directory,video_id):
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Use ffmpeg to extract frames
    ffmpeg.input(input_file).output(os.path.join(output_directory, f"img_{video_id}_%06d.png")).run()

from random import sample 

def pick_n_random_items(input_list, n):
    # Ensure n is not greater than the length of the input list
    n = min(n, len(input_list))

    # pick n random numbers between 0 and length of input_list
    val_indices = sample(range(0, len(input_list)), n)
    # get all indices that were not for validating
    train_indices = [i for i in range(0, len(input_list)) if i not in val_indices]

    return val_indices, train_indices


def write_data_row(data_row:dict,video_id:int,dataset_dir:str, video_base_dir:str, isTraining: bool = True):
    dir_name = "train" if isTraining else "val"
    video_id = adjust_string_length(str(video_id),3,"0")
    frames : [AnnotationsVideo] = convert_to_coco_format(data_row)        
    for frame in frames:
        frame.save_to_file(f"{dataset_dir}/{dir_name}/labels/",video_id)
    
    
    video_location = get_video_location(video_base_dir, data_row)
    # test if video exists
    if not os.path.exists(video_location):
        print(f"Video '{video_location}' does not exist")
    else:
        extract_frames(video_location,f"{dataset_dir}/{dir_name}/images",video_id)
    
def create_directory(directory_path):
    # Check if the directory already exists
    if not os.path.exists(directory_path):
        # If not, create the directory
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully")
    else:
        print(f"Directory '{directory_path}' already exists")    
    
    
if __name__ == "__main__":
    dataset_dir = "../../insects"
    video_dir = "../../videos_new_cutted"
    anotation_location = "../../export-result_11-12-23.ndjson"
    
    data = read_ndjson(anotation_location)
    
    # Create directory structure
    create_directory(dataset_dir)
    create_directory(os.path.join(dataset_dir, "train"))
    create_directory(os.path.join(dataset_dir, "val"))
    
    
    # Copy input into data.yaml
    with open(os.path.join(dataset_dir,"data.yaml"),"w") as f:
        f.write(
            """
train: ./train/images 
val: ./val/images
nc: 1 
names: ['insect']
            """
        )
        
    for dir in ["train","val"]:
        create_directory(os.path.join(dataset_dir,dir,"images"))
        create_directory(os.path.join(dataset_dir,dir,"labels"))
        
    
    
    val_indices, train_indices = pick_n_random_items(data,5)
    print("Validation indices:", val_indices, "\nTraining indices:", train_indices)

    # write data rows for each val index
    print("Writing validation data rows...")
    for i in val_indices:
        print(i)
        write_data_row(data[i],(i+1),dataset_dir,video_dir, False)

    # write data rows for each train index
    print("Writing training data rows...")
    for i in train_indices:
        write_data_row(data[i],(i+1),dataset_dir,video_dir)
    