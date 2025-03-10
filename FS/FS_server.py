from flask import Flask, request
import socket

app = Flask(__name__)

def fibonacci(n):
    try:
        n = int(n)
        if n < 0:
            return None  
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    except ValueError:
        return None  

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not hostname or not ip or not as_ip or not as_port:
        return "Missing parameters", 400

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"

    try:
        sock.sendto(message.encode(), (as_ip, int(as_port)))
        return "Registration successful", 201
    except:
        return "Registration failed", 500
    finally:
        sock.close()

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    
    if not number:
        return "Missing number parameter", 400
    
    result = fibonacci(number)
    
    if result is None:
        return "Invalid number", 400
    
    return str(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)