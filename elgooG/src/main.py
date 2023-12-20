from dns_server import *

def main():
    dns_server = DNSServer()
    dns_server.add_redirection('www.example.com', '66.22.84.27')
    dns_server.run_server_above_udp()

if __name__ == '__main__':
    main()