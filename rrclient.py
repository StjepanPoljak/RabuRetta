# Python3 Client Example

import socket
from rrcommon import *

class RabuRettaClientSettings():

    def __init__(self):
        self.saddr = None
        self.buffer_size = None

class RabuRettaClient():

    def __init__(self, settings):
        self.saddr = settings.saddr
        self.buffer_size = settings.buffer_size
        self.data_processor = RabuRettaDataProcessor()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.saddr)

    def wait_response(self):

        return self.sock.recv(self.buffer_size)

    def send_comm(self, comm, data_type, data):
        self.sock.send(bytes("*%s+" % RabuRettaComm.create(
            comm,
            data_type,
            data
            ).to_json(), "utf-8"))

    def process_message(self, message):
        user_input = None

        if message.request == "input":
            user_input = input(message.message)
            self.send_comm(
                message.rcomm,
                message.rdata_type,
                user_input)

    def start_client(self):

        while True:
            data = self.wait_response()

            if not data:
                break

            self.data_processor.add_data(
                    data,
                    self.process_message,
                    RabuRettaServerRequest
                    )

    def __del__(self):
        print("Closing socket...")
        self.sock.close()
