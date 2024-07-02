# Real-time Object Detection with YOLO

## Project Description

This project implements a real-time object detection system using the YOLO (You Only Look Once) algorithm with OpenCV. It features a graphical user interface built with tkinter, allowing users to perform object detection on live webcam feeds or video files. The system also includes logging functionality to record and save detection results.

## Features

- Real-time object detection using YOLOv3
- Graphical user interface for easy interaction
- Support for both webcam and video file input
- Adjustable confidence and threshold settings
- Real-time logging of detected objects
- Ability to save detection logs to CSV files

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.7 or higher
- OpenCV
- NumPy
- imutils
- Pillow (PIL)

You can install the required packages using pip:
pip install opencv-python numpy imutils pillow

Additionally, you'll need to download the YOLOv3 weights, configuration file, and COCO names file. Place these in a directory named `yolo-coco` in your project root:

- `yolov3.weights`
- `yolov3.cfg`
- `coco.names`

## Project Structure
project_root/
│
├── main.py            # Main application file
├── gui.py             # GUI implementation
├── README.md          # Project documentation
│
└── yolo-coco/         # YOLO model files
├── yolov3.weights
├── yolov3.cfg
└── coco.names
## How to Run

1. Ensure all prerequisites are installed and YOLO files are in place.
2. Open a terminal and navigate to the project directory.
3. Run the following command:
python main.py

4. The GUI will appear. Use the buttons to start/stop detection, open video files, and save logs.

## Usage

- Click "Start" to begin object detection on the webcam feed.
- Use "Open File" to select a video file for detection.
- Adjust the confidence and threshold sliders to fine-tune detection sensitivity.
- The detection log will appear in real-time in the text area.
- Click "Save Log" to save the current detection log as a CSV file.

## Classes and Functions

### `YOLODetector` class
- `__init__(self, yolo_dir="yolo-coco")`: Initializes the YOLO detector.
- `load_yolo(self)`: Loads the YOLO model and labels.
- `detect(self, frame, conf, thresh)`: Performs object detection on a given frame.

### `ObjectDetectionGUI` class
- `__init__(self, master)`: Initializes the basic GUI elements.
- `start_detection(self)`: Starts the detection process.
- `stop_detection(self)`: Stops the detection process.
- `open_file(self)`: Opens a file dialog to select a video file.

### `EnhancedObjectDetectionGUI` class (inherits from `ObjectDetectionGUI`)
- `__init__(self, master)`: Initializes the enhanced GUI with logging features.
- `detect_objects(self)`: Main detection loop.
- `log_detections(self, detections)`: Logs detected objects.
- `save_log(self)`: Saves the detection log to a CSV file.

## Future Enhancements

- Implement object tracking across frames
- Add support for multiple camera inputs
- Integrate different object detection models
- Implement more advanced analytics and visualizations

