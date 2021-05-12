import discum
import time
import multiprocessing
import asyncio
import json
import random
exit=False
once=False
wbm=[16,24]
class bot:
  owoid=408785106942164992
  channel=channel id #fill this
  token="token" #fill this
  commands=[
    "owo hunt",
    "owo battle"
    ]
  funcom=[
    "owo zoo",
    "owo money",
    "owo sell all",
    "owo cf 2",
    "owo sell uncommonweapons",
    "owo sell commonweapons",
    "owo sell epicweapons",
    "owo sell mythicweapons",
    "owo level",
    "owo lb all",
    "owo crate all",
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
def at():
  return f'\033[0;43m{time.strftime("%d %b %Y %H:%M:%S", time.localtime())}\033[0;21m'

client=discum.Client(token=bot.token, log=True)
def issuechecker():
  msgs=client.getMessages(str(bot.channel))
  print(msgs.text)
  msgs=json.loads(msgs.text)
  for msgone in msgs:
    if msgone['author']['id']==str(bot.owoid)
      msgonec=msgone['content']
      if "(2/5)" in str(msgonec):
          exit()
      if 'banned' in msgonec:
          owobot_fuse=False
          print(f'{at()}{bot.color.fail} !!! [BANLANDI] !!! {bot.color.reset} owobotdan banlandı, eğer botun bir sorunu olduğunu düşüyorsanız https://github.com/sudo-do/auto-owo-bot adresinden sorun raporu açın')
          exit()
      if 'complete your captcha' in msgonec:
          owobot_fuse=False
          print(f'{at()}{bot.color.warning} !! [CAPTCHA] !! {bot.color.reset} CAPTCHA   DOĞRULAMASI GEREKLİ {msgonec[-6:]}')
          exit()
def runner():
        command=random.choice(bot.commands)
        command2=random.choice(bot.commands)
        client.sendMessage(str(bot.channel), command)
        if not command2==command:
          time.sleep(1)
          client.sendMessage(str(bot.channel), command2)
        time.sleep(random.randint(wbm[0],wbm[1]))
async def mainexit():
  global exit
  x=True
  while x:
    await asyncio.sleep(2)
    if exit:
      exit()
def loopie():
  x=True
  while x:
    issuechecker()
    runner()
@client.gateway.command
def defination1(resp):
  global once
  if resp.event.message:
      if not once:
        once=True
        lol=multiprocessing.Process(target=loopie)
        lol.start()
        #lol.join()
client.gateway.run()
