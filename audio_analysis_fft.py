import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy import signal
import time
import pyaudio
import wave

def give_me_mags(f = None, tim = 10, file = None):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = tim
    if f == None:
        dec = input("Are you going to record(r) or using a file(f)?")
    elif f == 'voice_pass':
        dec = 'r'
    else:
        dec = 'f'
    if dec == 'r':
        name = str(input("Enter name of participant:"))
        WAVE_OUTPUT_FILENAME = name + '.wav'

        p = pyaudio.PyAudio()

        time.sleep(3)

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


        fs,data = wavfile.read(WAVE_OUTPUT_FILENAME)

    else:
        if f == None:
            recording = input("Enter name of file you want to use:")

        else:
           recording = file
        try:
            fs, data = wavfile.read(recording)
        except:
            recording = input('Enter name again: ')
            fs, data = wavfile.read(recording)


    channel_1 = data[:]
    if f == 'voice_pass':
        no_of_elements = 10000
    else:
        no_of_elements = 10000000
    fourier = np.fft.rfft(channel_1,no_of_elements)
    t = 1/44100
    freq = np.fft.rfftfreq(100,d = t)
    mag = np.abs(fourier)
    ##normalizing the magnitudes by dividing each mag by the maximum magnitude
    # max = np.nanmax(mag)
    # print("Dominant frequency is %d which is the %d harmonic"%(x,i))
    # plt.figure(1)
    # plt.stem(freq,mag/max , width = 1.5)
    # plt.xlabel('Freq(Hz)')
    # plt.ylabel('mag')
    # plt.show()


    return [fourier,mag,freq]
#
