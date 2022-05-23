from cgitb import text
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

import db_code

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
    signal_next = pyqtSignal(int)
    signal_up = pyqtSignal(int)
    signal_down = pyqtSignal(int)
    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent
        self.row = 0

    def run(self, page):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([12,16,18], GPIO.IN)
        if page == 3:
            try:
                GPIO.add_event_detect(12, GPIO.RISING, callback=self.test, bouncetime=800)
            except:
                GPIO.cleanup()
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup([12,16,18], GPIO.IN)
                GPIO.add_event_detect(12, GPIO.RISING, callback=self.test, bouncetime=800)
                GPIO.add_event_detect(16, GPIO.RISING, callback=self.up, bouncetime=800)
                GPIO.add_event_detect(18, GPIO.RISING, callback=self.down, bouncetime=800)
        
        else:
            try:
                GPIO.add_event_detect(12, GPIO.RISING, callback=self.test, bouncetime=800)
            except:
                GPIO.cleanup()
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup([12,16,18], GPIO.IN)
                GPIO.add_event_detect(12, GPIO.RISING, callback=self.test, bouncetime=800)


    def test(self,a):
        self.signal_next.emit(self.row)

    def up(self, a):
        self.row += 1
        self.signal_up.emit(self.row)
    
    def down(self, a):
        self.row -= 1
        self.signal_down.emit(self.row)
    
    def stop(self):
        self.quit()
        self.wait(1000)

class Thread_mic(QThread):
    signal_ready = pyqtSignal(bool)
    signal_retry = pyqtSignal(bool)
    signal_next = pyqtSignal(str)
    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent
        self.r = sr.Recognizer()

    def run(self):
        while True:
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)

                self.signal_ready.emit(True)
                try:
                    audio = self.r.listen(source, timeout = 5)
                except:
                    self.signal_retry.emit(True)
                    sleep(3)
                    continue
            try:
                text = r.recognize_google(audio, language='ko')
                break
            except:
                self.signal_retry.emit(True)
                sleep(3)
                continue

        self.signal_next.emit(text)
    
    def stop(self):
        self.quit()
        self.wait(1000)

class Thread_sql(QThread):
    signal_check = pyqtSignal(list)
    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent
        self.sql_db = db_code.sql()
        self.fb_db = db_code.database()
        
    def update(self):
        self.sql_db.clear()
        rooms = self.fb_db.read_data()
        for room in rooms:
            data = (room["number"], room["name"], room["charge"], room["phone"])
            self.sql_db.insert_rooms(data)
    
    def check(self, text):
        ret = []
        rows = self.sql_db.search()
        for row in rows:
            score = max(SequenceMatcher(None, row[1], input).ratio(), 
                    SequenceMatcher(None, row[1], input + "연구실").ratio())
            if score > 0.6 or row[0] in text or row[2] in text or text in row[1]:
                ret.append(row)
        return ret

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
        self.push.threadAction()
        self.deleteLater()

class listening_window(QMainWindow, form_listening_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.mic_listening = mic_listening()

    def threadAction(self):
        self.stt = Thread_mic(self) 
        self.sql = Thread_sql(self)
        self.stt.start()
        self.sql.start()
        self.stt.signal_ready.connect(self.ready_to_listening)
        self.stt.signal_next.connect(self.start_to_search)
        self.stt.signal_retry.connect(self.listen_failed)
        self.sql.signal_check.connect(self.btn_listening_to_search)

    def ready_to_listening(self):
        self.mic_listening.show()

    def listen_failed(self):
        self.mic_listening.close()
        # 인식 실패 문구 출력
        sleep(3)
    
    def start_to_search(self, text):
        self.stt.stop()
        self.sql.check(text)

    def btn_listening_to_search(self, data):
        self.mic_listening.close()
        self.done = done_window(data)
        self.sql.stop()
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

    def btn_done_to_map(self, idx):
        self.x.stop()
        obj = self.room_list_file[idx]
        num = obj[0]
        self.start = map_window(num, obj)
        self.start.show()
        self.start.threadAction()
        self.deleteLater()

class map_window(QMainWindow, form_map_class):
    def __init__(self, num, obj):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        url = db_code.storage.get_url(num)
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