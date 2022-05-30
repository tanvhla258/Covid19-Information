import socket, pickle
import time
import threading   
import pyodbc
import requests
import json
import tkinter as tk

from tkinter import messagebox




#can add IP addr in your computer
HOST =  "127.0.0.1"
SERVER_PORT = 64444
FORMAT = "utf8"
LOGIN = "login"
END = "x"
FAIL = "fail"
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


def GetAPI():
    url = 'https://coronavirus-19-api.herokuapp.com/countries'
    resp = requests.get(url).text
    data = json.loads(resp)
    with open('Api.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data
    
def ConnectToDBCountry():
    conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-12J6D6C\SQLEXPRESS;Database=API;UID=user;PwD=123456;')

    cursor = conx.cursor()
    return cursor

def ConnectToDBAccount():
    conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-12J6D6C\SQLEXPRESS;Database=Socket_Account;UID=user;PwD=123456;')

    cursor = conx.cursor()
    return cursor

def Insert_Acc(user,pswd):
    conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-12J6D6C\SQLEXPRESS;Database=Socket_Account;UID=user;PwD=123456;')

    cursor = conx.cursor()
    cursor.execute("insert Account values (?,?)",user,pswd)
    cursor.commit()

def Move_database(conn):
    cursor = ConnectToDBCountry()

    country = conn.recv(1024).decode(FORMAT)  

    cursor.execute("select * from Country where country = ?", country)

    data_country = cursor.fetchone()
    if data_country != None:
        print("OK")
        msg = pickle.dumps(data_country)
        
    else:
        msg = pickle.dumps(FAIL)
        print("no country")
    
    conn.sendall(msg)

    time.sleep(0.5)

    data = GetAPI()                      #Lay du lieu ve Covid
    for i in range(len(data)):
        if(country == data[i]['country']):
            cursor.execute("update Country set cases =?, todayCases=?, deaths=?, todayDeaths=?, recovered=?, active=?, critical=?, \
                        casesPerOneMillion=?, deathsPerOneMillion=?, totalTests=?, testsPerOneMillion=? where Country = ?", (data[i]['cases']\
                        ,data[i]['todayCases'], data[i]['deaths'], data[i]['todayDeaths'], data[i]['recovered'], data[i]['active'], data[i]['critical'],\
                            data[i]['casesPerOneMillion'], data[i]['deathsPerOneMillion'], data[i]['totalTests'], data[i]['testsPerOneMillion'], data[i]['country']))
            cursor.commit() 
            msg = OK

            conn.sendall(msg.encode(FORMAT))



def Insert_LiveAccount(user,addr):
    Ad.append(str(addr))
    ID.append(user)
    account=str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
    Live_Account.append(account)

def Remove_LiveAccount(addr):
    if(str(addr) in Ad):
        index = Ad.index(str(addr))
        Ad.remove(str(addr))
        del ID[index]
        del Live_Account[index]
    else:
        pass
def Check_LiveAccount(user):
    if user in ID:
        return True
    else:
        return False
 

def serverLogin(conn,addr):
    cursor = ConnectToDBAccount()
    user = conn.recv(1024).decode(FORMAT)
    conn.sendall(user.encode(FORMAT))  
    pswd = conn.recv(1024).decode(FORMAT)
    print(user,pswd)

    # query data: password
    cursor.execute("select pass from Account where username = ?", user)
    password = cursor.fetchone() 

    if (password != None):
        data_password = password[0]
        #verify login
        if (pswd == data_password):
            msg = OK
            if (Check_LiveAccount(user)==True):
                msg = LIVE_EXIST
            else:
                Insert_LiveAccount(user,addr)
        else:
            msg = FAIL

    else:
        msg = FAIL 
        
    conn.sendall(msg.encode(FORMAT))


def serverSignup(conn,addr):
    cursor = ConnectToDBAccount()
    user = conn.recv(1024).decode(FORMAT)
    print("username:--" + user +"--")

    conn.sendall(user.encode(FORMAT))

    pswd = conn.recv(1024).decode(FORMAT)
    print("password:--" + pswd +"--")


    cursor.execute("select * from Account where username = ?", user)
    username = cursor.fetchone()

    if (username == None):
        #Account doesn't exist
        Insert_Acc(user,pswd) 
        msg = OK
        
        Insert_LiveAccount(user,addr)
    else:
        msg = FAIL 
        print("Unsuccessfully")
    
    conn.sendall(msg.encode(FORMAT))

    

def find_country(conn):
    
    cursor = ConnectToDBCountry()
    country = conn.recv(1024).decode(FORMAT)

    cursor.execute("select * from Country where country = ?", country)

    
    data_country = cursor.fetchone()
    if data_country != None:
        print("OK")
        msg = pickle.dumps(data_country)
        
    else:
        msg = pickle.dumps(FAIL)
        print("no country")
    
    conn.sendall(msg)



def handleClient(conn: socket,addr):
    print("conn: ",conn.getsockname())
    print("adress: ",addr)

    
    while True:
        option = conn.recv(1024).decode(FORMAT)

        if option == LOGIN:
            serverLogin(conn,addr)
            print(Live_Account)

        if option == SEARCH:
            find_country(conn)    

        if option == SIGNUP:
            serverSignup(conn,addr)
 
        if option == LOGOUT:
            Remove_LiveAccount(addr) 

        if option == UP_DATE:
            Move_database(conn)

        if option == EXIT:
            Remove_LiveAccount(addr)          
            break
        

    conn.close()        

def runServer():
    try:
        print(HOST)
        print("Waiting for Client")

        while True:
            
            conn, addr = s.accept()
            
            clientThread = threading.Thread(target=handleClient, args=(conn,addr))
            clientThread.daemon = True 
            clientThread.start()

            
            #handle_client(conn, addr)
            print("end main-loop")

        
    except KeyboardInterrupt:
        print("error")
        s.close()
    finally:
        s.close()
        print("end")


class Startpage(tk.Frame):
    def __init__(self,parent,app_controller):
        tk.Frame.__init__(self,parent)
        self.configure(bg=BG_color)
        label_title = tk.Label(self, text = "Server", fg =L_color, font=("",L_size,"bold"), bg= BG_color)

        label_user = tk.Label(self, text ="username", fg =S_color , font =("",S_size),bg= BG_color)
        label_pswd = tk.Label(self, text ="password", fg =S_color, font =("",S_size),bg= BG_color)

        
        self.label_notice = tk.Label(self,text = "", bg = BG_color, font =("",S_size),)
        self.entry_user = tk.Entry(self,width = 30,bg = entry_color)
        self.entry_pswd = tk.Entry(self,width = 30,bg =entry_color)

        button_signin = tk.Button(self,text = "Log in", command = lambda: app_controller.check_admin(self), bg = entry_color)
        #button_exit = tk.Button(self,text= 'Exit', command = lambda:app_controller.Exit(self), bg = entry_color)
        
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()
        
        
        button_signin.pack()
        #button_exit.pack()

class Homepage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent) 
        self.configure(bg=BG_color)
        label_title = tk.Label(self, text="SERVER MANAGEMENT", font =("",L_size,"bold"), bg = BG_color, fg = L_color)
        label_connecting = tk.Label(self,text = "Connecting",font =("",18),bg = BG_color)
        
        self.label_LiveAcc = tk.Label(text = "",bg = BG_color,font =("",S_size))
        
        #btn_logout = tk.Button(self, text="Exit", command=lambda: app_controller.Exit(self,s))           
        button_refresh = tk.Button(self, text = "Refresh", command = lambda:app_controller.LiveAccount_control(self,Live_Account))

        label_title.place(x = 40,y=10)
        self.label_LiveAcc.place(x=165,y=150)
        button_refresh.place(x=200,y=300)
        label_connecting.place(x = 165,y = 100)

        #btn_logout.pack()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        option = ""
        self.title("Covid 19 News")
        self.geometry("400x250")
        #self.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            self.geometry("450x400")
        else:
            self.geometry("400x250")
        self.frames[FrameClass].tkraise()

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def check_admin(self,curFrame):
        user = curFrame.entry_user.get()
        pswd = curFrame.entry_pswd.get()

        if (user == "" or pswd == ""):
            curFrame.label_notice["text"] = "Fields can not be empty"
            curFrame.label_notice["bg"] = notice_color
            return
        else:
            curFrame.label_notice["text"] = ""
            curFrame.label_notice["bg"] = BG_color
        
        if (user != "admin" or pswd != "2412"):
            curFrame.label_notice["text"] = "Invalid server account"
            curFrame.label_notice["bg"] = notice_color
        else:
            self.showpage(Homepage)
    
    def LiveAccount_control(self,curFrame,list):
        try:
            acc = ''  
            if not list:
                acc =''
                curFrame.label_LiveAcc["text"] = acc
                curFrame.label_LiveAcc["bg"] = BG_color


            else:
                for item in list:
                    acc += (item +'\n')
                curFrame.label_LiveAcc["text"] = acc
                curFrame.label_LiveAcc["bg"] = entry_color
        except:
            pass

      

#------------------------- main --------------------------

# KHoi tao server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((HOST,SERVER_PORT))
s.listen()

Live_Account = [] # Ad+ID
Ad = [] # Chua dia chi
ID = [] # Chua ID
#======================================
# Connection

sThread = threading.Thread(target=runServer)
sThread.daemon = True 
sThread.start()



app = App()
app.mainloop()
s.close()
