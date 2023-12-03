# 1. Erst Build Data Set Durchlaufen lassen
# 2. convert bouonding box
# 3. cut images

from ultralytics import YOLO

model = YOLO('yolov8x-seg.pt')
results = model(r'C:\Users\timol\OneDrive - Universität Münster\10. Fachsemester_SS_2023\bachelor-thesis\Code\vid_examples\evaluation\Autobahn1s.mp4', save=True)
#print(results[3].masks)