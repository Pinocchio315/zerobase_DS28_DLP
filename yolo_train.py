import glob
import ultralytics
from ultralytics import YOLO
from ultralytics import settings

# upload a pretrained model v11
model = YOLO("yolo11n.pt")

# update a setting
settings.update({"runs_dir": "./YOLODataset/"})

# training
results = model.train(data="./YOLODataset/dataset.yaml", epochs=150, imgsz=320)

# test
files = glob.glob('./YOLODataset/images/test/*.*')

model.predict(files, save=True, imgsz=320, conf=0.3)

print('='*50)
print('DONE!')
