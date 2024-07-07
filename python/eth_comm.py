import socket

def tcp_client():
    host = '192.168.0.10'  # STM32 IP address
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello from PC')
        data = s.recv(1024)
        print('Received', repr(data))

if __name__ == "__main__":
    tcp_client()
