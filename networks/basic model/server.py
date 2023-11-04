import socket
from protocol import *
import random
from datetime import datetime

def get_time() -> str:
    return datetime.now().strftime("%a %b %d %H:%M:%S %Y")

def who_are_you() -> str:
    return "Gavriel's Server B)"

def get_random() -> str:
    return str(random.randint(1, 10))

def run_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(HOST_BIND)
        server_socket.listen()
        
        client_socket, client_address = server_socket.accept()
        
        commands: dict = {TIME : get_time, WHORU : who_are_you, RAND : get_random}
        
        with client_socket:
            is_connected = True
            while is_connected:
                command = protocol_recv(client_socket)
                if EXIT == command:
                    is_connected = False
                else:
                    if command in commands:
                        protocol_send(client_socket, commands[command]())
                    else:
                        protocol_send(client_socket, ERROR_MESSAGE)    

def main() -> None:
    run_server()
    
if __name__ == '__main__':
    main()