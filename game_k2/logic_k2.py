# k2_game/logic_k2.py


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
}



