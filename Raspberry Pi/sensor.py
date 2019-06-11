from __future__ import print_function

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import RPi.GPIO as GPIO
import time
import datetime
import httplib2
import os, io
from apiclient import discovery
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from picamera import PiCamera
from time import sleep
import GoogleDrive
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

camera = PiCamera()
email='x'
option='x'
numb=2
attachm=1

def options(email,option,numb,attachm):
    #odczytywanie z pliku 
    file = open("options.txt", "r")
    passy = open("passy.txt", "r")
    
    email = file.readline()
    option = file.readline()
    numb = int(file.readline())
    attachm = file.readline()
    passw = passy.readline()

def sendEmail():
    print("zalacznik: ",attachm)
    x= int(attachm)
    if x == 1:
        fromaddr =  "RPiSpyCamRPi@gmail.com"  #"YOUR EMAIL"
        toaddr = email              #"EMAIL ADDRESS YOU SEND TO"
 
        msg = MIMEMultipart()
 
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Wykryto ruch na twojej kamerze"
        now = datetime.datetime.now
        localtime = time.asctime(time.localtime(time.time()))
        print (localtime)
        body = ("Witaj \n Na twojej kamerze zostala wkryta aktywnosc. Sprawdz zalacznik lub zapis pod adresem: https://drive.google.com/open?id=1DCIiVclMjlSWsmbYZgRxr9xI0eqweNWw. Czas aktywnosci: " +localtime)
        
        
        msg.attach(MIMEText(body, 'plain'))
        #zalacznik w zaleznosci od opcji
        #print (option)
        op = option.strip()
        if op == "picture":
            
            filename = ("pic0.jpg")
            attachment = open("/home/pi/camera/"+filename, "rb")
        else:
            filename = ("video.h264")
            attachment = open("/home/pi/camera/"+filename, "rb")
 
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
        msg.attach(part)
        print("Wyslano z zalacznikiem")
    else:
        fromaddr =  "RPiSpyCamRPi@gmail.com"  #"YOUR EMAIL"
        toaddr = email              #"EMAIL ADDRESS YOU SEND TO"
 
        msg = MIMEMultipart()
 
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Wykryto ruch na twojej kamerze"
        now = datetime.datetime.now
        localtime = time.asctime(time.localtime(time.time()))
        print (localtime)
        body = ("Witaj \n Na twojej kamerze zostala wkryta aktywnosc. Sprawdz zapis pod adresem: https://drive.google.com/open?id=1DCIiVclMjlSWsmbYZgRxr9xI0eqweNWw. Czas aktywnosci: " +localtime)
        
        msg.attach(MIMEText(body, 'plain'))
        print("Wyslano bez zalacznika")
        
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, passw)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    
def takePic():
    n = int(numb)
    for i in range(n):
        camera.start_preview()
        sleep(2)
        j= str(i)
        camera.capture("/home/pi/camera/pic"+j+".jpg")
        camera.stop_preview()
         

def takeVid():
    camera.start_preview()
    camera.start_recording('/home/pi/camera/video.h264')
    sleep(10)
    camera.stop_recording()
    camera.stop_preview()
    

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
#options() #odczytanie z pliku txt 
file = open("options.txt", "r")
passy = open("passy.txt", "r")
email = file.readline()
option = file.readline()
numb = file.readline()
attachm = file.readline() 
passw = passy.readline()

while True:

    i=GPIO.input(11)
    #jezeli nastapila ziana przez aplikacje odczytaj ponownie
    #if int(neww )== 1:
    
    if i==0:                 #When output from motion sensor is LOW
        print ("No intruders",i)
    
        time.sleep(0.3)
    elif i==1:               #When output from motion sensor is HIGH
        start = time.time()
        options(email,option,numb,attachm)
        print ("Intruder detected",i)
        op = option.strip()
        if op == "picture":
            takePic()
            sendEmail()
            n = int(numb)
            start2 = time.time()
            for i in range(n):
                j =str(i)
                x=GoogleDrive.GoogleDrive('pic'+j+'.jpg','camera/pic'+j+'.jpg','image/jpeg')
            end2 = time.time()
            print(end2 - start2)    
        else:
            takeVid()
            start2 = time.time()
            x=GoogleDrive.GoogleDrive('video.h264','camera/video.h264','video/3gp')
            end2 = time.time()
            print(end2 - start2)
            sendEmail()
        end = time.time()
        print (end - start)
        time.sleep(0.3)
