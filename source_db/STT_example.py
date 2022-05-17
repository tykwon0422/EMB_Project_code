from Pyrebase_STT import STT

model = STT()
list = model.run()

for i in list:
    print(i)