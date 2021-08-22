#global variables
class varlib:
    G_window = None
    G_token = None
    G_username = None
    G_connected = None
    G_server = None
    G_channel = None
    G_remember_me = None
    G_messages_list = None
    w_method = "terminal"
    loginbuttontext = None

from tkinter.constants import S
import selfpy as discord
import asyncio, json, os, sys
class settings_raw:
    def __init__(self):
        self.settings = {
            "server": "",
            "channel": "",
            "token": "",
            "force_gui": ""
        }
        #open file
        try:
            with open("settings.json", "r") as f:
                x = json.load(f)
                if x["server"] and x["channel"] and x["token"]:
                    self.settings = x
                
        except:
            #create file
            with open("settings.json", "w") as f:
                json.dump(self.settings, f)
    token = property(lambda self: self.settings["token"])
    server = property(lambda self: self.settings["server"])
    channel = property(lambda self: self.settings["channel"])
    force_gui = property(lambda self: self.settings["force_gui"])
    def update(self, what, value):
        self.settings[what] = value
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)
settings = settings_raw()
class log:
    def __init__(self):
        self.logfile = open("log.txt", "a")
        self.logfile.write("\n\nNEW SESSION\n")
    def write(self, text):
        self.logfile.write(text)
try:
    import tkinter
    varlib.w_method = "tkinter"
except ImportError:
    try:
        import Tkinter as tkinter
        varlib.w_method = "tkinter"
    except ImportError:
        log.info("Unable to import tkinter, falling back to terminal")
        varlib.w_method = "terminal"
def killwindow():
    if varlib.G_window:
        varlib.G_window.destroy()
    varlib.G_window = False
if varlib.w_method == "tkinter":
    varlib.loginbuttontext = tkinter.StringVar().set("Login")    
#create 2 async loop
loop = asyncio.get_event_loop()
loop2 = asyncio.get_event_loop()
class window:
    async def loginpanel():
        if varlib.w_method == "tkinter": # if we use tkinter
            if varlib.G_window == None: # if we use tkinter and we didn't create a window yet
                #create window
                varlib.G_window = tkinter.Tk()
            else:
                #clear the window
                for i in varlib.G_window.winfo_children():
                    i.destroy()
            #main window settings
            varlib.G_window.title("Login - dsoc")
            varlib.G_window.configure(background='black')
            #add login widgets
            G_token_label = tkinter.Label(varlib.G_window, text="Enter Token", bg='black', fg='white', font=('Helvetica', 16))
            G_token_label.pack()
            G_token = tkinter.StringVar()
            G_token.set(settings.token)
            G_token_entry = tkinter.Entry(varlib.G_window, textvariable=G_token, bg='black', fg='white', font=('Helvetica', 16), show="*")
            G_token_entry.pack()
            #add remember me checkbox
            G_remember_me = tkinter.IntVar()
            G_remember_me.set(0)
            G_remember_me_checkbox = tkinter.Checkbutton(varlib.G_window, text="Remember me", variable=G_remember_me, bg='black', fg='white', font=('Helvetica', 16))
            G_remember_me_checkbox.pack()
            #add login button text variable
            G_login_button = tkinter.Button(varlib.G_window, textvariable=varlib.loginbuttontext, bg='black', fg='white', font=('Helvetica', 16), command=lambda: login_bridge(G_token.get(), G_remember_me.get()))
            G_login_button.pack()
            #finish
            asyncio.ensure_future(varlib.G_window.mainloop())
            async def update_window():
                while True:
                    await asyncio.sleep(0.1)
                    if varlib.G_window:
                        #update idle tasks
                        varlib.G_window.update_idletasks()
            asyncio.ensure_future(update_window())
        elif varlib.w_method == "terminal": # if we use terminal
            #clear the terminal according to the OS
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
            if not settings.token == "":
                print("Saved Token: " + "*"*len(settings.token)-5+settings.token[-5:]+"\n\n Logged in with saved token")
            else:
                #ask for token
                settings.update("token", input("Enter Token: "))
            if await login(settings.token, 1) == 0:
                print("Login failed")
                sys.exit(1)
def update_window_state_logged_in():
    #clear the window
    for i in varlib.G_window.winfo_children():
        i.destroy()
    #main window settings
    varlib.G_window.title("dsoc")
    varlib.G_window.configure(background='black')
    #add topbar
    G_topbar = tkinter.Frame(varlib.G_window, bg='orange')
    #add topbar widgets
    #add varlib.G_username
    G_username_label = tkinter.Label(G_topbar, textvariable=varlib.G_username, bg='orange', fg='white', font=('Helvetica', 16))
    G_username_label.pack()
    #add varlib.G_connected
    G_connected_label = tkinter.Label(G_topbar, textvariable=varlib.G_connected, bg='orange', fg='white', font=('Helvetica', 16))
    G_connected_label.pack()
    #add bottombar
    G_bottombar = tkinter.Frame(varlib.G_window, bg='orange')
    #add bottombar widgets
    #add varlib.G_server, channel
    G_server_label = tkinter.Label(G_bottombar, textvariable=varlib.G_server, bg='orange', fg='white', font=('Helvetica', 16))
    G_server_label.pack()
    G_channel_label = tkinter.Label(G_bottombar, textvariable=varlib.G_channel, bg='orange', fg='white', font=('Helvetica', 16))
    G_channel_label.pack()
    #add messages list
    varlib.G_messages_list = tkinter.Listbox(G_window, bg='orange', fg='white', font=('Helvetica', 16))
    varlib.G_messages_list.pack()
def add_message(message):
    varlib.G_messages_list.insert(tkinter.END, message)
    varlib.G_messages_list.see(tkinter.END) 
async def login(token, remember):
    varlib.loginbuttontext = tkinter.StringVar().set("logging in")
    await discord.client.login(token)
    update_window_state_logged_in()
    varlib.G_connected = "Connected"
    varlib.loginbuttontext = tkinter.StringVar().set("login")
    varlib.G_username = discord.client.user.name

def login_bridge(token, remember):
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(login(token, remember))

asyncio.run(window.loginpanel())

