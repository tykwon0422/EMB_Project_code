import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyDGIQoNHBmyjdiS3YLU_kFoGgyXzVcoM3k",
  'authDomain': "proj2022-3cd0d.firebaseapp.com",
  'databaseURL': "https://proj2022-3cd0d-default-rtdb.firebaseio.com",
  'projectId': "proj2022-3cd0d",
  'storageBucket': "proj2022-3cd0d.appspot.com",
  'messagingSenderId': "752819259660",
  'appId': "1:752819259660:web:dc7e0da1d53f6e7043e129",
  'measurementId': "G-3FSHGHRZ54"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()


#login
# email=input("Enter your email")
# password=input("Enter your password")
#
# try:
#     auth.sign_in_with_email_and_password(email, password)
#     print("Successfully signed in!")
# except:
#     print("Invalid user or password. Try again")

#sign up
# email = input("Enter your email")
# password = input("Enter your password")
# confirm_pass = input("Confirm Password")
# if password == confirm_pass:
#     try:
#         auth.create_user_with_email_and_password(email, password)
#         print("Success!")
#     except:
#         print("Error")


