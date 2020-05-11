from raburetta import RabuRettaRound
from test.rrrtest import RabuRettaRoundTests

import unittest
import sys

if __name__ == "__main__":

    if len(sys.argv) >= 2:
        if sys.argv[1] == "test":
            unittest.main(argv=['first-arg-is-ignored'], exit=False)
            # Note: The unittest should be in a separate file,
            # so we need to hack this a bit...

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
