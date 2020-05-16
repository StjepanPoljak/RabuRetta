import json

class RabuRettaCommon():

    @staticmethod
    def from_json(json_data, fields):
        tuple_ret = []

        for field in fields:
            tuple_ret.append(json_data[field] if field in json_data else None)

        return tuple(tuple_ret)

    @staticmethod
    def package(obj):

        return bytes("*%s+" % obj.to_json(), "utf-8")

class RabuRettaDataProcessor():

    def __init__(self):
        self.msg_start = None
        self.mqueue = []
        self.unfinished = ""

    def rrsort(self):
        split_index = None
        prev_order = None

        self.mqueue.sort(key=lambda o: o.order)

        for index, msg in enumerate(self.mqueue, start=0):

            if index > 0 and msg.order - prev_order > 1:
                split_index = index
                break

            prev_order = msg.order

        if split_index:

            for _ in range(0, split_index - 1):
                self.mqueue.append(self.mqueue.pop(0))

    def add_data(self, data, process_message, type):
            data_decoded = self.unfinished + data.decode("utf-8")

            for key, char in enumerate(data_decoded, start=0):

                if char == "*":
                    self.msg_start = key

                elif char == "+":

                    if (
                            self.msg_start is not None and
                            self.msg_start + 1 <= key):

                        self.mqueue.append(
                                type.from_json(
                                    data_decoded[self.msg_start + 1 : key]
                                    )
                                )
                    else:
                        print("NULL message received!")

                    self.msg_start = None

            if self.msg_start is not None:
                self.unfinished = data_decoded[self.msg_start:]

            self.rrsort()

            while len(self.mqueue) > 0:
                message = self.mqueue.pop(0)
                print(str(message))
                process_message(message)

class RabuRettaComm():
    order = 0
    max_order = 128

    def __init__(self, order, comm, data_type, data):
        self.order = order
        self.comm = comm
        self.data_type = data_type
        self.data = data

    @classmethod
    def create(cls, comm, data_type, data):
        order = RabuRettaServerRequest.order
        RabuRettaServerRequest.order += 1

        if RabuRettaServerRequest.order == RabuRettaServerRequest.max_order:
            RabuRettaServerRequest.order = 0

        return cls(order, comm, data_type, data)

    def to_json(self):

        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):

        return self.to_json()

    def __str__(self):

        return repr(self)

    @classmethod
    def from_json(cls, jdata):
        json_data = json.loads(jdata)

        return cls(*RabuRettaCommon.from_json(
                json_data, [
                    "order",
                    "comm",
                    "data_type",
                    "data"
                    ]))

class RabuRettaServerRequest():
    order = 0
    max_order = 128

    @classmethod
    def create(cls, request, message, rcomm, rdata_type):
        order = RabuRettaServerRequest.order
        RabuRettaServerRequest.order += 1

        if RabuRettaServerRequest.order == RabuRettaServerRequest.max_order:
            RabuRettaServerRequest.order = 0

        return cls(order, request, message, rcomm, rdata_type)

    def __repr__(self):

        return self.to_json()

    def __str__(self):

        return repr(self)

    def __init__(self, order, request, message, rcomm, rdata_type):
            self.order = order
            self.request = request
            self.message = message
            self.rcomm = rcomm
            self.rdata_type = rdata_type

    def to_json(self):

        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_json(cls, jdata):
        json_data = json.loads(jdata)

        return cls(*RabuRettaCommon.from_json(
                json_data, [
                    "order",
                    "request",
                    "message",
                    "rcomm",
                    "rdata_type"
                    ]))
