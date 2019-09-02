#-*- coding: utf-8 -*-
#bring text(tts) or record file
from socket import *
import time
import os
import urllib2
import urllib
from requests import get
from time import sleep

from subprocess import call

import sys
sys.path.append('/home/pi/naver')
import naver_config

#networking
HOST = ''
PORT = 8080
#PORT = 8860

BUFSIZE = 1024
ADDR = (HOST,PORT)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(5)



def naverTTS(text, outputfile):
  print("[naver] tts is started")
  
  data = "speaker=jinho&speed=0&text=" + text;
  url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
  
  request = urllib2.Request(url)
  request.add_header("X-NCP-APIGW-API-KEY-ID", naver_config.naver_id())
  request.add_header("X-NCP-APIGW-API-KEY", naver_config.naver_secret_key())
  
  response = urllib2.urlopen(request, data=data.encode('utf-8'))
  rescode = response.getcode()
  
  if rescode == 200 :
      response_body = response.read()
      
      with open(outputfile, 'wb') as f:
        f.write(response_body)
  else :
        print("Error Code:" + rescode)



#file download
def download(url):
    
    file_name = url.split('/')[-1]

    with open("/home/pi/" + file_name, "wb") as file:   
        response = get(url)               
        file.write(response.content)
        return file_name



while True:

    print 'Waiting for connection'
    client_socket, addr = server_socket.accept()
    print '...connected from :', addr

    try:
            
        while True:        
            data = ''
            data = client_socket.recv(BUFSIZE)
            
            if not data:
                break   
                
            # TTS
            if data == 'tts':
                print 'tts button is clicked'
                
                client_socket.send("send text\r\n")

                textdata = client_socket.recv(BUFSIZE)
                
                print(textdata)
                
                if not textdata :
                    break
                
                decoding_text = urllib.unquote(textdata)
                result = unicode(decoding_text,"utf-8")
                print result
                
                naverTTS(result, '/home/pi/tts.mp3')  
                os.system("mpg321 /home/pi/tts.mp3")


            # playing record 
            if data == 's3address':
                print 'playing record button is clicked' 
                         
                client_socket.send("send address\r\n")

                url_data = client_socket.recv(BUFSIZE)
                #print url_data
                
                record_file = download(url_data)
                #print record_file + ' download success'

                # convert mp4 to mp3
                call(["mplayer", "-novideo", "-nocorrect-pts", "-ao", "pcm:waveheader", "/home/pi/"+record_file])
                call(["lame", "-v", "/home/pi/Raspberrypi/TTS,STT/audiodump.wav", "/home/pi/Raspberrypi/TTS,STT/record.mp3"])
                os.remove("/home/pi/Raspberrypi/TTS,STT/audiodump.wav")
                
                os.system("mpg321 /home/pi/Raspberrypi/TTS,STT/record.mp3")
            
                #break
                
    except KeyboardInterrupt:
        client_socket.close()
            
