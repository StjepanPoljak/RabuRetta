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

class MoveResult():
    """ Note: 'message' is sent to player privately, and 'inform' publicly """

    def __init__(self, is_valid, status_updated, message=None, inform=None):
        self.is_valid = is_valid
        self.status_updated = status_updated
        self.message = message
        self.inform = inform

class Player():

    def __init__(self, id, name=None, age=0, type=PlayerType.Human):
        self.id = id
        self.name = name
        self.age = age
        self.type = type
        self.hand = []
        self.faceup = []
        self.status = PlayerStatus.InGame

    def add_card_to_hand(self, card):
        self.hand.append(card)

        if self.hand_count() > 2:
            raise Exception("Game logic error: too many cards in hand!")

    def hand_count(self):

        return len(self.hand)

    def play_card(self, card):

        if card not in self.hand:

            raise Exception("Game logic error: card not in hand")

        self.faceup.append(card)
        self.hand.remove(card)

    def get_hand(self):

        if len(self.hand) > 1:

            raise Exception("Game logic error: too many cards in hand")

        return self.hand[0]

    def is_protected(self):

        if not self.faceup:

            return False

        if self.faceup[-1].name == "Handmaid":

            return True

        return False

    def holds_card(self, card_name):

        for card in self.hand:

            if card.name == card_name:

                return True

        return False

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

    def get_card(self):
        card = self.pop(randint(0, len(self) - 1))
        card.count = 1

        return card

    def discard_and_draw(self, player):
        player.play_card(player.hand[0])
        self.draw_card(player_name)

    def draw_card(self, player):
        player.add_card_to_hand(self.get_card())

    def all_players_protected(self, except_player):

        for player in self.players:

            if player == except_player:

                continue

            if player.is_protected() is False:

                return False

        return True

    def all_players_out(self, except_player):

        for player in self.players:

            if except_player == player:

                continue

            if player.status != PlayerStatus.Loss:

                return False

        return True

    def get_player(self, id):

        return self.player_data[id - 1]

    def get_player_by_name(self, name):

        for player in self.player_data:

            if player.name == name:

                return player

        raise Exception(
            "No player named %s!" % name
            )

    def play_guard(self, player, target_player, guess):

        if guess == "Guard":

            return MoveResult(
                    is_valid=False,
                    status_updated=[],
                    message="You cannot guess Guard!"
                    )

        if target_player.holds_card(guess) is True:

            target_player.status = PlayerStatus.Loss

            return MoveResult(
                is_valid=True,
                status_updated=[target_player],
                message="You guessed correct!",
                inform="%s has defeated %s by guessing his card (%s)" % (
                    player.name,
                    target_player.name,
                    guess
                    )
                )

        return MoveResult(
            is_valid=true,
            status_updated=[],
            message="Your guess failed!",
            inform="%s failed in his guess: %s does not hold %s" % (
                player.name,
                target_player.name,
                guess
                )
            )

    def play_priest(self, player, target_player):

        return MoveResult(
            is_valid=True,
            status_updated=[],
            message="Player %s holds %s." % (
                target_player,
                target_player.get_hand()
                )
            )

    def play_baron(self, player, target_player):

        player_card = self.hand[0] \
            if self.hand[0].name != "Baron" else self.hand[1]

        if target_player.get_hand().value == player_card.value:

            return MoveResult(
                is_valid=True,
                status_updated=[],
                message="You both have %s." % player_card.name,
                inform="Nobody won!"
                )

        winner = (target_player.get_hand(), target_player) \
                if target_player.get_hand().value > player_card.value \
                    else (player_card, player)

        loser = (target_player.get_hand(), target_player) \
                if target_player.get_hand().value < player_card.value \
                    else (player_card, player)

        move_message = "%s held by %s won over %s held by %s." % (
                *winner, *loser)

        inform_message = "%s kicked %s out!" % (winner[1], loser[1])

        loser[1].status = PlayerStatus.Loss

        return MoveResult(
            is_valid=True,
            status_updated=[loser],
            message=move_message,
            inform=inform_message
            )

    def play_handmaid(self, player):

        return MoveResult(
                is_valid=True,
                status_updated=[],
                inform="%s is protected for this round!" % player.name
                )

    def play_prince(self, player, target_player):

        target_player_was_defeated = False
        end_status = []

        if target_player.holds_hand("Princess") is True:
            target_player.play_card(target_player.hand[0])
            target_player.status = PlayerStatus.Loss
            target_player_was_defeated = True
        else:
            self.discard_and_draw(target_player)

        if target_player_was_defeated is True:
            end_status = [target_player]

        return MoveResult(
                is_valid=True,
                status_updated=end_status,
                message=None,
                inform="%s discarded %s" % (target_player, target_player.faceup[-1])
                )

    def make_move(self, player, card, dict):

        if (
            card.name == "Guard" or card.name == "Priest"
            or card.name == "Baron" or card.name == "Prince"
            or card.name == "King"
            ):

            try:
                target_player = self.get_player_by_name(
                    dict["target_player"]
                    )

                if target_player.is_protected() is True:

                    return MoveResult(
                            is_valid=False,
                            status_updated=[],
                            message="Target player is protected by Handmaid!"
                            )

                if (
                    self.all_players_protected(
                        except_player=player) is False
                    and player == target_player
                    and card.name != "Prince"
                    ):

                    return MoveResult(
                        is_valid=False,
                        status_updated=[],
                        message="Cannot target yourself!"
                        )

            except Exception as e:

                return MoveResult(
                        is_valid=False,
                        status_updated=[],
                        message=str(e)
                        )

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

