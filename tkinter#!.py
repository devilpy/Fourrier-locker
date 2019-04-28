import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import audio_analysis_fft as fourier_comps
import numpy as np
import hash_it
import fourier_pass_locker as fplocker
import fourier_pass_unlocker as fpunlocker
from tkinter import filedialog

LARGE_FONT = ('Times', 16, 'bold')
normal_font = ('Verdana', 12)

class Fourier_pass_locker(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

    #need to make maxs, username, password, maxess available to all pages.

        self.shared_data = {}

        tk.Tk.wm_geometry(self, newGeometry = '600x200')
        tk.Tk.wm_title(self, 'Welcome to Fourier Pass Locker!')
        tk.Tk.iconbitmap(self, '@/home/naveen/Desktop/My_fourier_project/Traditional-Sri-Lankan-Wooden-Mask.xbm')
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

        label = tk.Label(self, text='Welcome to Fourier Pass Locker', bg = '#b6e7f9', font = LARGE_FONT)
        label.place(relx = 0.5 , rely = 0.05, anchor = 'n')

        btn1 = tk.Button(self, text='New Member', command=lambda: controller.show_frame(RegistrationPage), font = normal_font)
        btn1.place(relx = 0.25, rely = 0.5, anchor = 'n', relheight = 0.2, relwidth = 0.2)

        label2 = tk.Label(self, text='ALREADY A MEMBER?', bg = '#b6e7f9', font = normal_font)
        label2.place(relx= 0.75, rely = 0.5, anchor = 's')

        btn2 = tk.Button(self, text='Sign In!', command=lambda: controller.show_frame(Sign_in_page), font = normal_font)
        btn2.place(relx = 0.75, rely = 0.7, relheight = 0.2, relwidth = 0.2, anchor = 's')



class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):

        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg = '#b6e7f9')

        lbl1 = tk.Label(self, text='username', bg = '#b6e7f9')
        lbl1.place(relx = 0.25, rely = 0.1, anchor = 'n')
        self.txt1 = tk.Entry(self, width=20)
        self.txt1.place(relx = 0.55, rely=0.1, relwidth = 0.4, anchor = 'n')


        lbl2 = tk.Label(self, text='If you are ready, please prepare to deliver voice sample!', bg = '#b6e7f9')
        lbl2.place(relx=0.5,rely = 0.7, anchor = 's')
        btn1 = tk.Button(self, text='Record Voice Password for Locker', command=lambda: self.register_user(parent, controller))
        btn1.place(relx = 0.5, rely = 0.9, relheight = 0.2, relwidth = 0.5, anchor = 's' )

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
        lbl = tk.Label(self, text = 'SignIn', font = LARGE_FONT, bg='#b6e7f9')
        lbl.place(relx = 0.5, rely = 0.05, anchor = 'n')
        lbl1 = tk.Label(self, text='username', font = normal_font, bg='#b6e7f9')
        lbl1.place(relx = 0.2, rely = 0.2, relheight = 0.2, relwidth = 0.15)
        self.txt1 = tk.Entry(self)
        self.txt1.place(relx = 0.45, rely = 0.2, relheight = 0.2, relwidth = 0.4)

        btn1 = tk.Button(self, text='Record Voice Password for Locker',command=lambda: self.signme_in(parent, controller), font = normal_font)
        btn1.place(relx = 0.5, rely = 0.7, relheight = 0.2, relwidth = 0.5, anchor = 's')

    def signme_in(self, parent, controller):
        shit = Rec_page(parent, controller)
        key = shit.audio_analysis1(controller, parent,rec = 'voice', tim=5)
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
        user_pass_info = {}
        for element in users_and_passwords:
            usp = element.split('\n')
            us_and_p = usp[0].split(':')
            user_pass_info[us_and_p[0]] = us_and_p[1]
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

        btn1 = tk.Button(self, text='Generate password audio', command = lambda: controller.show_frame(Form_Page), font = normal_font)
        btn1.place(relx = 0.25, rely = 0.5, relheight = 0.2, relwidth = 0.4, anchor = 'n')

        btn2 = tk.Button(self, text='Retrieve password from audio', command = lambda: controller.show_frame(Form_Page2), font = normal_font)
        btn2.place(relx = 0.75, rely = 0.5, relheight = 0.2, relwidth = 0.45, anchor = 'n')


class Form_Page(tk.Frame):
    def __init__(self, parent, controller):

        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        label = tk.Label(self, text = 'Enter Details', font = LARGE_FONT , bg = '#b6e7f9')
        label.place(relx = 0.5, rely = 0.1, anchor = 'n', relheight = 0.2, relwidth = 0.25)

        lbl1 = tk.Label(self, text = 'account username', font = normal_font, bg = '#b6e7f9')
        lbl1.place(relx = 0.3, rely = 0.25, relheight = 0.1, relwidth = 0.25, anchor = 'n')
        txt1 = tk.Entry(self, width = 10)
        txt1.place(relx = 0.6, rely = 0.25, relheight = 0.1, relwidth = 0.25, anchor = 'n')

        lbl2 = tk.Label(self, text = 'account associated: eg:gmail,ebay etc', font = normal_font, bg = '#b6e7f9')
        lbl2.place(relx = 0.3, rely = 0.5, relheight = 0.1, relwidth = 0.3, anchor = 's')
        txt2 = tk.Entry(self, width=10)
        txt2.place(relx = 0.6, rely = 0.5, relheight = 0.1, relwidth = 0.25, anchor = 's')

        lbl3 = tk.Label(self, text='password', font = normal_font,bg = '#b6e7f9')
        lbl3.place(relx = 0.3, rely = 0.7, relheight = 0.1, relwidth = 0.25, anchor = 's')
        txt3 = tk.Entry(self, width=10)
        txt3.place(relx = 0.6, rely = 0.7, relheight = 0.1, relwidth = 0.25, anchor = 's')

        btn_home = ttk.Button(self, text = 'Home', command = lambda: controller.show_frame(StartPage))
        btn_home.place(relx = 0.3, rely = 0.95, height = 40, width = 100, anchor = 's')

        def click_submit():
            entries = []
            entries.append(txt1.get())
            entries.append(txt2.get())
            entries.append(txt3.get())
            self.controller.shared_data['entries'] = entries
            # print(self.controller.shared_data['entries'])
            controller.show_frame(Rec_or_Audiofile)
            # print(Fourier_pass_locker.shared_data)

        btn_submit = tk.Button(self, text='Submit', command=lambda: click_submit(), font = normal_font)
        btn_submit.place(relx = 0.6, rely = 0.95, height = 40, width = 100, anchor = 's')



class Form_Page2(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        # label = tk.Label(self, text = 'Enter Details')
        # label.pack(pady = 10, padx = 10)

        lbl1 = tk.Label(self, text='account associated', bg='#b6e7f9', font = normal_font)
        lbl1.place(relx = 0.3, rely = 0.1, relheight = 0.1, relwidth = 0.4, anchor = 'n')
        txt1 = tk.Entry(self, width=20)
        txt1.place(relx = 0.7, rely = 0.1, relheight = 0.1, relwidth = 0.4, anchor = 'n')

        lbl2 = tk.Label(self, text = 'Select Audio file', bg='#b6e7f9', font = normal_font)
        lbl2.place(relx = 0.3, rely = 0.6, anchor = 's',relheight = 0.2, relwidth = 0.4)
        btn1 = tk.Button(self, text = 'Open' ,command = lambda: click_open())
        btn1.place(relx = 0.7, rely = 0.6, height = 40, width = 100, anchor = 's')

        def click_open():
            acc_name = txt1.get()
            self.select_file(controller,parent,acc_name)

    def select_file(self, parent, controller,acc_name):
        file = filedialog.askopenfilename()
        self.is_acc_available(controller,parent, acc_name, file)

    def is_acc_available(self,controller, parent, acc_name, file):
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
            if hashed_user != acc_names[0]:
                pass
            elif hashed_user == acc_names[0]:
                if acc_names[1] == hashed_acc_name:
                    n = acc_names[2]
                    self.controller.shared_data['length'] = n
                    self.controller.show_frame(Process_Page)
                    password = fpunlocker.unlock_pass(file,n,maxess)
                    self.controller.show_frame(Final_Page)
                    tk.messagebox.showinfo('Successfully Retrieved!','Your password is %s' % password)
                    break
                else:
                    pass
            else:
                tk.messagebox.showinfo('Could not find account under %s' % username)
                controller.show_frame(Sign_in_page)

class Rec_or_Audiofile(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        selected = tk.IntVar()

        rad1 = tk.Radiobutton(self, text = 'Record Audio', value = 1, variable = selected, font = normal_font, bg='#b6e7f9')
        rad2 = tk.Radiobutton(self, text = 'Use audio file', value = 2, variable = selected, font = normal_font, bg='#b6e7f9')

        rad1.place(relx = 0.3, rely = 0.25, relheight = 0.2, relwidth = 0.4, anchor = 'n')
        rad2.place(relx = 0.7, rely = 0.25, relheight = 0.2, relwidth = 0.4, anchor = 'n')

        def choice_of_audio():
            if selected.get() == 1:
                controller.show_frame(Rec_page)
            else:
                controller.show_frame(Aud_page)


        btn1 = tk.Button(self, text = 'Okay', command = lambda: choice_of_audio())
        btn1.place(relx = 0.5, rely = 0.7, anchor = 's', height = 40, width = 100)


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

        labl1 = tk.Label(self, text = "Select the file you wish to use", bg='#b6e7f9' )
        labl1.place(relx = 0.25, rely = 0.5, relheight = 0.2, relwidth = 0.5, anchor = 'n')

        btn1 = tk.Button(self, text='Open', command=lambda: self.select_file(parent, controller))
        btn1.place(relx = 0.8, rely = 0.5,relheight = 0.2, relwidth = 0.2)

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
        self.select_location(controller)

    def select_location(self,controller):
        dir_name = filedialog.askdirectory()
        self.create_final_file(dir_name, controller)

    def create_final_file(self, dir_name, controller):
        self.controller = controller
        properties = self.controller.shared_data['properties']
        entries = self.controller.shared_data['entries']
        username = self.controller.shared_data['username']
        password = entries[2]
        n = len(password)
        maxess = self.controller.shared_data['maxess']
        maxs = self.controller.shared_data['maxs']
        account_username = entries[0]
        acc_associate = entries[1]
        user = account_username + '_' + acc_associate
        account_info_file = open('account_info.txt', 'a')
        encryp_user = hash_it.hash_me(username)
        encryp_acc = hash_it.hash_me(acc_associate)
        account_info_file.write(encryp_user + '=' + encryp_acc + '=' + str(n) + '\n')
        account_info_file.close()
        # all ascii values for possible password characters are within the range of 65 ~ 150, can be easily represented
        # as phase angles in degrees!
        fplocker.create_final(password,maxs,user,properties,maxess, dir_name)
        controller.show_frame(Final_Page)

class Final_Page(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg='#b6e7f9')

        labl1 = tk.Label(self, text='Awesome, Process was successful!', font = LARGE_FONT, bg='#b6e7f9')
        labl1.place(relx = 0.5, rely = 0.2, relheight = 0.2, relwidth = 0.6, anchor = 'n')

        btn_home = ttk.Button(self, text='Home', command=lambda: controller.show_frame(StartPage))
        btn_home.place(relx=0.3, rely=0.95, height=40, width=100, anchor='s')


app = Fourier_pass_locker()
app.mainloop()

