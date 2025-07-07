from itertools import combinations
import os

# --- Basic Single-Card Rules ---

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

# --- Multi-Card Rules ---

def adds_to_nine(cards):
    """Return True if any group of 3 number cards (Ace through 9) adds to 9 using accepted combos."""

    # Only allow these specific combinations of values
    valid_combos = {
        (1, 2, 6),
        (1, 3, 5),
        (1, 4, 4),
        (2, 3, 4)
    }

    # Only accept values from Ace to 9
    value_map = {
        'ace': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }

    def get_value(card_filename):
        base = os.path.splitext(card_filename)[0]  # e.g., '3_of_hearts'
        rank = base.split('_of_')[0]
        return value_map.get(rank)  # returns None if not in value_map (e.g., "jack")

    # Go through all combinations of 3 cards
    for combo in combinations(cards, 3):
        values = [get_value(card) for card in combo]
        if None in values:
            continue  # Skip if any card isn't 1–9
        if tuple(sorted(values)) in valid_combos:
            return True

    return False

def ace_and_black_jack(cards):
    has_ace = any(card.startswith("ace") for card in cards)
    has_black_jack = any(card.startswith("jack_of_spades") or card.startswith("jack_of_clubs") for card in cards)
    return has_ace and has_black_jack



DEALER_PATTERNS = {
    "Cards Adding to 9": adds_to_nine,
    "Ace and Black Jack": ace_and_black_jack,
    "Single Digit Primes": is_single_prime,
    "All Red": is_red,
    "All Black": is_black,
    "All Hearts": is_hearts,
    "All Diamonds": is_diamonds,
    "All Spades": is_spades,
    "All Clubs": is_clubs,
    "All Kings": is_king,
    "All Queens": is_queen,
    "All Jacks": is_jack
}



