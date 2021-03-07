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

## Install project requirements

Once you have your virtual environment setup and activated you will need to install your python packages. One way to do this is by doing `pip install <python package>`. For this project use the example listed below. It will installed the required libraries and dependencies for this specific project.

```bash
pip install -r requirements.txt
```

## Before running the code

A couple of things to note:

1. Modify the `ip_address_file.txt` file to update the list of ip addresses for the devices that you want to update.

2. Modify the device credentials in the `credentials.py` file. In this file are the creds that will be used to log into your network devices.

3. In the `banners/` directory is where we store the banners that will be used to update your devices. If you want to use a different banner you will need to do two things. By default the script uses the `cisco_devnet.txt` file.

    - ***FIRST*** create a new text banner file in the banners directory with the command line argument `banner motd ^ENTER CODE INSIDE HERE^`

    ![banner](https://github.com/labeveryday/Notes/blob/main/images/banner.png)

    - ***SECOND*** pass in the new file name as a command line argument `python main.py --banner <banner_name.txt>`

    >NOTE: There is no need to enter the file path. Just the name of the file!

    ```bash
    (venv) duan@ubuntu devicebanner$ python main.py -h
    usage: main.py [-h] [--banner BANNER]

    Pass banner file name argument

    optional arguments:
    -h, --help       show this help message and exit
    --banner BANNER  Optional argument to pass a new banner from the ./banners
                     directory. Example: 'legal_banner.txt'
    ```

## Example: Script in action

Now that the required dependencies are installed and updated you can now execute the script.

```bash
(venv) duan@ubuntu devicebanner$ python main.py
Attempting to log into 192.168.23.142.....
✅ Banner was successfully added to SW2-IOSv on 03-06-2021 18:38

Attempting to log into 192.168.23.143.....
✅ Banner was successfully added to SW3-IOSv on 03-06-2021 18:38

Attempting to log into 192.168.23.144.....
✅ Banner was successfully added to SW1-IOSv on 03-06-2021 18:38

Attempting to log into 192.168.23.145.....
❌ SSH timeout attempt to 192.168.23.145 on 03-06-2021 18:38

Attempting to log into 192.168.23.148.....
❌ Bad username or password to 192.168.23.148 on 03-06-2021 18:38

Attempting to log into 192.168.23.149.....
❌ SSH timeout attempt to 192.168.23.149 on 03-06-2021 18:38

Attempting to log into 192.168.23.150.....
✅ Banner was successfully added to R2-iosv on 03-06-2021 18:39

Attempting to log into 192.168.23.151.....
❌ SSH timeout attempt to 192.168.23.151 on 03-06-2021 18:39

Attempting to log into 192.168.23.153.....
❌ Unable to connect. Check network device SSH configuration to 192.168.23.153 on 03-06-2021 18:39

+-------------------+---------+
| Number_of_Devices | Status  |
+-------------------+---------+
|         5         | failed  |
|         4         | success |
+-------------------+---------+

Total Time Taken: 45.53 seconds

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
