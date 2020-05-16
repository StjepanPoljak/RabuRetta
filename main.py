from raburetta import RabuRettaRound
from test.rrrtest import RabuRettaRoundTests
from rrserver import RabuRettaServer, RabuRettaServerSettings
from rrclient import RabuRettaClient, RabuRettaClientSettings

import sys

buffer_size = 8

if __name__ == "__main__":

    if len(sys.argv) >= 2:

        if sys.argv[1] == "test":
            RabuRettaRoundTests.start()

        elif sys.argv[1] == "info":
            RabuRettaRound.print_info()

        elif sys.argv[1] == "server":

            if len(sys.argv) < 3:
                address = ("127.0.0.1", 0)
            else:
                address = (sys.argv[2], 0)

            rrss = RabuRettaServerSettings()
            rrss.address = address
            rrss.buffer_size = buffer_size

            try:
                RabuRettaServer(rrss)

            except KeyboardInterrupt:
                print("\nInterrupted by user...")

        elif sys.argv[1] == "client":

            if len(sys.argv) != 4:
                print("Please specify address and port number.")

            elif len(sys.argv) == 4:
                rrcs = RabuRettaClientSettings()
                rrcs.saddr = (sys.argv[2], int(sys.argv[3]))
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
