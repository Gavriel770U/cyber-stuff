HOST_BIND: tuple = ('0.0.0.0', 8820)
SERVER_ADDRESS: tuple = ('127.0.0.1', 8820)

FIRST_BYTES_AMOUNT: int = 2

TIME: str = 'TIME'
WHORU: str = 'WHORU'
RAND: str = 'RAND'
EXIT: str = 'EXIT'

EMPTY_MESSAGE: str = ' '
ERROR_MESSAGE: str = 'Wrong Protocol Command!'

def protocol_send(socket, message: str) -> None:
    message: str = message[:(10**FIRST_BYTES_AMOUNT-1)]
    socket.send(str(len(message)).zfill(FIRST_BYTES_AMOUNT).encode() + message.encode())

def protocol_recv(socket) -> str:
    length: int = int(socket.recv(FIRST_BYTES_AMOUNT).decode())
    return socket.recv(length).decode()