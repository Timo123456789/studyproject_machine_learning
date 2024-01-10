import cv2
import numpy as np

imageHeight = 1200
imageWidth = 1920

# Lade die Homographiematrix aus der YAML-Datei
fs = cv2.FileStorage('../../calib-1m_16mm_dvs-30_basler-70\calib-1m_16mm_dvs-30_basler-70\homography_calib.yaml', cv2.FILE_STORAGE_READ)
homogeneity_matrix = fs.getNode('H').mat()
# calculate inverse homography matrix
homogeneity_matrix = np.linalg.inv(homogeneity_matrix)


# path label
path = '../../insects/train/labels/img_001_000259.txt'
# Bounding box coordinates [x, y, width, height]
bounding_box_percent  = np.array([0.42109375,0.35,0.059895833333333336,0.09])

# dir image
path = '../../insects/train/images/img_001_002500.png'
# read image
img = cv2.imread(path)

# Convert percentages to pixel coordinates
x = int(bounding_box_percent[0] * imageWidth)
y = int(bounding_box_percent[1] * imageHeight)
width = int(bounding_box_percent[2] * imageWidth)
height = int(bounding_box_percent[3] * imageHeight)





# Assuming you have the distorted coordinates (u, v), and camera matrix K and distortion coefficients D
u = 100
v = 150
k1, k2, k3 = 0.1, 0.01, 0.001  # Example radial distortion coefficients
cx, cy = 320, 240  # Example principal point coordinates
fx, fy = 500, 500  # Example focal lengths

# Calculate undistorted coordinates
r = np.sqrt((u - cx)**2 + (v - cy)**2)
x_distorted = (u - cx) / fx
y_distorted = (v - cy) / fy
x_undistorted = x_distorted / (1 + k1 * r**2 + k2 * r**4 + k3 * r**6)
y_undistorted = y_distorted / (1 + k1 * r**2 + k2 * r**4 + k3 * r**6)

# Apply camera matrix to convert back to image plane
undistorted_homogeneous = np.array([[x_undistorted], [y_undistorted], [1]])
undistorted_pixel = np.dot(K, undistorted_homogeneous)
u_undistorted, v_undistorted = undistorted_pixel[0, 0] / undistorted_pixel[2, 0], undistorted_pixel[1, 0] / undistorted_pixel[2, 0]



print("Distorted Coordinates:", u, v)
print("Undistorted Coordinates:", u_undistorted, v_undistorted)








# Print the original and transformed coordinates
print("Original coordinates:")
print(f"X: {bounding_box_percent[0]}, Y: {bounding_box_percent[1]}, Width: {bounding_box_percent[3]}, Height: {bounding_box_percent[3]}")
print("Transformed coordinates:")
print(f"X: {transformed_top_left[0]}, Y: {transformed_top_left[1]}, Width: {transformed_width}, Height: {transformed_height}")

# draw bounding_box_percent
cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)

# draw transformed bounding box
cv2.rectangle(img, (int(transformed_top_left[0] * imageWidth), int(transformed_top_left[1] * imageHeight)), (int((transformed_top_left[0] + transformed_width) * imageWidth), int((transformed_top_left[1] + transformed_height) * imageHeight)), (0, 0, 255), 2)

# show image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


