import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import threading
from PIL import Image, ImageTk

class ObjectDetectionGUI:
    def __init__(self, master):
        self.master = master
        master.title("Object Detection")

        self.video_source = 0  # Default to webcam
        self.vid = None
        self.is_running = False

        # Create GUI elements
        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()

        self.btn_start = tk.Button(master, text="Start", width=10, command=self.start_detection)
        self.btn_start.pack(side=tk.LEFT)

        self.btn_stop = tk.Button(master, text="Stop", width=10, command=self.stop_detection)
        self.btn_stop.pack(side=tk.LEFT)

        self.btn_file = tk.Button(master, text="Open File", width=10, command=self.open_file)
        self.btn_file.pack(side=tk.LEFT)

        self.confidence_label = tk.Label(master, text="Confidence:")
        self.confidence_label.pack(side=tk.LEFT)
        self.confidence_slider = tk.Scale(master, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.confidence_slider.set(0.5)
        self.confidence_slider.pack(side=tk.LEFT)

        self.threshold_label = tk.Label(master, text="Threshold:")
        self.threshold_label.pack(side=tk.LEFT)
        self.threshold_slider = tk.Scale(master, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.threshold_slider.set(0.3)
        self.threshold_slider.pack(side=tk.LEFT)

    def start_detection(self):
        if not self.is_running:
            self.is_running = True
            self.vid = cv2.VideoCapture(self.video_source)
            self.detection_thread = threading.Thread(target=self.detect_objects)
            self.detection_thread.start()

    def stop_detection(self):
        self.is_running = False
        if self.vid:
            self.vid.release()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            self.video_source = file_path
            messagebox.showinfo("File Selected", f"Selected file: {file_path}")

    def detect_objects(self):
        # Here you would implement your object detection logic
        # For now, we'll just display the video feed
        while self.is_running:
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.canvas.photo = photo
            else:
                self.stop_detection()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionGUI(root)
    root.mainloop()