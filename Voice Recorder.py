import sounddevice
import soundfile
import numpy
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QVBoxLayout, 
QHBoxLayout, QPushButton, QComboBox, QListWidget)
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
        container_inner_main.setStyleSheet("background-color: transparent; border-radius: 5px;")
        Top= QHBoxLayout(container_inner_main)

        container_side_bar= QWidget()
        container_side_bar.setStyleSheet("background-color: #FF0000; border-radius: 5px;")
        side= QVBoxLayout(container_side_bar)

        #start side bar
        
        #TODO format Bar list
        Bar_list= QListWidget()
        Bar_list.addItems(['one', 'two'])
        Bar_list.setStyleSheet(''' 

''')

        side.addWidget(Bar_list)


        #End Side Bar

        container_main= QWidget()
        container_main.setStyleSheet("background-color: #800080; border-radius: 5px;")

        Top.addWidget(container_side_bar, stretch=1)
        Top.addWidget(container_main, stretch=5)

        container_bottom_bar= QWidget()
        #border radius curves the edges of the container slightly
        container_bottom_bar.setStyleSheet("background-color: #353535; border-radius: 5px;")
        bottom= QHBoxLayout(container_bottom_bar)
        bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #start of bottom bar
        mics= QComboBox()
        mics.addItems(['one', 'two'])
        mics.setStyleSheet('''
                QComboBox {
                    background-color: #545454;  
                    color: #FFFFFF;
                    border: 2px solid #000000;
                    padding-top: 6px;
                    padding-bottom: 6px;
                    padding-right: 120px;
                    font-size: 15px;
                    min-width: 90px;
                    max-width: 90px
                           }
                
                QComboBox:hover, QComboxBox:focus {
                    border: 2px solid #000000;
                    background-color: #808080                           
                           }
                
                QComboBox QAbstractItemView {
                    Background-color: #545454;
                    min-width: 214x;
                    max-width: 214px    
                          }
''')


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
                    background-color: #808080
                }}""")
        

        time= QLabel('00:00:00/00:00:00')
        time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        time.setFont(QFont('Arial', 20))

        Play_button= QPushButton('▶')
        Play_button.setFixedSize(QSize(button_size, button_size))
        Play_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #545454;
            color: white;
            border: 2px solid black;
            border-radius: {radius}px;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:pressed {{
            background-color: #808080
        }}""")

        Back_to_beginning= QPushButton('◀◀')
        Back_to_beginning.setFixedSize(QSize(button_size, button_size))
        Back_to_beginning.setStyleSheet(f"""
        QPushButton {{
            background-color: #545454;
            color: white;
            border: 2px solid black;
            border-radius: {radius}px;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:pressed {{
            background-color: #808080
        }}""")

        time_speed= QPushButton('1x')
        time_speed.setFixedSize(50, 50)
        time_speed.setStyleSheet(f"""
        QPushButton {{
            background-color: #545454;
            color: white;
            border: 2px solid black;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:pressed {{
            background-color: #808080
        }}""")

        #end bottom bar

        bottom.addWidget(mics)
        bottom.addStretch(1)
        bottom.addWidget(record_circle_button, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(time, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(Play_button, alignment= Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(Back_to_beginning, alignment= Qt.AlignmentFlag.AlignCenter)
        bottom.addStretch(2)
        bottom.addWidget(time_speed)

        main_layout.addWidget(container_inner_main, stretch=6)
        main_layout.addWidget(container_bottom_bar, stretch=1)



main()