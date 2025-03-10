import socket
import json
import os

SERVER_PORT = 53533
DNS_DB_FILE = "/app/dns_records.json"

def load_dns_records():
    if os.path.exists(DNS_DB_FILE):
        try:
            with open(DNS_DB_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_dns_records(records):
    with open(DNS_DB_FILE, 'w') as f:
        json.dump(records, f)

dns_records = load_dns_records()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', SERVER_PORT))

print("Authoritative Server is running...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()
    print(f"Received: {message}", flush=True)

    if 'VALUE=' in message:
        lines = message.split("\n")
        name, value = None, None

        for line in lines:
            if line.startswith("NAME="):
                name = line.split("=")[1]
            elif line.startswith("VALUE="):
                value = line.split("=")[1]

        if name and value:
            dns_records[name] = value  
            save_dns_records(dns_records)  
            print(f"Registered {name} -> {value}")
            server_socket.sendto("Success".encode(), client_address)

    else:
        lines = message.split("\n")
        name = None

        for line in lines:
            if line.startswith("NAME="):
                name = line.split("=")[1]

        if name and name in dns_records:
            response = f"TYPE=A\nNAME={name}\nVALUE={dns_records[name]}\nTTL=10"
            server_socket.sendto(response.encode(), client_address)
            print(f"Sent response: {response}")
        else:
            print("No matching record found.")