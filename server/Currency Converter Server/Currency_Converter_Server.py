import socket
import tkinter as tk
from typing import get_origin
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pickle
from datetime import datetime
import os
import threading
import time

from threading import Timer
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from PIL import Image,ImageTk
import emoji
import tkinter as tk
import urllib, json
import urllib.request as ur
import hashlib
from datetime import datetime
import requests

HOST = ''
PORT = 80
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(5)
clients=[]
nicknames=[] 
stop = False
One = True
isServerstop = False
Kick = False
IPaddres = requests.get('https://checkip.amazonaws.com').text.strip()

class FirstScreen(tk.Tk):
    def __init__(self,port):
        super().__init__()
        self.geometry("1080x720")
        self.title("Currency Converter")
        self.resizable(False,False)
        self.gui_done = False
        self.first_frame = tk.Frame(self, bg="red")
        self.first_frame.pack(fill="both", expand=True)

        #ICON
        app_icon = Image.open('image/icon.png')
        app_icon = ImageTk.PhotoImage(app_icon)
        self.iconphoto(False, app_icon)

        #BackGround
        background = Image.open("image/background.png")
        #background = background.resize((1080, 700), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        tk.Label(self.first_frame, image = self.background).place(x=0, y=0)

        # On or Off server:
        red = Image.open("image/off.png")
        red = red.resize((15, 15), Image.ANTIALIAS)
        self.red = ImageTk.PhotoImage(red)
       
        green = Image.open("image/on.png")
        green = green.resize((15, 15), Image.ANTIALIAS)
        self.green = ImageTk.PhotoImage(green)

        self.server_state = tk.Label(self.first_frame, image = self.green, bd = 0, bg = "#ee2f7b", activebackground = "#ee2f7b")
        self.server_state.place(x=18, y=693)
        self.server_cmt = tk.Label(self.first_frame, text = "Ready to connect", font = ("times new roman",12),fg = "white" ,bd = 0, bg = "#ef437b", activebackground = "#ef437b")
        self.server_cmt.place(x = 40, y = 690)


        # Message area
        self.text_area = tk.scrolledtext.ScrolledText(self.first_frame, bg = "white", bd = 0, font=("Transformers Movie",14))
        self.text_area.place(x=369,y=84, width = 672, height = 500)
        self.text_area.config(state='disabled',fg="#00B7FE")
        
        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Close server")
        receive_thread = threading.Thread(target = self.receive)
        receive_thread.start()

        # Kick button
        kick_button_img = Image.open("image/kickbtn.png")
        kick_button_img = kick_button_img.resize((82,58), Image.ANTIALIAS)
        kick_button = ImageTk.PhotoImage(kick_button_img)
        self.button_kick=tk.Button(self.first_frame,cursor="hand2",image = kick_button, bg="#f05c77",bd = 0,command = self.writeKick, activebackground = "#f05c77").place(x=230,y=624)
        
        # Start Stop button:
        start_button_img = Image.open("image/startbtn.png")
        start_button_img = start_button_img.resize((130,55), Image.ANTIALIAS)
        start_button = ImageTk.PhotoImage(start_button_img)
        self.button_start=tk.Button(self.first_frame,cursor="hand2",image = start_button,bg="#f3776e",bd = 0,activebackground = "#f3776e",command=self.start).place(x=30,y=65)

        stop_button_img = Image.open("image/stopbtn.png")
        stop_button_img = stop_button_img.resize((130,55), Image.ANTIALIAS)
        stop_button = ImageTk.PhotoImage(stop_button_img)
        self.button_stop=tk.Button(self.first_frame,cursor="hand2",image = stop_button,bg="#f4836a",bd = 0,activebackground = "#f4836a",command=self.close).place(x=179,y=65)

        # user area
        self.text_user = tk.scrolledtext.ScrolledText(self.first_frame, font=("Transformers Movie",14))
        self.text_user.config(state='disabled',fg="#00B7FE", bg = "white", bd = 0)
        self.text_user.configure(bg="white")
        self.text_user.place(x=50,y=160,width=248,height=433)

        # Kick input
        self.input_kick = tk.Entry(self.first_frame, bg = "white", bd = 0)
        self.input_kick.config(font=("Transformers Movie",14), justify = "center")
        self.input_kick.place(x=48, y=637,width=145,height=35)

        # Message input
        self.input = tk.Entry(self.first_frame, bg = "white", bd = 0)
        self.input.config(font=("Transformers Movie",14))
        self.input.place(x=361, y=635,width=580,height=40)

        # Message send button:
        send_button_img = Image.open("image/sendbtn.png")
        send_button_img = send_button_img.resize((82,58), Image.ANTIALIAS)
        send_button = ImageTk.PhotoImage(send_button_img)
        self.send=tk.Button(self.first_frame,cursor="hand2",image = send_button, bd = 0, bg="#f69360", activebackground = "#f69360", command=self.ServerChat).place(x=972,y=624)
        
        # Thread start:
        thread2 = threading.Thread(target=self.ServerChat,args=( ))
        thread2.start() 
        self.protocol("WM_DELETE_WINDOW",self.stopScream)
        self.gui_done = True
        self.mainloop()

#--------------- function of KICK-------------------------
    def kickClient(self,name):
        global Kick
        if name in nicknames:
            Kick = True
            name_index= nicknames.index(name)
            client_kick=clients[name_index]
            clients.remove(client_kick)
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{name} were KICK\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            client_kick.send("You were kicked by admin \n".encode('utf-8'))   
            client_kick.close()
            nicknames.remove(name)
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{name} disconnected\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            self.broadcast(f"{name} disconnect server\n".encode('utf-8'))
        

    def writeKick(self):
        name_kick = self.input_kick.get()
        self.name_kick=name_kick
        self.input_kick.delete(0,END)
        self.kickClient(name_kick)
        

#===========================================================
# send mess of server to clients          
    def broadcast(self,message):
        for client in clients:
            client.send(message)

    def getdata(self):
        url = 'http://api.exchangeratesapi.io/v1/latest?access_key=0852994b72a73bd10dd418d01965b968'
        response = ur.urlopen(url)
        data = json.loads(response.read())
        with open('data.json', 'w') as f:
            json.dump(data['rates'], f)

    def command(self):
        self.getdata()

    def getInfo(self,client,currency):
        price = '' 
        f = open('data.json',)
        data = json.load(f)
        base = data['VND']
        if currency in data:
            rate = round((base / data[currency]))
            mess = f''' ----------->on {datetime.now()}<-------------
                          1 {currency} = {rate} VND\n'''
            client.send(mess.encode('utf-8'))
            #client.send(f"1 {currency} = {rate} VND\n".encode('utf-8'))
        else:
            client.send(f"{currency} couldn't be found\n".encode('utf-8'))

    def set_interval(self,func, sec):
        sectemp = 0.1
        i=1
        while True:
            func()
            while (i<=sec/0.1): 
                time.sleep(sectemp)
                i+=1
            i=1
        

    def update(self):
        url = 'http://api.exchangeratesapi.io/v1/latest?access_key=0852994b72a73bd10dd418d01965b968'
        if len(nicknames)==0: return "out"
        self.text_area.config(state='normal')
        self.text_area.insert('end',"Updating ...\n")
        
        try:
            response = ur.urlopen(url)
            data = json.loads(response.read())
            with open('data.json', 'w') as f:
                json.dump(data['rates'], f)
            
            self.text_area.insert('end',f"Update information successfully.\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
        except:
            self.text_area.insert('end',f"Error !!!\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')

    def handle(self,client):
         while True :
            try:
                message = client.recv(1024).decode('utf-8')
                temp = message.split(':')
                currency = 'currency'
                if temp[1][1] != '/':
                    self.text_area.config(state='normal')
                    self.text_area.insert('end',"User chat\n")
                    self.text_area.insert('end',message)
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
                    self.broadcast(message.encode('utf-8'))
                else:
                    if currency in temp[1]:
                        currency_choosen = temp[1][11:len(temp[1])-1]
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',"User converted currency\n")
                        self.text_area.insert('end',f"Currrecy : {currency_choosen}\n")
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
                        self.getInfo(client,currency_choosen)
            except:
                global Kick
                if Kick==False:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname=nicknames[index]
                    self.text_user.config(state='normal')
                    self.text_user.insert('end',f"{nickname} disconnected\n")
                    self.text_user.yview('end')
                    self.text_user.config(state='disabled')
                    self.broadcast(f"{nickname} disconnect server\n".encode('utf-8'))
                    nicknames.remove(nickname)
                Kick = False
                break
        
    # Send message to client
    def ServerChat(self):
        index=self.input.get()
        if index=='/member':
            self.input.delete(0, END)
            mess = f'Member online: {len(nicknames)}\n'
            self.text_area.config(state='normal')
            self.text_area.insert('end',mess)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            for nickname in nicknames:
                nickname = f'{nickname} '
                self.text_area.config(state='normal')
                self.text_area.insert('end',nickname)
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
            self.text_area.config(state='normal')
            self.text_area.insert('end','\n')
            self.text_area.yview('end')
            self.text_area.config(state='disabled')    
            return
        if index=='/ip':
            global IPaddres
            IPaddres=f'{IPaddres}\n'
            self.input.delete(0, END)
            self.text_area.config(state='normal')
            self.text_area.insert('end',IPaddres)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            return
        if index != '\n' and index != "":
            self.input.delete(0, END)
            inp="server: " + index + '\n'
            self.text_area.config(state='normal')
            self.text_area.insert('end',inp)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            self.broadcast(inp.encode('utf-8'))

    def start(self):
        global server
        global isServerstop
        global server_cmt
        if isServerstop==True:
            self.server_state.config(image = self.green)
            self.server_cmt.config(text = "Ready to connect")
            isServerstop = False
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            HOST = ''
            PORT = 80
            server.bind((HOST,PORT))
            server.listen(5)
            print("start")
            self.text_area.config(state='normal')
            self.text_area.insert('end',"Server started\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            receive_thread = threading.Thread(target = self.receive)
            receive_thread.start()
        else:
            messagebox.showerror("Warning","SERVER HAD STARTED! ")
    def close(self):
            global server
            global isServerstop
            global server_cmt
            if isServerstop == False:
                isServerstop = True
                self.text_area.config(state='normal')
                self.text_area.insert('end',"Server stopped\n")
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
                print("stop")
                self.server_state.config(image = self.red)
                self.server_cmt.config(text = "Server is offline")
                self.broadcast('Server offline'.encode('utf-8'))
                for client in clients:
                    global Kick
                    Kick = True
                    client.close()
                Kick = True
                clients.clear()
                nicknames.clear()
                if (One==True):
                    time.sleep(0)
                server.close()
            else :
                messagebox.showerror("Warning","SERVER HAD STOPPED ! ")
    def stopScream(self):
        global server
        res = messagebox.askyesno(title='Warning !',message="Do you really want to disconnect ?")
        if res:
            
            self.broadcast('Server offline'.encode('utf-8'))

            for client in clients:
                global Kick
                Kick = True
                client.close()
            Kick = True
            clients.clear()
            nicknames.clear()  
            self.destroy()
            if (One==True):
                time.sleep(0)
            server.close()

    def stop(self):
        global isServerstop
        if (isServerstop==0):
            messagebox.showerror("Error","Stop server before closing Window.")
        else:
            self.first_frame.destroy()
            exit(0)


    #-------Login--------
    def checkLogin(self,nickname,password):
        salt = "5gz"
        check_password = password+salt
        check_password = hashlib.md5(check_password.encode())
        for line in open("data/accounts.txt","r").readlines():
            login_info = line.split()
            
            if nickname == login_info[0] and check_password.hexdigest() == login_info[1]:
                return True
        return False    

    def ProcessLogin(self,nickname,password,client,address):
        if self.checkLogin(nickname,password) == True:
            
            if nickname in nicknames:
                client.send('logged'.encode('utf-8'))
                self.text_user.config(state='normal')
                self.text_user.insert('end',f"{address} disconnected\n")
                self.text_user.yview('end')
                self.text_user.config(state='disabled')
                client.close()
                
            else:
                client.send('true'.encode('utf-8'))
                nicknames.append(nickname)    
                clients.append(client) 
                self.text_area.config(state='normal')
                self.text_area.insert('end',"User login\n")
                self.text_area.insert('end',f"Username : {nickname}\n")
                self.text_area.yview('end')
                self.text_area.config(state='disabled')

                self.text_user.config(state='normal')
                self.text_user.insert('end',f"Username : {nickname}\n")
                self.text_user.yview('end')
                self.text_user.config(state='disabled')


                self.broadcast(f"{nickname} connected to server \n".encode('utf-8'))
                client.send(f"Connected to server. \n".encode("utf-8"))
                thread1 = threading.Thread(target= self.handle, args=(client,) )
                thread1.start()
        else:
            client.send('wrong_pass'.encode('utf-8'))
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{address} disconnected\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            client.close()
    
    #========register=========
    def checkRegister(self,nickname,password):
        salt = "5gz"
        
        for line in open("data/accounts.txt","r").readlines():
            account_info = line.split()
            if nickname==account_info[0]:
                return False
        return True

    def ProcessRegister(self,nickname,password,client,address):
        if self.checkRegister(nickname,password)==True:
            client.send('complete'.encode('utf-8'))
            file = open("data/accounts.txt","a")
            salt = "5gz"
            reg_password = password+salt
            reg_password = hashlib.md5(reg_password.encode())
            file.write(f"\n{nickname} {reg_password.hexdigest()}")

            self.text_area.config(state='normal')
            self.text_area.insert('end',"User register\n")
            self.text_area.insert('end',f"Username: {nickname}\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            client.close()
        else:
            client.send('exists'.encode('utf-8'))
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{address} sisconnected\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            client.close()


    def receive(self):
        try: 
            global One
            while True:
                global server
                if self.gui_done:
                    client,address  = server.accept()

                    self.text_user.config(state='normal')
                    self.text_user.insert('end',f"Connected with{str(address)}\n")
                    self.text_user.yview('end')
                    self.text_user.config(state='disabled')

                    if len(clients)==5:
                        client.send('not_allowed'.encode())
                
                        continue
                    else:
                        client.send('allowed'.encode())
                    try:
                        nickname= client.recv(1024).decode('utf-8')
                        password= client.recv(1024).decode('utf-8')
                        
                    # print(option,nickname,password)
                    except:
                        self.text_user.config(state='normal')
                        self.text_user.insert('end',f"{address} disconnected\n")
                        self.text_user.yview('end')
                        self.text_user.config(state='disabled')
                        client.close()
                        break
                    option = nickname[0]
                    nickname = nickname[1:]
                    if option=='1': self.ProcessLogin(nickname,password,client,address)
                    if option=='2': self.ProcessRegister(nickname,password,client,address)
                    if len(nicknames) > 0 and One == True: 
                        t = threading.Thread(target=self.set_interval,args=(self.update,3600,), daemon=True)
                        t.start()
                        One = False

        except socket.error:
            print("Shutting down")
            
       
FirstScreen(PORT)
