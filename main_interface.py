from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QProgressBar, QGridLayout
from PyQt5.QtCore import Qt
import copy_images
from PyQt5.QtWidgets import QSizePolicy

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Copy Images")
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.file_path_label = QLabel("inital_pose文本路径:")
        self.file_path_entry = QLineEdit()
        self.browse_button = QPushButton("Browse1")
        self.browse_button.clicked.connect(self.browse_file)

        self.output_path_label = QLabel("影像拷贝输出路径:")
        self.output_path_entry = QLineEdit()
        self.output_browse_button = QPushButton("Browse2")
        self.output_browse_button.clicked.connect(self.browse_directory)

        self.progress = QProgressBar()

        self.run_button = QPushButton("运行")
        self.run_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.run_button.clicked.connect(self.run_main_and_handle_result)

        self.cancel_button = QPushButton("关闭")
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.cancel_button.clicked.connect(self.close)

        self.layout.addWidget(self.file_path_label, 0, 0)
        self.layout.addWidget(self.file_path_entry, 0, 1)
        self.layout.addWidget(self.browse_button, 0, 2)
        self.layout.addWidget(self.output_path_label, 1, 0)
        self.layout.addWidget(self.output_path_entry, 1, 1)
        self.layout.addWidget(self.output_browse_button, 1, 2)
        self.layout.addWidget(self.progress, 2, 0, 1, 3)
        self.layout.addWidget(self.run_button, 3, 1, Qt.AlignRight)
        self.layout.addWidget(self.cancel_button, 3, 2, Qt.AlignRight)

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt);;All files (*.*)")
        if filename:
            self.file_path_entry.setText(filename)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory")
        if directory:
            self.output_path_entry.setText(directory)

    def run_main_and_handle_result(self):
        self.progress.setValue(0)
        result = copy_images.copy_images_main(self.file_path_entry.text(), self.output_path_entry.text(), self.progress)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()