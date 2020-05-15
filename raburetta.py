from random import randint
import copy
from enum import Enum

class Card():
    """Rabu Retta card class"""

    def __init__(self, name, value, count=1):
        """Rabu Retta card init"""

        self.name = name
        self.value = value
        self.count = count

    def __repr__(self):

        return "Card(%s, %s, %s)" % (self.name, self.value, self.count)

    def __str__(self):

        return "%s (%d)" % (self.name, self.value)

class PlayerType(Enum):
    Human = 1
    AI = 2

class PlayerStatus(Enum):
    InGame = 1
    Win = 2
    Loss = 3

class Player():

    def __init__(self, id, age=0, type=PlayerType.Human):
        self.id = id
        self.hand = []
        self.faceup = []
        self.type = type
        self.age = age
        self.status = PlayerStatus.Playing

    def add_card_to_hand(self, card):
        self.hand.append(card)

        if self.hand_count() > 2:
            raise Exception("Game logic error: too many cards in hand!")

    def hand_count(self):

        if not self.hand:
            return 0

        card_count = 0

        for card in self.hand:
            card_count += card.count

        return card_count

    def play_card(self, card):

        if card not in self.hand:
            raise Exception("Game logic error: card not in hand")

        self.faceup.append(card)
        self.hand.remove(card)

    def __hash__(self):

        return self.id

# Note: str() is used to create output for end-user,
# while repr() is used for debugging purposes, i.e.
# for official representation of the object

class RabuRettaRound():
    """Rabu Retta round class"""

    # static / class variable
    card_pool = [
            Card("Princess", 8),
            Card("Countess", 7),
            Card("King", 6),
            Card("Prince", 5, 2),
            Card("Handmaid", 4, 2),
            Card("Baron", 3, 2),
            Card("Priest", 2, 2),
            Card("Guard", 1, 5)
            ]

    rounds_played = 0

    def __init__(self, players=4):
        """Rabu Retta round init"""

        if players > 4 or players < 0:
            raise Exception("Invalid number of players (2-4)")

        self.length_hash = -1
        self.players = players
        self.deck = copy.deepcopy(RabuRettaRound.card_pool)
        to_remove = randint(0, len(self) - 1)

        self.facedown = []
        self.faceup = []

        self.facedown.append(self.pop(to_remove))

        if players == 2:
            for _ in range(0, 3):
                self.faceup.append(self.pop(randint(0, len(self) - 1)))

        self.player_data = [ Player(id) for id in range(1, players + 1) ]

    @staticmethod
    def print_info():
        """static method to print info"""

        print("Rabu Retta is a great game!")

    def __len__(self):
        """for len(RabuRettaRound())"""

        if self.length_hash > -1:
            return self.length_hash

        sum = 0
        for card in self.deck:
            sum += card.count
        return sum

    def __getitem__(self, index):
        """for RabuRettaRound()[index]"""

        length = len(self)

        position = index if index >= 0 else length + index

        if position >= length:
            raise IndexError

        current = 0

        for card in self.deck:

            if position >= current and position < current + card.count:
                return card

            current += card.count

        raise IndexError

    def pop(self, index=-1):
        """implement pop() method"""

        to_remove = self[index]
        del self[index]

        return to_remove

    def get_player(self, player):

        return self.player_data[player - 1]

    def get_card(self):
        card = self.pop(randint(0, len(self) - 1))
        card.count = 1

        return card

    def give_card_from_deck_to_player(self, player):
        self.get_player(player).add_card_to_hand(self.get_card())


    def __delitem__(self, index):
        """remove card from the deck (del implementation)"""

        length = len(self)

        to_remove = index if index >= 0 else length + index

        if to_remove >= length:
            raise IndexError

        current = 0

        for card_index, card in enumerate(self.deck, start=0):

            if to_remove >= current and to_remove < current + card.count:

                if card.count == 1:
                    to_return = self.deck.pop(card_index)
                    self.length_hash -= 1
                    return to_return

                elif card.count > 1:
                    card.count -= 1
                    self.length_hash -= 1

                    return card
                else:
                    raise IndexError

            current += card.count

    def __repr__(self):

        return str(list(map(lambda card: repr(card), self.deck)))

    def __str__(self):

        display_string = "RabuRetta round for %d players." % self.players

        if self.faceup:
            display_string += (
                    "\nFaceup cards:\n\t" +
                    str(list(map(lambda card: str(card), self.faceup)))
                    )
        if self.facedown:
            display_string += (
                    "\nNumber of facedown cards: %d" % len(self.facedown)
                    )

        return display_string

    def __del__(self):
        """Called when garbage collector calls destructor"""

        RabuRettaRound.rounds_played += 1

