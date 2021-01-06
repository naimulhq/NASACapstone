# Training on the Jetson Nano

### 1. Install Pytorch using provided downloader

```
cd jetson-inference/build
./install-pytorch.sh
Once it is running, a GUI should pop up. Follow instructions on GUI to download Pytorch
```
### 2. Set up training requirements (Only if project built from scratch)

```
cd TrainingTools/ssd
wget https://nvidia.box.com/shared/static/djf5w54rjvpqocsiztzaandq1m3avr7c.pth -O models/mobilenet-v1-ssd-mp-0_675.pth
pip3 install -v -r requirements.txt
```
### 3. Set up directory heirarchy

```
Inside the ssd directory, add the following directories and subdirectories:
- Annotations/
      - *.xml
- ImageSets/
      - Main
            - train.txt
            - trainval.txt
- JPEGImages/
      - *.jpg
- labels.txt

```

* Annotations will contain all the .xml files from the image dataset
* ImageSets/Main will have two files: train.txt and trainval.txt . These files are identical and have the filename of the images without the .jpg extension. Example shown below
```
20200917-162237
20200917-162252
20200917-162314
20200917-162332
20200917-162351
20200917-162414
20200917-162429
20200917-162447
```

* JPEGImages contains all the .jpg images from the dataset.
* labels.txt contains all the labels of the dataset.

### 4. PascalVOC Format Preprocessing

* Since the LabelImg tool we are using does not create a full file structure, we need to do some preprocessing before performing the training. 
```
python3 vision/datasets/generate_vocdata.py ./labels.txt
```

* For more details, look at this issue: https://github.com/dusty-nv/jetson-inference/issues/789

### 5. Mounting Swap Memory and Disabling GUI

* Since training uses up large amounts of data, it is highly likely that we will run out of memory during the training process. To prevent segmentation faults and other runtime errors from occuring, we create a Swap Memory and mount it. This ensures that when we do run out of memory on the RAM, we are able to use physical memory. Although it will take longer, it ensures that everything runs smoothly.

* For us, I determined that using 8GB of Swap Memory is sufficient enough to run the training. Run the commands below

```
sudo fallocate -l 8G /mnt/8GB.swap
sudo mkswap /mnt/8GB.swap
sudo swapon /mnt/8GB.swap
```

Then add the following line to the end of `/etc/fstab` to make the change persistent:

``` bash
/mnt/8GB.swap  none  swap  sw 0  0
```

Now your swap file will automatically be mounted after reboots.  To check the usage, run `swapon -s` or `tegrastats`.

* It is also recommended to diable the GUI since it uses up valuable memory. To disable the GUI, you can press Ctrl + Alt + F3. You will need to login with your username and password once disabling the GUI. Once training is complete, you can press Ctrl + Alt + F1 to return to GUI.

### 6. Training and Conversion

* To begin training the model, run the following in the ssd directory:
```
python3 train_ssd.py --dataset-type=voc --data=./ --model-dir=models/<Desired Name> --batch-size=1 --workers=0 --epochs=1
```

* Before performing the conversion, remove labels.txt from the ssd directory. It is not needed since another labels.txt will be created in the models folder and will cause errors if not deleted.
* Once training is complete, we convert our model to .onnx so that we can load it with TensorRT:

``` bash
python3 onnx_export.py --model-dir=models/<Desired Name>
```

This will save a model called `ssd-mobilenet.onnx` under `TrainingTools/ssd/models`

* Lastly, to create a live stream, just run my-detection.py from src. You might need to change the paths for the models and labels argument.

