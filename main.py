#! /usr/bin/env python3
import sys
sys.path.append('../')
import time
import datetime
from credentials import *
from netmiko import ConnectHandler

banner = open('./banners/cisco_devnet.txt')


def openFile():
    with open('ipaddress.txt', 'r') as file:
        ip_list = []
        for line in file:
            ip_list.append(line.strip())
    return ip_list

def get_date():
    return datetime.datetime.now()

def login(ip, username=USERNAME, password=PASSWORD, device_type=DEVICE_TYPE):
    return ConnectHandler(ip=ip, device_type=device_type, username=username, password=password)

def send_banner(ip):
    if type(ip) == list:
        print(True)
    for i in ip:
        net_connect = ConnectHandler(ip=ip, device_type=device_type, username=username, password=password)
        print('Connecting to %s' % ip)
        time.sleep(1)
        device_hostname = net_connect.send_command('show run | include hostname')
        hostname = device_hostname[9:]
        device_serial = net_connect.send_command('show inventory | include PID')
        time.sleep(1)
        net_connect.write_channel('config t \n')
        time.sleep(1)
        net_connect.write_channel(str(banner.read()) + '\n')
        time.sleep(3)
        net_connect.write_channel('exit \n')
        time.sleep(1)
        net_connect.write_channel('wri mem \n')
        time.sleep(2)
        show_session = net_connect.read_channel()
        print(show_session)
        time.sleep(1)
 
    clock = now.strftime('%m-%d-%Y %H:%M')
    output = [hostname, ip, device_serial, clock]

banner.close()
