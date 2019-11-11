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
push_service = FCMNotification(api_key="AAAArfxMe64:APA91bHDeSVpSBnDHcm55daMpwr_4P_6SMNyfSthExdS5qji3UbibyrR9iNXWByVACxxDFRm_KJN14PKsAm7TnrBnou2G09KSKIFwApl307pccrBU0vTETZZq-zYDVs-pKWimiC44ToG")
registration_id = "cBZEdoeLvAk:APA91bHhobeW0MiDnR9991pAQ3356QM20dzNGOUfo3ZTSLILXQ_WvyTsYANPwBhoze47J-uZKva6R9Lm82O_sgLi8JHgg5wzQ7fKJJOv0bsbt5oD75QszSSU-oFSstNy2Ad0hQWULNg0"
#registration_id = "eGu6ibIMpaw:APA91bEgVgH7hMjNXAyEFA-6RdrDAGFh7E7-yFHaqUXli81dLnFFH84pHTga2rpAkr_EnsnTndvYVkSMgKXZIGRmhnmpUbS67nFyGxrrIYQkuVD2cPsMBdA_7dYkPJzP1Ha7k54bKhpW"
#stt
client_id = "r6o83og4g9"
client_secret = "xDA4x1qdyaXQNl7Lp6VlEb37oQUmlDvHStqGuwKJ"
lang = "Kor"
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

#server networking init 
ctrCmd = ['1','0']

HOST = ''
PORT = 8888
BUFSIZE = 1024
ADDR = (HOST,PORT)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(5)
server_socket.settimeout(3)

#client networking init
c_host='192.168.0.32'
#c_host='192.168.0.20'
c_port=8885
c_addr =(c_host, c_port)


#door bell if 0: off 1: on
door_bell_on = 0
loop_ctrl = 0
loop_ctrl2 = 0

#button & led init
Button = 18
LED_G = 23
LED_B = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button, GPIO.IN)
GPIO.setup(LED_G,GPIO.OUT)
GPIO.setup(LED_B,GPIO.OUT)

GPIO.output(LED_G, True)
GPIO.output(LED_B, True)

#mic setting init
form_1 = pyaudio.paInt16
chans=1
samp_rate = 44100
chunk = 4096
record_secs = 5     #record time
dev_index = 1
wav_output_filename = 'outsider_record.wav'

confirm_data = ''


################################
print 'Start'
print "ring the door bell"
    
while True:
    if GPIO.input(Button)==0:
        door_bell_on=1 #on
        result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
        print result
        os.system("mpg321 doorbell_sound.mp3") #doorbell sound on
        
        while True:
            try:
                print 'Waiting for connection'
                #if 'yes' signal from android
                c_response, addr = server_socket.accept()
                print '...connected from :', addr
                confirm_data = c_response.recv(BUFSIZE)
                                           
            except timeout:
                pass
            except error:
                print 'connection error'
                break
            
            
            if confirm_data == ctrCmd[0]: #yes
                GPIO.output(LED_B,False)
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
                        #need outsider_record.wav
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
                GPIO.output(LED_B,True)
                print 'connection refused'
                if(loop_ctrl2 == 1):
                        loop_ctrl2=0
                        break
                loop_ctrl2 = 1
                continue

server_socket.close()
GPIO.cleanup()
