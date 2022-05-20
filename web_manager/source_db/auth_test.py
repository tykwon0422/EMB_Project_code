import pyrebase
from time import sleep
import sqlite3

firebaseConfig = {
    #use your firebaseconfig
}


firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

# 한 계정에 여러번 연결 가능
# login
# email=input("Enter your email")
# password=input("Enter your password")
#
# try:
#     auth.sign_in_with_email_and_password(email, password)
#     print("Successfully signed in!")
#     while True:
#         sleep(1)
# except:
#     print("Invalid user or password. Try again")

# sign up
# email = input("Enter your email")
# password = input("Enter your password")
# confirm_pass = input("Confirm Password")
# if password == confirm_pass:
#     try:
#         auth.create_user_with_email_and_password(email, password)
#         print("Success!")
#     except:
#         print("Error")

db = firebase.database()


floors = db.get()
# for floor in floors.each():
#     print("{}, {}".format(floor.key(), type(floor.key())))
# db.child(0).remove()
# floor = db.get()
# print(floors.val())
floors_data = []
i = 0
for floor in floors.each():
    if floor.key() == 0:
        continue

    floor_data = []
    # print(format(floor.key()))
    rooms = db.child(floor.key()).get()
    for room in rooms.each():
        room_data = []
        # print('호실: {}'.format(room.key()), end=' ')
        room_data.append(room.key())
        try:
            room_data.append(room.val()['name'])
            # print('이름: {}'.format(room.val()['name']), end=' ')
        except:
            try:
                room_data.append(room.val()['이름'])
                # print('이름: {}'.format(room.val()['이름']), end=' ')
            except:
                room_data.append('없음')
                # print('이름: 미정', end=' ')

        try:
            room_data.append(room.val()['담당자'])
            # print('담당자: {}'.format(room.val()['담당자']), end=' ')
        except:
            room_data.append('없음')
            # print('담당자: 없음', end=' ')

        try:
            room_data.append(room.val()['담당자 번호'])
            # print('담당자: {}'.format(room.val()['담당자 번호']))
        except:
            room_data.append('없음')
            # print('담당자 번호: 없음')

        floor_data.append(room_data)
    floors_data.append(floor_data)

print(floors_data)
# for data_list in floors_data:
#     print(data_list)
#
# conn = sqlite3.connect("./test.db")
#
#
# with conn:
#     sql = "INSERT INTO rooms (room_number, room_name, charge, phone) VALUES (?,?,?,?)"
#     cur = conn.cursor()
#     for floor_data in floors_data:
#         f_data = []
#         for data in floor_data:
#             item = (data[0], data[1], data[2], data[3])
#             f_data.append(item)
#         print(f_data)
#         cur.executemany(sql, f_data)
#
#     conn.commit()


# for floor in floors.each():
#   rooms = db.child(floor.key()).get()
#   for room in rooms.each():
#     if '강의실' in room.val()['이름']:
#       print(room.val())