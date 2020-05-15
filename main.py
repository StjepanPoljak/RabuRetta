from raburetta import RabuRettaRound
from test.rrrtest import RabuRettaRoundTests
from rrserver import RabuRettaServer, RabuRettaServerSettings
from rrclient import RabuRettaClient, RabuRettaClientSettings

import sys

address = ("127.0.0.1", 12000)
buffer_size = 1024

if __name__ == "__main__":

    if len(sys.argv) >= 2:

        if sys.argv[1] == "test":
            RabuRettaRoundTests.start()

        elif sys.argv[1] == "info":
            RabuRettaRound.print_info()

        elif sys.argv[1] == "server":
            rrss = RabuRettaServerSettings()
            rrss.address = address
            rrss.buffer_size = buffer_size

            try:
                RabuRettaServer(rrss)

            except KeyboardInterrupt:
                print("\nInterrupted by user...")

        elif sys.argv[1] == "client":
            rrcs = RabuRettaClientSettings()
            rrcs.saddr = ("127.0.0.1", 12000)
            rrcs.buffer_size = buffer_size

            try:
                rrc = RabuRettaClient(rrcs)
                rrc.start_client()
            except KeyboardInterrupt:
                print("\nInterrupted by user...")

        else:
            print(
                    "Use 'test' option to run unit tests "
                    "and 'info' to get information on RabuRetta"
                    )
    else:
        rrr = RabuRettaRound(2)
        print(rrr)
        print("You got the card from the deck:\n\t" + str(rrr.get_card()))
