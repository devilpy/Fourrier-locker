import audio_analysis_fft as aud_an
import numpy as np
import math
from scipy.io import wavfile
import fourier_pass_unlocker as unlocker

user = input('Enter your username or email: ')
acc = input('What is the name of the account your password is associated with?:')
password = input('Enter your password: ')
n = len(password)
f_m = aud_an.give_me_mags()
mag = f_m[1]
freq = f_m[2]
fourier = f_m[0]
sorted_f = sorted(mag)
maxs = []
m = -1
for k in range(n):
    index = np.where(mag == sorted_f[m])
    maxs.append(index[0][0])
    m += -1
print('prepare to deliver voice code:...')
key = aud_an.give_me_mags('voice_pass', tim = 5)
maxess = []
j = -1
for k in range(5):
    index = np.where(key[1] == sorted(key[1])[j])
    maxess.append(index[0][0])
    j += -1
print(maxess)
#
# ----------------------------------------------------------
# Fisher_yates shuffle
def yates(a,b):
    for ind in b:
        if ind >= len(a):
            x = ind%len(a)
            a.append(a[x])
        else:
            x = ind
            a.append(a[x])
        for i in range(x,len(a)-1):
            a[i] = a[i+1]
        a.pop()
        # print(a)
    return a


#-------------------------------------------------------------------------

#applying the ascii values of characters of passwords in to the fourier elements of indexes in alpha
#all ascii values for possible password characters are within the range of 65 ~ 150, can be easily represented
#as phase angles in degrees!
ascii_password = []
for char in password:
    ascii_password.append(ord(char))

alpha_pass = yates(ascii_password, maxess)


#altering the phase values of fourier elements with indexes in alpha
for max in range(n):
    indice = maxs[max]
    fourier[indice] = mag[indice]*complex(math.cos(math.radians(alpha_pass[max])), math.sin(math.radians(alpha_pass[max])))
    print(np.angle(fourier[indice]))

# creating the modified audio file
data = np.fft.irfft(fourier)
name_of_newaud = input('Enter the name of the audio file: ')
name = name_of_newaud + '.wav'
print(name)
wavfile.write(name, 44100, data)



