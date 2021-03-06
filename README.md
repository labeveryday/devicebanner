# devicebanner

This is a script that leverages the [netmiko library](https://pyneng.readthedocs.io/en/latest/book/18_ssh_telnet/netmiko.html) to update the banner motd on a network device. Then output the results to `results.csv`. Use this script to learn the basics of python.

> NOTE: This code will run on Linux, MAC and Windows

## Download the Code

To get started: Download the code and cd the `devicebanner` directory

```bash
git clone https://github.com/labeveryday/devicebanner
cd device banner
```

## Python Virtual Environment

When executing python code or installing python applications you should get into the practice of creating and managing python virtual environments.
This will allow you to run different versions of a python library while avoiding version conflicts. My preferred tool for python virtual environments is `venv`
There are many other tools available. Remember to explore and find what works best for you.

**On Linux or Mac**

```python
python3 -m venv venv
source venv/bin/activate
```

**On Windows**

```cmd
python3 -m venv venv
.\venv\Scripts\activate.bat
```

## Before running the code

A couple of things to note:

1. Modify the `ip_address_file.txt` file to update the list of ip addresses for the devices that you want to update.

2. Modify the device credentials in the `credentials.py` file. These are the creds that will be used to log into your network devices.

3. In the `banners/` directory is where you store the banners that will be used to update your devices. If you want to use a different banner you will need to do two things.

    - First create a new text banner file in the banners directory with the command line command `banner motd ^ENTER CODE HERE`

    ![banner](https://github.com/labeveryday/Notes/blob/main/images/banner.png)

    - Second you will need to enter the name of the file as an argument on line 109 of `main.py`

    >NOTE: There is no need to enter the file path. Just the name of the file!

    ![banner_arg](https://github.com/labeveryday/Notes/blob/main/images/banner_arg.png)

## Example: Script in action

Now that you have everything installed and updated you can execute the script

**Failed Attempt**

```bash
(venv) duan@ubuntu devicebanner$ python main.py
Attempting to log into 192.168.23.143.....
******************************
TCP connection to device failed.

Common causes of this problem are:
1. Incorrect hostname or IP address.
2. Wrong TCP port.
3. Intermediate firewall blocking access.

Device settings: cisco_ios 192.168.23.143:22


******************************

```

## TO BE CONTINUED....

### About me

Introverted Network Automation Engineer that is changing lives as a Developer Advocate for Cisco DevNet. Pythons scripts are delicious. Especially at 2am on a Saturday night.

My hangouts:

- [LinkedIn](https://www.linkedin.com/in/duanlightfoot/)

- [Twitter](https://twitter.com/labeveryday)