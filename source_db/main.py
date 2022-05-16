import pyrebase
import sqlite3

import datetime

from enum import auto
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

firebaseConfig = {
    'apiKey': "AIzaSyDGIQoNHBmyjdiS3YLU_kFoGgyXzVcoM3k",
    'authDomain': "proj2022-3cd0d.firebaseapp.com",
    'databaseURL': "https://proj2022-3cd0d-default-rtdb.firebaseio.com",
    'projectId': "proj2022-3cd0d",
    'storageBucket': "proj2022-3cd0d.appspot.com",
    'messagingSenderId': "752819259660",
    'appId': "1:752819259660:web:dc7e0da1d53f6e7043e129",
    "measurementId": "G-3FSHGHRZ54"
}

firebase = pyrebase.initialize_app(firebaseConfig)


class authorization:
    def __init__(self):
        self.auth = firebase.auth()


class storage:
    def __init__(self):
        self.stor = firebase.storage()

    def upload(self, file_name, cloud_file_name, path=None):
        if path:
            self.stor.child(path).child(cloud_file_name).put(file_name)
        else:
            self.stor.child(cloud_file_name).put(file_name)

    def download_file(self, path, filename):
        download_name = 'download.jpg'
        self.stor.child(path + filename).download("", download_name)


class database:
    def __init__(self):
        self.db = firebase.database()

    def push(self, path, data):
        self.db.child(path).push(data)

    def set(self, path, data):
        self.db.child(path).set(data)

    def update(self, path, data):
        self.db.child(path).update(data)

    def delete(self, path, key):
        self.db.child(path).child(key).remove()

    def read_key(self, path=None):
        if path:
            datas = self.db.child(path).get()
        else:
            datas = self.db.get()
        ret = []
        for data in datas.each():
            ret.append(data.key())
        return ret

    def read_data(self, path=None, keyword=None):
        if keyword:
            if path:
                datas = self.db.child(path).order_by_child(keyword).get()
            else:
                datas = self.db.order_by_child(keyword).get()
        else:
            if path:
                datas = self.db.child(path).get()
            else:
                datas = self.db.get()

        ret = []
        for data in datas.each():
            ret.append(data.val())
        return ret


class sql:
    def __init__(self):
        self.conn = sqlite3.connect('./database.db')
        cur = self.conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS rooms(room_number, room_name, charge, phone)"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS latest(room_number, root, qr, time)"
        cur.execute(sql)

    # sql is string, data is tuple


    def execute(self, sql, data=None):
        with self.conn:
            cur = self.conn.cursor()
            if data:
                try:
                    cur.executemany(sql, data)
                except:
                    return -1
            else:
                try:
                    cur.execute(sql)
                except:
                    return -1

            self.conn.commit()
            return 1

        # data is tuple.


    def insert_rooms(self, data):
        sql = "INSERT INTO  rooms (room_number, room_name, charge, phone) VALUES (?, ?, ?, ?)"
        return self.execute(sql, data)

        # data is tuple.


    def insert_latest(self, data):
        sql = "INSERT INTO latest (room_number, root, qr) VALUES (?, ?, ?)"
        return self.execute(sql, data)

        # text is string.


    def search(self, text):
        default = "SELECT * FROM rooms"
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * from rooms where id=? or name=?", (text, text))
            rows = cur.fetchall()

        return rows

        # rooms and data are list.


    def update_changes(self, rooms, data):
        update_sql = []
        cur = self.conn.cursor()
        for i in range(len(rooms)):
            room = rooms[i]
            key_chain = data[i].keys()
            for key in key_chain:
                sql = "UPDATE rooms SET {} = ? WHERE room_number = {}".format(key, data[i][key], room)
                if self.execute(sql) == -1:
                    print("Update failed. point is {}.".format(key))
                    return -1


formClass = uic.loadUiType("../UI/main.ui")[0]


class Ui(QMainWindow, formClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dataList = []
        self.column = 4

    def home(self):
        self.stackedWidget.setCurrentWidget(self.page_home)

    def change_window(self, p_num):
        page_num = 'page' + p_num
        self.stackedWidget.setCurrentWidget(self.page_num)

    def updateList(self, data):
        rows = len(data)
        for row in range(rows):
            for col in range(self.column):
                self.tableWidget.setItem(row, col, QTableWidgetItem(data[row][col]))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    currentUi = Ui()
    currentUi.show()
    sys.exit(app.exec_())