import socket

class DNSServer:
    def __init__(self) -> None:
        self.__is_running: bool = True
        """
        self.__redirection_table structure:
        Source IP : Destination IP
        """
        self.__redirection_table: dict = {}
    
    @property
    def __DNS_SERVER_IP(self) -> str:
        return '0.0.0.0'
    
    @property
    def __DNS_SERVER_PORT(self) -> int:
        return 53
    
    @property
    def __DEFAULT_BUFFER_SIZE(self) -> int:
        return 1024
    
    @property
    def __DNS_SERVER_ADDRESS(self) -> tuple:
        return (self.__DNS_SERVER_IP, self.__DNS_SERVER_PORT)
    
    @property
    def __ZERO_BYTE(self) -> bytes:
        return b'\x00'
    
    @property
    def __BYTEORDER_BIG(self) -> str:
        return 'big'
    
    @property
    def __BYTE_DOT(self) -> str:
        return b'.'
    
    @property
    def __NO_ERROR_FLAGS(self) -> bytes:
        return b'\x81\x80'
    
    @property
    def __NO_RR(self) -> bytes:
        return b'\x00\x00'
    
    @property
    def __ONE_RR(self) -> bytes:
        return b'\x00\x01'
    
    @property
    def __TTL(self) -> bytes:
        return b'\x00\x00\x00\xaf'
    
    @property
    def __DATA_LENGTH(self) -> bytes:
        return b'\x00\04'
    
    @property
    def __DOMAIN_POINTER(self) -> bytes:
        return b'\xc0\x0c'

    def __domain_to_dns_domain(self, domain: str) -> bytes:
        split = domain.split(".")
        result = b""
        for part in split:
            result += len(part).to_bytes(1, self.__BYTEORDER_BIG) + part.encode()
        return result + self.__ZERO_BYTE


    def __address_to_dns_address(self, address: str) -> bytes:
        result = b""
        for num in address.split("."):
            result += int(num).to_bytes(1, self.__BYTEORDER_BIG)
        return result
    
    def set_redirection_table(self, redirection_table: dict) -> None:
        self.__redirection_table = redirection_table
    
    def add_redirection(self, src_ip: str, dst_ip: str) -> None:
        if src_ip in self.__redirection_table:
            return
        else:
            self.__redirection_table[src_ip] = dst_ip          
    
    def get_redirection_table(self) -> dict:
        return self.__redirection_table 
    
    def __int_to_bytes(self, value: int) -> bytes:
        return bytes([value])
            
    def __parse_dns_request_query(self, query: bytes) -> dict:
        query_data: dict = {}
        query_data_name = b''
        byte: bytes = b''
        index: int = 12
        
        query_data["Transaction ID"] = query[0:2]
        query_data["Flags"] = query[2:4]
        query_data["Questions"] = query[4:6]
        query_data["Answer RRs"] = query[6:8]
        query_data["Authority RRs"] = query[8:10]
        query_data["Additional RRs"] = query[10:12]
        
        while (byte := self.__int_to_bytes(query[index])) != self.__ZERO_BYTE:
            index += 1
            length = int.from_bytes(byte, byteorder=self.__BYTEORDER_BIG)
            query_data_name += query[index:index+length] + self.__BYTE_DOT
            index += length

        query_data["Name"] = query_data_name[:-1]
        query_data["Type"] = query[-4:-2]
        query_data["Class"] = query[-2:]
        
        return query_data
    
    def __create_dns_response_query(self, request_query: bytes) -> bytes:
        request_query_data = self.__parse_dns_request_query(request_query)
        response_query = request_query_data["Transaction ID"]
        response_query += self.__NO_ERROR_FLAGS
        response_query += request_query_data["Questions"]
        response_query += self.__ONE_RR
        response_query += self.__NO_RR * 2 # for Authority RRs and Additional RRs
        
        domain = request_query_data["Name"].decode()
        
        # Add Query data
        response_query += self.__domain_to_dns_domain(domain)
        response_query += request_query_data["Type"]
        response_query += request_query_data["Class"]
        
        # Add Answer data
        response_query += self.__DOMAIN_POINTER
        response_query += request_query_data["Type"]
        response_query += request_query_data["Class"]
        response_query += self.__TTL
        response_query += self.__DATA_LENGTH
        
        if domain in self.__redirection_table:
            response_query += self.__address_to_dns_address(self.__redirection_table[domain])
        else:
            response_query += self.__address_to_dns_address("127.0.0.1")          
        
        return response_query
    
    def __dns_handler(self, data: bytes, address: tuple) -> bytes:
        result = self.__create_dns_response_query(data)
        #* print(f"RESULT: {result}")
        return result
    
    def run_server_above_udp(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(self.__DNS_SERVER_ADDRESS)
        print("Server started successfully! Waiting for data...")
        
        while self.__is_running:
            try:
                data, address = server_socket.recvfrom(self.__DEFAULT_BUFFER_SIZE)
                print(f"data: {data} type: {type(data)}\n address: {address} type: {type(address)}")
                server_socket.sendto(self.__dns_handler(data, address), address)
            except Exception as e:
                print(f"Client exception! {e}")