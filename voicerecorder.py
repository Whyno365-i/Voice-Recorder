import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
import os
import ctypes
from send2trash import send2trash
from mutagen.mp3 import MP3 
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton,
                               QComboBox, QListWidget, QMenu, QDialog, QSlider, QSpacerItem)
from PySide6.QtCore import Qt, QSize, QUrl, QTimer
from PySide6.QtGui import QFont, QAction, QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

def main():
    app = QApplication()
    window = Voice_recorder()
    window.show()
    app.exec()



class Voice_recorder(QMainWindow):
    def __init__(self):
        #TODO Make app logo
        super().__init__()
        self.setWindowTitle('Voice Recorder')
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
        self.setWindowIcon(QIcon('App_logo.ico'))
        self.resize(1100, 700)
        self.setMinimumSize(500, 500)

        self.mp3_basename= ''
        self.is_showing= True
        self.is_paused= False
        self.seconds=0
        self.minutes=0
        self.hours=0
        self.one_time= True

        
        self.sample_rate= 0
        self.channels= 1
        self.max_duration= 3600
        self.audio_data=None

        #You have to initazile it here so you don't recreate it and you later check if the path is different and update it
        self.player= QMediaPlayer()
        self.audio_output= QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        
        self.main_app()
    
    def main_app(self):
        main_container= QWidget()
        self.setCentralWidget(main_container)
        main_layout= QVBoxLayout(main_container)

        container_inner_main= QWidget()
        #border radius curves the edges of the container slightly
        container_inner_main.setStyleSheet("background-color: transparent; border-radius: 5px;")
        Top= QHBoxLayout(container_inner_main)

        self.container_side_bar= QWidget()
        self.container_side_bar.setStyleSheet("background-color: #353535; border-radius: 5px;")
        self.container_side_bar.setFixedWidth(195)
        side= QVBoxLayout(self.container_side_bar)

        #start side bar
        self.Bar_list= QListWidget()
        self.Bar_list.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.Bar_list.currentTextChanged.connect(self.file_playing)
        self.side_bar_files()
        self.Bar_list.setStyleSheet(''' 
            QListWidget{
                background-color: Transparent;
                font-family: Arial; 
                font-size: 20px; 
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

        side.addWidget(self.Bar_list)
        #End Side Bar

        container_main= QWidget()
        container_main.setStyleSheet("background-color: Transparent; border-radius: 5px;")
        Top_inner= QVBoxLayout(container_main)

        #Start Container_main
        container_inner_top_bar= QWidget()
        container_inner_top_bar.setStyleSheet("background-color: #353535; border-radius: 5px;")
        inner_top_bar= QHBoxLayout(container_inner_top_bar)

        #Start Container_inner_top_bar
        open_side= QPushButton('≡')
        open_side.clicked.connect(self.hide_side)
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
        self.name= QLabel(f'{self.mp3_basename}')
        self.name.setFont(QFont('Arial', 20))

        three_dots= QPushButton('···')
        three_dots.setFixedSize(QSize(40,40))
        three_dots.setStyleSheet('''
            QPushButton {
                background: Transparent;
                font: bold 30px;            
                }
            
            QPushButton:hover {
                background-color: #808080;
                }
            
            QPushButton::menu-indicator {
                image: none;
                width: 0px;
            }
    ''')

        dropdown= QMenu(self)

        dropdown.setStyleSheet('''
            QMenu::item {
                font-size: 20px;
                border-radius: 5px;
                padding-right: 30px;
                padding-top: 5px;
                padding-bottom: 5px;
            }

            QMenu::item:selected {
                background-color: #808080;
            }

''')

        rename= QAction('Rename', self)
        show_folder= QAction('Show in Folder', self)
        delete= QAction('Delete', self) 
        refresh= QAction('Refresh Files', self)

        rename.triggered.connect(self.rename_file)
        show_folder.triggered.connect(self.open_folder)
        delete.triggered.connect(self.delete_file)
        refresh.triggered.connect(lambda: (self.Bar_list.clear(), self.side_bar_files()))

        dropdown.addAction(rename)
        dropdown.addAction(show_folder)
        dropdown.addAction(delete)
        dropdown.addAction(refresh)

        three_dots.setMenu(dropdown)


        inner_top_bar.addWidget(open_side)
        inner_top_bar.addWidget(self.name)
        inner_top_bar.addStretch()
        inner_top_bar.addWidget(three_dots)


        #End Container_inner_top_bar

        self.container_inner_bottom_main= QWidget()
        self.container_inner_bottom_main.setStyleSheet("background-color: #353535; border-radius: 5px;")
        self.audio_place= QVBoxLayout(self.container_inner_bottom_main)


        self.container_record= QWidget()
        self.container_record.setStyleSheet("background-color: #353535; border-radius: 5px;")
        self.record_place= QHBoxLayout(self.container_record)

        #Start container_record
        self.recording= QLabel('Recording')
        self.recording.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recording.setStyleSheet('''
            QLabel{
                font: 50px;
            }
''')


        self.recording_label()
        #End container_record

        Top_inner.addWidget(container_inner_top_bar, stretch=1)
        Top_inner.addWidget(self.container_inner_bottom_main, stretch=13)
        Top_inner.addWidget(self.container_record, stretch=13)
        self.container_record.hide()


        #End Container_main


        Top.addWidget(self.container_side_bar, stretch=1)
        Top.addWidget(container_main, stretch=5)

        container_bottom_bar= QWidget()
        #border radius curves the edges of the container slightly
        container_bottom_bar.setStyleSheet("background-color: #353535; border-radius: 5px;")
        bottom= QHBoxLayout(container_bottom_bar)
        bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #start of bottom bar
        self.mics= QComboBox()
        self.find_mics()
        #list is important and you can't just put brackets around it!
        self.mics.addItems(list(self.mics_dictionary.keys()))
        self.mics.setStyleSheet('''
                QComboBox {
                    background-color: #545454;  
                    color: #FFFFFF;
                    border: 2px solid #000000;
                    padding-top: 6px;
                    padding-bottom: 6px;
                    padding-right: 25px;
                    font-size: 15px;
                    min-width: 120px;
                    max-width: 240px;
                            }
                
                QComboBox:hover {
                    border: 2px solid #000000;
                    background-color: #808080;                           
                            }
                
                QComboBox QAbstractItemView {
                    Background-color: #545454;
                    min-width: 120x; 
                    max-width: 280px;   
                            }
    ''')


        self.record_circle_button= QPushButton('○')
        self.record_circle_button.setCheckable(True)
        self.record_circle_button.clicked.connect(self.record)

        button_size= 65
        self.record_circle_button.setFixedSize(QSize(button_size, button_size))

        self.radius= button_size//2
        self.record_circle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #FF0000;
                    color: white;
                    border: 2px solid black;
                    border-radius: {self.radius}px;
                    font-size: 16px;
                    font-weight: bold;
                }} 
                QPushButton:hover {{
                    background-color: #f22952
                }}""")
        

        self.time= QLabel('00:00:00/00:00:00')
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.time.setFont(QFont('Arial', 20))

        self.Play_button= QPushButton('▶')
        self.Play_button.setCheckable(True)
        self.Play_button.clicked.connect(self.play)
        self.Play_button.setFixedSize(QSize(button_size, button_size))
        self.Play_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #545454;
            color: white;
            border: 2px solid black;
            border-radius: {self.radius}px;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:hover {{
            background-color: #808080
        }}""")

        self.Pause_button= QPushButton('| |')
        self.Pause_button.clicked.connect(self.pause)
        self.Pause_button.setFixedSize(QSize(button_size, button_size))
        self.Pause_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #545454;
            color: white;
            border: 2px solid black;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:hover {{
            background-color: #808080
        }}""")



        self.Back_to_beginning= QPushButton('◀◀')
        self.Back_to_beginning.clicked.connect(self.back)
        self.Back_to_beginning.setFixedSize(QSize(button_size, button_size))
        self.Back_to_beginning.setStyleSheet(f"""
        QPushButton {{
            background-color: #545454;
            color: white;
            border: 2px solid black;
            border-radius: {self.radius}px;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:hover {{
            background-color: #808080
        }}""")

        self.time_speed= QPushButton('1x')
        self.time_speed.clicked.connect(self.speed)
        self.time_speed.setFixedSize(50, 50)
        self.time_speed.setStyleSheet(f"""
        QPushButton {{
            background-color: #545454;
            color: white;
            border: 2px solid black;
            font-size: 16px;
            font-weight: bold;
        }} 
        QPushButton:hover {{
            background-color: #808080
        }}""")

        bottom.addWidget(self.mics)
        bottom.addStretch(1)
        bottom.addWidget(self.record_circle_button, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(self.time, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(self.Play_button, alignment= Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(self.Pause_button, alignment= Qt.AlignmentFlag.AlignCenter)
        bottom.addWidget(self.Back_to_beginning, alignment= Qt.AlignmentFlag.AlignCenter)
        bottom.addStretch(2)
        bottom.addWidget(self.time_speed)
        self.Pause_button.hide()

        #end bottom bar

        main_layout.addWidget(container_inner_main, stretch=6)
        main_layout.addWidget(container_bottom_bar, stretch=1)
        self.Back_to_beginning.hide()

    def record(self, checked):
        #So basically it calls the attribute self.audio_file_dir.
        self.n = max(
            (
                int(n) + 1
                #The for loop checks through all the files in the audio files folder. Check the self.audio_files attribute and you'll understand
                for f in self.audio_files_dir.glob("recording*.mp3")
                #This removes the prefix recording leaving you the number.
                if (n := f.stem.removeprefix("recording")).isdigit()
            ),
            #This is a fall back incase there is no files with recording prefix.
            default=1,
        )

        if checked:
            self.Play_button.hide()
            self.Back_to_beginning.hide()
            self.time_speed.hide()
            self.container_inner_bottom_main.hide()
            self.container_record.show()
            self.amount_time= QTimer(self)
            self.amount_time.timeout.connect(self.clock)
            self.amount_time.start(1000)
            self.mics.setEnabled(False)
            self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}')
            self.time.setFont(QFont('Arial', 30))        
            self.record_circle_button.setText('| |')
            self.record_circle_button.setStyleSheet('''
                QPushButton {
                    background-color: #545454;
                    color: white;
                    border: 2px solid black;
                    font-size: 16px;
                    font-weight: bold;                                
                    }
                
                QPushButton:hover {
                    background-color: #808080;
                    }
''')

            self.using_mic()


            print('Recording')
            self.audio_data= sd.rec(int(self.max_duration*self.sample_rate), samplerate=self.sample_rate,
                                     channels=self.channels, dtype='float32', device= self.device_index)
            
            self.start_time= sd.get_stream().time

        else:
            self.stopped_recording()


    def hide_side(self):
        if self.is_showing:
            self.container_side_bar.hide()
            self.is_showing=False
        
        else:
            self.container_side_bar.show()
            self.is_showing=True

        self.recording_label()
    
    #The @property makes the function an attribute making it easier to compute. (saves computing power)
    @property
    def audio_files_dir(self):
        #__file__ is the current file name and Path() around it turns it into a pathlib object
        #resolve() it is everything before the current file
        #parent is adding the current file making it a full abosoulte path
        return Path(__file__).resolve().parent / "audio files"


    def file_playing(self):
        #so currentItem() brings the hash of the Listwidget box and .text() extracts the text from it
        self.mp3_basename= self.Bar_list.currentItem().text()
        self.name.setText(self.mp3_basename)

        audio_file= MP3(str(self.audio_files_dir / f'{self.mp3_basename}.mp3'))

        self.duration= audio_file.info.length

        self.total_duration(int(self.duration)*1000)

    
        self.timestamp_buttons()


        try:
            self.slider.deleteLater()
            n= 0

        except RuntimeError:
            self.slider= QSlider(Qt.Orientation.Horizontal)
            n=1

        except AttributeError:
            self.slider= QSlider(Qt.Orientation.Horizontal)
            n=1

        if n == 0:
            self.slider= QSlider(Qt.Orientation.Horizontal)

        self.audio_place.addWidget(self.slider)

        #The code interperts the time in miliseconds but you were giving it seconds
        #So multiplying it by 1000 fixes that
        self.slider.setMaximum(int(self.duration) * 1000)

        self.slider.setMinimumHeight(410)
        self.slider.setMaximumHeight(410)
        self.slider.setStyleSheet('''
            QSlider::groove:horizontal {
                border: 1px solid #545454;
                height: 8px;
                background: #545454;
                border-radius: 2px; 
            }
        

            QSlider::handle:horizontal {
                background: #FFFFFF;
                border:2px solid #000000;
                width: 6px;
                height: 390px;
                margin: -196px 0px;
                border-radius: 2px; 
            }

''')

        self.slider.sliderPressed.connect(self.slider_pressed_2)
        #the line below says when the slider is released run the slider_released method. More information in the method
        self.slider.sliderReleased.connect(self.slider_released_2)
        #This line below makes it so that when the slider is moved it updates the position but only when the user is clicking on it
        self.slider.sliderMoved.connect(self.before_player)


    def play(self, playing):
        if self.name:
            if playing:
                self.Back_to_beginning.show()
                self.Pause_button.show()
                self.record_circle_button.hide()
                self.time_speed.setEnabled(False)
                self.Play_button.setText('◻')
                self.Play_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #FF0000;
                        color: white;
                        border: 2px solid black;
                        border-radius: {self.radius}px;
                        font-size: 16px;
                        font-weight: bold;
                    }} 
                    QPushButton:hover {{
                        background-color: #f22952
                    }}""")

                #the line below says that when the player positions change run the update_slider method
                #This method updates the slider
                self.player.positionChanged.connect(self.update_slider)
                #the line below says when the slider is pressed run the slider_pressed method. More information in the method
                self.slider.sliderPressed.connect(self.slider_pressed)
                #the line below says when the slider is released run the slider_released method. More information in the method
                self.slider.sliderReleased.connect(self.slider_released)
                #This line below makes it so that when the slider is moved it updates the position but only when the user is clicking on it
                self.slider.sliderMoved.connect(self.player.setPosition)



                #The following line gets the path to the file using the attribute audio_files_dir and adding the file_name.mp3
                new_audio_file= self.audio_files_dir / f"{self.mp3_basename}.mp3"
                #This makes it an absolute path not a relative path
                new_source= QUrl.fromLocalFile(new_audio_file.absolute())

                #Uses the variable above to check if it's the same or new to see if it should over write the varaible
                if self.player.source() != new_source:
                    self.player.setSource(new_source)

                
                if self.time_speed.text() == '1x':
                    self.player.setPlaybackRate(1.0)
                    self.amount_time_2= QTimer(self)
                    self.amount_time_2.timeout.connect(self.playing_clock)
                    self.amount_time_2.start(1000)
        
                elif self.time_speed.text() == '2x':
                    self.player.setPlaybackRate(2.0)
                    self.amount_time_2= QTimer(self)
                    self.amount_time_2.timeout.connect(self.playing_clock)
                    self.amount_time_2.start(500)

                elif self.time_speed.text() == '3x':
                    self.player.setPlaybackRate(3.0)
                    self.amount_time_2= QTimer(self)
                    self.amount_time_2.timeout.connect(self.playing_clock)
                    self.amount_time_2.start(333)

                elif self.time_speed.text() == '4x':
                    self.player.setPlaybackRate(4.0)
                    self.amount_time_2= QTimer(self)
                    self.amount_time_2.timeout.connect(self.playing_clock)
                    self.amount_time_2.start(250)

                self.player.durationChanged.connect(self.total_duration)

                self.player.play()


                self.player.mediaStatusChanged.connect(lambda status: self.stopped_playing() if status == QMediaPlayer.MediaStatus.EndOfMedia else None)
            
            else:
                #DON'T FORGET PARENTHESES! WITHOUT IT NOTHING WORKS!!!!!!!
                self.stopped_playing()
            
        else:

            return
    
    def back(self):
        self.player.setPosition(0)
        self.seconds=0
        self.minutes=0
        self.hours=0
        self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}/{self.hours_2:02d}:{self.minutes_2:02d}:{self.seconds_2:02d}')


        if not self.is_paused:
            self.player.play()
        
        else:
            return
    
    def pause(self):
        if not self.is_paused:
            self.player.pause()
            self.amount_time_2.timeout.disconnect(self.playing_clock)
            self.is_paused= True
            self.Pause_button.setText('▶')
            self.Pause_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #545454;
                    color: white;
                    border: 2px solid black;
                    border-radius: {self.radius}px;
                    font-size: 16px;
                    font-weight: bold;
                }} 
                QPushButton:hover {{
                    background-color: #808080
                }}""")
        
        else:
            self.player.play()
            self.is_paused= False
            self.slider_released()
            self.Pause_button.setText('| |')
            self.Pause_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #545454;
                    color: white;
                    border: 2px solid black;
                    font-size: 16px;
                    font-weight: bold;
                }} 
                QPushButton:hover {{
                    background-color: #808080
                }}""")


    def stopped_playing(self):
        self.record_circle_button.show()
        self.Back_to_beginning.hide()
        self.Pause_button.hide()
        self.time_speed.setEnabled(True)
        self.is_paused= False
        self.time.setText('00:00:00/00:00:00')
        self.total_duration(int(self.duration)*1000)
        self.amount_time_2.stop()
        self.seconds=0
        self.minutes=0
        self.hours=0
        self.seconds_2=0
        self.minutes_2=0
        self.hours_2=0


        self.Play_button.setText('▶')
        self.Play_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #545454;
                color: white;
                border: 2px solid black;
                border-radius: {self.radius}px;
                font-size: 16px;
                font-weight: bold;
            }} 
            QPushButton:hover {{
                background-color: #808080
            }}""")

        self.Pause_button.setText('| |')
        self.Pause_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #545454;
                color: white;
                border: 2px solid black;
                font-size: 16px;
                font-weight: bold;
            }} 
            QPushButton:hover {{
                background-color: #808080
            }}""")

        self.player.stop()


    def stopped_recording(self):
            self.Play_button.show()
            self.Back_to_beginning.show()
            self.time_speed.show()
            self.container_inner_bottom_main.show()
            self.container_record.hide()
            self.amount_time.stop()
            self.time.setText('00:00:00/00:00:00')
            self.time.setFont(QFont('Arial', 20))
            self.mics.setEnabled(True)
            self.seconds=0
            self.minutes=0
            self.hours=0
            self.record_circle_button.setText('○')
            self.record_circle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #FF0000;
                    color: white;
                    border: 2px solid black;
                    border-radius: {self.radius}px;
                    font-size: 16px;
                    font-weight: bold;
                }} 
                QPushButton:hover {{
                    background-color: #f22952
                }}""")

            #lets say that sound card (self.start_time) says it's inernal stop watch is 120 secs
            #then after a couple of minutes bam you stop it and get the current time 124 secs
            #Then duration gets the difference between the two and 
            #samples_recorded and audio variable splice it to get rid of the unnessary parts
            duration= sd.get_stream().time - self.start_time
            sd.stop()
            print('finished')

            samples_recorded= int(duration * self.sample_rate)
            audio= self.audio_data[:samples_recorded] # type: ignore
            
            # create audio files directory if it does not already exist
            self.audio_files_dir.mkdir(exist_ok=True)
            
            # increment count until you hit an output path that does not already exist
            # the walrus operator ':=' assigns 'output_path' to the new Path object each iteration
            while (output_path := self.audio_files_dir / f'recording{self.n}.mp3').exists():
                self.n += 1
            
            sf.write(output_path, audio, self.sample_rate)
            print('success!')

            self.n+=1

            self.Bar_list.clear()
            self.side_bar_files()




    def speed(self):
        #The problem was that when the button was clicked it would go to the next one and the next one ending me right where I started
        #So by doing elifs instead of a lot of ifs it made it check until one fits and after it stops checking
        if self.time_speed.text() == '1x':
            self.time_speed.setText('2x')
        
        elif self.time_speed.text() == '2x':
            self.time_speed.setText('3x')

        elif self.time_speed.text() == '3x':
            self.time_speed.setText('4x')

        elif self.time_speed.text() == '4x':
            self.time_speed.setText('1x')


    def clock(self):
        self.seconds+=1

        if self.seconds == 60:
            self.seconds= 0
            self.minutes+=1
        
        if self.minutes == 60:
            self.minutes=0
            self.hours+=1

        self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}')

        self.update_recording_label()


    def total_duration(self, duration):

        total_seconds= int(duration/1000)

        self.hours_2= total_seconds // 3600
        self.minutes_2= (total_seconds % 3600) // 60
        self.seconds_2= total_seconds % 60

        self.time.setText(f'00:00:00/{self.hours_2:02d}:{self.minutes_2:02d}:{self.seconds_2:02d}')


    def playing_clock(self):
        self.seconds+=1

        if self.seconds == 60:
            self.seconds= 0
            self.minutes+=1
        
        if self.minutes == 60:
            self.minutes=0
            self.hours+=1

        self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}/{self.hours_2:02d}:{self.minutes_2:02d}:{self.seconds_2:02d}')


    def side_bar_files(self):
        def sort_fname(fname):
            idx = -1
            if fname.startswith("recording"):
                suffix = fname.removeprefix("recording")
                if suffix.isdigit():
                    idx = int(suffix)
            return idx, fname.lower()

        path_list=sorted(
            (f.stem for f in self.audio_files_dir.glob("*.mp3")),
            key=sort_fname,
        )
        self.Bar_list.addItems(path_list)

        for i in range(self.Bar_list.count()):
            item= self.Bar_list.item(i)
            item.setSizeHint(QSize(0,120))
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)


    def find_mics(self):
        #The following if statment checks if the variable mics_dictionary.
        #If it doesn't exist than it creates the variable mics_dictionary
        #Otherwise it clears the dictionary.
        #This preserves the identity of the variable and is easier to compute
        if not hasattr(self, "mics_dictionary"):
            self.mics_dictionary= {}
        else:
            self.mics_dictionary.clear()
        wasapi = next((api for api in sd.query_hostapis() if "WASAPI" in api["name"]), None)
        if wasapi is None:
            return

        devices = sd.query_devices()
        # use 'devices' list of indices in wasapi dict
        for idx in wasapi["devices"]:
            dev = devices[idx]
            # skip if there are no input channels
            if dev["max_input_channels"] <= 0:
                continue
            self.mics_dictionary[dev["name"]] = idx


    def using_mic(self):
        microphone= self.mics.currentText()

        self.device_index= self.mics_dictionary.get(microphone, None)

        self.device_info= sd.query_devices(self.device_index)
        self.sample_rate= int(self.device_info['default_samplerate'])


    def open_folder(self):
        os.startfile(self.audio_files_dir)

    def delete_file(self):
        send2trash(os.path.join(self.audio_files_dir / f'{self.mp3_basename}.mp3'))
        self.Bar_list.clear()
        self.side_bar_files()


    def rename_file(self):
        class rename_box(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle('Rename')
                self.setFixedSize(QSize(150, 100))

                layout= QGridLayout()

                self.text= QLineEdit()
                self.text.setPlaceholderText('Rename')
                self.text.setStyleSheet('''
                    QLineEdit {
                        font: 20px;
                    }
''')

                ok= QPushButton('ok')
                ok.clicked.connect(self.accept)


                
                layout.addWidget(self.text, 1, 1)
                layout.addWidget(ok, 2, 1)
                self.setLayout(layout)


            def get_text(self):
                #This function return the text in self.text
                return self.text.text()


        box= rename_box()

        #the if statement runs the Qdailog box and then when ok is clicked it gets the text from the box using
        #The get_text function
        if box.exec() == QDialog.Accepted: # type: ignore
            self.new_name= box.get_text()

            if self.new_name == '' or r'<>:"/\|?*' in self.new_name:
                return
            
            else:
                old_path= self.audio_files_dir / f'{self.mp3_basename}.mp3'
                new_path= self.audio_files_dir / f'{self.new_name}.mp3'
                os.rename(str(old_path), str(new_path))
                self.Bar_list.clear()
                self.side_bar_files()


    def update_slider(self, position):
        if hasattr(self, 'current_position') and self.one_time:
            self.player.setPosition(self.current_position)
            self.slider.setValue(self.current_position)
            self.one_time=False
            self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}/{self.hours_2:02d}:{self.minutes_2:02d}:{self.seconds_2:02d}')
        #Self.slider.isSliderDown() checks if the slider is being held or dragged and returns a bool
        #So the if statment says that not holding the slider or dragged it updates the position
        if not self.slider.isSliderDown():
            self.slider.setValue(position)
            self.total_duration(int(self.duration)*1000)
            self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}/{self.hours_2:02d}:{self.minutes_2:02d}:{self.seconds_2:02d}')

    def slider_pressed(self):
        #If the slider is pressed it stops the audio
        self.player.positionChanged.disconnect(self.update_slider)
        self.amount_time_2.timeout.disconnect(self.playing_clock)
        self.slider.sliderMoved.connect(self.update_time)

    def slider_released(self):
        if self.is_paused:
            self.update_time()
            return


        self.update_time()
        #It makes it so the slider starts updating again and audio
        self.player.positionChanged.connect(self.update_slider)
        self.amount_time_2.timeout.connect(self.playing_clock)
        #This updates the player to the new position
        self.player.setPosition(self.slider.value())

    def update_time(self):
        self.total_duration(int(self.duration)*1000)
        value= int(self.slider.value()) // 1000

        total_seconds= value

        self.hours= total_seconds // 3600
        self.minutes= (total_seconds % 3600) // 60
        self.seconds= total_seconds % 60

        self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}/{self.hours_2:02d}:{self.minutes_2:02d}:{self.seconds_2:02d}')


    def update_slider_2(self, position):
        #Self.slider.isSliderDown() checks if the slider is being held or dragged and returns a bool
        #So the if statment says that not holding the slider or dragged it updates the position
        if not self.slider.isSliderDown():
            self.slider.setValue(position)

    def slider_pressed_2(self):
        #If the slider is pressed it stops the audio
        self.player.positionChanged.disconnect(self.update_slider_2)
        self.slider.sliderMoved.connect(self.update_time_2)

    def slider_released_2(self):
        self.update_time()
        #It makes it so the slider starts updating again and audio
        self.player.positionChanged.connect(self.update_slider_2)
        #This updates the player to the new position
        self.player.setPosition(self.slider.value())

    def update_time_2(self):
        self.total_duration(int(self.duration)*1000)
        value= int(self.slider.value()) // 1000

        total_seconds= value

        self.hours= total_seconds // 3600
        self.minutes= (total_seconds % 3600) // 60
        self.seconds= total_seconds % 60

        self.time.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}/{self.hours_2:02d}:{self.minutes_2:02d}:{self.seconds_2:02d}')


    def before_player(self):
        self.current_position= self.slider.value()

    def timestamp_buttons(self):
        #hasattr only works on attributes so you need self
        #You should only use hasattr on attributes not local variables
        if not hasattr(self, 'timestamp_container'):
            self.timestamp_container= QWidget()
            self.timestamp_container.setStyleSheet("background-color: Transparent; border-radius: 5px;")
            self.audio_place.addWidget(self.timestamp_container, stretch=2)
            self.timestamps= QHBoxLayout(self.timestamp_container)

        else:
            pass


        if hasattr(self, 'twenty'):
            self.twenty.deleteLater()
            self.fourty.deleteLater()
            self.fifty.deleteLater()
            self.sixety.deleteLater()
            self.eighty.deleteLater()
    
        twenty_text= f'{self.duration * .20:.2f}'

        if float(twenty_text) >= 60:
            twenty_minutes= float(twenty_text) // 60

            twenty_seconds= float(twenty_text) % 60

            twenty_text= f'{int(twenty_minutes)}:{twenty_seconds:.2f}'

        else:
            twenty_text= f'00:{twenty_text}'


        fourty_text= f'{self.duration * .40:.2f}'

        if float(fourty_text) >= 60:
            fourty_minutes= float(fourty_text) // 60

            fourty_seconds= float(fourty_text) % 60

            fourty_text= f'{int(fourty_minutes)}:{fourty_seconds:.2f}'

        else:
            fourty_text= f'00:{fourty_text}'


        fifty_text= f'{self.duration * .50:.2f}'

        if float(fifty_text) >= 60:
            fifty_minutes= float(fifty_text) // 60

            fifty_seconds= float(fifty_text) % 60

            fifty_text= f'{int(fifty_minutes)}:{fifty_seconds:.2f}'

        else:
            fifty_text= f'00:{fifty_text}'


        sixety_text= f'{self.duration * .60:.2f}'

        if float(sixety_text) >= 60:
            sixety_minutes= float(sixety_text) // 60

            sixety_seconds= float(sixety_text) % 60

            sixety_text= f'{int(sixety_minutes)}:{sixety_seconds:.2f}'

        else:
            sixety_text= f'00:{sixety_text}'


        eighty_text= f'{self.duration * .80:.2f}'

        if float(eighty_text) >= 60:
            eighty_minutes= float(eighty_text) // 60

            eighty_seconds= float(eighty_text) % 60

            eighty_text= f'{int(eighty_minutes)}:{eighty_seconds:.2f}'

        else:
            eighty_text= f'00:{eighty_text}'

        self.twenty= QPushButton()
        #You use d for ints and f for floats 
        self.twenty.setText(twenty_text)
        self.twenty.setStyleSheet('''
            QPushButton {
                border: 2px solid #FFFFFF;
                max-width: 60px;
            }
''')

        self.fourty= QPushButton()
        #You use d for ints and f for floats 
        self.fourty.setText(fourty_text)
        self.fourty.setStyleSheet('''
            QPushButton {
                border: 2px solid #FFFFFF;
                max-width: 60px;
            }
''')

        self.fifty= QPushButton()
        #You use d for ints and f for floats 
        self.fifty.setText(fifty_text)
        self.fifty.setStyleSheet('''
            QPushButton {
                border: 2px solid #FFFFFF;
                max-width: 60px;
            }
''')


        self.sixety= QPushButton()
        #You use d for ints and f for floats 
        self.sixety.setText(sixety_text)
        self.sixety.setStyleSheet('''
            QPushButton {
                border: 2px solid #FFFFFF;
                max-width: 60px;
            }
''')


        self.eighty= QPushButton()
        #You use d for ints and f for floats 
        self.eighty.setText(eighty_text)
        self.eighty.setStyleSheet('''
            QPushButton {
                border: 2px solid #FFFFFF;
                max-width: 60px;
            }
''')
        
        self.twenty.clicked.connect(lambda: self.timestamp_function(self.twenty))
        self.fourty.clicked.connect(lambda: self.timestamp_function(self.fourty))
        self.fifty.clicked.connect(lambda: self.timestamp_function(self.fifty))
        self.sixety.clicked.connect(lambda: self.timestamp_function(self.sixety))
        self.eighty.clicked.connect(lambda: self.timestamp_function(self.eighty))



        self.timestamps.addWidget(self.twenty)
        self.timestamps.addWidget(self.fourty)
        self.timestamps.addWidget(self.fifty)
        self.timestamps.addWidget(self.sixety)
        self.timestamps.addWidget(self.eighty)


    def timestamp_function(self, button):
        if button == self.twenty:
            self.new_value= self.duration * 200

        if button == self.fourty:
            self.new_value= self.duration * 400

        if button == self.fifty:
            self.new_value= self.duration * 500

        if button == self.sixety:
            self.new_value= self.duration * 600

        if button == self.eighty:
            self.new_value= self.duration * 800 

        self.slider.setSliderPosition(self.new_value)
        self.slider_released_2()
        self.before_player()


    def recording_label(self):
        if hasattr(self, 'spacer'):
            self.record_place.removeItem(self.spacer)

        if self.is_showing:
            self.spacer= QSpacerItem(95, 20)
            self.record_place.addWidget(self.recording)
            self.record_place.addItem(self.spacer)

        else:
            self.record_place.addWidget(self.recording)


    def update_recording_label(self):
        if self.recording.text() == 'Recording':
            self.recording.setText('Recording.')

        elif self.recording.text() == 'Recording.':
            self.recording.setText('Recording..')

        elif self.recording.text() == 'Recording..':
            self.recording.setText('Recording...')

        elif self.recording.text() == 'Recording...':
            self.recording.setText('Recording')
        

if __name__ == "__main__":
    main()