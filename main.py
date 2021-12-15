import discum_c844aef
import time
import multiprocessing
import json
import random
import re
import os
try:
  from tkinter import messagebox
  use_terminal=False
except:
  use_terminal=True
once=False
wbm=[12,16]
update = 0
class bot:
  owoid=408785106942164992 #user id of the owo bot

  with open('settings.json', "w+") as file:
    try:
      data = json.load(file)
      token = data["token"]
      channel = data["channel"]
      proxy = data["proxy"]
      proxyserver = data["proxy_"]["server"]
      proxyport = data["proxy_"]["port"]
    except:
      temp={}
      temp["token"] = input("please enter your dc token for once: ")
      temp["channel"] = input("please enter the id of the channel: ")
      while True:
        temp["proxy"] = input("will you use proxy? [YES/NO]")
        temp["proxy_"] = {}
        if temp["proxy"].upper() == "YES":
          temp["proxy_"]["server"] = input("Proxy server: ")
          temp["proxy_"]["port"] = input("Proxy server port: ")
          break
        if temp["proxy"].upper() == "NO":
          temp["proxy_"]["server"] = None
          temp["proxy_"]["port"] = None
          break
      json.dump(temp, file)
      token = temp["token"]
      channel = temp["channel"]
      proxy = temp["proxy"]
      proxyserver = temp["proxy_"]["server"]
      proxyport = temp["proxy_"]["port"]
  commands=[
    "owo hunt",
    "owo hunt",
    "owo battle"
    ]
  class color:
    purple = '\033[95m'
    okblue = '\033[94m'
    okcyan = '\033[96m'
    okgreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    reset = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    if os.name == "nt":
      purple = ''
      okblue = ''
      okcyan = ''
      okgreen = ''
      warning = ''
      fail = ''
      reset = ''
      bold = ''
      underline = ''
def at():
  return f'\033[0;43m{time.strftime("%d %b %Y %H:%M:%S", time.localtime())}\033[0;21m'
def report_error(content):
  if use_terminal:
    print(at(), content)
  else:
    messagebox.showerror("OWO Auto Farm", content)
client=discum_c844aef.Client(token=bot.token,proxy_host=bot.proxyserver, proxy_port=bot.proxyport, log=False)
def issuechecker():
  msgs=client.getMessages(str(bot.channel), num=10)
  msgs=json.loads(msgs.text)
  owodes=0
  for msgone in msgs:
    if msgone['author']['id']==str(bot.owoid):
      owodes=owodes+1
      msgonec=msgone['content']
      if "DM" in str(msgonec):
          return "exit"
      if "(2/5)" in str(msgonec):
          return "exit"
      if "(3/5)" in str(msgonec):
          return "exit"
      if "(4/5)" in str(msgonec):
          return "exit"
      if "(5/5)" in str(msgonec):
          return "exit"
      if 'banned' in msgonec:
          print(f'{at()}{bot.color.fail} !!! [BANNED] !!! {bot.color.reset} your account have been banned from owo bot please open a issue on the Support Discord server')
          return "exit"
      if 'complete your captcha' in msgonec:
          print(f'{at()}{bot.color.warning} !! [CAPTCHA] !! {bot.color.reset} CAPTCHA   ACTION REQUİRED {msgonec[-6:]}')
          return "exit"
      if 'support guild!' in msgonec:
          print(f'{at()}{bot.color.warning} !! [CAPTCHA] !! {bot.color.reset} CAPTCHA   ACTION REQUİRED')
          return "exit"
      if 'captcha' in msgonec:
          return "exit"
      if 'Beep Boop.' in msgonec:
          return "exit"
  if not owodes:
    return "exit"
def security():
        if issuechecker() == "exit":
          report_error("Ban-security triggered, answer the captcha")
          exit()
def runner():
        global wbm
        command=random.choice(bot.commands)
        command2=random.choice(bot.commands)
        client.typingAction(str(bot.channel))
        client.sendMessage(str(bot.channel), command)
        print(f"{at()}{bot.color.okgreen} [SENT] {bot.color.reset} {command}")
        if not command2==command:
          client.typingAction(str(bot.channel))
          time.sleep(13)
          client.sendMessage(str(bot.channel), command2)
          print(f"{at()}{bot.color.okgreen} [SENT] {bot.color.reset} {command2}")
        time.sleep(random.randint(wbm[0],wbm[1]))
def owopray():
  client.sendMessage(str(bot.channel), "owo pray @a")
  print(f"{at()}{bot.color.okgreen} [SENT] {bot.color.reset} owo pray")
  time.sleep(13)
def gems():
  client.typingAction(str(bot.channel))
  time.sleep(3)
  client.sendMessage(str(bot.channel), "owo inv")
  print(f"{at()}{bot.color.okgreen} [SENT] {bot.color.reset} owo inv")
  time.sleep(5)
  msgs=client.getMessages(str(bot.channel), num=5)
  msgs=json.loads(msgs.text)
  inv = 0
  for msgone in msgs:
    if msgone['author']['id']==str(bot.owoid) and 'Inventory' in msgone['content']:
      inv=re.findall(r'`(.*?)`', msgone['content'])
  if not inv:
    security()
  else:
    if '50' in inv:
      client.sendMessage(str(bot.channel), "owo lb all")
      print(f"{at()}{bot.color.okgreen} [SENT] {bot.color.reset} owo lb all")
      time.sleep(13)
      gems()
      return
    for item in inv:
      try: 
        if int(item) > 100:
          inv.pop(inv.index(item)) #weapons
      except: #backgounds etc
        inv.pop(inv.index(item))
    tier = [[],[],[]]
    print(f"{at()}{bot.color.okblue} [INFO] {bot.color.reset} Found {len(inv)} gems Inventory")
    for gem in inv:
      gem =int(gem)
      if 50 < gem < 60:
        tier[0].append(gem)
      elif 60 < gem < 70:
        tier[1].append(gem)
      elif 70 < gem < 80:
        tier[2].append(gem)
    for level in range(0,3):
      if not len(tier[level]) == 0:
        client.sendMessage(str(bot.channel), "owo use "+str(max(tier[level])))
        print(f"{at()}{bot.color.okgreen} [SENT] {bot.color.reset} owo use {str(max(tier[level]))}")
        time.sleep(6)
def loopie():
  x=True
  pray = 0
  gem=pray
  main=time.time()
  while x:
      runner()
      if time.time() - pray > random.randint(300, 600):
        security()
        owopray()
        pray=time.time()
      if time.time() - gem > random.randint(500, 1200):
        security()
        gems()
        gem=time.time()
      
      if time.time() - main > random.randint(1000, 2000):
        time.sleep(random.randint(200, 350))
        security ()
        main=time.time()
@client.gateway.command
def defination1(resp):
  global once
  if not once:
    once=True
    if __name__ == '__main__':
      lol=multiprocessing.Process(target=loopie)
      lol.run()
print(bot.token)
client.gateway.run()
