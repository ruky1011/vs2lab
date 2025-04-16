"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

telephoneBook = {
        "Hans": "1234",
        "Peter": "5678",
        "Paul": "91011",
        "Max": "121314",
        "Sabine": "151617"
}

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server initialized and bound to socket.")

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        self._logger.info("Server is now listening for connections.")
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                self._logger.info(f"Connection accepted from {address}")
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        self._logger.info("No data received, closing connection.")                        
                        try:
                            data = connection.recv(1024)
                        except ConnectionResetError:
                            logging.warning("Connection reset by peer")
                            break
                        break  # stop if client stopped
                    self._logger.info(f"Received data: {data.decode('ascii')}")
                    response = Server.requestHandler(self, data)
                    self._logger.info(f"Sending response: {response}")
                    connection.send(response.encode('ascii'))
                connection.close()  # close the connection
                self._logger.info("Connection closed.")
            except socket.timeout:
                self._logger.debug("Socket timeout, no incoming connections.")
        self.sock.close()
        self._logger.info("Server socket closed.")

    
    def requestHandler(self, data):
        decodedData = data.decode('ascii')
        if decodedData.startswith("GET "):
            name = decodedData[4:]
            if name in telephoneBook:
                return name + ": " + telephoneBook[name]
            else:
                return "Name not in telephonebook"
        elif decodedData.startswith("GETALL"):
            allEntries = ""
            for names, number in telephoneBook.items():
                allEntries = allEntries + names + ": " + number + "\n"
            return allEntries
        else:
            return "Command not found"
        

class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client initialized and connected to server socket.")

    def call(self, msg_in):
        """ Call server """
        self.logger.info(f"Sending message to server: {msg_in}")
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        self.logger.info(f"Received response from server: {msg_out}")
        self.sock.close()  # close the connection
        self.logger.info("Client socket closed.")
        return msg_out
    
    def close(self):
        """ Close socket """
        self.logger.info("Closing client socket.")
        self.sock.close()