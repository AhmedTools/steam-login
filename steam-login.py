import os
import json
try:from Crypto.PublicKey import RSA
except:os.system('pip install pycryptodome')
try:from bs4 import BeautifulSoup
except:os.system('pip install beautifulsoup')
try:from Crypto.Cipher import PKCS1_v1_5
except:os.system('pip install pycryptodome')
try:import base64
except:os.system('pip install base64')
import time
import random
import requests
def infomations(data2):
   steam_id = data2['transfer_parameters']['steamid']
   url = 'https://steamid.pro/lookup/'
   message_text = ""
   try:
        r = requests.get(f'{url}{steam_id}')
        soup = BeautifulSoup(r.text, 'html.parser')
        divs_info = soup.find_all('div', class_='col-lg-6 col-12')
        bans_div = divs_info[1]
        bans = bans_div.find('table', class_='rtable rtable-bordered table-fixed table-responsive-flex').find_all('tr')
        bans_info = []
        for ban in bans:
            tds = ban.find_all('td')
            bans_info.append(f"{tds[0].text} : {tds[1].text}")
        price = soup.find('span', class_='number-price')
        hours_div = divs_info[1]
        hours_info = hours_div.find_all('table', class_='rtable rtable-bordered table-fixed table-responsive-flex')[1]
        hours_played = hours_info.find_all('td')
        info_div = soup.find('div', class_='ml-3')
        mix_info = info_div.find_all('span')
        nick = info_div.find('h1', class_='mb-0 text-white').text
        steam_level = mix_info[0].text
        message_text += '='*15
        message_text += f'\nNickname : {nick}\n'
        message_text += f'Steam Level : {steam_level}\n'
        for ban in bans_info:
            message_text += f'{ban}\n'

        message_text += f"Account Price : {price.text}\n"
        message_text += f'Hours Played : {hours_played[1].text}\n'
        message_text += '='*15
        print(message_text)
   except Exception as ex:
        print(ex)
def cookies(username, password):
    session = requests.Session()
    url = 'https://steamcommunity.com/login/getrsakey/'
    data = {'username': username, 'donotcache': str(int(time.time() * 1000))}
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    response = session.post(url, data=data, headers=headers)
    data = response.json()
    stime = data['timestamp']
    mod = int(data["publickey_mod"], 16)
    exp = int(data["publickey_exp"], 16)
    npassword(mod, exp, stime, password, username, session)
def npassword(mod, exp, stime, password, username, session):
    rsa = RSA.construct((mod, exp))
    cipher = PKCS1_v1_5.new(rsa)
    epassword = base64.b64encode(cipher.encrypt(password.encode('utf-8'))).decode('utf-8')
    login(password, epassword, username, stime, session)
def login(password, epassword, username,stime, session):
    url = 'https://steamcommunity.com/login/dologin/'
    data = {
        "username": username,
        "password": epassword,
        "emailauth": "",
        "loginfriendlyname": "",
        "captchagid": "-1",
        "captcha_text": "",
        "emailsteamid": "",
        "rsatimestamp": stime,
        "remember_login": False,
        "donotcache": int(time.time() * 1000)
    }
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    response = session.post(url, data=data, headers=headers)
    data2 = response.json()
    if data == None or 'Please verify your humanity' in data2['message']:
    	print(f'- You Have Been Blocked')
    elif data2['success']:
        print(f'- Done Login : [ Username : {username} | Password : {password} ]')
        infomations(data2)
    else:
        print(f'- Error Login : [ Username : {username} | Password : {password} ]')
if __name__ == "__main__":
	email = input('- Enter E-mail : ')
	password = input('- Enter Password : ')
	cookies(email,password)