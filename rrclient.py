# Python3 Client Example

import socket
from rrcommon import *

class RabuRettaClientSettings():

    def __init__(self):
        self.saddr = None
        self.buffer_size = None
        self.error_recover = None

class RabuRettaClient():

    def __init__(self, settings):
        self.saddr = settings.saddr
        self.buffer_size = settings.buffer_size
        self.data_processor = RabuRettaDataProcessor()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.saddr)
        self.prev_message = None

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
            if message.rcomm:
                self.send_comm(
                    message.rcomm,
                    "string",
                    user_input
                    )
            else:

                scomm, sdata = (user_input, "")

                try:
                    scomm, sdata = user_input.split(" ", 1)

                except ValueError:
                    pass

                finally:
                    self.send_comm(
                        scomm,
                        "string",
                        sdata
                        )

        elif message.request == "output":
            print(message.message)

        elif message.request == "kick":
            print(message.message)
            quit()

        elif message.request == "error":
            print("Server error: %s" % message.message)

            if message.rcomm == "retry" and self.prev_message is not None:
                self.process_message(self.prev_message)
            else:
                quit()

        if message.request != "error":
            self.prev_message = message

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
