from imageai.Detection.Custom import DetectionModelTrainer
from preprocessing import preprocessData

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="C:\\Users\\18186\\Downloads\\Image Dataset\\")
trainer.setTrainConfig(object_names_array=["Mounting Plate", "Bottom Plate", "Motor"], batch_size=4, num_experiments=200)
trainer.trainModel()