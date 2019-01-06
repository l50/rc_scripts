# rc_scripts
[![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/l50/rc_scripts/blob/master/LICENSE)

This repo is used to house various metasploit resource scripts and associated wrappers. It currently includes the following:

- ```windows/eternalblue.rc``` -- Used to automatically exploit eternal blue and then dump the hashes of the users on the target system

- ```linux/shellshock.rc``` -- Used for post exploitation automation activities, as well as establishing a session to a system that's vulnerable to shell shock. It's launched from a wrapper, ```shellshock.py```, which takes care of the exploitation piece. This was done because the shellshock module in the metasploit framework was not working for me.

- ```linux/rogue_backdoor.rc``` -- Used for post exploitation automation activities, as well as establishing a session to a system with a backdoor. It's launched from a wrapper, ```rogue_backdoor.py```, which takes care of the exploitation piece.
