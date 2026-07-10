import sounddevice
import soundfile
import numpy
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

def main():
    app = QApplication()
    window = Voice_recorder()
    window.show()
    app.exec()


class Voice_recorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Voice Recorder')
        self.resize(1100, 700)
        self.setMinimumSize(500, 500)

        main_container= QWidget()
        self.setCentralWidget(main_container)
        main_layout= QVBoxLayout(main_container)

        container_inner_main= QWidget()
        #border radius curves the edges of the container slightly
        container_inner_main.setStyleSheet("background-color: #add8e6; border-radius: 5px;")
        Top= QHBoxLayout(container_inner_main)

        container_bar= QWidget()
        container_bar.setStyleSheet("background-color: #FF0000; border-radius: 5px;")

        container_main= QWidget()
        container_main.setStyleSheet("background-color: #800080; border-radius: 5px;")

        Top.addWidget(container_bar, stretch=1)
        Top.addWidget(container_main, stretch=5)

        container_bottom_bar= QWidget()
        #border radius curves the edges of the container slightly
        container_bottom_bar.setStyleSheet("background-color: #008000; border-radius: 5px;")
        bottom= QHBoxLayout(container_bottom_bar)
        bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)


        record_circle_button= QPushButton('○')

        button_size= 65
        record_circle_button.setFixedSize(QSize(button_size, button_size))

        radius= button_size//2
        record_circle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #FF0000;
                    color: white;
                    border: 2px solid black;
                    border-radius: {radius}px;
                    font-size: 16px;
                    font-weight: bold;
                }} 
                QPushButton:pressed {{
                    background-color: #000000
                }}""")
        

        time= QLabel('00:00:00/00:00:00')
        time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        time.setFont(QFont('Arial', 20))

        Play_button= QPushButton('▶')
        Play_button.setFixedSize(QSize(button_size, button_size))
        Play_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #808080;
            color: white;
            border: 2px solid black;
            border-radius: {radius}px;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:pressed {{
            background-color: #000000
        }}""")

        bottom.addStretch(1)
        bottom.addWidget(record_circle_button, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(time, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(Play_button, alignment= Qt.AlignmentFlag.AlignCenter)

        bottom.addStretch(1)


        main_layout.addWidget(container_inner_main, stretch=6)
        main_layout.addWidget(container_bottom_bar, stretch=1)



main()