import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import robot
import lcddriver
import subprocess
from pyzbar.pyzbar import decode
from sms import send
import serial
GPIO.setmode(GPIO.BCM)#GPIO.BOARD
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
cap = cv2.VideoCapture(0)
product=["Rice","Wheat","Sugar","billing"]
tag=["115117103971","119104101971","114105991010",b'5400C50A23B8']
F=[0,0,0,0]
price=[20,60,79]
amount=0
balance=300
display = lcddriver.lcd()
port = serial.Serial("/dev/serial0",9600,timeout=0.1)

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data: " + str(barcodeData) + " | Type: " + str(barcodeType)
        
        cv2.putText(image, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255), 2)
        print("Barcode: "+barcodeData +" | Type: "+barcodeType)
        return(barcodeData)



robot.stop()
count=0
items = []
try:
    while(True):#while(True):
        display.lcd_clear()
        display.lcd_display_string("Waiting...", 1)
        ret, img = cap.read()
        if(ret):
            rcv=str(decoder(img))
##        f=open("card.txt",'r')
        payid=str(port.readline())
##        f.close()
        print("Pay ID: ",payid)
        # resize imag to 50% in each axis
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        # convert BGR image to a HSV image
        print("Size:",img.shape)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
        lower_range = np.array([24, 100, 100], dtype=np.uint8) 
        upper_range = np.array([44, 255, 255], dtype=np.uint8)

        # create a mask for image
        mask = cv2.inRange(hsv, lower_range, upper_range)
        ret,thresh = cv2.threshold(mask,127,255,0)
        #finding all possible contours based on mask
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if(len(contours)>0):
            c = max(contours, key=cv2.contourArea)#find the contour with maximum size
            ((x, y), radius) = cv2.minEnclosingCircle(c)#find x,y coordinates of the contour
            M = cv2.moments(c)
            robot.stop()
            #print(x,y)
            if radius > 10:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))            
                cv2.circle(img, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                cv2.circle(img, center, 5, (0, 0, 255), -1)
                area = cv2.contourArea(c)
                print("area: ",area)
                print("X:",x)
                if(area>4500 and area<=10000):
                    print("stop")
                    robot.stop()
                elif(area>10000):
                    robot.Down(30)
                elif(x>180 and x<=320):
                    print("right")
                    robot.Right(50)
                    time.sleep(.05)
                    robot.stop()
                elif(x<=100 and x>0):
                    print("left")
                    robot.Left(50)
                    time.sleep(.05)
                    robot.stop()
                elif(x<=180 and x>100):
                    print("forward")
                    if(area<2000):
                        robot.Forward(50)
                    else:
                        robot.Forward(20)
        if(rcv in tag):
            if(tag.index(rcv)<=2):
                if(F[tag.index(rcv)]==0):
                    GPIO.output(21,True)
                    time.sleep(1)
                    GPIO.output(21,False)
                    print(product[tag.index(rcv)],"added")
                    items.append(product[tag.index(rcv)]+" : "+str(price[tag.index(rcv)]))
                    amount=amount+price[tag.index(rcv)]
                    data = product[tag.index(rcv)]+"added"
                    display.lcd_clear()
                    display.lcd_display_string(data, 1)
                    display.lcd_display_string("Total:"+str(amount), 2)
                    F[tag.index(rcv)]=1
                    for i in range(20):
                        ret,frame=cap.read()
                    time.sleep(1)
                elif(F[tag.index(rcv)]==1):
                    GPIO.output(21,True)
                    time.sleep(1)
                    GPIO.output(21,False)
                    print(product[tag.index(rcv)],"removed")
                    items.discard(product[tag.index(rcv)]+" : "+str(price[tag.index(rcv)]))
                    amount=amount-price[tag.index(rcv)]
                    data = product[tag.index(rcv)]+"removed"
                    display.lcd_clear()
                    display.lcd_display_string(data, 1)
                    display.lcd_display_string("Total:"+str(amount), 2)
                    F[tag.index(rcv)]=0
                    for i in range(20):
                        ret,frame=cap.read()
                    time.sleep(1)
        if('5400C50A23B8' in payid and balance>=amount):
            print (amount," reduced from your card")
            balance=balance-amount
            data = str(amount)+" reduced from your card" + "\n\rbalance: "+ str(balance)
            print ("current balance: ",balance)
            display.lcd_clear()
            display.lcd_display_string(str(amount)+" reduced", 1)
            display.lcd_display_string("balance: "+str(balance), 2)
            for i in items:
                print(i)
##            send(data)
            count=0
            time.sleep(3)                
        elif(balance<amount and count==1):
            count+=1
            print("Insufficient Funds")
            display.lcd_clear()
            display.lcd_display_string("Insufficient Funds", 1)
            display.lcd_display_string("Recharge", 2)
##            send("Insufficient funds transaction failed")
            time.sleep(3)                
                 
                
##        cv2.imshow('mask',mask)
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


         
    cv2.destroyAllWindows()
except KeyboardInterrupt:
    GPIO.cleanup()
