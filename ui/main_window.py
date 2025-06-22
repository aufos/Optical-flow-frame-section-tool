import random
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QImage
from ui.zoom_pan_graphics_view import ZoomPanGraphicsView
from exporters.kitti_exporter import KITTIExporter

class VideoFrameComparer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Frame Comparer")
        self.setFixedSize(1300, 750)

        self.cap = None
        self.total_frames = 0
        self.frame_index = 0
        self.offset = 1
        self.video_path = ""

        # self.annotations = []
        # self.selected_frame1_point = None
        # self.selected_frame2_point = None
        self.max_pairs = 10
        self.idx_count = 0
        self.colors = []

        self.exporter = KITTIExporter()

        self.init_ui()

    def init_ui(self):
        QApplication.setStyle("fusion")

        self.load_button = QPushButton("Load Video")
        self.load_button.clicked.connect(self.load_video)
        self.video_path_label = QLabel("No video loaded")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setVisible(False)
        self.slider.valueChanged.connect(self.update_frames)

        self.timestamp_input = QLineEdit()
        self.timestamp_input.setPlaceholderText("Enter timestamp (mm:ss)")
        self.timestamp_input.editingFinished.connect(self.update_frame_from_timestamp)
        self.timestamp_input.setVisible(False)

        self.offset_selector = QSpinBox()
        self.offset_selector.setMinimum(1)
        self.offset_selector.setValue(1)
        self.offset_selector.setPrefix("Offset: ")
        self.offset_selector.valueChanged.connect(self.update_offset)
        self.offset_selector.setVisible(False)

        self.prev_button = QPushButton("<< Prev")
        self.next_button = QPushButton("Next >>")
        self.prev_button.clicked.connect(self.go_prev)
        self.next_button.clicked.connect(self.go_next)

        self.label1 = QLabel("Frame: -")
        self.label2 = QLabel("Frame: -")

        self.image_view1 = ZoomPanGraphicsView()
        self.image_view2 = ZoomPanGraphicsView()

        self.save_button = QPushButton("Save Annotation")
        self.save_button.clicked.connect(self.export_annotations_manual)

        main_layout = QVBoxLayout()

        load_layout = QHBoxLayout()
        load_layout.addWidget(self.load_button)
        load_layout.addWidget(self.video_path_label)
        main_layout.addLayout(load_layout)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.timestamp_input)
        slider_layout.addWidget(self.slider)
        main_layout.addLayout(slider_layout)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.prev_button)
        control_layout.addWidget(self.offset_selector)
        control_layout.addWidget(self.next_button)
        control_layout.addWidget(self.save_button)
        main_layout.addLayout(control_layout)

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.label1, alignment=Qt.AlignCenter)
        label_layout.addWidget(self.label2, alignment=Qt.AlignCenter)
        main_layout.addLayout(label_layout)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_view1)
        image_layout.addWidget(self.image_view2)
        main_layout.addLayout(image_layout)

        self.setLayout(main_layout)

    def set_max_pairs(self, val):
        self.max_pairs = val

    def load_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if not file_name:
            QMessageBox.warning(self, "Error", "No video file selected.")
            return

        self.cap = cv2.VideoCapture(file_name)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Failed to open video file.")
            return

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_path = file_name
        self.video_path_label.setText(file_name)

        self.slider.setMaximum(self.total_frames - 2)
        self.slider.setValue(0)
        self.slider.setVisible(True)
        self.timestamp_input.setVisible(True)
        self.offset_selector.setVisible(True)

        self.prev_button.setEnabled(True)
        self.next_button.setEnabled(True)

        self.update_frames(0)

    def update_offset(self, val):
        self.offset = val
        self.update_frames(self.frame_index)

    def get_frame(self, index):
        if index >= self.total_frames:
            return None
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = self.cap.read()
        if not ret:
            QMessageBox.warning(self, "Error", "Failed to retrieve frame.")
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        return QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

    def update_frames(self, value):
        if self.cap is None:
            QMessageBox.warning(self, "Error", "No video loaded.")
            return

        self.frame_index = value
        frame1 = self.get_frame(value)
        frame2 = self.get_frame(value + self.offset)

        if frame1:
            self.label1.setText(f"Frame: {value}")
            self.image_view1.set_image(frame1, reset_view=False)
            # self.draw_annotations(frame1, frame=1)
        if frame2:
            self.label2.setText(f"Frame: {value + self.offset}")
            self.image_view2.set_image(frame2, reset_view=False)
            # self.draw_annotations(frame2, frame=2)

        seconds = int(self.frame_index / self.cap.get(cv2.CAP_PROP_FPS))
        minutes = seconds // 60
        seconds = seconds % 60
        self.timestamp_input.setText(f"{minutes:02}:{seconds:02}")

    def update_frame_from_timestamp(self):
        timestamp = self.timestamp_input.text()
        if ':' not in timestamp:
            return
        minutes, seconds = map(int, timestamp.split(':'))
        frame_time = minutes * 60 + seconds
        frame_index = int(frame_time * self.cap.get(cv2.CAP_PROP_FPS))
        self.slider.setValue(min(frame_index, self.total_frames - 1))

    def go_prev(self):
        if self.cap is None:
            QMessageBox.warning(self, "Error", "No video loaded.")
            return
        new_index = max(0, self.frame_index - 1)
        self.slider.setValue(new_index)

    def go_next(self):
        if self.cap is None:
            QMessageBox.warning(self, "Error", "No video loaded.")
            return
        new_index = min(self.total_frames - self.offset - 1, self.frame_index + 1)
        self.slider.setValue(new_index)

    def export_annotations_automate(self):
        """
        Automatically exports annotations for selected pairs of video frames.
        For every 10-frame interval, it retrieves two frames (frame_i and frame_{i+10})
        and exports their annotation data using the configured exporter.
        """
        export_dir = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if not export_dir:
            QMessageBox.warning(self, "Error", "No export directory selected.")
            return

        if self.cap is None:
            QMessageBox.warning(self, "Error", "No video loaded.")
            return

        total_pairs = 20  # Step of 10
        for i in range(0, total_pairs * 10, 10):
            frame1 = self.get_frame(i)
            frame2 = self.get_frame(i + 10)
            if frame1 is None or frame2 is None:
                print(f"Skipping pair {i}-{i+10} due to frame retrieval failure.")
                continue
            self.exporter.export(self.idx_count, frame1, frame2, export_dir)
            self.idx_count+=1;

    def export_annotations_manual(self):
        """
        Mannually select frame pairs and exports their annotation data using the configured exporter.
        """
        export_dir = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if not export_dir:
            QMessageBox.warning(self, "Error", "No export directory selected.")
            return

        img1 = self.get_frame(self.frame_index)
        img2 = self.get_frame(self.frame_index + self.offset)

        if img1 is None or img2 is None:
            QMessageBox.warning(self, "Error", "Failed to retrieve frames for export.")
            return

        self.exporter.export(self.frame_index, img1, img2, export_dir)