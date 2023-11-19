
"""Trying to recreate UNO in Python."""

import os

from enum import Enum
from typing import Literal

class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    NONE = 5

    def __str__(self) -> str:
        return str(self.value)

class Value(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 9
    NINE = 9
    SKIP = 10
    REVERSE = 11
    PLUS_TWO = 12
    COLOR_CHANGER = 13
    PLUS_FOUR = 14

    def __str__(self) -> str:
        return str(self.value)

class UnoError(Exception):
    def __init__(self, message: str = "no description provided") -> None:
        self.message = message

    def __str__(self) -> str:
        return f"UnoError: {self.message}"




class Card:
    def __init__(self, value: Value, color: Color) -> None:
        self.value = value
        self.color = color
    
    def __str__(self) -> str:
        return f"Card {self.value}: {self.color.name}"

    def __repr__(self) -> str:
        return f"Card {self.value}: {self.color.name}"
    
    @property
    def get_color(self) -> Color:
        return self.color
    
    @property
    def get_color_name(self) -> str:
        return self.color.name

    @property
    def get_value(self) -> Value:
        return self.value
    
    @property
    def get_value_name(self) -> str:
        return self.value.name



class PlayerDeck:
    pass



class Player:
    def __init__(self, name: str) -> None:
        self.deck = PlayerDeck()
        self.name = name
    
    def __str__(self) -> str:
        return f"Player {self.name}: {self.deck}."

    def cards_number(self) -> int:
        return len(self.deck.get_contains)
    
    def play_card(self, card: Card):
        self.deck.remove_card(card)
    
    def add_card(self, card: Card):
        self.deck.add_card(card)
    
    def get_deck(self) -> PlayerDeck:
        return self.deck
    
    @property
    def sort_deck(self):
        self.deck.get_contains().sort(key=lambda card: card.get_value.value)
        self.deck.get_contains().sort(key=lambda card: card.get_color.value)
    
    def get_card(self, index: int) -> Card:
        return self.deck.get_contains()[index]
    
    def has_card(self, card: Card) -> bool:
        return card in self.deck.get_contains()

    @property
    def count_cards(self) -> int:
        return len(self.deck.get_contains())
    




class PlayerDeck:
    def __init__(self, contains: list[Card] = []) -> None:
        self.contains = contains
    
    def add_card(self, card: Card) -> None:
        self.contains.append(card)
    
    def remove_card(self, card: Card) -> None:
        try: 
            self.contains.remove(card)
        except ValueError:
            raise UnoError("Card not in deck")

    def __str__(self) -> str:
        return f"Deck: {self.contains.__str__()}"

    
    def get_contains(self) -> list[Card]:
        return self.contains




class Deck:
    def __init__(self, contains: list[Card] or None = None) -> None:
        self.contains = contains if contains is not None else self.generate_deck
    
    @property
    def generate_deck(self) -> list[Card]:
        from random import shuffle, choice
        cards = []

        for color in Color:
            for value in Value:
                if value == Value.COLOR_CHANGER or value == Value.PLUS_FOUR:
                    cards.append(Card(value, Color.NONE))
                else:
                    if color != Color.NONE:
                        cards.append(Card(value, color))
                    else:
                        cards.append(Card(value, choice([Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW])))

        shuffle(cards)

        return cards

    def give_card_to_player(self, player: Player) -> None:
        player.add_card(self.contains.pop())
    
    @property
    def shuffle(self) -> None:
        from random import shuffle
        shuffle(self.contains)
    


class Game:
    def __init__(self):
        self.deck = Deck()
        self.players: list[Player] = []
        self.current_player = None
        self.current_player_index = 0
        self.current_card = None
        self.direction = 1
        self.winner = None
        self.cards_number = 7 
        self.is_plus_two = False
        self.is_plus_four = False
        self.starting_card = None
    
    def edit_params(self, *, cards_number: int = 7, direction: Literal[1, -1] = 1) -> None:
        self.cards_number = cards_number
        self.direction = direction
    
    def add_player(self, player: Player) -> None:
        self.players.append(player)
    
    def remove_player(self, player: Player) -> None:
        try:
            self.players.remove(player)
        except ValueError:
            raise UnoError("Player not in game.")
    
    def pre_start(self):

        from random import randint

        self.deck.shuffle
        self.current_card = self.deck.contains.pop()
        if len(self.players) < 2:
            raise UnoError("Not enough players.")
        
        for player in self.players:
            for _ in range(self.cards_number):
                self.deck.give_card_to_player(player)
        
        self.current_player = self.players[0]

        self.starting_card = self.deck.contains.pop(randint(0, len(self.deck.contains) - 1))
    
    @property
    def start(self):
        self.pre_start()
        while self.winner is None:
            self.play()
    
    def play(self):
        self.current_player = self.players[self.current_player_index]
        self.current_player_index += self.direction

        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
        elif self.current_player_index < 0:
            self.current_player_index = len(self.players) - 1
        

        print(f"Current player: {self.current_player.name}")
        self.player()
    
    def player(self):
        match input("What do you want to do? (play, show): "):
            case "play":
                while True:
                    if self.is_plus_two:
                        print("You got a +2 card, you have to get 2 cards.")
                        for _ in range(2):
                            self.deck.give_card_to_player(self.current_player)
                        
                        self.is_plus_two = False

                        break
                    elif self.is_plus_four:
                        print("You got a +4 card, you have to get 4 cards.")
                        for _ in range(4):
                            self.deck.give_card_to_player(self.current_player)
                        
                        self.is_plus_four = False

                        break

                    print(f"{self.current_card.__str__()}")

                    color = input("Enter your card color: ").strip()
                    value = input("Enter your card value: (in letters) (if 11: reverse, 12: plus_two, 13: color_changer, 14: plus_four) (finish with uno if uno) ").strip().lower()
                    if value.endswith("uno"):
                        if self.current_player.count_cards == 2:
                            print("You did say uno correctly!")
                        else:
                            print("You didn't say uno correctly, you have to get 2 cards.")
                            for _ in range(2):
                                self.deck.give_card_to_player(self.current_player)
                    
                            
                        
                    card = Card(Value[value.upper()], Color[color.upper()])

                    if self.current_player.has_card(card):
                        if self.can_play(card):
                            self.current_player.play_card(card)
                            self.current_card = card
                            
                            if card.get_value == Value.PLUS_FOUR:
                                new_color = input("Enter the new color: ")
                                self.current_card.color = Color[new_color.upper()]
                                self.is_plus_four = True
                            elif card.get_value == Value.COLOR_CHANGER:
                                new_color = input("Enter the new color: ")
                                self.current_card.color = Color[new_color.upper()]
                            elif card.get_value == Value.REVERSE:
                                self.direction *= -1
                            elif card.get_value == Value.SKIP:
                                self.current_player_index += self.direction
                            elif card.get_value == Value.PLUS_TWO:
                                self.is_plus_two = True

                            if self.current_player.count_cards == 0:
                                self.winner = self.current_player
                                print("Congratulations, you won the game!")
                            
                            break
                        else:
                            print("You can't play this card.")
                    else:
                        print("You don't have this card.")
                
            case "show":
                print(self.current_player.deck)
                self.player()
    
    def can_play(self, card: Card):
        if self.current_card.get_color == card.get_color or self.current_card.get_value == card.get_value:
            return True
        elif card.get_value == Value.COLOR_CHANGER or card.get_value == Value.PLUS_FOUR:
            return True
        
        return False

    def get_winner(self) -> Player:
        return self.winner

    def get_current_player(self) -> Player:
        return self.current_player
    
    def get_current_card(self) -> Card:
        return self.current_card
    
    def get_current_card_color(self) -> Color:
        return self.current_card.get_color
    
    def get_current_card_value(self) -> Value:
        return self.current_card.get_value
    
    def get_current_player_index(self) -> int:
        return self.current_player_index
    
    def get_direction(self) -> Literal[1, -1]:
        return self.direction
    
    def get_players(self) -> list[Player]:
        return self.players
    
    def get_deck(self) -> Deck:
        return self.deck
    
    def get_starting_card(self) -> Card:
        return self.starting_card
    


# Executing the game with the uno.py with create a simple game
# Including two players and 7 cards.
if __name__ == "__main__":
    game = Game()
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    
    game.add_player(player1)
    game.add_player(player2)

    game.start()