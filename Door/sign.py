#-*- coding: utf-8 -*-
from time import sleep
from socket import *
import os
import sys
import requests
import subprocess

#server networking init 
# 1 : YES streaming, 0 : NO streaming
ctrCmd = ['1','0']

HOST = ''
PORT = 8745
BUFSIZE = 1024
ADDR = (HOST,PORT)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(5)
confirm_data = ''


################################
print 'Start cam & outsider program'

while True:   
            try:
                print 'sign.py Waiting for connection'
                #if 'yes' signal from android
                c_response, addr = server_socket.accept()
                print '...connected from :', addr
                confirm_data = ''
                confirm_data = c_response.recv(BUFSIZE)                                         
            except error:
                print 'connection error'
                break
                        
            if confirm_data == ctrCmd[1]: #NO streaming
                os.system("sudo pkill mjpg.sh")
                os.system("sudo pkill mjpg_streamer")
                
                print("streaming off")
                print("outsider detect on")
                os.system("sudo python outsider.py &")
                                                          
            elif confirm_data == ctrCmd[0]: #YES streaming
                os.system("sudo pkill -f outsider.py")
                print("outsider detect off")
                print("streaming on")
                os.system("./mjpg.sh &")                
                
            elif confirm_data == '':             
                continue

server_socket.close()
GPIO.cleanup()
