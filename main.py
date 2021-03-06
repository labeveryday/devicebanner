#! /usr/bin/env python
# Script updates the motd banner on cisco devices
# Uses banner from ./banners dir
# Outputs results to results.csv file
# Will run on linux and windows
import time
import datetime
import csv
import contextlib
import io
# Import variables from credentials.py
from credentials import *
from pathlib import Path
from netmiko import ConnectHandler, ssh_exception
from paramiko.ssh_exception import SSHException
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
    banner = openfile(banner_file)
    ip_list = openfile(ip_file).splitlines()
    header = ["device_ip", "status", "reason", "date/time"]
    with open(results, 'wt') as file:
        writer = csv.writer(file)
        writer.writerow(i for i in header) 
        for ip in ip_list:
            print(f"Attempting to log into {ip}.....")
            # This is to redirect stderr if netmiko can't connect
            with contextlib.redirect_stderr(io.StringIO()):
                try:
                    net_connect = connect(ip)
                    send_banner(banner, net_connect)
                    save(net_connect)
                    hostname = get_device_info(net_connect)['hostname']
                    writer.writerow((ip, "success", None, get_date()))
                    connect_successful.append(ip)
                    print(f"✅ Banner was successfully added to {hostname} on {get_date()}\n")
                except (ssh_exception.NetMikoTimeoutException, ssh_exception.NetMikoAuthenticationException,
                        SSHException) as e:
                    print(f"❌ SSH timeout attempt to {ip} on {get_date()}\n")
                    writer.writerow((ip,"failed","ssh timeout", get_date()))
                    connect_failed.append(ip)
                    continue            
    print(tabulate([[len(connect_failed), "failed"], [len(connect_successful), "success"]],
                    headers=["Number_of_Devices", "Status"], tablefmt="pretty"))

def openfile(filename):
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
    return ConnectHandler(ip=ip, device_type=device_type,
                          username=username, password=password, banner_timeout=5)

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
    """
    POST copy running config to startup config
        Args:
            net_connect (object): Netmiko ConnectHandler object
        return: None
        rtype: None
    """
    net_connect.send_command("wri mem")


if __name__ == "__main__":
    starttime = time.time()
    main()  # <--- Pass a new banner file name here
    print(f"\nTotal Time Taken: {str(round(time.time() - starttime, 2))} seconds\n")
