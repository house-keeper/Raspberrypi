#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from socket import *
import pyaudio
import wave
import os
import sys
import json
import requests

#stt
client_id = "r6o83og4g9"
client_secret = "xDA4x1qdyaXQNl7Lp6VlEb37oQUmlDvHStqGuwKJ"
lang = "Kor"
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

#client networking init
c_host='192.168.0.11'
#c_host='192.168.0.20'
c_port=8885
c_addr =(c_host, c_port)

#button & led init
Button = 18
LED_G = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button, GPIO.IN)
GPIO.setup(LED_G,GPIO.OUT)

GPIO.output(LED_G, True)

#mic setting init
form_1 = pyaudio.paInt16
chans=1
samp_rate = 44100
chunk = 4096
record_secs = 5     #record time
dev_index = 1
wav_output_filename = 'outsider_record.wav'

loop_ctrl=0

while True:                       
    if GPIO.input(Button)==0:
        GPIO.output(LED_G,False)

        #recordVoice #def
        audio = pyaudio.PyAudio()                        
        stream=audio.open(format = form_1,rate=samp_rate,channels=chans, input_device_index = dev_index, input=True, frames_per_buffer=chunk)
        frames=[]
        print "############Button is Pressed############"
        print("녹음 중 입니다.")
                                        
        while GPIO.input(Button)==0: #버튼누른상태
            data = stream.read(chunk)
            frames.append(data)
                                                    
        print("녹음이 완료되었습니다.") #버튼 뗐을때
        GPIO.output(LED_G,True)                    
        #storeRecord
        stream.stop_stream()
        stream.close()
        audio.terminate()
                                                
        wavefile=wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()            
                                
        #naverSTT
        data = open('/home/pi/outsider_record.wav', 'rb')
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(url,  data=data, headers=headers)
        rescode = response.status_code
        if(rescode == 200):
            print (response.text)
            print(type(response.text))
                            
            #send socket
                
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(c_addr)
            client_socket.send(response.text.encode('utf8')
            client_socket.close()
            print "send"
                
           
                            
            loop_ctrl=0
            continue
        else:
            print("Error : " + response.text)
        
    if GPIO.input(Button)!=0:
                        
        if loop_ctrl == 0:
                print 'connected with master'
                print "Button is Not Pressed!"
                print "you can speak when bluelight is on"
                print "your message is recorded while greenlight is on"
                loop_ctrl=1
                continue
                        
        if loop_ctrl == 1:                    
                continue       
