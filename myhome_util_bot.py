#-*- coding: utf-8 -*-
#
# github:      https://github.com/thkang0/telegram-bot
#
import telebot
import socket
import struct
import os
import sys
import ConfigParser

bot = telebot.TeleBot("175881767:AAG6nfgAprdHkTjbK6JZdZdsE76cbu5kMhE")

USAGE = u"""[사용법] 아래 명령어를 메시지로 보내거나 버튼을 누르시면 됩니다.
/wol - (해당 서버에 wol packet을 보낸다. ex) wol server_name )
/list - (현재 등록되어 있는 서버 목록)
/add_host - (새로 추가할 서버 ex) add_host mylaptop XX:XX:XX:XX:XX:XX )
/del_host - (기존에 등록된 서버 삭제 ex) del mylaptop )
/help  - (이 도움말 보여주기)
"""

def add_host_mac(host, mac):
    if len(mac) == 12:
        pass
    elif len(mac) == 12 + 5:
        sep = mac[2]
        mac= mac.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # insert host and mac into DB
    return True

def del_host_mac(host):
    return True

def get_host_mac(host):
    return mac

def wake_on_lan(host):
    """ Switches on remote computers using WOL. """

    try:
      macaddress = get_host_mac(host)
      #macaddress = myconfig[host]['mac']

    except:
      return False

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = ''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = ''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (myconfig['General']['broadcast'], 7))
    return True

@bot.message_handler(commands='help')
def help(message):
    bot.reply_to(message, USAGE)

@bot.message_handler(commands='add_host')
def add_server(msg):
    cid = msg.chat.id
    text = msg.text
    
    bot.send_chat_action(cid, 'typing')

    if len(text.split()) == 3:
        host = text.split()[1]
        mac = text.split()[2]
        add_host_mac(host, mac)    
    else:
        bot.reply_to(msg, "Incorrect command. It should be \"add_host host mac_address\"") 


@bot.message_handler(commands='help')
def help(message):
    bot.reply_to(message, USAGE)

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)

bot.polling()

