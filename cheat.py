import discum_c844aef as discum
import requests
email_auth = 0
token_auth = 1
class ec:
    s = requests.Session()
    log={"console":True, "file":False}
    api_version = 9
    discord = 'https://discord.com/api/v'+repr(api_version)+'/'

def check_creditials(method, input1, input2):
    if method == email_auth:
        return email_validate_login(input1, input2)
    elif method == token_auth:
        return token_validate_login(input1)

def email_validate_login(email, password):
    try:
        return discum.Client.login(self=ec,email=email, password=password)[0]
    except Exception as e:
        print (e)
        return False
def token_validate_login(token):
    try:
        return discum.Client.checkToken(self=ec, token=token)
    except Exception as e:
        print (e)
        return False

def run(method, input1, input2 = "", window = None):
    if method == token_auth:
        client = discum.Client(token=input1)
    else:
        client = discum.Client(email=input1, password=input2)
    client.gateway.run(auto_reconnect=True)
    
    # SUNUCU VE KANAL SOR

    #LOGİN DENEMESİNDEKİ RESPONSE'Yİ KAYDET TKİNTER PENCERESİ AÇ BURAYA AKTAR
    # TKİNTER WİNDOW DEĞİŞKENİ

    # MANUEL ASYNC SİSTEM KUR
     #DİSCUM MODULÜNDE TRUE ÇALIŞACAK BİR LOOP OLUŞTUR
     #DİSCUM İŞLERİNİ YAPSIN ARDINDAN 1 SANİYE GEÇMİŞSE OWO'YU İŞLESİN
     # OWO KODUNU MASYNC YAZ
     # MASYNC WELCOME TO THE CLANG AEQWRWAS 
