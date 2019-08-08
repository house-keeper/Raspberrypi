from socket import *
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
    
control_pins = [7,11,13,15]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
    
halfstep_seq_up = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

halfstep_seq_down = halfstep_seq_up[::-1]


ctrCmd = ['1','0']

HOST = ''
PORT = 8080
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
        print 'Waiting for connection'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from :', addr
        try:
                while True:
                        data = ''
                        data = tcpCliSock.recv(BUFSIZE)
                        if not data:
                                break
                        if data == ctrCmd[0]:
                            for i in range(512):
                                for halfstep in range(8):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq_up[halfstep][pin])
                                    time.sleep(0.001)
                            print 'window is open'
                        if data == ctrCmd[1]:
                            for i in range(512):
                                for halfstep in range(8):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq_down[halfstep][pin])
                                    time.sleep(0.001)    
                            print 'window is close'
        except KeyboardInterrupt:
                GPIO.cleanup()
tcpSerSock.close();

