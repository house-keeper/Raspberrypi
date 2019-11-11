#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from pyfcm import FCMNotification
from time import sleep
from socket import *
import pyaudio
import wave
import os
import sys
import json
from collections import OrderedDict
import requests

import sys
sys.path.append('/home/pi/naver')
import fcm_config
sys.path.append('/home/pi/naver')
import naver_config

#fcm push alert 
reload(sys)
sys.setdefaultencoding('utf-8')
#s = '인터폰을 받으시게'
s = '인터폰을 받으시겠습니까?'
print str(unicode(s))
data_message = {
    "title" : "Notice",
    "body" : str(unicode(s))    
}
push_service = FCMNotification(api_key = fcm_config.fcm_api_key())
registration_id = fcm_config.fcm_registration_id()

#stt
client_id = naver_config.naver_id()
client_secret = naver_config.naver_secret_key()
lang = "Kor"
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

#server networking init 
ctrCmd = ['1','0']

HOST = ''
PORT = 8885
BUFSIZE = 1024
ADDR = (HOST,PORT)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(5)
server_socket.settimeout(3)

#client networking init
c_host='192.168.0.9'
c_port=8881
c_addr =(c_host, c_port)


#door bell if 0: off 1: on
door_bell_on = 0
loop_ctrl = 0
loop_ctrl2 = 0

#button & led init
Button = 23
LED_G = 17
LED_B = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button, GPIO.IN)
GPIO.setup(LED_G,GPIO.OUT)
GPIO.setup(LED_B,GPIO.OUT)

#mic setting init
form_1 = pyaudio.paInt16
chans=1
samp_rate = 44100
chunk = 4096
dev_index = 1
wav_output_filename = '/home/pi/outsider_record.wav'



################################
print 'Start'
print "ring the door bell"
    
while True:
        
    if GPIO.input(Button)==0:
        door_bell_on=1 #on
        result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
        print result
        os.system("mpg321 /home/pi/doorbell_sound.mp3") #doorbell sound on
        
        while True:
            try:
                print 'Waiting for connection'
                #if 'yes' signal from android

                c_response, addr = server_socket.accept()
                print '...connected from :', addr
                confirm_data = ''
                confirm_data = c_response.recv(BUFSIZE)                             
            except timeout:
                pass
            except error:
                print 'connection error'
                break
            
            
            if confirm_data == ctrCmd[0]: #yes
                GPIO.output(LED_B,GPIO.LOW)
                while True:                       
                    if GPIO.input(Button)==0:
                        GPIO.output(LED_G,GPIO.LOW)
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
                        GPIO.output(LED_G,GPIO.HIGH)                    
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
                            
                            #send socket
                            
                            try:
                                client_socket = socket(AF_INET, SOCK_STREAM)
                                client_socket.connect(c_addr)
                                #client_socket.connect(c_addr)
                                client_socket.send(response.text)
                                client_socket.close()
                                print "send"
                            except error:
                                break
                                
                            loop_ctrl=0
                            
                            break
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
                            #TODO:blue light problem
                            continue                                                                                    
                     
            if confirm_data == ctrCmd[1]:
                door_bell_on=0
                GPIO.output(LED_B,GPIO.HIGH)
                print 'connection refused'
                if(loop_ctrl2 == 1):
                        loop_ctrl2=0
                        break
                loop_ctrl2 = 1
                continue

server_socket.close()
GPIO.cleanup()
