#! /usr/bin/env python
# Script updates the motd banner on cisco devices
# Uses banner from ./banners dir
# Outputs results to results.csv file
# Will run on linux and windows
import argparse
import contextlib
import csv
import datetime
import io
import time
# Import variables from credentials.py
from credentials import *
from pathlib import Path
from ciscoconfparse import CiscoConfParse
from netmiko import ConnectHandler, ssh_exception
from paramiko.ssh_exception import SSHException
from tabulate import tabulate


banner_path = Path('./banners/')
local_path = Path('./')
ip_file = local_path / 'ip_address_file.txt'
results = local_path / 'results.csv'

def main(banner_name='cisco_devnet.txt'):
    """
    POST Main function that updates devices with entered banner motd
        Args:
            banner_name (str): Banner file name (default: 'cisco_devnet.txt')
        return: None
        rtype: None
    """
    failed_connection = []
    successful_connection = []
    banner_file = banner_path / banner_name
    try:
        banner = openfile(banner_file)
    except FileNotFoundError as e:
        print("\n***Try again!***")
        print(f"No such file or directory: {banner_name}\n")
        exit()
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
                    successful_connection.append(ip)
                    print(f"✅ Banner was successfully added to {hostname} on {get_date()}\n")
                except ssh_exception.NetMikoTimeoutException:
                    print(f"❌ SSH timeout attempt to {ip} on {get_date()}\n")
                    writer.writerow((ip,"failed","SSH Timeout", get_date()))
                    failed_connection.append(ip)
                except ssh_exception.NetMikoAuthenticationException:
                    print(f"❌ Bad username or password to {ip} on {get_date()}\n")
                    writer.writerow((ip,"failed","Bad username or password", get_date()))
                    failed_connection.append(ip)
                except SSHException:
                    print(f"❌ Unable to connect. Check network device SSH configuration to {ip} on {get_date()}\n")
                    writer.writerow((ip,"failed","Unable to connect. Check network device SSH configuration", get_date()))
                    failed_connection.append(ip)
    print(tabulate([[len(failed_connection), "failed"], [len(successful_connection), "success"]],
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

def get_device_running_config(net_connect):
    """
    GET network device running configuration
        Args:
            net_connect (object): Netmiko ConnectHandler object
        return: Network device running-config
        rtype: str
    """
    return net_connect.send_command('show running-config')

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

def parse_config(config):
    """
    PARSE a cisco device configuration
        Args:
            config (str): Device configurations
        return: configuration list 
        rtype: list
    """
    return CiscoConfParse(config.splitlines(), syntax='ios')

if __name__ == "__main__":
    starttime = time.time()
    parser = argparse.ArgumentParser(description="Pass banner file name argument")
    parser.add_argument("--banner", help="Optional argument to pass a new banner\
                        from the ./banners directory. Example: 'legal_banner.txt'")
    args = parser.parse_args()
    if args.banner != None:
        main(args.banner)
    else:
        main()
    print(f"\nTotal Time Taken: {str(round(time.time() - starttime, 2))} seconds\n")
