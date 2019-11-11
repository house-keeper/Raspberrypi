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
server_socket.settimeout(5)


#door bell if 0: off 1: on
door_bell_on = 0
loop_ctrl = 0

#button & led init
Button = 18
LED_B = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button, GPIO.IN)
GPIO.setup(LED_B,GPIO.OUT)
GPIO.output(LED_B, True)



################################
print 'Start'
print "ring the door bell"
    
while True:
    
    if GPIO.input(Button)==0:
        door_bell_on=1 #on
        result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)
        print result
        os.system("mpg321 doorbell_sound.mp3") #doorbell sound on & need doorbell_sound.mp3
        
        while True:
            try:
                print '0,1 Waiting for connection'
                #if 'yes' signal from android
                c_response, addr = server_socket.accept()
                print '...connected from :', addr
                confirm_data = ''
                confirm_data = c_response.recv(BUFSIZE)
                                           
            #except timeout:
             #   pass
            except error:
                print 'connection error'
                break
            
            
            if confirm_data == ctrCmd[0]: #yes
                GPIO.output(LED_B,False)
                print '************door_bell_ring_ready************'
                os.system("sudo python speakTotext.py &")
                continue
                
                                                                                                 
                     
            elif confirm_data == ctrCmd[1]:
                door_bell_on=0
                print '**************connection end from phone*************'
                GPIO.output(LED_B,True)
                os.system("sudo pkill -f speakTotext.py")
                print "ring the door bell"
                break

server_socket.close()
GPIO.cleanup()

