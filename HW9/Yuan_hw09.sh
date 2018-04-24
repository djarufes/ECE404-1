#!/usr/bin/env bash
#Homework Number: 9
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 3/27/2018

#PLACE NO RESTRICTION ON OUTBOUND PACKETS
iptables -I OUTPUT 1 -j ACCEPT

#BLOCK A LIST OF SPECIFIC IP ADDRESSES FOR ALL INCOMING CONNECTIONS
iptables -A INPUT -s 10.10.0.0/64.255.255.255 -j DROP

#BLOCK YOUR COMPUTER FROM BEING PINGED BY ALL OTHER HOSTS
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

#SETUP PORT FORWARDING FROM AN UNUSED PORT OF CHOICE TO PORT 22
iptables -t nat -A PREROUTING -p tcp --dport 400 -j DNAT --to 192.168.2.2:22
iptables -A INPUT -p tcp --dport 400 -j ACCEPT
iptables -A FORWARD -p tcp --dport 22 -j ACCEPT

#ALLOW FOR SSH ACCES TO YOUR MACHINE FROM ONLY ECN DOMAIN
iptables -A INPUT -s ! ecn.purdue.edu -p tcp --dport 22 -j REJECT

#ONLY ALLOWS A SINGLE IP ADDRESS TO ACCESS FOR HTTP
iptables -A INPUT -p tcp -s ! 192.168.2.2 --dport 80 -j REJECT

#PERMIT AUTH/IDENT ON PORT 113
iptables -A INPUT -p tcp -m tcp --syn --dport 113 -j ACCEPT