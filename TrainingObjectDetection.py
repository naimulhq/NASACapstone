from imageai.Detection.Custom import DetectionModelTrainer
from preprocessing import preprocessData
import os


if os.path.isdir("C:\\Users\\18186\\Downloads\\Image Dataset\\train") is True and os.path.isdir("C:\\Users\\18186\\Downloads\\Image Dataset\\validation") is True:
    pass
else:
    preprocessData()


trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="C:\\Users\\18186\\Downloads\\Image Dataset\\")
trainer.setTrainConfig(object_names_array=["Mounting Plate", "Bottom Plate", "motor"], batch_size=4, num_experiments=10)
trainer.trainModel()