import socket
import threading
from datetime import datetime

# Fake services and ports
SERVICES = {
    "Fake-FTP": 2121,
    "Fake-SSH": 2222,
    "Fake-HTTP": 8080
}
def classify_attack(command):
    if "wget" in command or "curl" in command:
        return "Malware Download Attempt"
    elif "rm -rf" in command:
        return "Destructive Command"
    elif "nc" in command or "netcat" in command:
        return "Backdoor Attempt"
    elif "chmod" in command:
        return "Privilege Escalation"
    elif command == "":
        return "Brute Force / Login Attempt"
    else:
        return "Reconnaissance / Unknown"
    test
def log_to_file(data):
    with open("honeypot.log","a") as f:
        f.write(data+"\n")

def log_attack(service, addr, port):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{time},{service},{addr[0]},{port}\n"

    print(log_entry)

    with open("honeypot.log", "a") as f:
        f.write(log_entry)

def start_honeypot(service, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", port))
    sock.listen(5)

    print(f"[+] {service} honeypot running on port {port}")

    while True:
        conn, addr = sock.accept()
        log_attack(service, addr, port)

        try:
            conn.send(b"login:")
            username= conn.recv(1024).decode(errors="ignore").strip()   
            conn.send(b"password: ")
            password = conn.recv(1024).decode(errors="ignore").strip() 
            conn.send(b"$ ")
            command = conn.recv(1024).decode(errors="ignore").strip()
            attack_log = (
              f"\n[{datetime.now()}]\n"
              f"Service: {service}\n"
              f"IP: {addr[0]}\n"
              f"Port: {port}\n"
              f"Username Tried: {username}\n"
              f"Password Tried: {password}\n"
              f"Command Executed: {command}\n"
              f"Attack Type: {classify_attack(command)}\n"
              + "-"*50
           )
            print(attack_log)
            log_to_file(attack_log)
           
        except Exception as e:
            pass

        conn.close() 

# Start all honeypots
for service, port in SERVICES.items():
    thread = threading.Thread(target=start_honeypot, args=(service, port))
    thread.daemon = True
    thread.start()

print("\n[+] Honeypot is ACTIVE. Waiting for attackers...\n")

while True:
    pass
