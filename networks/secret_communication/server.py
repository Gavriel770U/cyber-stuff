from scapy.all import *
from consts import *

class SecretServer:
    def __init__(self) -> None:
        self.__running = True
    
    def __udp_filter(self, packet) -> bool:
        return (
            Ether in packet and
            IP in packet and
            UDP in packet and
            SERVER_IP == packet[IP].dst and
            CLIENT_PORT == packet[UDP].sport
        )
    
    def print_data(self, packet) -> None:
        packet.show()
    
    def run(self) -> None:
        while self.__running:
            packets = sniff(count=1, lfilter=self.__udp_filter)
            for packet in packets:
                if packet:
                    if Raw in packet:
                        data = packet[Raw].load.decode()
                        if EMPTY_MESSAGE == data:
                            print(chr(packet[UDP].dport), end=EMPTY_CHAR)
                            # send response packet, similar principle as TCP ACK
                            response = Ether(dst=getmacbyip(packet[IP].src)) / IP(src=packet[IP].dst, dst=packet[IP].src) / UDP(sport=packet[UDP].dport, dport=packet[UDP].sport) / Raw(EMPTY_MESSAGE.encode()) 
                            sendp(response, verbose=False)
                            
if __name__ == '__main__':
    server = SecretServer()
    server.run()