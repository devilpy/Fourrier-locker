import audio_analysis_fft as aud_an
import numpy as np
import math

#decrypt yates (going backwards!)

def un_yates(a,b):
    b.reverse()
    for ind in b:
        c = a[-1]
        if ind >= len(a):
            x = ind%len(a)
        else:
            x = ind
        for i in range(len(a) - 2 , x-1, -1):
            a[i+1] = a[i]
        a[x] = c
    return a
#--------------------------------------------
def unlock_pass(audio, n, yates_indexes):
    four_specs = aud_an.give_me_mags(f = 'audio', file = audio)
    mag = four_specs[1]
    fourier = four_specs[0]
    sorted_f = sorted(mag)
    maxs = []
    m = -1
    for k in range(n):
        index = np.where(mag == sorted_f[m])
        maxs.append(index[0][0])
        m += -1
    pass_chars = []
    for item in maxs:
        angle_rad = np.angle(fourier[item])
        print(angle_rad)
        angle_deg = math.degrees(angle_rad)
        print(angle_deg)
        deg_char = chr(round(angle_deg))
        pass_chars.append(deg_char)

    pass_list = un_yates(pass_chars, yates_indexes)
    password = ''
    for letter in pass_list:
        password = password + letter

    return password

# ----------------------------------------------------------------
#
# creating the modified audio file
# data = np.fft.irfft(fourier)
# name_of_newaud = input('Enter the name of the audio file: ')
# name = name_of_newaud + '.wav'
# print(name)
# wavfile.write(name, 44100, data)
#
# #testing unlocking live...
#
# password = unlock_pass(name, n , maxess)
# print(password)
