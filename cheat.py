import subprocess
import sys

try:
    import sentry_sdk
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sentry_sdk"])
    import sentry_sdk
finally:
    sentry_sdk.init(
    "https://eabaa0df4a2e43f78b2fd8bac57cacc2@o985801.ingest.sentry.io/5943549",
    traces_sample_rate=1.0
    )
    print("sentry issue tracer running")
try:
    import selfpy as discord #pip installation overrides for discord.py
except:
    import setup
    setup.main()
finally:
    import selfpy as discord
import os #used to restart
import sys #used to restart
import random #used to get random seconds
import json 
import datetime #used in log class
import asyncio #used in token checker
import requests #idk where tf i used this
import re #used in gemchecker_inventory
import base64 #used for auto captcha solver
import aiohttp 
async def captcha_solver(message):
    
    #return 1 if solveable
    #return 0 if not solveable

    captcha_image = message.attachments[0]
    captcha_image_url = captcha_image.url
    #use a web service to solve captcha
    #if captcha solving service is enabled
    if settings["captchaservice"]["use_service_to_solve_captchas"] == True:
        #get captcha service name
        captcha_service = settings["captchaservice"]["captcha_service"]
        #switch captcha service
        if captcha_service == "anti-captcha":
            ## api docs : https://anti-captcha.com/tr/apidoc/methods/createTask
            #url: https://api.anti-captcha.com/createTask
            #Type: POST
            #Content-type: application-json
            

            #response when no error
            #{
            #    "errorId": 0,
            #    "taskId": 7654321
            #}

            #response when error
            #{
            #    "errorId": 1,
            #    "errorCode": "ERROR_KEY_DOES_NOT_EXIST",
            #    "errorDescription": "Account authorization key not found in the system"
            #}
            #get captcha api key from settings
            api_key = settings["captchaservice"] ["api_key"]
            #download captcha image get base64 use aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(captcha_image_url) as resp:
                    image_data = await resp.read()
            #encode image to base64
            image_data_base64 = base64.b64encode(image_data).decode('utf-8')

            post_data = {
            "clientKey": api_key,
            "task":
                {
                    "type":"ImageToTextTask",
                    "body":image_data_base64,
                    "phrase":False,
                    "case":False,
                    "numeric":0,
                    "math":False,
                    "minLength":0,
                    "maxLength":0,
                    "websiteURL": "discord selfbot owo bot by sudo-do"
                }
            }
            #send post request
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.anti-captcha.com/createTask', json=post_data) as resp:
                    response = await resp.json()
            #get_task_status
            async def get_task_status(task_id):
                #url: https://api.anti-captcha.com/getTaskResult
                #Type: POST
                #Content-type: application-json
                #response when no error
                #{
                #    "errorId":0,
                #    "status":"ready",
                #    "solution":
                #        {
                #            "text":"deditur",
                #            "url":"http:\/\/61.39.233.233\/1\/147220556452507.jpg"
                #        },
                #    "cost":"0.000700",
                #    "ip":"46.98.54.221",
                #    "createTime":1472205564,
                #    "endTime":1472205570,
                #    "solveCount":"0"
                #}
                #response when error
            
                post_data = {
                "clientKey": api_key,
                "taskId": task_id
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post('https://api.anti-captcha.com/getTaskResult', json=post_data) as resp:
                        response = await resp.json()
                #check if error
                error = response["errorId"]

                #status
                status = response["status"]

                if error:
                    #log error
                    log.error("CAPTCHA SERVICE ERROR: "+str(response["errorDescription"]))
                    print(response)
                    return False
                else:
                    return status
            #get task result
            async def get_task_result(task_id):
                #url: https://api.anti-captcha.com/getTaskResult
                #Type: POST
                #Content-type: application-json
                #response when no error
                #{
                #    "errorId":0,
                #    "status":"ready",
                #    "solution":
                #        {
                #            "text":"deditur",
                #            "url":"http:\/\/61.39.233.233\/1\/147220556452507.jpg"
                #        },
                #    "cost":"0.000700",
                #    "ip":"46.98.54.221",
                #    "createTime":1472205564,
                #    "endTime":1472205570,
                #    "solveCount":"0"
                #}
                #response when error
            
                post_data = {
                "clientKey": api_key,
                "taskId": task_id
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post('https://api.anti-captcha.com/getTaskResult', json=post_data) as resp:
                        response = await resp.json()
                #check if error
                error = response["errorId"]

                #status
                status = response["status"]

                if error:
                    #log error
                    log.error("CAPTCHA SERVICE ERROR: "+str(response["errorDescription"]))
                    print(response)
                    return False
                else:
                    return response["solution"]["text"]
            if response["errorId"] == 0:
                #get task id
                task_id = response["taskId"]
                #get task status
                task_status = await get_task_status(task_id)
                #check if solved
                while task_status != "ready":
                    await asyncio.sleep(5)
                    task_status = await get_task_status(task_id)
                #get task result
                task_result = await get_task_result(task_id)
                #return result
                await message.channel.send(task_result)
                #check if we successed
                captcha_response_response = await DCL.wait_for('message', check=lambda message: message.author == message.author and any(x in message.content for x in ["Wrong verification code!", "I have verified that you are human!"]))
                if "Wrong verification code!" in captcha_response_response.content:
                    #log error and stop program
                    log.error("CAPTCHA ERROR: Wrong verification code!")
                    log.warning("CAPTCHA WARNING: Please solve the captcha soon!")
                    await DCL.close()
                elif "I have verified that you are human!" in captcha_response_response.content:
                    #log success
                    log.info("CAPTCHA SUCCESS: Verified!")
                    runtime_broker.is_running = True
        else:
            log.error("Captcha service not supported | "+captcha_service)
            return 0

def check_token(token):
    response = requests.get('https://discord.com/api/v6/auth/login', headers={"Authorization": token})
    return True if response.status_code == 200 else False
DCL = discord.Client()
actionafter = None
async def cheat():
    await DCL.wait_until_ready()
    while 1:
        try:
            message = get_command_message()
            while  1:
                nextmessage = get_command_message()
                message = nextmessage
                #send message to the channel
                await waitbefore(message, nextmessage)
                if runtime_broker.is_running:
                    await send_message_with_logging(message)
                else:
                    while not runtime_broker.is_running:
                        await asyncio.sleep(1)
                    await send_message_with_logging(message)
                if message == "owo hunt":
                    #check gems

                    try:
                        msg = await DCL.wait_for('message', check=gemchecker_inventory, timeout=30)
                    except asyncio.TimeoutError:
                        log.warning("Hunt action message didn't received in time, gem checking ignored. TIMEOUT 30")
                        continue
                    
        except Exception as e:
            log.error("Error in main cheat loop: "+str(e))
            pass
#create loop in discord client
global settings, prerun, owoid
owoid = 408785106942164992
prerun = False
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
    prerun = True
    while 1:
        print('Please enter your token:')
        token = input()
        if check_token(token):
            break
        else:
            print("Invalid token")
    print("Do you want to save the token (y/n)?")
    answer = input()
    settings = {'token':token, 'server': None, 'channel': None, 'username': None, 'humanize_time': True}
    if answer == 'y':
        with open('settings.cfg', 'w') as f:
            json.dump(settings, f)
    else:
        print(answer, 'Token not saved')
if settings["server"] == None or settings["server"] == False:
    prerun = True
if settings["channel"] == None or settings["channel"] == False:
    prerun = True
@DCL.event
async def on_ready():
    print('Logged in')
    if not runtime_broker.is_ready:
        runtime_broker.is_ready = 1
        runtime_broker.is_running = 1
        #update settings with username
        settings["username"] = DCL.user.name
        #save settings
        with open('settings.cfg', 'w') as f:
            json.dump(settings, f)
        log.info("Logged in as " + DCL.user.name + "(" + str(DCL.user.id) + ")")
        await DCL.close()
if prerun:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DCL.start(settings["token"]))
    log.info("Logged out")



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
print("Welcome "+settings["username"]+"!")
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
if prerun:
    log.info("Restart the script to run")
    exit(0)

def issuechecker(message):
    #RETURN TRUE İF İSSUE
    #RETURN FALSE IF SAFE   
    #++ RETURN 2 İF USE CAPTCHA SOLVİLNG SERVİCE
    ###CHECK WARNİNG AND BANNED STATUS
    ##check if the user warned with captcha
    log.info("issue checker handled message "+str(message.id))
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
    ###check if message has attachment
    if message.attachments:
        for attachment in message.attachments:
            #if message attachment name is captcha.*
            if attachment.filename.startswith("captcha"):
                log.warning("User "+DCL.user.name+" has been received a captcha")
                if settings["captchaservice"]["use_service_to_solve_captchas"] == True:
                    log.info("Captcha service is enabled\nTrying to solve the captcha with service")
                    return 2
                else:
                    log.error("Captcha solving service is not enabled")
                    return 1
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
                    send_message_with_logging("owo wb all")
                elif random.randint(0,3) == 0:
                    log.info("+regex_result.group(0)+"+"Weapon box will be opened because :: %33 OPEN IT INSTANTLY")
                    #send message to the channel
                    send_message_with_logging("owo wb all")

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
                    send_message_with_logging("owo lb all")
                elif random.randint(0,3) == 0:
                    log.info("+regex_result.group(0)+"+"Lootbox will be opened because :: %33 OPEN IT INSTANTLY")
                    #send message to the channel
                    send_message_with_logging("owo lb all")
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
                    send_message_with_logging("owo lb all")
                elif random.randint(0,3) == 0:
                    log.info("+regex_result.group(0)+"+"Gem will be opened because :: %33 OPEN IT INSTANTLY")
                    #send message to the channel
                    send_message_with_logging("owo lb all")
def trace_gems(message):
    # gemchecker.gems.ids # emoji id of the gems

    text = message.content

    try:
        text = text.split("hunt is empowered by")[1].split("!")
    except IndexError:
        log.info("no gems used")
        for gemtype in userdata.active_gems:
            userdata.active_gems[gemtype] = 0
    #find gems in text update actively 
    # # userdata.active_gems
    for gemtype in gemchecker.gems.ids:
        for gem in gemtype:
            if gem in text:
                userdata.active_gems[gemtype] = gemchecker.gems.codes[gemchecker.gems.ids[gemtype].index(gem)]

#gem checker
class userdata:
    active_gems = {
        "hunting": None,
        "empowering": None,
        "lucky": None
    }
    inventory =  {
        #hunting
        51: 0,
        52: 0,
        53: 0,
        54: 0,
        55: 0,
        56: 0,
        57: 0,
        #empowering
        65: 0,
        66: 0,
        67: 0,
        68: 0,
        69: 0,
        70: 0,
        71: 0,
        #Lucky
        72: 0,
        73: 0,
        74: 0,
        75: 0,
        76: 0,
        77: 0,
        78: 0
    }
    owocash = None

class gemchecker:

    class gems:
        #use id of the gems to dedect them
        ids = {
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
        #use code of the gem to dedect them
        codes = {
            "Hunting": [ #Diamond gem
                #from common to fabled
                ## Common,Uncommon,Rare,Epic,Mystical,Legendary,Fabled
                51, #Common
                52, #Uncommon
                53, #Rare
                54, #Epic
                55, #Mystical
                56, #Legendary
                57 #Fabled | UNKNOWN
            ],
            "Empowering": [ #Round gem
                #from common to fabled
                ## Common,Uncommon,Rare,Epic,Mystical,Legendary,Fabled
                65, #Common
                66, #Uncommon
                67, #Rare
                68, #Epic
                69, #Mystical
                70, #Legendary
                71 #Fabled | UNKNOWN
            ],
            "Lucky": [ #Heart gem
                #from common to fabled
                ## Common,Uncommon,Rare,Epic,Mystical,Legendary,Fabled
                72, #common
                73, #uncommon
                74, #rare
                75, #Epic
                76, #Mystical
                77, #Legendary
                78 #Fabled | UNKNOWN
            ],
        }  
    async def check_missing_gems(message): #use after every hunt, to the hunt message
        m = message.content
        for gtype in gemchecker.gems.ids:
            for gid in gemchecker.gems.ids[gtype]:
                if gid in m:
                    pass
                else:
                    #parse inventory
                    _ = False
                    for gid in gemchecker.gems.codes[gtype]:
                        log.info("Gem "+str(gid)+" which is class "+gtype+" missing")
                        if not _:
                            if userdata.inventory[gid] > 0:
                                log.info("Gem "+str(gid)+" will be used")
                                await use_gem(message,gid)
                                userdata.inventory[gid] -= 1
                                
                                _ = True
async def use_gem(message,gid):
    await send_message_with_logging(message.channel, "owo use "+str(gid))

async def fill_gems():
    for gemtype in userdata.active_gems:
        
        
 
async def update_inventory():
    await send_message_with_logging("owo inv")
    log.info("Updating inventory")
    await DCL.wait_for('message', check=lambda message: message.author.id == owoid and "Inventory" in message.content)
    #normalize the message as a fuckin markdown is the ast thing we want in this script
    m = message.content.replace("**", "")
    m = m.replace("*", "")
    #cut head to hold inventory as is
    m = m.strip("=")[-1]
    #remove emojis
    #replace everything between < and > with ""
    m = re.sub(r"<(.*?)>", "", m)

    # EXPECTİNG RESULT
    # "\n`52`\u2070\u00b9    `53`\u2070\u00b9    `54`\u2070\u00b9    `55`\u2070\u00b2\n`56`\u2070\u00b9    `65`\u2070\u00b9    `66`\u2070\u00b2    `68`\u2070\u00b2\n`69`\u2070\u00b3    `72`\u2070\u2079    `73`\u2070\u2074    `75`\u2070\u2075\n`100`\u00b9\u2078    `103`\u2070\u00b9    `110`\u2070\u00b9    `111`\u2070\u00b9\n`2--`\ud83d\uddbc\u2070\u00b9"
    #call superscript_normalizer
    m = superscript_normalizer(m)
    #now we have '\n`52`01    `53`01    `54`01    `55`02\n`56`01    `65`01    `66`02    `68`02\n`69`03    `72`09    `73`04    `75`05\n`100`18    `103`01    `110`01    `111`01\n`2--`\ud83d\uddbc01'
    #remove all the newlines
    m = m.replace("\n", "    ")
    #split the string by spaces
    m = m.split("    ")
    #drop the first element
    m = m[1:]
    #for each element in the list remove the first character
    for i in range(len(m)):
        #remove the first character
        m[i] = m[i][1:]
    inventory = {}
    #inventory syntax:: item[int] = amount[int]
    #for each element strip with ` and save it to the dict
    for i in m:
        #split the string by `
        i = i.split("`")
        #save the item to the dict
        inventory[int(i[0])] = int(i[1])
    #now the dict is like
    #{
        #item id: amount
    #}
    #delete items over 100
    for i in inventory:
        if i > 100:
            #delete the item from the dict
            del inventory[i]
    userdata.inventory = inventory
    #x is total amount of gems
    x = 0
    #for each item in the inventory
    for i in inventory:
        #add the amount to x
        x += inventory[i]
    


        

        
    

def superscript_normalizer(string): #convert unicode shit in inventory message to normal text
    #small numbers called superscript numbers
    superscript_numbers = {
        "\u2070": "0",
        "\u00b9": "1",
        "\u00b2": "2",
        "\u00b3": "3",
        "\u2074": "4",
        "\u2075": "5",
        "\u2076": "6",
        "\u2077": "7",
        "\u2078": "8",
        "\u2079": "9"
    }
    for key, value in superscript_numbers.items():
        string = string.replace(key, value)
    return string
        
        

#on message
@DCL.event
async def on_message(message):
    if message.author == DCL.user:
        return
    elif message.author.id == 408785106942164992: 
        #print the message received with log info
        issue = issuechecker(message)
        if issue == 0:
            log.info("issuechecker: safe")
        elif issue == 1:
            #captcha received, auto solve disabled
            log.warning("Captcha received, please manually solve it")
            log.info("to solve captchas automatically install a captcha solving service, read readme for more info")
            runtime_broker.is_running = 0
            log.info("waiting captcha to be solved")
            captcha_response_response = await DCL.wait_for('message', check=lambda message: message.author == message.author and any(x in message.content for x in ["Wrong verification code!", "I have verified that you are human!"]))
            if "Wrong verification code!" in captcha_response_response.content:
                #log error and stop program
                log.error("CAPTCHA ERROR: Wrong verification code!")
            elif "I have verified that you are human!" in captcha_response_response.content:
                #log success
                log.info("CAPTCHA SUCCESS: Verified!")
                runtime_broker.is_running = True
        elif issue == 2:
            #captcha received, auto solve enabled
            log.warning("Captcha received, attempting to solve it")
            #solve the captcha
            captcha_solver(message)
async def waitbefore(message1, message2):
    #hunt battle 2 times
    if any (message1 == x for x in ["owo hunt", "owo battle"]) and any (message2 == x for x in ["owo hunt", "owo battle"]):
        if settings["humanize_time"]:
            r = random.randint(random.randint(5,15), random.randint(20,25))
            await asyncio.sleep(r)
        else:
            r = random.randint(15,20)
            await asyncio.sleep(r)
    else: #falldown
        if settings["humanize_time"]:
            r = random.randint(random.randint(10,15), random.randint(15,20))
        else:
            r = random.randint(15,20)
        await asyncio.sleep(r)

def get_command_message():
    #1/15 change to get pointless message
    if random.randint(1,15) == 10:
        return random.choice([
            "owo sell all",
            "owo coinflip 5", "owo coinflip 10", "owo coinflip 25", "owo coinflip 50", "owo coinflip 100", "owo coinflip 250"
        ])
    return random.choice([
    "owo hunt", "owo battle"
    ])
#connect gateway,
#on ready

async def send_message_with_logging(message):
    #send message to channel
    await DCL.get_channel(settings["channel"]).send(message)
    #log message
    log.info("sent: "+message)
async def parse_quest(message):
    pass
    #todo
@DCL.event
async def on_ready():
    log.info("Logged in 692")
    #send message to channel
    m = [
        "owo quest",
        "owo daily"
    ]
    await send_message_with_logging(m[0])
    await waitbefore(m[0], m[1])
    await send_message_with_logging(m[1])
    #set true runtime broker
    runtime_broker.is_running = True
    runtime_broker.is_ready = True
DCL.loop.create_task(cheat())
DCL.run(settings["token"])