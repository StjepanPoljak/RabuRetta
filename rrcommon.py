import json

class RabuRettaComm():

    def __init__(self, comm, data_type, data):
        self.comm = comm
        self.data_type = data_type
        self.data = data

    def to_json(self):

        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def from_json(self, jdata, process_data):

        json_data = json.loads(jdata)

        self.comm = json_data["comm"] if "comm" in json_data else None
        self.data_type = json_data["data_type"] if "data_type" in json_data else None
        self.data = json_data["data"] if "data" in json_data else None
