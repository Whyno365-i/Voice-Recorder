import sounddevice as sd
import soundfile as sf
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QWidgetAction, QGridLayout, QVBoxLayout, QListWidgetItem,
QHBoxLayout, QPushButton, QComboBox, QListWidget, QMenu)
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
        container_side_bar.setStyleSheet("background-color: #353535; border-radius: 5px;")
        container_side_bar.setFixedWidth(195)
        side= QVBoxLayout(container_side_bar)

        #start side bar
        Bar_list= QListWidget()
        Bar_list.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        Bar_list.addItems(['one', 'two', 'three', 'four', 'five', 'six', 'seven'])
        for i in range(Bar_list.count()):
            item= Bar_list.item(i)
            item.setSizeHint(QSize(0,120))
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        

        Bar_list.setStyleSheet(''' 
            QListWidget{
                background-color: Transparent;
                font-family: Arial; 
                font-size: 30px; 
                font-style: normal;     
                }
            
            QListWidget::item {
                background-color: #545454;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 0px 0px;
                }
            QListWidget::item:hover {
                background-color: #808080
                }
''')

        side.addWidget(Bar_list)


        #End Side Bar

        container_main= QWidget()
        container_main.setStyleSheet("background-color: #800080; border-radius: 5px;")
        Top_inner= QVBoxLayout(container_main)

        #Start Container_main
        container_inner_top_bar= QWidget()
        container_inner_top_bar.setStyleSheet("background-color: #013220; border-radius: 5px;")
        inner_top_bar= QHBoxLayout(container_inner_top_bar)

        #Start Container_inner_top_bar
        open_side= QPushButton('≡')
        open_side.setFixedSize(QSize(40,40))
        open_side.setStyleSheet(''' 
            QPushButton {
                background-color: Transparent;
                font: 40px;
                padding-bottom: 7px;
                }
            
            QPushButton:hover {
                background-color: #808080
                }
''')
        name= QLabel('Name')
        name.setFont(QFont('Arial', 20))

        three_dots= QPushButton('...')
        three_dots.setFixedSize(QSize(40,40))
        three_dots.setStyleSheet('''
            QPushButton {
                background: Transparent;
                font: 30px;
                padding-bottom: 15px;                 
                }
            
            QPushButton:hover {
                background-color: #808080
                }
''')


        inner_top_bar.addWidget(open_side)
        inner_top_bar.addWidget(name)
        inner_top_bar.addStretch()
        inner_top_bar.addWidget(three_dots)


        #End Container_inner_top_bar

        container_inner_bottom_main= QWidget()
        container_inner_bottom_main.setStyleSheet("background-color: #39FF14; border-radius: 5px;")
        Top_inner.addWidget(container_inner_top_bar, stretch=1)
        Top_inner.addWidget(container_inner_bottom_main, stretch=13)


        #End Container_main


        Top.addWidget(container_side_bar, stretch=1)
        Top.addWidget(container_main, stretch=5)

        container_bottom_bar= QWidget()
        #border radius curves the edges of the container slightly
        container_bottom_bar.setStyleSheet("background-color: #353535; border-radius: 5px;")
        bottom= QHBoxLayout(container_bottom_bar)
        bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #start of bottom bar
        mics= QComboBox()
        mics.addItems(['one', 'two', 'three', 'four', 'five'])
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


        self.record_circle_button= QPushButton('○')
        self.record_circle_button.setCheckable(True)
        self.record_circle_button.clicked.connect(self.record)

        button_size= 65
        self.record_circle_button.setFixedSize(QSize(button_size, button_size))

        radius= button_size//2
        self.record_circle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #FF0000;
                    color: white;
                    border: 2px solid black;
                    border-radius: {radius}px;
                    font-size: 16px;
                    font-weight: bold;
                }} 
                QPushButton:hover {{
                    background-color: #f22952
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
        bottom.addWidget(self.record_circle_button, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(time, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(Play_button, alignment= Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(Back_to_beginning, alignment= Qt.AlignmentFlag.AlignCenter)
        bottom.addStretch(2)
        bottom.addWidget(time_speed)

        main_layout.addWidget(container_inner_main, stretch=6)
        main_layout.addWidget(container_bottom_bar, stretch=1)
        
        self.sample_rate= 44100
        self.channels= 1
        self.max_duration= 3600
        self.audio_data=None

    def record(self, checked):
        with open('recording number', 'r') as f:
            n= int(f.read().strip())


        if checked:
            self.record_circle_button.setText('| |')
            self.record_circle_button.setStyleSheet('''
                QPushButton {
                    background-color: #545454                                
                    }
''')
            print('Recording')
            self.audio_data= sd.rec(int(self.max_duration*self.sample_rate), samplerate=self.sample_rate,
                                     channels=self.channels, dtype='float32')
            
            self.start_time= sd.get_stream().time

        else:
            self.record_circle_button.setText('○')

            #lets say that sound card (self.start_time) says it's inernal stop watch is 120 secs
            #then after a couple of minutes bam you stop it and get the current time 124 secs
            #Then duration gets the difference between the two and samples_recorded and audio variable 
            #splice it to get rid of the unnessary parts
            duration= sd.get_stream().time - self.start_time
            sd.stop()
            print('finished')

            samples_recorded= int(duration * self.sample_rate)
            audio= self.audio_data[:samples_recorded] # type: ignore

            ouput_name= f'audio files/recording{n}.mp3'
            sf.write(ouput_name, audio, self.sample_rate)
            print('success!')

            n+=1

            with open('recording number', 'w') as f:
                f.write(str(n))



main()