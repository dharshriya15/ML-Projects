import numpy as np
import cv2
import os
from gui import ObjectDetectionGUI
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext
import csv
from datetime import datetime

class YOLODetector:
    def __init__(self, yolo_dir="yolo-coco"):
        self.conf = 0.5
        self.thresh = 0.3
        self.yolo_dir = yolo_dir
        self.load_yolo()

    def load_yolo(self):
        labels_path = os.path.sep.join([self.yolo_dir, "coco.names"])
        self.LABELS = open(labels_path).read().strip().split("\n")

        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")

        weights_path = os.path.sep.join([self.yolo_dir, "yolov3.weights"])
        config_path = os.path.sep.join([self.yolo_dir, "yolov3.cfg"])

        print("[INFO] loading YOLO from disk...")
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect(self, frame, conf, thresh):
        (H, W) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.ln)

        boxes = []
        confidences = []
        classIDs = []

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > conf:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf, thresh)

        detections = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = f"{self.LABELS[classIDs[i]]}: {confidences[i]:.4f}"
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                detections.append({
                    'label': self.LABELS[classIDs[i]],
                    'confidence': confidences[i],
                    'box': (x, y, w, h)
                })

        return frame, detections

class EnhancedObjectDetectionGUI(ObjectDetectionGUI):
    def __init__(self, master):
        super().__init__(master)
        self.yolo_detector = YOLODetector()
        
        self.log_area = scrolledtext.ScrolledText(master, height=10)
        self.log_area.pack(pady=10)
        
        self.btn_save_log = tk.Button(master, text="Save Log", width=10, command=self.save_log)
        self.btn_save_log.pack(side=tk.LEFT)
        
        self.detections_log = []

    def detect_objects(self):
        while self.is_running:
            ret, frame = self.vid.read()
            if ret:
                conf = self.confidence_slider.get()
                thresh = self.threshold_slider.get()
                frame, detections = self.yolo_detector.detect(frame, conf, thresh)
                
                # Log detections
                self.log_detections(detections)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.canvas.photo = photo
            else:
                self.stop_detection()
                break

    def log_detections(self, detections):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for detection in detections:
            log_entry = f"{timestamp} - Detected {detection['label']} (Confidence: {detection['confidence']:.2f})\n"
            self.log_area.insert(tk.END, log_entry)
            self.log_area.see(tk.END) 
            self.detections_log.append({
                'timestamp': timestamp,
                'label': detection['label'],
                'confidence': detection['confidence'],
                'box': detection['box']
            })

    def save_log(self):
        filename = f"object_detection_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'label', 'confidence', 'box']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.detections_log:
                writer.writerow(entry)
        self.log_area.insert(tk.END, f"Log saved to {filename}\n")
        self.log_area.see(tk.END)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedObjectDetectionGUI(root)
    root.mainloop()