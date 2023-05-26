import socket
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from datetime import datetime
import threading
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from PIL import Image,ImageTk
import emoji
import tkinter as tk
from datetime import datetime

import sys
import errno

PORT = 80

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
class FirstScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.title("Currency Converter")
        self.resizable(False,False)
        self.first_frame= tk.Frame(self,bg="red")
        self.first_frame.pack(fill="both",expand=True)

        #ICON
        app_icon = Image.open('image/icon.png')
        app_icon = ImageTk.PhotoImage(app_icon)
        self.iconphoto(False, app_icon)

        #BACKGROUND
        background = Image.open("image/login.png")
        background = background.resize((1080,720), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        tk.Label(self.first_frame, image=self.background).place(x=0, y=0)

        # User:
        self.txt_user=Entry(self.first_frame,font=("Amaranth Bold",20),bg="white",fg = "#00B7FE", bd = 0, justify = "center")
        self.txt_user.place(x=700,y=407,width=250,height=35)
        
        # Password:
        self.txt_pass=tk.Entry(self.first_frame,show="*",font=("Amaranth Bold",20),bg="white",fg = "#00B7FE",bd = 0, justify = "center")
        self.txt_pass.place(x=700,y=477,width=250,height=35)

        # IP:
        self.txt_ip = Entry(self.first_frame,font=("Amaranth Bold",20),bg="white", fg = "#00B7FE", bd = 0, justify = "center")
        self.txt_ip.place(x=700,y=547,width=250,height=35)

        # Create new account:
        tk.Button(self.first_frame,cursor="hand2",text="Create New Account",command = self.createAccount,bg="#f69360",fg="white",bd=0,font=("times new roman",12), activebackground = '#f69360').place(x=830,y=590)

        # Login:
        login_button_img = Image.open("image/buttonlogin.png")
        login_button_img = login_button_img.resize((160,40), Image.ANTIALIAS)
        login_button = ImageTk.PhotoImage(login_button_img)
        tk.Button(self.first_frame,cursor="hand2",command = self.login_funtion, image = login_button, bd = 0, bg = '#f58a66', activebackground = '#f58a66').place(x=730,y=620)

        self.mainloop()

    def createAccount(self):
        msg = Toplevel() 
        msg.geometry("360x500")
        msg.title("Create Account")
        msg.resizable(False,False)
        msg.configure(bg="white")

        #ICON
        app_icon = Image.open('image/icon.png')
        app_icon = ImageTk.PhotoImage(app_icon)
        msg.iconphoto(False, app_icon)

        # Background:
        bg_register = Image.open("image/register.png")
        bg_register = bg_register.resize((360,500), Image.ANTIALIAS)
        bg_register_img = ImageTk.PhotoImage(bg_register)
        tk.Label(msg, image = bg_register_img).place(x=0, y=0)

        # User:
        self.acc_user=Entry(msg,font=("Amaranth Bold",16),bg="white",fg = "#00B7FE", bd = 0,justify = "center")
        self.acc_user.place(x=105,y=284,width=190,height=30)
                
        # Pass:
        self.acc_pass=tk.Entry(msg,show="*",font=("Amaranth Bold",16),bg="white",fg = "#00B7FE", bd = 0,justify = "center")
        self.acc_pass.place(x=105,y=336,width=190,height=30)

        # IP:
        self.acc_ip=Entry(msg,font=("Amaranth Bold",16),bg="white",fg = "#00B7FE", bd = 0,justify = "center")
        self.acc_ip.place(x=105,y=387,width=190,height=30)
        
        # Register:
        register_button_img = Image.open("image/buttonregister.png")
        register_button_img = register_button_img.resize((160,40), Image.ANTIALIAS)
        register_button = ImageTk.PhotoImage(register_button_img)
        tk.Button(msg,cursor="hand2",command=self.register_user,image = register_button, bd = 0, bg = '#f05b77', activebackground = '#f05b77').place(x=95,y=430,width=180,height=40)
        
        msg.mainloop()


    #-------------register--------------------

    def checkRegister(self,nickname):
        for line in open("data/accounts.txt","r").readlines():
            account_info = line.split()
            if nickname==account_info[0]:
                return False
        return True

    def register_user(self):
        nickregister = self.acc_user.get()
        passregister = self.acc_pass.get()
        HOST = self.acc_ip.get()
        if (nickregister == '' or passregister == ''):
            messagebox.showerror("Error","Invalid Username/Password")

        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((HOST,PORT))
                status = client.recv(1024).decode('utf-8')
                if status == 'not_allowed':
                    client.close()
                    messagebox.showinfo(title="Can't connect !", message='Sorry, server is completely occupied.'
                                                                         'Try again later')
                    return
            except ConnectionRefusedError:
                messagebox.showinfo(title="Can't connect !", message="Server is offline , try again later.")
                print("Server is offline , try again later.")
                return
            except socket.gaierror:
                messagebox.showerror(title="Error", message="Error IP")
                return
            except socket.timeout:
                messagebox.showerror(title="Error", message="Can't connect to IP")
                return

            # Send info to server
            nickregister= f'2{nickregister}'
            client.send(nickregister.encode('utf-8'))
            client.send(passregister.encode('utf-8'))
            
            # Receive info from server
            result = client.recv(1024).decode('utf-8')
            if result == 'exists':
                self.txt_user.delete(0, END)
                self.txt_pass.delete(0, END)
                self.txt_ip.delete(0,END)
                messagebox.showerror("Error","Username already exists")
                client.close()
            else:
                messagebox.showinfo("Congratulations","Successful account registration")
                client.close()



                
    #-------------login side-----------------   

    def login_funtion(self):
        nicknameClient=self.txt_user.get()
        passwordClient=self.txt_pass.get()
        HOST = self.txt_ip.get()
       
        if HOST == "":
            messagebox.showerror("Error","Invalid IP!!!")

        if nicknameClient == "" or passwordClient=="":        
            messagebox.showerror("Error!!!","Invalid Username or Password")
        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((HOST,PORT))
                status = client.recv(1024).decode('utf-8')
                print(status)
                if status == 'not_allowed':
                    client.close()
                    messagebox.showinfo(title="Can't connect!", message='Sorry, server is completely occupied.'
                                                                             'Try again later,')
                    return
            except ConnectionRefusedError:
                messagebox.showinfo(title="Can't connect!", message="Server is offline , Try again later.")
                print("Server is offline , try again later.")
                return
            except socket.gaierror:
                messagebox.showerror(title="Error", message="Error IP!")
                return
            except socket.timeout:
                messagebox.showerror(title="Error", message="Can't connect to IP!")
                return
            except socket.error as msg:
                print("Socket Error: %s" % msg)
                return

            # Server works -> send info to server
            nicknameClient= f'1{nicknameClient}'
            client.send(nicknameClient.encode('utf-8'))
            client.send(passwordClient.encode('utf-8'))
            nicknameClient = nicknameClient[1:]

            result = client.recv(1024).decode('utf-8')
            if result == 'wrong_pass':
                self.txt_user.delete(0, END)
                self.txt_pass.delete(0, END)
                self.txt_ip.delete(0, END)
                messagebox.showerror("Error","Username or Password incorrect")
                client.close()
            else:
                if result == 'logged':
                    self.txt_user.delete(0, END)
                    self.txt_pass.delete(0, END)
                    self.txt_ip.delete(0,END)
                    messagebox.showerror("Error","Username is logged in")
                    client.close()
                else: 
                    Clinet(self, self.first_frame,client,nicknameClient,passwordClient,HOST,PORT)
            
            


# Logined screen
class Clinet(tk.Canvas):
    def __init__(self, parent, first_frame,client,txt_user,txt_pass,host,port):
        super().__init__(parent)
        self.window = 'ChatScreen'
        self.first_frame = first_frame
        self.first_frame.pack_forget()
        self.sock = client
        self.parent = parent

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        x_co = int((screen_width / 2) - (1010 / 2))
        y_co = int((screen_height / 2) - (650 / 2)) - 80
        self.parent.geometry("1080x720")
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect((host,port))

    #-----------------------------------------------------------------------------------
     

        #SET BACKGROUND
        background = Image.open("image/root.png")
        background = background.resize((1080, 720), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        tk.Label(self, image=self.background).place(x=0, y=0)


        #BUTTON SEND
        send_label=Image.open("image/buttonsend.png")
        send_label=send_label.resize((80,57),Image.ANTIALIAS)
        send_label=ImageTk.PhotoImage(send_label)
        self.send_label = tk.Button(self, cursor ="hand2",image=send_label,command=self.write, bd = 0, bg = '#f37b6d', activebackground = '#f37b6d')

#----------------------------------CURRENCY---------------------------------------------

        self.combo = ttk.Combobox(self, justify = "center", font = ("times new roman",15))

        self.combo['values']= ("USD","AED","AFN","ALL","AMD","ANG","AOA","ARS","AUD","AWG","AZN","BAM","BBD","BDT"
        ,"BGN","BHD","BIF","BMD","BND","BOB","BRL","BSD","BTC","BTN","BWP","BYN","BYR","BZD","CAD","CDF","CHF","CLF",
        "CLP","CNY","COP","CRC","CUC","CUP","CVE","CZK","DJF","DKK","DOP","DZD","EGP","ERN","ETB","EUR","FJD","FKP",
        "GBP","GEL","GGP","GHS","GIP","GMD","GNF","GTQ","GYD","HKD","HNL","HRK","HTG","HUF","IDR","ILS","IMP","INR",
        "IQD","IRR","ISK","JEP","JMD","JOD","JPY","KES","KGS","KHR","KMF","KPW","KRW","KWD","KYD","KZT","LAK","LBP",
        "LKR","LRD","LSL","LTL","LVL","LYD","MAD","MDL","MGA","MKD","MMK","MNT","MOP","MRO","MUR","MVR","MWK","MXN",
        "MYR","MZN","NAD","NGN","NIO","NOK","NPR","NZD","OMR","PAB","PEN","PGK","PHP","PKR","PLN","PYG","QAR","RON",
        "RSD","RUB","RWF","SAR","SBD","SCR","SDG","SEK","SGD","SHP","SLL","SOS","SRD","STD","SVC","SYP","SZL","THB",
        "TJS","TMT","TND","TOP","TRY","TTD","TWD","TZS","UAH","UGX","USD","UYU","UZS","VEF","VND","VUV","VUV","WST",
        "XAF","XAG","XAU","XCD","XDR","XOF","XPF","YER","ZAR","ZMK","ZMW","ZWL")
         
        self.combo.current(0) 
        self.combo.place(x=774,y=635,width = 172, height = 41)
        #tk.Label(self,text="Choose currency",font=("Impact",10),fg="white",bg="#010E1E").place(x=200,y=550)

        # Button search:
        search_img = Image.open("image/buttonsearch.png")
        search_img = search_img.resize((64,64),Image.ANTIALIAS)
        search_img = ImageTk.PhotoImage(search_img)
        self.search_button = tk.Button(self,cursor = 'hand2', image=search_img,command=self.choose_currency, bd = 0, bg = "#f69161", activebackground = "#f69161").place(x = 982, y = 622)
        #tk.Button(self,text="Search",command=self.choose_currency, borderwidth = 0).place(x=500,y=550)

        # Setting
        self.nickname = txt_user
        self.password = txt_pass
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop) 
        receive_thread = threading.Thread(target = self.receive)
        gui_thread.start()
        receive_thread.start()
        self.pack(fill="both", expand=True)
        self.mainloop()

    # Loop:
    def gui_loop(self):
        self.text_area = tk.scrolledtext.ScrolledText(self, bd = 0)
        self.text_area.place(x=60, y= 90, width = 970, height = 490)
        self.text_area.config(state='disabled',fg="#00B7FE", font = ("Transformers Movie",14))
        self.text_area.configure(bg="white")
    
        #tk.Label(self,image=self.chat_msg,bg="#010E1E").place(x=500,y=400)
       
        # Chat input area:
        self.input_area = tk.Text(self, bd = 0, bg = "white") 
        self.input_area.config(font=("Transformers Movie",14))
        self.input_area.place(x=50, y=632, width = 555, height = 45)
        self.send_label.place(x=648,y=625)
  
        # Create def of button and set image
        
        self.gui_done = True

    def User_manual(self):
        manual=Tk()
        manual.title("User manual")
        manual.resizable(False,False)
        manual.geometry("400x400")
        self.text_user = tk.scrolledtext.ScrolledText(manual)
        self.text_user.config(state='disabled',fg="#00B7FE")
        self.text_user.configure(bg="white")
        self.text_user.place(x=0,y=0,width=400,height=400)
    def choose_currency(self):
        self.country = self.combo.get()
        print(self.country)
        self.country = "/currency " + self.country
        name_country = f"{self.nickname} : {self.country}\n"
        self.sock.send(name_country.encode('utf-8'))
        

#-------------------------------------------------------------------------------
    def write(self,event=None):
        if(self.input_area.get('1.0', 'end') != '\n'):
            message = f"{self.nickname} : {self.input_area.get('1.0', 'end')}"
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.parent.destroy()
        self.sock.close()
        exit(0)
        

    def receive(self):  
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                print("You disconnected ...")
                self.sock.close()
                break
            except ConnectionResetError:
                messagebox.showinfo(title='No Connection!', message="Server offline... Try connecting again later")
                self.sock.close()
                self.first_screen()
                break 

    #def currency_show (self):

    def first_screen(self):
        self.destroy()
        self.parent.geometry("1080x720")
        self.parent.first_frame.pack(fill="both", expand=True)
        self.window = None
    def on_closing(self):
        if self.window == 'ChatScreen':
            res = messagebox.askyesno(title='Warning!',message="Do you really want to disconnect?")
            if res:
                
                self.sock.close()
                self.first_screen()
        else:
            self.parent.destroy()



FirstScreen()