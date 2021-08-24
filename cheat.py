import selfpy as discord
import random
import json
import datetime
import asyncio
import requests
import re
#custom exception class
class relogin(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
    
def check_token(token):
    response = requests.get('https://discord.com/api/v6/auth/login', headers={"Authorization": token})
    return True if response.status_code == 200 else False
DCL = discord.Client()
async def cheat():
    if runtime_broker.is_running == 0:
        return
    while 1:
        try:
            #wait till client ready
            await DCL.wait_until_ready()
            message = get_command_message()
            while  1:
                message = nextmessage
                nextmessage = get_command_message()
                #send message to the channel
                waitbefore(message, nextmessage)
                if runtime_broker.is_running:
                    await DCL.send_message(DCL.get_channel(settings["channel"]), message)
                else:
                    while not runtime_broker.is_running:
                        await asyncio.sleep(1)
                    await DCL.send_message(DCL.get_channel(settings["channel"]), message)
                if message == "owo hunt":
                    #check gems
                    #check_gems()
                    pass
        except:
            pass
#create loop in discord client
DCL.loop.create_task(cheat())
global settings
try:
    import colorama
    colorama.init()
    colorize_info = lambda time, text: colorama.Fore.GREEN + time + colorama.Fore.RESET + " " + text
    colorize_error = lambda time, text: colorama.Fore.RED + time + colorama.Fore.RESET + " " + text
    colorize_warning = lambda time, text: colorama.Fore.YELLOW + time + colorama.Fore.RESET + " " + text
except ImportError:
    print("Suggested module not found::: Colorama")
    colorize_info = lambda time, text: time+text
    colorize_error = lambda time, text: time+text
    colorize_warning = lambda time, text: time+text
class runtime_broker:
    is_running = 0
    is_ready = 0
class log:
    #function for print info
    def info(text):
        #print time and text colored
        print(colorize_info(str(datetime.datetime.now()), text))
    #function for print error
    def error(text):
        #print time and text colored
        print(colorize_error(str(datetime.datetime.now()), text))
    #function for print warning
    def warning(text):
        #print time and text colored
        print(colorize_warning(str(datetime.datetime.now()), text))
#open settings.cfg create if not exists
try:
    f = open('settings.cfg')
    try:
        settings = json.load(f)
    except json.JSONDecodeError:
        raise(FileNotFoundError)
    try:
        settings["token"]
        try:
            print("Login as "+settings['username']+"? ")
        except KeyError:
            print("Login as Unknown User? ")
        print("y/n")
        if input().lower() == "y":
            pass
        else:
            raise(relogin)
    except KeyError:
        print("Error: No token found in settings.cfg")
        raise(FileNotFoundError)
    except discord.LoginFailure:
        print("Error: Invalid token in settings.cfg")
        raise(FileNotFoundError)
    except relogin:
        print("Relogin")
        raise(FileNotFoundError)
    except:
        print("Error: Unexpected error")
        raise(FileNotFoundError)
    finally:
        f.close()
    #chech token
    if not check_token(settings["token"]): 
        print('Invalid token')
        raise(FileNotFoundError)

except FileNotFoundError:
    #ask token
    while 1:
        print('Please enter your token:')
        token = input()
        if check_token(token):
            break
        else:
            print("Invalid token")

@DCL.event
async def on_ready():
    print('Logged in')
    if not runtime_broker.is_ready:
        runtime_broker.is_ready = 1
        runtime_broker.is_running = 1
        log.info("Logged in as " + DCL.user.name + "(" + str(DCL.user.id) + ")")
        await DCL.logout()
loop = asyncio.get_event_loop()
loop.run_until_complete(DCL.start(settings["token"]))
log.info("Logged out")


print("Do you want to save the token for "+DCL.user.name+" (y/n)?")
answer = input()
settings = {'token':settings["token"], 'server': None, 'channel': None, 'username': DCL.user.name}
if answer == 'y':
    with open('settings.cfg', 'w') as f:
        json.dump(settings, f)
else:
    print(answer, 'Token not saved')

#server name by id
def server_name(id):
    for server in DCL.guilds:
        if server.id == id:
            return server.name
    return "Unknown"
#channel name by id
def channel_name(id):
    for server in DCL.guilds:
        for channel in server.channels:
            if channel.id == id:
                return channel.name
    return "Unknown"
#update settings.cfg
def update_settings(setting, value):
    with open('settings.cfg', 'r') as f:
        settings = json.load(f)
        settings[setting] = value
        #save settings
        with open('settings.cfg', 'w') as f:
            json.dump(settings, f)
print("Welcome "+DCL.user.name+"!")
try:
    settings["server"]
except KeyError:
    settings["server"] = False
try:
    settings["channel"]
except KeyError:
    settings["channel"] = False
if settings["server"] and settings["channel"]:
    print("You are currently in "+server_name(settings["server"])+" on "+channel_name(settings["channel"])+".")
    print("you can change this in settings.cfg or use settings.py")
else:
    print("You need to select a server and channel to use the cheat")
    print("Please select a server:")
    servers, i= [], 0
    for server in DCL.guilds:
        servers.append(server.id)
        print(i, server.name, server.id, "\n")
        i += 1
    while 1:
        try:
            x = int(input())
            if x >= 0 and x < len(servers):
                settings["server"] = servers[x]
                break
            else:
                print("Invalid server")
        except ValueError:
            print("Invalid server")
        except:
            print("Unexpected error")
    print("Please select a channel:")
    channels, i, err= [], 0, []
    for server in DCL.guilds:
        if server.id == settings["server"]:
            for channel in server.channels:
                if isinstance(channel, discord.TextChannel):
                    permissions = server.me.permissions_in(channel)
                    if not permissions.read_messages:
                        err.append("Channel "+channel.name+" is not readable")
                    elif not permissions.send_messages:
                        err.append("Channel "+channel.name+" is not writable")
                    else:
                        channels.append(channel.id)
                        print(i, channel.name, channel.id, "\n")
                        i += 1
    print("\n".join(err))
    while 1:
        try:
            x = int(input())
            if x >= 0 and x < len(channels):
                settings["channel"] = channels[x]
                break
            else:
                print("Invalid channel")
        except ValueError:
            print("Invalid channel")
        except:
            print("Unexpected error")
    print("You are now in "+server_name(settings["server"])+" on "+channel_name(settings["channel"])+".")
    try:
        update_settings("server", settings["server"])
        update_settings("channel", settings["channel"])
        print("you can change this in settings.cfg or use settings.py")
    except:
        print("Unable to update config")
        print("Error: Unexpected error")
    
def issuechecker(message):
    #RETURN TRUE İF İSSUE
    #RETURN FALSE IF SAFE   

    ###CHECK WARNİNG AND BANNED STATUS
    ##check if the user warned with captcha
    if "**"+DCL.user.name+"**! Please complete your captcha to verify that you are human!" in message.content:
        regex_expression = "((\([1-5]/5\))"
        regex_result = re.search(regex_expression, message.content)
        if regex_result:
            log.warning("User "+DCL.user.name+" has been warned for captcha"+print(regex_result.group(0))+"/5")
            return 1
    ##check if the user is banned
    if "**"+DCL.user.name+"**!  You have been banned for" in message.content:
        regex_expression =  "( [1-9]H )"
        regex_result = re.search(regex_expression, message.content)
        if regex_result:
            log.warning("User "+DCL.user.name+" has been banned for "+regex_result.group(0)+" hours")
            return 1

def boxchecker(message):
    if "**"+DCL.user.name+"**, You found a" in message.content:
        if "weapon" in message.content:
            #use wb all
            regex_expression = "(\[[1-3]/3\])"
            regex_result = re.search(regex_expression, message.content)
            if regex_result:
                log.info("User "+DCL.user.name+" has found a weapon box "+regex_result.group(0)+"/3")
                if int(regex_result.group(0)[1]) == 3:
                    log.info("+regex_result.group(0)+"+"Weapon box will be opened because :: WHEN FULL OPEN ALL")
                    #send message to the channel
                    DCL.send_message(DCL.get_channel(settings["channel"]), "owo wb all")
                elif random.randint(0,3) == 0:
                    log.info("+regex_result.group(0)+"+"Weapon box will be opened because :: %33 OPEN IT INSTANTLY")
                    #send message to the channel
                    DCL.send_message(DCL.get_channel(settings["channel"]), "owo wb all")

                    return 1
        elif "lootbox" in message.content:
            #use lb all
            regex_expression = "(\[[1-3]/3\])"
            regex_result = re.search(regex_expression, message.content)
            if regex_result:
                log.info("User "+DCL.user.name+" has found a lootbox "+regex_result.group(0)+"/3")
                if int(regex_result.group(0)[1]) == 3:
                    log.info("+regex_result.group(0)+"+"Lootbox will be opened because :: WHEN FULL OPEN ALL")
                    #send message to the channel
                    DCL.send_message(DCL.get_channel(settings["channel"]), "owo lb all")
                elif random.randint(0,3) == 0:
                    log.info("+regex_result.group(0)+"+"Lootbox will be opened because :: %33 OPEN IT INSTANTLY")
                    #send message to the channel
                    DCL.send_message(DCL.get_channel(settings["channel"]), "owo lb all")
#gem checker
def gemchecker(message):
    ##USE ONLY AFTER HUNT
    gems = {
        "Lucky": [ #Heart gem
            #from common to fabled
            ## Common, Uncommon, Rare, Epic, Mystical, Legendary, Fabled
            510366763255463936, #common
            510366764249382922, #uncommon
            0, #Rare | UNKNOWN
            0, #Epic
            0, #Mystical
            0, #Legendary
            0 #Fabled
        ],
        "Empowering": [ #Round gem
            #from common to fabled
            ## Common,Uncommon,Rare,Epic,Mystical,Legendary,Fabled
            510366792024195072, #Common
            510366792095367189, #Uncommon
            0, #Rare | UNKNOWN
            510366792800272394, #Epic
            510366792447819777, #Mystical
            0, #Legendary | UNKNOWN
            0 #Fabled | UNKNOWN
        ],
        "Hunting": [ #Diamond gem
            #from common to fabled
            ## Common,Uncommon,Rare,Epic,Mystical,Legendary,Fabled
            0, #Common | UNKNOWN
            492572122514980864, #Uncommon
            492572122888011776, #Rare
            492572122477101056, #Epic
            492572122590478356, #Mystical
            492572124251422720, #Legendary
            0 #Fabled | UNKNOWN
        ]
    }
    if "**"+DCL.user.name+"**, You found a" in message.content:
        if "gem" in message.content:
            #use wb all
            regex_expression = "(\[[1-3]/3\])"
            regex_result = re.search(regex_expression, message.content)
            if regex_result:
                log.info("User "+DCL.user.name+" has found a gem "+regex_result.group(0)+"/3")
                if int(regex_result.group(0)[1]) == 3:
                    log.info("+regex_result.group(0)+"+"Gem will be opened because :: WHEN FULL OPEN ALL")
                    #send message to the channel
                    DCL.send_message(DCL.get_channel(settings["channel"]), "owo lb all")
                elif random.randint(0,3) == 0:
                    log.info("+regex_result.group(0)+"+"Gem will be opened because :: %33 OPEN IT INSTANTLY")
                    #send message to the channel
                    DCL.send_message(DCL.get_channel(settings["channel"]), "owo lb all")


#on message
@DCL.event
async def on_message(message):
    if message.author == DCL.user:
        return
    elif message.author.id == 408785106942164992: 
        #print the message received with log info
        log.info(message.content)

async def waitbefore(message1, message2):
    #hunt battle 2 times
    if any (message1 == x for x in ["owo hunt", "owo battle"]) and any (message1 == x for x in ["owo hunt", "owo battle"]):
        if settings.humanize_time:
            r = random.randint(random.randint(10,15), random.randint(20,25))
            await asyncio.sleep(r)
        else:
            r = random.randint(15,20)
            await asyncio.sleep(r)
def get_command_message():
    return random.choice([
    "owo hunt", "owo battle"
    ])
#connect gateway
loop.run_until_complete(DCL.start(settings["token"]))