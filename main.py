from netmiko import ConnectHandler
import getpass
import time
import datetime

# ip_file = open('ipaddress.txt')
# 
# creds = {`username`: input('Enter username: '),
#          'password': getpass.getpass(),
#          'device_type': 'cisco_ios'}
# 
# 
# 
# now = datetime.datetime.now()
# 
# for i in ip_file:
#     ip = i.strip()
#     net_connect = ConnectHandler(ip=ip, device_type=device_type, username=username, password=password)
#     print('Connecting to %s' % ip)
#     time.sleep(1)
#     device_hostname = net_connect.send_command('show run | include hostname')
#     hostname = device_hostname[9:]
#     device_serial = net_connect.send_command('show inventory | include PID')
#     time.sleep(1)
#     net_connect.write_channel('config t \n')
#     time.sleep(1)
#     net_connect.write_channel(str(banner.read()) + '\n')
#     time.sleep(3)
#     net_connect.write_channel('exit \n')
#     time.sleep(1)
#     net_connect.write_channel('wri mem \n')
#     time.sleep(2)
#     show_session = net_connect.read_channel()
#     print(show_session)
#     time.sleep(1)
# 
#     clock = now.strftime('%m-%d-%Y %H:%M')
#     output = [hostname, ip, device_serial, clock]
#     sheet.append(output)
# 
#     workbook.save(file_location)
# 
# input('##### Enable Secret Update Successfully #####\n Press Enter to Exit')
