import socket

def run_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', 8820))
        server_socket.listen()

        client_socket, client_address = server_socket.accept()
        
        with client_socket:
            is_client_connected = True
            is_server_connected = True
            while is_server_connected:
                while is_client_connected:
                    data = client_socket.recv(1024).decode()
                    print('Client sent:', data)
                    if "server exit" == data.lower():
                        is_server_connected = False
                        is_client_connected = False
                    elif "exit" == data.lower():
                        is_client_connected = False    
                    else:    
                        reply = 'echo '+data
                        client_socket.send(reply.encode())

def main() -> None:
    run_server()
        
if __name__ == '__main__':
    main()                        