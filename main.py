#! /usr/bin/env python
# Script updates the motd banner on cisco devices
# Uses banner from ./banners dir
# Outputs results to results.csv file
# Will run on linux and windows
import time
import datetime
import csv
# Import variables from credentials.py
from credentials import *
from pathlib import Path
from netmiko import ConnectHandler, ssh_exception
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from tabulate import tabulate


banner_path = Path('./banners/')
local_path = Path('./')
ip_file = local_path / 'ip_address_file.txt'
results = local_path / 'results.csv'

def main(banner_name='cisco_devnet.txt'):
    """
    Main function that executes all functions.
    """
    connect_failed = []
    connect_successful = []
    banner_file = banner_path / banner_name
    banner = openFile(banner_file)
    ip_list = openFile(ip_file).splitlines()
    header = ['device_ip', 'status', 'date/time']
    with open(results, 'wt') as file:
        writer = csv.writer(file)
        writer.writerow(i for i in header) 
        for ip in ip_list:
            print(f"Attempting to log into {ip}.....")
            try:
                net_connect = connect(ip)
            except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
                print("*" * 30)
                print(f"{e}")
                print("*" * 30 + "\n")
                writer.writerow((ip,"failed",get_date()))
                connect_failed.append(ip)
                continue
            send_banner(banner, net_connect)
            save(net_connect)
            hostname = get_device_info(net_connect)['hostname']
            writer.writerow((ip, "success", get_date()))
            connect_successful.append(ip)
            print(f"Banner was successfully added to {hostname} on {get_date()}\n")
    print(tabulate([[len(connect_failed), "failed"], [len(connect_successful), "success"]],
                    headers=["Number_of_Devices", "Status"], tablefmt="pretty"))

def openFile(filename):
    """
    OPEN a file, read and return the data
        Args:
            filename (str): file name of text doc
        return: string data
        rtype: str
    """
    with open(filename, 'r') as f:
        filename = f.read()
    return filename

def get_date():
    """
    GET Current Date and Time
        return: Date/time '03-05-2021 12:04'
        rtype: str
    """
    return datetime.datetime.now().strftime('%m-%d-%Y %H:%M')

def connect(ip, username=USERNAME, password=PASSWORD, device_type=DEVICE_TYPE):
    """
    CONNECT to a network device
        Args:
            ip (str): IP address of device
            username (str): Device login username
            password (str): Device login password
            device_type (str): Device type i.e. 'cisco_ios'
        return: netmiko ConnectHandler object
        rtype: class (object)
    """
    return ConnectHandler(ip=ip, device_type=device_type, username=username, password=password)

def get_device_info(net_connect):
    """
    GET network device info
        Args:
            net_connect (object): Netmiko ConnectHandler object
        return: Network device show version info
        rtype: dict
    """
    return net_connect.send_command('show version', use_textfsm=True)[0]

def send_banner(banner, net_connect):
    """
    POST network device banner motd
        Args:
            banner (list): Banner command set list
            net_connect (object): Netmiko ConnectHandler object
        return: Network device show version info
        rtype: None
    """
    net_connect.send_config_set(banner, cmd_verify=False)

def save(net_connect):

    net_connect.send_command("wri mem")


if __name__ == "__main__":
    starttime = time.time()
    main()  # <--- Pass a new banner file name here
    print(f"Total Time Taken: {str(round(time.time() - starttime, 2))} seconds")
