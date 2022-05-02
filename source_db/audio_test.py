import pyaudio
import numpy as np

CHUNK = 2**10
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=2)