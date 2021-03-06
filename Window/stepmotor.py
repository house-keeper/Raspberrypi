import time
import RPi.GPIO as GPIO

from socket import *


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
    
control_pins = [7,11,13,15]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
    
halfstep_seq_down = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

halfstep_seq_up = halfstep_seq_down[::-1]

ctrCmd = ['1', '0'] # 1 : open / 0 : close

HOST = ''
PORT = 8989
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)


while True:
        print 'step motor Waiting for connection'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from :', addr
        try:
                while True:
                        data = ''
                        data = tcpCliSock.recv(BUFSIZE)
                        print(data)
                        
                        if not data:
                                break
                                
                        if data == ctrCmd[0]:
                            for i in range(300):
                                for halfstep in range(8):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq_up[halfstep][pin])
                                    time.sleep(0.001)
                            print 'window is open\n'
                            
                        if data == ctrCmd[1]:
                            for i in range(300):
                                for halfstep in range(8):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq_down[halfstep][pin])
                                    time.sleep(0.001)    
                            print 'window is close\n'
                            
        except KeyboardInterrupt:
                GPIO.cleanup()
                
                
tcpSerSock.close();

