from firebase import Firebase

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

firebase = Firebase(firebaseConfig)

db = firebase.database()
storage = firebase.storage()

# data = {"name": "Joe"}
# db.child("users").push(data)
# data = {"name": "Moon", "age": 24}
# db.child("users").child("user02").set(data)

name = 'Kim'
#
users = db.child("users").get()
for user in users.each():
    if user.val()['name'] == name:
        print(user.val())

# storage.child("test.jpg").put("123456.jpg")
# url = storage.child("test.jpg").get_url(None)
# print(url)
# key = "305"
# storage.child("room/"+key+"/map.jpg").put("123456.jpg")
# url = storage.child("room/"+key+"/map.jpg").get_url(None)
#
# data = {
#     "name": "holy!",
#     "Phone": '010-1234-5678',
#     "Photo": url
# }
# db.child("rooms").child(key).update(data)
