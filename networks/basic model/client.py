import socket
from protocol import *

def run_client() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDRESS)
        
        is_connected = True
        
        while is_connected:
            data = input('Insert data for the server: ')
            protocol_send(client_socket, data)
            if EXIT == data:
                is_connected = False
            else:
                server_reply = protocol_recv(client_socket)
                print(server_reply)
        
def main() -> None:
    run_client()
    
if __name__ == '__main__':
    main()            