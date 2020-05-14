from raburetta import RabuRettaRound
from test.rrrtest import RabuRettaRoundTests
from rrserver import RabuRettaServer, RabuRettaServerSettings

import sys

if __name__ == "__main__":

    if len(sys.argv) >= 2:

        if sys.argv[1] == "test":
            RabuRettaRoundTests.start()

        elif sys.argv[1] == "info":
            RabuRettaRound.print_info()

        elif sys.argv[1] == "server":
            rrss = RabuRettaServerSettings()
            rrss.address = '127.0.0.1'
            rrss.port = 12000

            try:
                RabuRettaServer(rrss)

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
