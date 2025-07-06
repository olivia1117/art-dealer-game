# 68_game/logic_68.py

from collections import Counter


def is_red(card):
    return card.endswith("hearts.png") or card.endswith("diamonds.png")

def is_black(card):
    return card.endswith("spades.png") or card.endswith("clubs.png")

def is_hearts(card):
    return card.endswith("hearts.png")

def is_diamonds(card):
    return card.endswith("diamonds.png")

def is_spades(card):
    return card.endswith("spades.png")

def is_clubs(card):
    return card.endswith("clubs.png")

def is_king(card):
    return card.startswith("king")

def is_queen(card):
    return card.startswith("queen")

def is_jack(card):
    return card.startswith("jack")

def is_single_prime(card):
    return card.startswith("2") or card.startswith("3") or card.startswith("5") or card.startswith("7")

#1 and 8, 4 and 5, 6 and 3, 7 and 2
def adds_to_nine(card):
    return (card.startswith("ace") and card.startswith("8")) or (card.startswith("2") and card.startswith("7")) or (card.startswith("3") and card.startswith("6")) or (card.startswith("4") and card.startswith("5"))

def is_ace_and_blackjack(card):
    return card.startswith("ace") and ((card.startswith("jack") and (card.endswith("spades.png") or card.endswith("clubs.png"))))



def extract_rank(card):
    return card.split("_of_")[0]

def extract_suit(card):
    return card.split("_of_")[1].replace(".png", "")

def check_pair(cards):
    ranks = [extract_rank(c) for c in cards]
    return any(count == 2 for count in Counter(ranks).values())


def check_three_of_a_kind(cards):
    ranks = [extract_rank(c) for c in cards]
    return 3 in Counter(ranks).values()

def check_flush(cards):
    suits = [extract_suit(c) for c in cards]
    return len(set(suits)) == 1


def check_straight(cards):
    rank_order = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
    ranks = [extract_rank(c) for c in cards]
    try:
        indices = sorted(rank_order.index(r) for r in ranks)
    except ValueError:
        return False
    return all(indices[i] + 1 == indices[i + 1] for i in range(len(indices) - 1))



DEALER_PATTERNS = {
    "All Red": is_red,
    "All Black": is_black,
    "All Hearts": is_hearts,
    "All Diamonds": is_diamonds,
    "All Spades": is_spades,
    "All Clubs": is_clubs,
    "All Kings": is_king,
    "All Queens": is_queen,
    "All Jacks": is_jack,
    "Single Digit Primes": is_single_prime,
    "Cards Adding to 9": adds_to_nine,
    "Ace and Black Jack": is_ace_and_blackjack,
    #basic poker hands
    "Three of a Kind": check_three_of_a_kind,
    "Pair": check_pair,
    "Straight": check_straight,
    "Flush": check_flush

}
