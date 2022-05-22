from dataclasses import dataclass
import os
import sys
import time
from xmlrpc.client import boolean
from Pyrebase_STT import STT
import urllib.request

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import speech_recognition as sr
from difflib import SequenceMatcher

import background_rc
import description_rc
import mic_rc
import button_rc
import select_rc

import RPi.GPIO as GPIO

from time import sleep

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form_wait = resource_path('navi_mirror_wait.ui')
form_wait_class = uic.loadUiType(form_wait)[0]

form_start = resource_path('navi_mirror_start.ui')
form_start_class = uic.loadUiType(form_start)[0]

form_listening = resource_path('navi_mirror_listening.ui')
form_listening_class = uic.loadUiType(form_listening)[0]

form_mic_listening = resource_path('mic_listening.ui')
form_mic_listening_class = uic.loadUiType(form_mic_listening)[0]

form_search = resource_path('navi_mirror_search.ui')
form_search_class = uic.loadUiType(form_search)[0]

form_mic_search = resource_path('mic_search.ui')
form_mic_search_class = uic.loadUiType(form_mic_search)[0]

form_done = resource_path('navi_mirror_done.ui')
form_done_class = uic.loadUiType(form_done)[0]

form_map = resource_path('navi_mirror_map.ui')
form_map_class = uic.loadUiType(form_map)[0]

class Thread_btn(QThread):
    signal_next = pyqtSignal(bool)
    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def run(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([12,16,18], GPIO.IN)
        try:
            GPIO.add_event_detect(12, GPIO.RISING, callback=self.test, bouncetime=800)
        except:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup([12,16,18], GPIO.IN)
            GPIO.add_event_detect(12, GPIO.RISING, callback=self.test, bouncetime=800)

    def test(self,a):
        self.signal_next.emit(True)
    
    def stop(self):
        self.quit()
        self.wait(1000)

class Thread_mic(QThread):
    signal_next = pyqtSignal(list)
    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def run(self):
        search = STT()
        lst = search.run()
        self.signal_next.emit(lst)
    
    def stop(self):
        self.quit()
        self.wait(1000)

class wait_window(QMainWindow, form_wait_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
    def threadAction(self):
        self.x = Thread_btn(self) 
        self.x.start()
        self.x.signal_next.connect(self.btn_wait_to_start)

    def btn_wait_to_start(self):
        self.x.stop()
        self.push = start_window()
        self.push.show()
        self.push.threadAction()
        self.deleteLater()
        
class start_window(QMainWindow, form_start_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
    def threadAction(self):
        self.x = Thread_btn(self) 
        self.x.start()
        self.x.signal_next.connect(self.btn_start_to_push)

    def btn_start_to_push(self):
        self.x.stop()
        self.push = listening_window()
        self.push.show()
        self.push.mic_listening.show()
        self.push.threadAction()
        self.deleteLater()

class listening_window(QMainWindow, form_listening_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.mic_listening = mic_listening()

    def threadAction(self):
        self.x = Thread_mic(self) 
        self.x.start()
        self.x.signal_next.connect(self.btn_listening_to_search)

    def btn_listening_to_search(self, data):
        self.x.stop()
        self.mic_listening.close()
        self.done = done_window(data)
        self.done.show()
        self.done.threadAction()
        self.deleteLater()

class mic_listening(QWidget, form_mic_listening_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(464, 1296)

        self.movie = QMovie('mic_listening.gif', QtCore.QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)

        self.mic_listening_gif.setMovie(self.movie)
        self.movie.start()

class done_window(QMainWindow, form_done_class):
    def __init__(self, data):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.room_list_file = data
        self.room_list.setRowCount(len(self.room_list_file))

        for row in range(len(self.room_list_file)):
            for column in range(len(self.room_list_file[row])):
                self.room_list.setItem(row, column, QTableWidgetItem(self.room_list_file[row][column]))

    def threadAction(self):
        self.x = Thread_btn(self) 
        self.x.start()
        self.x.signal_next.connect(self.btn_done_to_map)

    def btn_done_to_map(self):
        self.x.stop()
        self.start = map_window()
        self.start.show()
        self.start.threadAction()
        self.deleteLater()

class map_window(QMainWindow, form_map_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        url = "http://cafefiles.naver.net/data21/2006/12/6/291/12801024-1-badpark.jpg"
        map_url = urllib.request.urlopen(url).read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(map_url)
        self.map.setPixmap(pixmap)

    def threadAction(self):
        self.x = Thread_btn(self) 
        self.x.start()
        self.x.signal_next.connect(self.btn_map_to_start)

    def btn_map_to_start(self):
        self.x.stop()
        self.start = start_window()
        self.start.show()
        self.start.threadAction()
        self.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = wait_window()
    myWindow.threadAction()
    myWindow.show()
    app.exec_()