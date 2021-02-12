#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 00:51:39 2020

@author: kaede
"""

import discord
import requests
from datetime import datetime
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import settings


#cannot close a running event loopの場合は $pip install tornado==4.5.3

TOKEN = settings.token
print(TOKEN)

client = discord.Client()

url = "https://spla2.yuu26.com/schedule"
salmon_url = "https://spla2.yuu26.com/coop/schedule"
discord_url = "https://discord.com/channels/769876735042781204/770952004373708810"

USER = settings.user
PASS = settings.password

payload = {"key1":"value1", "key2":"value2"}

r = requests.get(url, params=payload)
sal_r = requests.get(salmon_url, params=payload)

splat_stg = r.json()
salmon_stg = sal_r.json()

next_l = splat_stg["result"]["league"]
next_sal = salmon_stg["result"][0]

giji_dict = {"デュアル":"3.6",
             "シャプマ":"1.7 | 2.4 | 3.1",
             "L3":"1.5 | 2.2",
             "H3":"2.8 | 3.4",
             "プライム":"2.8 | 3.4",
             "クアッド":"3.6",
             "マニュ":"1.8 | 2.4 | 3.1",
             "ハイドラ":"1.2",
             "竹":"3.5",
             }

dateTime = "09:00"

@client.event
async def on_ready():
    print("接続に成功しました！")
    


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global err_flg
    global amg_flg
    
    if not(message.author.bot):
        print(datetime.now(), message.author.name, "が発言")
        
    elif message.author.bot:
        return
    
    if message.content == "among":
        amg_flg = True
        err_flg = False
        
        global browser
        browser = webdriver.Chrome(executable_path = "D:\\Users\maple\python\chromedriver.exe")

        browser.implicitly_wait(3)
        browser.get(discord_url)
        
        mail_content = browser.find_element_by_name("email")
        time.sleep(1)
        mail_content.clear()
        mail_content.send_keys(USER)
        
        pass_content = browser.find_element_by_name("password")
        time.sleep(1)
        pass_content.clear()
        pass_content.send_keys(PASS)
        
        login_content = browser.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]/div")
        time.sleep(1)
        login_content.click()
        time.sleep(3)
        
    if message.content == "splat":
        err_flg = False
    
        
    if message.content[0:2] == "擬似" and len(message.content) != 2:
        giji_weapon = message.content[2:]
        giji_value = giji_dict[f"{giji_weapon}"]
        send_text = f"**{giji_weapon}**の擬似確メイン性能：```\n{giji_value}```"
        err_flg = False
    
    elif message.content == "/lg" or message.content == "リグ":
        send_text = "```ルール：" + "\t" + next_l[0]["rule_ex"]["name"] + "\nステージ：" + "\t" + next_l[0]["maps_ex"][0]["name"] + " | " + next_l[0]["maps_ex"][1]["name"] + "```"
        err_flg = False
        
    elif message.content == "/lg_n" or message.content == "次のリグ":
        send_text = "```ルール：" + "\t" + next_l[1]["rule_ex"]["name"] + "\nステージ：" + "\t" + next_l[1]["maps_ex"][0]["name"] + " | " + next_l[1]["maps_ex"][1]["name"] + "```"
        err_flg = False
    
    elif message.content == "スナイプ":
        send_text = "https://spla-tool.com/snipe-timer/"
        err_flg = False

    elif message.content == "/gj" or message.content == "擬似":
        send_text = "武器種を入力："
        err_flg = True
       
    elif err_flg:
        if message.content in list(giji_dict.keys()):
            giji_weapon = message.content
            giji_value = giji_dict[f"{giji_weapon}"]
            send_text = f"**{giji_weapon}**の擬似確メイン性能：```\n{giji_value}```"
            err_flg = False
        else:
            err_flg = False
            return
    elif message.content == "move":
        err_flg = False
        if amg_flg == True:
            admin_message = "!fmove 一般 mute"
            amg_flg = False
        elif amg_flg == False:
            admin_message = "!fmove mute 一般"
            amg_flg = True
        
        input_content = browser.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/form/div/div/div[1]/div/div[3]/div[2]/div")
        time.sleep(1)
        input_content.send_keys(admin_message)
        time.sleep(0.5)
        input_content.send_keys(Keys.ENTER)

    else:
        err_flg = False
        return

    if message.content != "move":
        await message.channel.send(send_text)
        
@client.event
async def on_voice_state_update(member, before, after): 
    print(datetime.now(), str(member) + " がボイスチャンネル " + str(after) + " に入室しました")
    if before.channel == after.channel:
        pass
    else:
        if after.channel == client.get_channel(770951160797593601): #一般->mute
            if len(after.channel.members) == 1:
                admin_message = "!fmove 一般 mute"
        elif after.channel == client.get_channel(769876735042781208): #mute -> 一般
            if len(after.channel.members) == 1:
                admin_message = "!fmove mute 一般"
        input_content = browser.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/form/div/div/div[1]/div/div[3]/div[2]/div")
        time.sleep(1)
        input_content.send_keys(admin_message)
        time.sleep(0.5)
        input_content.send_keys(Keys.ENTER)
    

async def SendMessage():
    channel = client.get_channel(402990446877343744)
    salmon_time = next_sal["start"]
    salmon_stage = next_sal["stage"]["name"]
    await channel.send(f"**{salmon_time}**からのバイト情報\n```{salmon_stage} ブキ：？？？？```")

@tasks.loop(seconds=60)
async def time_check():
    global next_l
    now_p = str(datetime.now())
    now_p = now_p.split()[1][:5]
    r = requests.get(url, params=payload)
    sal_r = requests.get(salmon_url, params=payload)

    splat_stg = r.json()
    salmon_stg = sal_r.json()

    next_l = splat_stg["result"]["league"]
    next_sal = salmon_stg["result"][0]
    if now_p == dateTime and next_sal["weapons"][0]["name"] == "？":
        await SendMessage()
        
time_check.start()

client.run(TOKEN)
