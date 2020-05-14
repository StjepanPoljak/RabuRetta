from raburetta import RabuRettaRound
from test.rrrtest import RabuRettaRoundTests

import sys

if __name__ == "__main__":

    if len(sys.argv) >= 2:

        if sys.argv[1] == "test":
            RabuRettaRoundTests.start()

        elif sys.argv[1] == "info":
            RabuRettaRound.print_info()

        else:
            print(
                    "Use 'test' option to run unit tests "
                    "and 'info' to get information on RabuRetta"
                    )
    else:
        rrr = RabuRettaRound(2)
        print(rrr)
        print("You got the card from the deck:\n\t" + str(rrr.get_card()))
