from tkinter import *

root = Tk()

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

print("{} x {}".format(monitor_width, monitor_height))
