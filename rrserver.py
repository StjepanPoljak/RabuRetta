# RabuRetta Server

import socket
import time
import selectors
import types
from enum import Enum
from rrcommon import *

class RabuRettaServerSettings():

    def __init__(self):
        self.address = None
        self.timesleep = 60
        self.timetry = 5
        self.buffer_size = None
        self.f_table = {}
        self.new_conn = None
        self.on_error = None

class RabuRettaUserPrivilege(Enum):
    Admin = 1
    Ordinary = 2
    Unassigned = 3

class RabuRettaUser():

    def __init__(self, addr):
        self.addr = addr
        self.data_processor = RabuRettaDataProcessor()
        self.outgoing = b""

        self.priv = RabuRettaUserPrivilege.Unassigned
        self.name = None
        self.age = None

    def __hash__(self):

        return self.addr

class RabuRettaServer():

    def __init__(self, rrss):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.buffer_size = rrss.buffer_size

        self.f_table = rrss.f_table
        self.new_conn = rrss.new_conn
        self.on_error = rrss.on_error

        attempt = rrss.timetry
        sock_addr = rrss.address

        while True:

            try:
                self.sock.bind(sock_addr)
                if (sock_addr[1] == 0):
                    sock_addr = (sock_addr[0], self.get_port())

            except OSError:

                if attempt == 0:
                    raise Exception(
                            "Could not bind socket to %s:%d." %
                            sock_addr
                            )

                print("Socket busy, retrying in 60s...")
                time.sleep(rrss.timesleep)

                attempt -= 1

                continue

            else:
                print("Socket bound to %s:%d." % sock_addr)

                break

        self.sock.listen()

        print("Waiting for connections...")

        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)

        while True:
            events = self.sel.select(timeout=None)

            for key, mask in events:

                if key.data is None:
                    addr = self.accept_conn()
                else:
                    self.process_data(key, mask, addr)

    def has_admin(self):

        return False if len(
            [ u for u in self.users.values()
                if u.priv == RabuRettaUserPrivilege.Admin
            ]) == 0 else True

    def get_port(self):

        return self.sock.getsockname()[1]

    def send_request(self, addr, request, message, data):
        self.users[addr].outgoing += RabuRettaCommon.package(
                RabuRettaServerRequest.create(
                    request,
                    message,
                    data
                    )
                )

    def accept_conn(self):
        conn, addr = self.sock.accept()
        conn.setblocking(False)

        print(
                "Accepted connection from: %s" %
                str(addr)
                )

        self.users[addr] = RabuRettaUser(addr)

        self.sel.register(
                conn,
                selectors.EVENT_READ | selectors.EVENT_WRITE,
                types.SimpleNamespace(
                    inb=b'',
                    outb=b''
                    )
                )

        if self.new_conn is not None:
            self.new_conn(self, addr)

        return addr

    def process_request(self, addr, message):

        if message.comm in self.f_table:
            try:
                if self.f_table[message.comm](
                        self,
                        addr,
                        *(el for el in message.data.split())
                        ) == False:
                    quit()

            except TypeError as e:
                self.server_error(
                        addr,
                        str(e)
                        )

        else:
            self.server_error(
                    addr,
                    "Invalid command '%s'" % message.comm
                    )

    def server_error(self, addr, error_message):

        if self.on_error:
            if self.on_error(addr, error_message) == False:
                quit()

        else:
            self.send_request(
                    addr,
                    "error",
                    error_message,
                    "retry"
                    )

    def del_user(self, addr):

        if addr not in self.users:

            return

        del self.users[addr]

    def process_data(self, key, mask, addr):
        sock = key.fileobj

        if mask & selectors.EVENT_READ:
            data = sock.recv(self.buffer_size)

            if data and addr in self.users:
                self.users[addr].data_processor.add_data(
                        data,
                        lambda msg: self.process_request(addr, msg),
                        RabuRettaComm
                        )
            else:
                print(
                        "Closing connection to %s..." %
                        str(addr)
                        )
                self.sel.unregister(sock)
                sock.close()

                if addr in self.users:
                    del self.users[addr]

        elif mask & selectors.EVENT_WRITE:

            if addr in self.users and self.users[addr].outgoing:
                key.data.outb += self.users[addr].outgoing
                self.users[addr].outgoing = b""

            if key.data.outb:
                sent_bytes = key.fileobj.send(key.data.outb)
                key.data.outb = key.data.outb[sent_bytes:]

    def __del__(self):
        print("Closing socket...")
        self.sock.close()

