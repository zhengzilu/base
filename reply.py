#coding=utf8
import itchat
from itchat.content import TEXT
from itchat.content import *
import sys
import time
import re
import requests, json
import aiml
import os


# When recieve the following msg types, trigger the auto replying.
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True, isMpChat=True)
def text_reply(msg):
    global auto_reply, robort_reply, peer_list

    # The command signal of "[自动回复]"   
    if msg['FromUserName'] == myUserName and msg['Content'] == u"开启自动回复":
        auto_reply = True
        itchat.send_msg(u"[自动回复]已经打开。\n", msg['FromUserName'])
    elif msg['FromUserName'] == myUserName and msg['Content'] == u"关闭自动回复":
        auto_reply = False
        itchat.send_msg(u"[自动回复]已经关闭。\n", msg['FromUserName'])
    # elif not msg['FromUserName'] == myUserName:    
    else:    
        if auto_reply == True:
            itchat.send_msg(u"[自动回复]您好，我现在不在，一会儿再和您联系。\n", msg['FromUserName'])
        else:            
            '''
            For none-filehelper message,
            if recieve '= =', start robort replying.
            if recieve 'x x', stop robort replying.
            '''
            
            if (msg['Content'] == u"Hi~" or msg['Content'] == u".") and msg['FromUserName'] == myUserName:
                #我自己发
                robort_reply = True
                peer_list.append(msg['ToUserName'])
                friend = itchat.search_friends(userName=msg['ToUserName'])
                print("start chatting with %s"%friend['RemarkName'])
                return
            elif msg['Content'] == u"嘿嘿":
                #接收到别人的消息
                robort_reply = True
                peer_list.append(msg['FromUserName'])
                friend = itchat.search_friends(userName=msg['FromUserName'])
                print("start chatting with %s"%friend['NickName'])
                kaichangbai = '您好'+friend['NickName']+'，您的智障好友已上线。回复”闭嘴“，立即下线。[Smile]'
                itchat.send(kaichangbai, msg['FromUserName'])
                return
            elif msg['Content'] == u"emm"and msg['FromUserName'] == myUserName:
                      #我自己发
                robort_reply = False
                peer_list.remove(msg['ToUserName'])
                friend = itchat.search_friends(userName=msg['ToUserName'])
                print("finish chatting with %s"%friend['NickName'])
                return
            elif msg['Content'] == u"闭嘴":
                      #接收到别人的消息
                robort_reply = False
                peer_list.append(msg['FromUserName'])
                friend = itchat.search_friends(userName=msg['FromUserName'])
                print("finish chatting with %s"%friend['NickName'])
                kaichangbai = '那我走了，不要想我。[Cry]'
                itchat.send(kaichangbai, msg['FromUserName'])
                return
            # Let Turing reply the msg.
            if robort_reply == True and msg['FromUserName'] in peer_list:
                # Sleep 1 second is not necessary. Just cheat human.  
                time.sleep(1)
                Url="http://www.tuling123.com/openapi/api"
                data={
                    "key":"1c1f65a0d65a4b53ad47aee7ef2a7c54",
                    "info":msg['Content'],
                    "userid":"robot"
                }
                m = requests.post(Url,data=data).json()
                itchat.send(m['text'], msg['FromUserName'])
                if m['code'] == 200000:
                    itchat.send(m['url'], msg['FromUserName'])
                if m['code'] == 302000:
                    itchat.send(m['list'], msg['FromUserName'])
                if m['code'] == 308000:
                    itchat.send(m['list'], msg['FromUserName'])
    return


# Main
if __name__ == '__main__':
    # Set the hot login
    itchat.auto_login(enableCmdQR=-2, hotReload=True)

    # Get your own UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    print(myUserName)
    auto_reply = False
    robort_reply = False
    peer_list = []

    itchat.run()
