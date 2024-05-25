import network
import usocket as socket
import ujson
from driver import Driver
import time

class Host:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(False)
    
    def connect(self):
        self.sta_if.active(True)
        self.sta_if.connect(self.ssid, self.password)
        for i in range(5):
            if self.sta_if.isconnected():
                print('Connected to WiFi')
                print('IP:', self.sta_if.ifconfig()[0])
                return
            else:
                print('Failed to connect to WiFi')
                time.sleep(1)

class Server:
    def __init__(self):
        self.server_socket = None
        self.__listener = None
        
    def set_listener(self, listener: Driver):
        self.__listener = listener

    def initialize(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 8000))  # Bind to all available interfaces
        self.server_socket.listen(1)  # Listen for incoming connections
        print('Server initialized')
        
    def _connect(self):
        while True:
            client_socket, client_address = self.server_socket.accept()  # Accept incoming connection
            print('Connection from:', client_address[0])

            request = client_socket.recv(1024)
            request = request.decode("utf-8") # convert bytes to string
            self.__process_data(request, client_socket)
            client_socket.close()
            
    def __process_data(self, data, client_socket):
        """
        400 - wrong request
        """
        command = self.__request_parser(data).get("command")
        code = self.__listener.listen(command)
        response = f"HTTP/1.1 {code} OK\r\n\r\n"  # Status line and empty headers
        client_socket.send(response.encode("utf-8"))
        
    def __request_parser(self, data):
        splited_data = data.replace("\r", "").split("\n")
        try:
            json_data = ujson.loads(splited_data[-1])
            return json_data
        except Exception as e:
            print("Error parsing JSON:", e)

    def start(self):
        self._connect()
        print("runed")

    def stop(self):
        if self.server_socket:
            self.server_socket.close()
            print('Server stopped')
        else:
            print('Server not initialized')
            

class AccessPoint:
    pass

class Connection:
    pass

