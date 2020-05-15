# Python3 Client Example

import socket
from rrcommon import RabuRettaComm

class RabuRettaClientSettings():

    def __init__(self):
        self.saddr = None
        self.buffer_size = None

class RabuRettaClient():

    def __init__(self, settings):

        self.saddr = settings.saddr
        self.buffer_size = settings.buffer_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.saddr)

    def wait_response(self):

        return self.sock.recv(self.buffer_size)

    def send_comm(self, comm, data_type, data):

        self.sock.send(bytes(RabuRettaComm(comm, data_type, data).to_json(), "utf-8"))

    def start_client(self):

        user_input = None

        while True:

            if not hasattr(self, "name"):
                user_input = input("Type in your name (q to quit): ")

            if not user_input:
                continue

            self.send_comm("set_name", "string", user_input)
            data = self.wait_response()

            if data:
                print(data.decode("utf-8"))

        while user_input != "q":

            user_input = input("Type in a message (q to quit): ")

            if user_input != "q":
                user_bytes = bytes(user_input, "utf-8")
                self.sock.send(user_bytes)
                data = self.sock.recv(64)

                print("Server response: %s" % data.decode("utf-8"))

    def __del__(self):
        print("Closing socket...")
        self.sock.close()
