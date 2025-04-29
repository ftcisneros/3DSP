# Driver Drowsiness Detection Safety System

## Members
- Alex Krajewski  
- Fernanda Tecocoatzi-Cisneros

## Project Overview
This system detects driver drowsiness through yawning and provides real-time alerts to help prevent road accidents. It uses a webcam or video input to monitor the driver and raises alerts when signs of drowsiness are detected.

## Features
- Real-time webcam monitoring
- Custom-trained YOLOv5 model for yawning detection
- Console-based alert notifications
- Easy-to-run detection and training notebooks

## Model & Training
- YOLOv5 with PyTorch for object detection
- OpenCV for video/image capture
- Python 3 (Jupyter Notebook environment)
- Local machine for training
- Webcam for testing

## File Descriptions
- `yawn_alert_system.ipynb`: Runs the trained model on webcam or video to detect yawns and send alerts
- `Alert.py`: Handles logic for triggering alerts
- `Notify.py`: Sends alert message (prints to console) 
- `DrowsinessDetection.ipynb`: Used for training the custom YOLOv5 model
- `/yolov5`: YOLOv5 source code (cloned from official Ultralytics repo)
  - `/data/images/`: Training images (video frames)
  - `/data/labels/`: YOLO-format annotation files
  - `/runs/`: Training outputs including model weights

## Installation & Dependencies

Make sure to install the following before running `yawn_alert_system.ipynb`:

```bash
pip install torch torchvision torchaudio
pip install opencv-python
pip install pyodbc         
pip install -U ultralytics
```

## How to Run Detection
1. Open `yawn_alert_system.ipynb` in Jupyter Notebook.
2. This notebook uses your webcam for live detection via `cv2.VideoCapture()`.
3. If a yawn is detected, the system will print:  
   `"Yawn detected! Sending alert..."`

## Notes
- The images used to train the model have been excluded due to large data size. Therefore, `DrowsinessDetection.ipynb` will not run. 
- This project was developed and tested on Python 3 in Jupyter Notebook.
- Model was trained locally using extracted frames from driver videos.

## Acknowledgements 
- YOLOv5 by Ultralytics
- YawDD Dataset
- Label Studio for video annotation