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

class RabuRettaUserPrivilege(Enum):
    Admin = 1
    Ordinary = 2

class RabuRettaUser():

    def __init__(self, addr, priv):
        self.priv = priv
        self.addr = addr
        self.data_processor = RabuRettaDataProcessor()

class RabuRettaServer():

    def __init__(self, rrss):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []
        self.buffer_size = rrss.buffer_size

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
            [ u for u in self.users
                if u.priv == RabuRettaUserPrivilege.Admin
            ]) == 0 else True

    def get_port(self):

        return self.sock.getsockname()[1]

    def accept_conn(self):
        conn, addr = self.sock.accept()
        conn.setblocking(False)

        greet_req = RabuRettaCommon.package(
                RabuRettaServerRequest.create(
                    "input",
                    "Type in your name: ",
                    "set_name",
                    "string"
                    )
                )

        print(
                "Accepted connection from: %s" %
                str(addr)
                )

        self.sel.register(
                conn,
                selectors.EVENT_READ | selectors.EVENT_WRITE,
                types.SimpleNamespace(
                    user_id=len(self.users),
                    addr=addr,
                    inb=b'',
                    outb=greet_req,
                    )
                )

        self.users.append(
                RabuRettaUser(
                    addr,
                    RabuRettaUserPrivilege.Ordinary if self.has_admin()
                    else RabuRettaUserPrivilege.Admin
                    )
                )

        return addr

    def simple_print(self, addr, message):
        print(
                "Got message from %s: %s" %
                (str(addr), message)
                )

    def process_data(self, key, mask, addr):
        sock = key.fileobj

        if mask & selectors.EVENT_READ:
            data = sock.recv(self.buffer_size)

            if data:
                self.users[key.data.user_id].data_processor.add_data(
                        data,
                        lambda msg: self.simple_print(addr, msg),
                        RabuRettaComm
                        )
            else:
                print(
                        "Closing connection to %s..." %
                        str(addr)
                        )
                self.sel.unregister(sock)
                sock.close()

                for user in self.users:
                    if user.addr == addr:
                        self.users.remove(user)
                        break

        elif mask & selectors.EVENT_WRITE:

            if key.data.outb:
                sent_bytes = key.fileobj.send(key.data.outb)
                key.data.outb = key.data.outb[sent_bytes:]

    def __del__(self):
        print("Closing socket...")
        self.sock.close()

