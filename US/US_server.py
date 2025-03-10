from flask import Flask, request
import socket
import requests

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci_handler():
    """Handle requests for Fibonacci numbers"""
    
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return "Missing required parameters", 400
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_query = f"TYPE=A\nNAME={hostname}"
    sock.sendto(dns_query.encode(), (as_ip, int(as_port)))
    
    response, _ = sock.recvfrom(1024)
    response_data = response.decode()
    
    fs_ip = None
    for line in response_data.split('\n'):
        if line.startswith('VALUE='):
            fs_ip = line.split('=')[1]  
            break
    
    if not fs_ip:
        return "Could not resolve Fibonacci server", 500
    
    fibonacci_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    fs_response = requests.get(fibonacci_url)
    
    if fs_response.status_code == 200:
        return fs_response.text, 200
    else:
        return "Fibonacci server error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)