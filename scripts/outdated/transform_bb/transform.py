import cv2
import numpy as np

imageHeight = 1200
imageWidth = 1920
K_raw = np.array([[3.4282342621186917e+03, 0, 5.8492539985078872e+02],
              [0, 3.4307180137736227e+03, 3.9762805716217571e+02],
              [0, 0, 1]])

D_raw = np.array([-3.2728658644963399e-01, -3.7426333714414590e+00, -1.1636502963546388e-03, 1.9210369248074133e-03, 4.8738196170909852e+01])
K_dng = np.array([[4.8672516529450268e+03, 0, 8.6721913003296606e+02],
              [0, 4.8342721349834974e+03, 5.6766429521805446e+02],
              [0, 0, 1]])

D_dng = np.array([-4.1537882678358434e-01, 1.1559861246670058e-01, 1.7994519558784615e-03, 1.3499632712320707e-03, 3.0006172384779313e+00])



# image
path = '../../insects/train/images/img_001_002500.png'
img = cv2.imread(path)

# Lade die Homographiematrix aus der YAML-Datei
fs = cv2.FileStorage('../../calib-1m_16mm_dvs-30_basler-70\calib-1m_16mm_dvs-30_basler-70\homography_calib.yaml', cv2.FILE_STORAGE_READ)
homogeneity_matrix = fs.getNode('H').mat()
# calculate inverse homography matrix
homogeneity_matrix = np.linalg.inv(homogeneity_matrix)


# path label
path = '../../insects/train/labels/img_001_000259.txt'
# Bounding box coordinates [x, y, width, height]
bb  = np.array([960, 600, 25, 25])
# draw bounding_box_percent
cv2.rectangle(img, (bb[0], bb[1]), (bb[0] + bb[2], bb[1] + bb[3]), (0, 255, 0), 2)

# substract half width and height
bb[0] -= round(imageWidth / 2)
bb[1] -= round(imageHeight / 2)

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
new_bbb = np.array([min_x, min_y, new_width, new_height])

#add half width and height
new_bbb[0] += round(imageWidth / 2)
new_bbb[1] += round(imageHeight / 2)

# y offsset
# new_bbb[1] -= 90

# Print the original and transformed coordinates
print("Original coordinates:")
print(bb)
print("Transformed coordinates:")
print(new_bbb)



# Convert to percentages
new_bbb[0] /= imageWidth
new_bbb[1] /= imageHeight
new_bbb[2] /= imageWidth
new_bbb[3] /= imageHeight

# draw transformed bounding box
cv2.rectangle(img, (int(new_bbb[0] * imageWidth),
                     int(new_bbb[1] * imageHeight)),
                       (int(new_bbb[0] * imageWidth) + int(new_bbb[2] * imageWidth),
                        int(new_bbb[1] * imageHeight) + int(new_bbb[3] * imageHeight)), (0, 0, 255), 2)

# show image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


