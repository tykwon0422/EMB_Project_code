from Pyrebase_STT import STT

model = STT()
list = model.run()

if len(list) == 0:
    exit()

for i in list:
    print(i)
