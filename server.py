# coding: utf-8
#ソケットサーバ兼main.py
from websocket_server import WebsocketServer
import re
import pandas as pd
#from item import return_data as rd
#from data import data

    
#受け取ったメッセージがエンコードされてるからデコード
def bytes_to_japanese(message):
  text = ''
  for e in message.split(','):
    text += str(hex(int(e)))
  result = bytes.fromhex(re.sub('0x','',text)).decode()
  return result
    
#クライアントが接続してきた時  
def new_client(client, server):
  server.send_message_to_all("こんにちは、ユーザー")
  
#クライアントから入力文きた時  
def receive_message(client, server, message):
  #ex)message:'227,129,138,227,129,132'
  r = bytes_to_japanese(message)
  #テキストrに対して処理を行う
  #result = rd(r)
  print(r)
  df = pd.read_csv('sample.csv', index_col=['label'])
  total = ','.join(df.loc['total'].values.astype('str').tolist()) 
  today = ','.join(df.loc['today'].values.astype('str').tolist()) 
  mess = 'お前はよくやってるよ'
  server.send_message_to_all(mess + ',' + total + ',' + today)
  
server = WebsocketServer(50007, host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_message_received(receive_message)
server.run_forever()
