import unittest
from random import randint
from raburetta import RabuRettaRound

class RabuRettaRoundTests(unittest.TestCase):

    def test_type(self):
        """Test if type is RabuRettaRound"""

        self.assertEqual(type(RabuRettaRound()), RabuRettaRound)

    def test_players(self):
        """Test exception raising on invalid number of players"""

        for num in range(0, 4):
            if num <= 0 or num > 4:
                self.assertRaises(Exception, RabuRettaRound(num))
            else:
                try:
                    RabuRettaRound(num)
                except Exception:
                    self.fail("Number of players should be valid.")

    def test_len(self):
        """Test deck size for various player number inputs."""

        for _ in range(0, 100):
            for num in range(2, 5):
                self.assertEqual(len(RabuRettaRound(num)), 12 if num == 2 else 15)

    def test_getitem(self):
        """Test __getitem__ method"""

        for num in range(2,5):
            rrr = RabuRettaRound(num)
            rrr_length = len(rrr)
            card = None
            card_hash = {}

            for index in range(-3 - rrr_length, rrr_length + 3):

                if ((index >= rrr_length and index >= 0) or
                    (-index > rrr_length and index <= 0)):

                    with self.assertRaises(IndexError):
                        rrr[index]

                    # Note: self.assertRaises(IndexError, rrr[index])
                    # won't work because rrr[index] will raise IndexError
                    # before self.assertRaises gets called; another
                    # solution would be to make rrr[index] a method, e.g.:
                    # self.assertRaises(IndexError, lambda: rrr[index])

                else:
                    try:
                        card = rrr[index]

                    except IndexError:
                        self.fail(
                                "Index " + str(index) + " should not be " +
                                " out of bounds (length: " + str(rrr_length) + ")."
                                )

            for index in range(0, rrr_length):

                try:
                    card = rrr[index]
                    card_hash[card.name] += 1

                except KeyError:
                    card_hash[card.name] = 1

                except IndexError:
                    self.fail("Index out of bounds!")

            try:
                for card in rrr.deck:
                    self.assertEqual(card_hash[card.name], card.count)

            except KeyError:
                self.fail(card.name + " not hashed!")

    def test_iter(self):
        """Test iter and last"""

        for num in range(2, 5):

            rrr = RabuRettaRound(num)
            rrr_iter = iter(rrr)

            # Note: __getitem__ and __len__ are enough
            # to provide for __iter__

            rrr_length = len(rrr)
            item = None
            counter = 0

            while True:
                try:
                    item = next(rrr_iter)
                    self.assertTrue(counter < rrr_length)
                    counter += 1

                except StopIteration:
                    self.assertEqual(item, rrr[-1])
                    break

    def test_add_to_hand(self):

        for num in range(2, 5):
            rrr = RabuRettaRound(num)

            curr_player = randint(1, num)

            self.assertEqual(rrr.get_player(curr_player).hand_count(), 0)

            rrr.give_card_from_deck_to_player(curr_player)

            self.assertEqual(rrr.get_player(curr_player).hand_count(), 1)

            rrr.give_card_from_deck_to_player(curr_player)

            self.assertEqual(rrr.get_player(curr_player).hand_count(), 2)

            with self.assertRaises(Exception):
                rrr.give_card_from_deck_to_player(curr_player)
