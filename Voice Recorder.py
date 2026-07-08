import sounddevice
import soundfile
import numpy
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout
from PySide6.QtCore import Qt

def main():
    app = QApplication()
    window = Voice_recorder()
    window.show()
    app.exec()


class Voice_recorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Voice Recorder')

        container= QWidget()
        container.setStyleSheet("background-color: #add8e6; border-radius: 5px;")
        self.setCentralWidget(container)

        layout= QGridLayout(container)

        label= QLabel('Label')

        layout.addWidget(label, 1, 2)

main()