# RabuRetta Server

import socket
import time
import selectors
import types

class RabuRettaServerSettings():

    def __init__(self):
        self.address = None
        self.port = None
        self.timesleep = 60
        self.timetry = 5

class RabuRettaServer():

    def __init__(self, rrss):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        attempt = rrss.timetry
        sock_addr = (rrss.address, rrss.port)

        while True:

            try:
                self.sock.bind(sock_addr)

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
                    addr = accept_conn(self.sock)
                else:
                    process_data(key, mask, addr)

    def accept_conn(self):
        conn, addr = self.sock.accept()
        conn.setblocking(False)

        print(
                "Accepted connection from: %s" %
                str(addr)
                )

        sel.register(
                conn,
                selectors.EVENT_READ | selectors.EVENT_WRITE,
                types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
                )

        return addr

    def process_data(key, mask, addr):
        sock = key.fileobj

        if mask & selectors.EVENT_READ:
            data = sock.recv(64)

            if data:
                print(
                        "Got message from %s: %s" %
                        (str(addr), data.decode("utf-8"))
                        )
                key.data.outb += data

            else:
                print(
                        "Closing connection to %s..." %
                        str(addr)
                        )
                sel.unregister(sock)
                sock.close()

        elif mask & selectors.EVENT_WRITE:

            if key.data.outb:
                key.fileobj.send(b"OK")
                key.data.outb = b""

    def __del__(self):
        print("Closing socket...")
        self.sock.close()

