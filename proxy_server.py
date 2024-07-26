import os
import sys
import subprocess
import threading
from flask import Flask, request
import time

def modify_hosts_file(domain, redirect_ip="127.0.0.1"):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect_entry = f"{redirect_ip} {domain}\n"

    try:
        with open(hosts_path, 'r') as file:
            lines = file.readlines()

        if any(redirect_entry.strip() in line.strip() for line in lines):
            print("Entry already exists in hosts file.")
            return

        with open(hosts_path, 'a') as file:
            file.write(redirect_entry)
        
        print(f"Added entry to hosts file: {redirect_entry}")

    except PermissionError:
        print("Permission denied: Please run this script as administrator.")
        sys.exit(1)

def flush_dns():
    if sys.platform == 'win32':
        subprocess.run(["ipconfig", "/flushdns"], check=True)
    else:
        print("DNS flush command is only applicable for Windows systems in this script.")

def start_flask_server():
    app = Flask(__name__)

    @app.route('/ex/sgsk/get.php')
    def intercept_request():
        key = request.args.get('key')
        if key == '123456':
            return "SGSK09000677A301"
        else:
            return "Key not recognized"
        # AD050845 || SQB55A67EDEA116B

    @app.route('/ex/sgjq/get.php')
    def intercept_get_request():
        key = request.args.get('key')
        if key == 'AD050845':
            return "AD050845 || SQB55A67EDEA116B"
    context = ('cert.pem', 'key.pem')
    app.run(host="127.0.0.1", port=443,ssl_context=context)

def main():
    domain = "siguojunqi.top"
    
    # Modify hosts file
    modify_hosts_file(domain)
    
    # Flush DNS cache
    flush_dns()

    # Start Flask server in a separate thread
    server_thread = threading.Thread(target=start_flask_server)
    server_thread.daemon = True
    server_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    main()
