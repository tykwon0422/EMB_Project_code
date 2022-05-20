import pyrebase
import urllib

firebaseConfig = {
    #use your firebaseconfig
}


firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()

# login
# email=input("Enter your email")
# password=input("Enter your password")
#
# try:
#     auth.sign_in_with_email_and_password(email, password)
#     print("Successfully signed in!")
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

# storage
# upload

# print(storage.child(cloudfilename).get_url(None))

# download
# cloudfilename=input('cloudfilename')
# storage.child(cloudfilename).download("","download_text.txt")

# read fileim
# cloudfilename=input('cloudfilename')
# url=storage.child(cloudfilename).get_url(None)
# f=urllib.request.urlopen(url).read()
# print(f)

# database
# data = {'age': 32, 'address': 'New york', 'employed': True, 'name': 'John smith'}

# push function makes a unique key.
# db.child('test').push(data)

# set function delete data and write another data into key('test')
# db.child('test').set(data)

# update function update data when key is already in path. if key isn't, make path and upload data
# db.child('test').child('new_root').update({'new_key':'anothor_data'})

# floors = db.get()
# for floor in floors.each():
#   rooms = db.child(floor.key()).get()
#   for room in rooms.each():
#     if '강의실' in room.val()['이름']:
#       print(room.val())

# delete
# db.child('test').child('new_root').child('new_key').remove()

# read
floors = db.get()
for floor in floors.each():
    if floor.key() == 0:
        continue
    rooms = db.child(floor.key()).order_by_child("name").get()
    for room in rooms.each():
        print(room.key(), room.val()["name"])
