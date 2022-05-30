import tkinter as tk
from tkinter import messagebox
from tkinter import font

import socket, pickle



#can add IP addr in your computer
HOST =  "127.0.0.1"
SERVER_PORT = 64444
FORMAT = "utf8"

FAIL = "fail"
LOGIN = "login"
OK = "ok"
EXIT ="exit"
SEARCH = "search"
SIGNUP ="signup"
LOGOUT = "logout"
LIVE_EXIST = "Live_exist"
UP_DATE = "update"

    
BG_color = "LightSkyBlue2"
L_color = "PaleGreen4"
S_color = "black"
entry_color ="khaki1"
notice_color = "DarkSlateGray3"

L_size = 25
S_size = 10


class Startpage(tk.Frame):
    def __init__(self,parent,app_controller):
        tk.Frame.__init__(self,parent)
        self.configure(bg=BG_color)
        label_title = tk.Label(self, text = "LOG IN", fg =L_color, font=("",L_size,"bold"), bg= BG_color)

        label_user = tk.Label(self, text ="username", fg =S_color , font =("",S_size),bg= BG_color)
        label_pswd = tk.Label(self, text ="password", fg =S_color, font =("",S_size),bg= BG_color)

        
        self.label_notice = tk.Label(self,text = "", bg = BG_color, font =("",S_size),)
        self.entry_user = tk.Entry(self,width = 30,bg = entry_color)
        self.entry_pswd = tk.Entry(self,width = 30,bg =entry_color)

        button_signin = tk.Button(self,text = "Log in", command = lambda: app_controller.logIn(self, client), bg = entry_color)
        #button_exit = tk.Button(self,text= 'Exit', command = lambda:app_controller.Exit(self,client), bg = entry_color)
        button_signup = tk.Button(self,text ="Sign up", command=lambda:app_controller.signUp(self,client), bg = entry_color)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()
        
        
        button_signin.pack()
        button_signup.pack()
        #button_exit.pack()


class Homepage(tk.Frame):
    def __init__(self, parent, app_controller):
        global my_user

        tk.Frame.__init__(self, parent)
        self.configure(bg=BG_color)
        print(my_user)
        label_title = tk.Label(self, text="HOME PAGE", font =("",L_size,"bold"), bg = BG_color, fg = L_color)
        
        btn_logout = tk.Button(self, text="Log out", command=lambda: app_controller.logOut(self,client))
        btn_search = tk.Button(self, text = "Search country",command = lambda: app_controller.search_country(self, client))

        self.label_notice = tk.Label(self, text ="", bg =BG_color, font=("",S_size))
        self.label_info = tk.Label(self, text = "", bg =entry_color, font =("",S_size),width=22,height=14)
        self.entry_country = tk.Entry(self,width = 30,bg = entry_color)
        self.user_name = tk.Label(self, text='Hi' + my_user, bg =BG_color, font=("",S_size))
        #button_exit = tk.Button(self,text= 'Exit', command = lambda:app_controller.Exit(self,client))
        button_update = tk.Button(self, text='Update', command= lambda:app_controller.Update(self, client))
        

        label_title.pack()
        self.entry_country.pack()
        btn_search.pack()
        button_update.pack()
        
        self.label_notice.pack()
        self.label_info.pack()
        self.user_name.place(x=0, y=0)

        
        btn_logout.pack()
        #button_exit.pack()


def show_country(data_country):
        text = ('country: ' + data_country[0] + '\n' + 
        'case: ' + data_country[1] + '\n' + 
        'todayCases: ' + data_country[2] + '\n' +
        'deaths: ' + data_country[3] + '\n' +
        'todayDeaths: ' + data_country[4] + '\n' +
        'recovered: ' + data_country[5] + '\n' +
        'active: ' + data_country[6] + '\n' +
        'critical: ' + data_country[7] + '\n' +
        'casesPerOneMillion: ' + data_country[8] + '\n' +
        'deathsPerOneMillion: ' + data_country[9] + '\n' +
        'totalTests: ' + data_country[10] + '\n' +
        'testsPerOneMillion: ' + data_country[11])
        return text


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        option = ""
        self.title("Covid 19 News")
        self.geometry("400x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
       
        self.resizable( width=False, height = False)

        #Create container
        container = tk.Frame()
        container.configure(bg = "#00FFCC")

        container.pack(side= "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        

        self.frames = {}
        for F in (Startpage,Homepage):
            frame =F(container, self)
            frame.grid(row = 0, column =0 , sticky = "nsew")
            self.frames[F] = frame
        
        self.frames[Startpage].tkraise()

    def showpage(self, FrameClass):
        if (FrameClass == Homepage):
            self.geometry("500x400")
        else:
            self.geometry("400x250")

        self.frames[FrameClass].tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            try:
                option = LOGOUT
                client.sendall(option.encode(FORMAT))
            except:
                pass
    
    def logIn(self,curFrame,sck):
        global my_user
        try:
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if (user == "" or pswd == ""):
                curFrame.label_notice["text"] = "Fields can not be empty"
                curFrame.label_notice["bg"] = notice_color
                return
            else:
                curFrame.label_notice["text"] = ""
                curFrame.label_notice["bg"] = BG_color


            #Send option
            option = LOGIN
            sck.sendall(option.encode(FORMAT))


            #Send account
            sck.sendall(user.encode(FORMAT))   
            sck.recv(1024)
            sck.sendall(pswd.encode(FORMAT))

            #Receive login check
            msg = sck.recv(1024).decode(FORMAT)
            print(msg)
            if (msg == FAIL):
                curFrame.label_notice["text"] = "Invalid user or password"
                curFrame.label_notice["bg"] = notice_color

            elif msg == LIVE_EXIST:
                curFrame.label_notice["text"] = "This account is already in use"
                curFrame.label_notice["bg"] = notice_color

            else:
                self.showpage(Homepage)
                my_user = user
                print("Your user login: ",user)
                
                
        except:
            curFrame.label_notice["text"] = "Server is not responding"
            curFrame.label_info["bg"] = notice_color

    
    def signUp(self,curFrame, sck):    
        global my_user

        try:
        
            user = curFrame.entry_user.get()
            pswd = curFrame.entry_pswd.get()

            if pswd == "":
                curFrame.label_notice["text"] = "password cannot be empty"
                return 
            else:
                curFrame.label_notice["text"] = ""


            #notice server for starting log in
            option = SIGNUP
            sck.sendall(option.encode(FORMAT))
            
            
            #send username and password to server
            sck.sendall(user.encode(FORMAT))
            print("input:", user)

            sck.recv(1024)
            print("s responded")

            sck.sendall(pswd.encode(FORMAT))
            print("input:", pswd)


            # see if login is accepted
            msg = sck.recv(1024).decode(FORMAT)
            print("accepted: "+ msg)

            if msg == OK:
                self.showpage(Homepage)
                curFrame.label_notice["text"] = ""
                my_user = user

            else:
                curFrame.label_notice["text"] = "username already exists"
                curFrame.label_notice["bg"] = notice_color


        except:
            curFrame.label_notice["text"] = "Server is not responding"
            curFrame.label_info["bg"] = notice_color
    
    def logOut(self ,curFrame,sck):
        try:
            option = LOGOUT
            sck.sendall(option.encode(FORMAT))
            self.showpage(Startpage)
        except:
            curFrame.label_notice["text"] = "Server is not responding"
            curFrame.label_info["bg"] = notice_color


    def search_country(self,curFrame,sck):
        try:
            country = curFrame.entry_country.get()
            if (country == ""):
                curFrame.label_notice["text"] = "Fields can not be empty"
                curFrame.label_info["text"] = ""
                curFrame.label_info["bg"] = BG_color

                curFrame.label_notice["bg"] = notice_color
                return
            else:
                curFrame.label_notice["text"] = ""

            #Send option
            option = SEARCH
            sck.sendall(option.encode(FORMAT))

            #Send country
            sck.sendall(country.encode(FORMAT))   

        
            #Receive covid info
            msg = sck.recv(1024)
            data_country = pickle.loads(msg)
            
            if (data_country == FAIL):
                curFrame.label_notice["text"] = "Country not found"
                curFrame.label_info["text"] = ""
                curFrame.label_info["bg"] = BG_color

                curFrame.label_notice["bg"] = notice_color         
            else:
                text = show_country(data_country)
                curFrame.label_info["text"] = 'COVID 19 Information\n'+text
                curFrame.label_info["bg"] = entry_color


            
        except:
            curFrame.label_notice["text"] = "Server is not responding"
            curFrame.label_info["bg"] = notice_color
    

    def Update(self, curFrame, sck):
        try:
            country = curFrame.entry_country.get()

            if (country == ""):
                curFrame.label_notice["text"] = "Fields can not be empty"
                return
            else:
                curFrame.label_notice["text"] = "" 
            
            option = UP_DATE
            sck.sendall(option.encode(FORMAT))

            sck.sendall(country.encode(FORMAT))


            msg = sck.recv(1024)
            data_country = pickle.loads(msg)

            if (data_country == FAIL):
                curFrame.label_notice["text"] = "Country not found"
                curFrame.label_info["text"] = ""
                curFrame.label_info["bg"] = BG_color
                curFrame.label_notice["bg"] = notice_color  
         
            else:
                msg = sck.recv(1024).decode(FORMAT)
                if msg == OK:
                    curFrame.label_notice["text"] = "Update Successfully, please Search Again!"
                    curFrame.label_info["text"] = ""
                    curFrame.label_info["bg"] = BG_color

                    curFrame.label_notice["bg"] = notice_color
                    
                else:
                    curFrame.label_notice["text"] = "Unsuccessfully"
                    curFrame.label_info["text"] = ""
                    curFrame.label_info["bg"] = BG_color

                    curFrame.label_notice["bg"] = notice_color

        except:
            curFrame.label_notice["text"] = "Server is not responding"
            curFrame.label_info["bg"] = notice_color   

    '''
    def Exit(self,sck):
        try: 
            option = EXIT 
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                sck.sendall(option.encode(FORMAT))
                self.destroy()
            else:
                option = 'continue'
                sck.sendall(option.encode(FORMAT))
        except:
            pass
    '''
#----------------------- MAIN ------------------------------
my_user = 'none'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,SERVER_PORT))
print("CLIENT")

app = App()
try:
    app.mainloop()
    print(my_user)
except:
    print("server is not responding")
    client.close()

finally:
    client.close()
