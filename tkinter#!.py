import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import audio_analysis_fft as fourier_comps
import numpy as np
import hash_it
import fourier_pass_locker as fplocker
import fourier_pass_unlocker as fpunlocker
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

        for F in (WelcomePage,StartPage, Form_Page, Form_Page2, Rec_or_Audiofile, Rec_page, Aud_page, Process_Page, RegistrationPage,
                  Final_Page, Sign_in_page):

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
        shaEncryp = hash_it.hash_me(text)
        shit = Rec_page(parent, controller)
        key = shit.audio_analysis1(controller, parent,rec = 'my_voice',tim = 5)
        maxess = []
        j = -1
        for k in range(5):
            index = np.where(key[1] == sorted(key[1])[j])
            maxess.append(index[0][0])
            j += -1
        print(maxess)
        sha_myspecs = hash_it.hash_me(str(maxess))

        membersFile = open('members.txt', 'a')
        membersFile.write(shaEncryp + ':' + sha_myspecs + '\n')
        membersFile.close()
        controller.show_frame(Sign_in_page)

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
        key = shit.audio_analysis1('voice', tim=5)
        maxess = []
        j = -1
        for k in range(5):
            index = np.where(key[1] == sorted(key[1])[j])
            maxess.append(index[0][0])
            j += -1
        self.controller.shared_data['maxess'] = maxess
        user_specs = hash_it.hash_me(str(maxess))

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
        username = self.txt1.get()
        self.controller.shared_data['username'] = username
        shaEncryp = hash_it.hash_me(username)

        if shaEncryp in user_pass_info.keys() and user_specs == user_pass_info[shaEncryp] :
            controller.show_frame(StartPage)
        elif shaEncryp in user_pass_info.keys() and user_specs != user_pass_info[shaEncryp] :
            tk.messagebox.showinfo('Could not SignIN!', 'Incorrect Voice Password')
            controller.show_frame(Sign_in_page)
        else:
            tk.messagebox.showinfo('Could not SignIn!', 'User not registered!')
            controller.show_frame(RegistrationPage)

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

        lbl1 = tk.Label(self, text = 'acc username')
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

        lbl1 = tk.Label(self, text='account associated')
        lbl1.grid(column=0, row=0)
        txt1 = tk.Entry(self, width=20)
        txt1.grid(column=1, row=0)

        lbl2 = tk.Label(self, text = 'Select Audio file')
        lbl2.grid(column = 0, row = 1)
        btn1 = tk.Button(self, text = 'Open' ,command = lambda: click_open())
        btn1.grid(column = 1, row = 1)

        def click_open():
            acc_name = txt1.get()
            self.select_file(controller,parent,acc_name)


        btn_home = ttk.Button(self, text = 'Home', command = lambda: controller.show_frame(StartPage))
        btn_home.grid(column = 3, row = 1)

        btn_home = ttk.Button(self, text = 'Next')
        btn_home.grid(column = 0, row = 3)

        btn_home = ttk.Button(self, text = 'Generate', command = lambda: controller.show_frame(Form_Page))
        btn_home.grid(column = 1, row = 3)

    def select_file(self, parent, controller,acc_name):
        file = filedialog.askopenfilename()
        self.is_acc_available(controller,parent, acc_name, file)

    def is_acc_available(self,controller, parent, acc_name, file):
        self.controller = controller
        maxess = self.controller.shared_data['maxess']
        username = self.controller.shared_data['username']
        hashed_user = hash_it.hash_me(username)
        hashed_acc_name = hash_it.hash_me(acc_name)
        acc_file = open('account_info.txt', 'r')
        acc_data = acc_file.readlines()
        acc_file.close()
        for element in acc_data:
            acc = element.split('\n')
            acc_names = acc[0].split('=')
            if username != acc_names[0]:
                pass
            elif hashed_user == acc_names[0] and username[1] == hashed_acc_name:
                n = acc_names[1]
                self.controller.shared_data['length'] = n
                controller.show_frame(Process_Page)
                password = fpunlocker.unlock_pass(file,n,maxess)
                controller.show_frame(Final_Page)
                tk.messagebox.showinfo('Your password is %s' % password)
            else:
                tk.messagebox.showinfo('Could not find account under %s' % username)
                controller.show_frame(Sign_in_page)

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

        btn1 = tk.Button(self, text = 'START RECORDING', command = lambda: self.audio_analysis1(controller, parent))
        btn1.grid(column = 1, row = 0)

    def audio_analysis1(self, controller, parent, rec=None, tim = 10):
        if rec == None:
            x = Process_Page(parent, controller)
            Process_Page.get_maxs(x, controller)
            controller.show_frame(Process_Page)
            self.controller.shared_data['properties'] = fourier_comps.give_me_mags(tim = tim)
        else:
            return fourier_comps.give_me_mags(f = 'voice_pass', tim = tim)


class Aud_page(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        labl1 = tk.Label(self, text = "Select the file you wish to use" )
        labl1.grid(column = 0, row = 0)

        btn1 = tk.Button(self, text='Open', command=lambda: self.select_file(parent, controller))
        btn1.grid(column=2, row=0)

    def aud_analysis2(self, file, parent, controller):
        self.controller.shared_data['properties'] = fourier_comps.give_me_mags(file = file, f = 'usingfile')
         # print(self.controller.shared_data['properties'])
        controller.show_frame(Process_Page)
        x = Process_Page(parent, controller)
        Process_Page.get_maxs(x, controller)

    def select_file(self, parent, controller):
        file = filedialog.askopenfilename()
        self.aud_analysis2(file, parent, controller)



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
        n = len(entries[2])
        properties = self.controller.shared_data['properties']
        maxs = fplocker.get_maxs(properties, n)
        self.controller.shared_data['maxs'] = maxs
        self.create_final_file(controller)


    def create_final_file(self, controller):
        self.controller = controller
        properties = self.controller.shared_data['properties']
        entries = self.controller.shared_data['entries']
        username = self.controller.shared_data['username']
        password = entries[2]
        n = len(password)
        maxess = self.controller.shared_data['maxess']
        maxs = self.controller.shared_data['maxs']
        user = entries[0]
        account_name = entries[1]
        account_info_file = open('account_info.txt', 'a')
        encryp_user = hash_it.hash_me(username)
        encryp_acc = hash_it.hash_me(account_name)
        account_info_file.write(encryp_user + '=' + encryp_acc + '=' + str(n) + '\n')
        account_info_file.close()
        # all ascii values for possible password characters are within the range of 65 ~ 150, can be easily represented
        # as phase angles in degrees!
        fplocker.create_final(password,maxs,user,properties,maxess)
        controller.show_frame(Final_Page)

class Final_Page(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        labl1 = tk.Label(self, text='Awesome, Process was successful!')
        labl1.pack()

app = Fourier_pass_locker()
app.mainloop()

