import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from scipy.io import wavfile
import math
import yates_unyates as yts
import time
import pyaudio
import wave
from tkinter import filedialog

class Fourier_pass_locker(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

    #need to make maxs, username, password, maxess available to all pages.

        self.shared_data = {}

        tk.Tk.wm_geometry(self, newGeometry = '500x200')
        tk.Tk.wm_title(self, 'Welcome to Fourier Pass Locker!')
        # tk.Tk.iconbitmap(self, default = 'devilpy_logo.ico')
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (WelcomePage,StartPage, Form_Page, Form_Page2, Rec_or_Audiofile, Rec_page, Aud_page, Process_Page, RegistrationPage, Sign_in_page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0 , column = 0 , sticky = 'nsew')

        self.show_frame(WelcomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        tk.Frame.configure(self, bg = '#b6e7f9')

        label = tk.Label(self, text='Welcome to Fourier_Pass_Locker', bg = '#b6e7f9')
        label.grid(column = 1 , row = 0)

        btn1 = tk.Button(self, text='New Member', command=lambda: controller.show_frame(RegistrationPage))
        btn1.grid(column=1, row=2)

        label2 = tk.Label(self, text='ALREADY A MEMBER?', bg = '#b6e7f9')
        label2.grid(column=1, row=4)

        btn2 = tk.Button(self, text='Sign In!', command=lambda: controller.show_frame(Sign_in_page))
        btn2.grid(column= 1, row=5)



class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):

        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg = '#b6e7f9')

        lbl1 = tk.Label(self, text='username')
        lbl1.grid(column=0, row=1)
        self.txt1 = tk.Entry(self, width=10)
        self.txt1.grid(column=1, row=1)


        lbl2 = tk.Label(self, text='If you are ready, please prepare to deliver voice sample!')
        lbl2.grid(column=0, row=2)

        btn1 = tk.Button(self, text='Record Voice Password for Locker', command=lambda: self.register_user(parent, controller))
        btn1.grid(column=1, row=2)

    def register_user(self, parent, controller):
        text = self.txt1.get()
        shit = Rec_page(parent, controller)
        key = shit.audio_analysis('voice', tim = 5)
        maxess = []
        j = -1
        for k in range(5):
            index = np.where(key[1] == sorted(key[1])[j])
            maxess.append(index[0][0])
            j += -1
        print(maxess)
        membersFile = open('members.txt', 'a')
        membersFile.write(text + ':' + str(maxess) + '\n')
        membersFile.close()
        self.controller.shared_data['maxess'] = maxess
        controller.show_frame(StartPage)

class Sign_in_page(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        lbl1 = tk.Label(self, text='username')
        lbl1.grid(column=0, row=1)
        self.txt1 = tk.Entry(self, width=10)
        self.txt1.grid(column=1, row=1)

        btn1 = tk.Button(self, text='Record Voice Password for Locker',
                         command=lambda: self.signme_in(parent, controller))
        btn1.grid(column=1, row=2)

    def signme_in(self, parent, controller):
        shit = Rec_page(parent, controller)
        key = shit.audio_analysis('voice', tim=5)
        maxess = []
        j = -1
        for k in range(5):
            index = np.where(key[1] == sorted(key[1])[j])
            maxess.append(index[0][0])
            j += -1
        self.controller.shared_data['maxess'] = maxess
        membersFile = open('members.txt', 'r')
        users_and_passwords = membersFile.readlines()
        membersFile.close()
        print(users_and_passwords)
        user_pass_info = {}
        for element in users_and_passwords:
            usp = element.split('\n')
            us_and_p = usp[0].split(':')
            user_pass_info[us_and_p[0]] = us_and_p[1]
        print(user_pass_info)
        if self.txt1.get() in user_pass_info.keys() and self.controller.shared_data['maxess'] == user_pass_info[self.txt1.get()] :
            controller.show_frame(StartPage)
        elif self.txt1.get() in user_pass_info.keys() and self.controller.shared_data['maxess'] != user_pass_info[self.txt1.get()] :
            tk.messagebox.showinfo('Could not SignIN!', 'Incorrect Vocie Password')
        else:
            tk.messagebox.showinfo('Could not SignIn!', 'User not registered!')

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        btn1 = tk.Button(self, text='Generate password audio', command = lambda: controller.show_frame(Form_Page))
        btn1.grid(column=0, row=1)

        btn2 = tk.Button(self, text='Retrieve password from audio', command = lambda: controller.show_frame(Form_Page2))
        btn2.grid(column=1, row=1)


class Form_Page(tk.Frame):
    def __init__(self, parent, controller):

        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        label = tk.Label(self, text = 'Enter Details')
        label.grid(column = 2, row = 0)

        lbl1 = tk.Label(self, text = 'username')
        lbl1.grid(column = 0, row = 1)
        txt1 = tk.Entry(self, width = 10)
        txt1.grid(column = 1, row = 1)

        lbl2 = tk.Label(self, text = 'account associated')
        lbl2.grid(column = 0, row = 2)
        txt2 = tk.Entry(self, width=10)
        txt2.grid(column=1, row=2)

        lbl3 = tk.Label(self, text='password')
        lbl3.grid(column=0, row=3)
        txt3 = tk.Entry(self, width=10)
        txt3.grid(column=1, row=3)

        btn_home = ttk.Button(self, text = 'Home', command = lambda: controller.show_frame(StartPage))
        btn_home.grid(column = 3, row = 2)

        def click_submit():
            entries = []
            entries.append(txt1.get())
            entries.append(txt2.get())
            entries.append(txt3.get())
            self.controller.shared_data['entries'] = entries
            # print(self.controller.shared_data['entries'])
            controller.show_frame(Rec_or_Audiofile)
            # print(Fourier_pass_locker.shared_data)

        btn_submit = tk.Button(self, text='Submit', command=lambda: click_submit())
        btn_submit.grid(column=2, row=2)



class Form_Page2(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        # label = tk.Label(self, text = 'Enter Details')
        # label.pack(pady = 10, padx = 10)

        lbl1 = tk.Label(self, text = 'Audio file')
        lbl1.grid(column = 0, row = 0)
        txt1 = tk.Entry(self, width = 10)
        txt1.grid(column = 1, row = 0)

        lbl2 = tk.Label(self, text = 'account associated')
        lbl2.grid(column = 0, row = 1)
        txt2 = tk.Entry(self, width=10)
        txt2.grid(column=1, row=1)

        btn_home = ttk.Button(self, text = 'Home', command = lambda: controller.show_frame(StartPage))
        btn_home.grid(column = 3, row = 1)

        btn_home = ttk.Button(self, text = 'Next')
        btn_home.grid(column = 0, row = 3)

        btn_home = ttk.Button(self, text = 'Create', command = lambda: controller.show_frame(Form_Page))
        btn_home.grid(column = 1, row = 3)



class Rec_or_Audiofile(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        selected = tk.IntVar()

        rad1 = tk.Radiobutton(self, text = 'Record Audio', value = 1, variable = selected)
        rad2 = tk.Radiobutton(self, text = 'Use audio file', value = 2, variable = selected)

        rad1.grid(column = 0, row = 0)
        rad2.grid(column = 1, row = 0)

        def choice_of_audio():
            if selected.get() == 1:
                controller.show_frame(Rec_page)
            else:
                controller.show_frame(Aud_page)


        btn1 = tk.Button(self, text = 'Okay', command = lambda: choice_of_audio())
        btn1.grid(column = 1, row = 3)


class Rec_page(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        lbl1 = tk.Label(self, text = 'Press Start to start recording!')
        lbl1.grid(column = 0, row = 0)

        btn1 = tk.Button(self, text = 'START RECORDING', command = lambda: self.audio_analysis())
        btn1.grid(column = 1, row = 0)

    def audio_analysis(self, controller, parent, rec=None, tim = 10):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = tim
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

        fs, data = wavfile.read(WAVE_OUTPUT_FILENAME)

        channel_1 = data[:]
        if rec == None:
            no_elem = 10000000
        else:
            no_elem = 10000
        fourier = np.fft.rfft(channel_1, no_elem)
        t = 1 / 44100
        freq = np.fft.rfftfreq(100, d=t)
        mag = np.abs(fourier)

        if rec == None:
            x = Process_Page(parent, controller)
            Process_Page.get_maxs(x, controller)
            controller.show_frame(Process_Page)
            self.controller.shared_data['properties'] = [fourier, mag, freq]
        else:
            return [fourier, mag, freq]


class Aud_page(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        labl1 = tk.Label(self, text = "Select the file you wish to use" )
        labl1.grid(column = 0, row = 0)


    def aud_analysis2(self, file, parent, controller):
        recording = file
        try:
            fs, data = wavfile.read(recording)
        except:
            recording = input('Enter name again: ')
            fs, data = wavfile.read(recording)

        channel_1 = data[:]
        fourier = np.fft.rfft(channel_1, 10000000)
        t = 1 / 44100
        freq = np.fft.rfftfreq(100, d=t)
        mag = np.abs(fourier)

        self.controller.shared_data['properties'] = [fourier, mag, freq]
         # print(self.controller.shared_data['properties'])
        controller.show_frame(Process_Page)
        x = Process_Page(parent, controller)
        Process_Page.get_maxs(x, controller)

    def select_file(self, parent, controller):
        file = filedialog.askopenfilename()
        self.aud_analysis2(file, parent, controller)

        btn1 = tk.Button(self, text = 'Open', command = lambda: self.select_file(parent, controller))
        btn1.grid(column = 2, row = 0)


class Process_Page(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        labl1 = tk.Label(self, text="Processing your information...")
        labl1.grid(column=0, row=0)

    def get_maxs(self,controller):
        self.controller = controller
        entries = self.controller.shared_data['entries']
        properties = self.controller.shared_data['properties']
        mag = properties[1]
        fourier = properties[0]
        password = entries[2]
        sorted_f = sorted(mag)
        maxs = []
        m = -1
        n = len(password)
        for k in range(n):
            index = np.where(mag == sorted_f[m])
            maxs.append(index[0][0])
            m += -1
        print(maxs)
        self.controller.shared_data['maxs'] = maxs


    def create_final_file(self, controller, parent):
        self.controller = controller
        properties = self.controller.shared_data['properties']
        entries = self.controller.shared_data['entries']
        password = entries[2]
        mag = properties[1]
        fourier = properties[0]
        maxess = self.controller.shared_data['maxess']
        maxs = self.controller.shared_data['maxs']
        user = entries[0]
        account_name = entries[1]
        # all ascii values for possible password characters are within the range of 65 ~ 150, can be easily represented
        # as phase angles in degrees!
        ascii_password = []
        for char in password:
            ascii_password.append(ord(char))

        alpha_pass = yts.yates(ascii_password, maxess)

        # altering the phase values of fourier elements with indexes in alpha
        for m in range(n):
            indice = maxs[m]
            fourier[indice] = mag[indice] * complex(math.cos(math.radians(alpha_pass[m])),
                                                math.sin(math.radians(alpha_pass[m])))
            print(np.angle(fourier[indice]))

        # creating the modified audio file
        data = np.fft.irfft(fourier)
        name_of_newaud = user + '_' + account_name
        name = name_of_newaud + '.wav'
        print(name)
        wavfile.write(name, 44100, data)
        # fourier_locker()


app = Fourier_pass_locker()
app.mainloop()

