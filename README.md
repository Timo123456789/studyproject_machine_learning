# studyproject_machine_learning

## RGB Group

### next steps
- distribute tasks
- shift bounding boxes to RGB stream
- implement preprocessing ideas
- parallel: train YOLO and compare results
  - train on raw RGB stream -> implement pipeline
  - after finished pipeline: train on preprocessed images 

### ideas preprocessing
- picture subtraction
- background subtraction
  - KNN-bs
  - MOG2
- convert RGB in greyscale or HSV
- delete different bands -> try and error (lower priority)
- neighborhood operations
  - edge detection
- optical flow
