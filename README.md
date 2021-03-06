# devicebanner

This is a script that leverages the [netmiko library](https://pyneng.readthedocs.io/en/latest/book/18_ssh_telnet/netmiko.html) to update the banner motd on a network device. Once the device update has been attempted the update status is then output to the `results.csv` file. Use this script to learn the basics of python.

> NOTE: This code will run on Linux, MAC and Windows

## Download the Code

To get started: Download the code and cd to the `devicebanner` directory

```bash
git clone https://github.com/labeveryday/devicebanner
cd device banner
```

## Python Virtual Environment

When executing python code or installing python packages you should get into the practice of creating and managing python virtual environments.
This will allow you to run different versions of a python library while avoiding software version conflicts. My preferred tool for python virtual environments is [venv](https://docs.python.org/3/library/venv.html)
There are many other tools available. Remember to explore and find the one that works best for you.

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

2. Modify the device credentials in the `credentials.py` file. In this file are the creds that will be used to log into your network devices.

3. In the `banners/` directory is where we store the banners that will be used to update your devices. If you want to use a different banner you will need to do two things.

    - ***FIRST*** create a new text banner file in the banners directory with the command line argument `banner motd ^ENTER CODE INSIDE HERE^`

    ![banner](https://github.com/labeveryday/Notes/blob/main/images/banner.png)

    - ***SECOND*** you will need to enter the name of the file as an argument on line 109 of `main.py`

    >NOTE: There is no need to enter the file path. Just the name of the file!

    ![banner_arg](https://github.com/labeveryday/Notes/blob/main/images/banner_arg.png)

## Example: Script in action

Now that you have everything installed and updated you can execute the script.

```bash
(venv) duan@ubuntu devicebanner$ python main.py
Attempting to log into 192.168.23.142.....
✅ Banner was successfully added to SW2-IOSv on 03-06-2021 10:32

Attempting to log into 192.168.23.143.....
✅ Banner was successfully added to SW3-IOSv on 03-06-2021 10:32

Attempting to log into 192.168.23.144.....
✅ Banner was successfully added to SW1-IOSv on 03-06-2021 10:32

Attempting to log into 192.168.23.145.....
❌ SSH timeout attempt to 192.168.23.145 on 03-06-2021 10:32

Attempting to log into 192.168.23.148.....
✅ Banner was successfully added to R1-iosv on 03-06-2021 10:32

Attempting to log into 192.168.23.149.....
❌ SSH timeout attempt to 192.168.23.149 on 03-06-2021 10:32

Attempting to log into 192.168.23.150.....
❌ SSH timeout attempt to 192.168.23.150 on 03-06-2021 10:32

Attempting to log into 192.168.23.151.....
❌ SSH timeout attempt to 192.168.23.151 on 03-06-2021 10:32

Attempting to log into 192.168.23.153.....
❌ SSH timeout attempt to 192.168.23.153 on 03-06-2021 10:32

+-------------------+---------+
| Number_of_Devices | Status  |
+-------------------+---------+
|         5         | failed  |
|         4         | success |
+-------------------+---------+
Total Time Taken: 37.61 seconds

```

Once the script has been executed the results will begin to print to the screen. Once complete you can now verify the results in the `results.csv` file and on the network device.

**Banner results.csv**

![banner results](https://github.com/labeveryday/Notes/blob/main/images/banner_results.png)

**Banner verification on router**

![Device banner results](https://github.com/labeveryday/Notes/blob/main/images/banner_example.png)

This script is still in progress. The next phase will be to added device banner verification to ensure that the desired banner state has been implemented. `STAY TUNED`

### About me

Introverted Network Automation Engineer that is changing lives as a Developer Advocate for Cisco DevNet. Pythons scripts are delicious. Especially at 2am on a Saturday night.

My hangouts:

- [LinkedIn](https://www.linkedin.com/in/duanlightfoot/)

- [Twitter](https://twitter.com/labeveryday)