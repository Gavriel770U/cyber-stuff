from scapy.all import *
from consts import *
import time

class SecretClient:
    def __init__(self) -> None:
        self.__running = True
        
    def __is_server_response(self, packet) -> bool:
        return (
            Ether in packet and
            IP in packet and
            UDP in packet and
            SERVER_IP == packet[IP].src
        )

    def send_data(self, data: str) -> None:
        data += NEWLINE
        for char in data:
            response = None
            while not response:
                #print(f"Sending {char}...")
                packet = Ether(dst=getmacbyip(SERVER_IP)) / IP(dst=SERVER_IP) / UDP(sport=CLIENT_PORT, dport=ord(char)) / Raw(EMPTY_MESSAGE.encode())
                sendp(packet, verbose=False)
                responses = sniff(count=1, timeout=TIMEOUT_VALUE, lfilter=self.__is_server_response)
                for response in responses:
                    if Raw in packet:
                        data = packet[Raw].load.decode()
                        if not EMPTY_MESSAGE == data:
                            response = None
                    else:
                        response = None

    def run(self) -> None:
        while self.__running:
            data = input('Enter message for the server: ')
            if 'exit' == data.lower():
                self.__running = False
            else:
                self.send_data(data)

if __name__ == "__main__":
    client = SecretClient()
    client.run()