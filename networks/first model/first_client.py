import socket

def run_client() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 8820))
        is_connected = True

        while is_connected:
            message = input('Enter message for the server: ')
            client_socket.send(message.encode())
            if not ("exit" == message.lower()) and not ("server exit" == message.lower()):
                data = client_socket.recv(1024).decode()
                print('Server sent:', data)
            else:
                is_connected = False

def main() -> None:
    run_client()

if __name__ == '__main__':
    main()                    