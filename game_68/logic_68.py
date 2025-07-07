
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
    return ((card.startswith("ace") and card.endswith("8")) or (card.startswith("8") and card.endswith("ace")) 
            or (card.startswith("2") and card.endswith("7")) or (card.startswith("7") and card.endswith("2")) 
            or (card.startswith("3") and card.endswith("6")) or (card.startswith("6") and card.endswith("3")) 
            or (card.startswith("4") and card.endswith("5")) or (card.startswith("5") and card.endswith("4")))

def is_ace_and_blackjack(card):
    return card.startswith("ace") and ((card.startswith("jack") and (card.endswith("spades.png") or card.endswith("clubs.png"))))



def extract_rank(card):
    card = card.strip().lower()
    if "_of_" in card and card.endswith(".png"):
        return card.split("_of_")[0]
    return ""

def extract_suit(card):
    card = card.strip().lower()
    if "_of_" in card and card.endswith(".png"):
        parts = card.split("_of_")
        suit = parts[1].replace(".png", "")
        return suit
    return ""


def check_pair(cards):
    ranks = []
    for c in cards:
        rank = extract_rank(c)
        ranks.append(rank)

    rank_counts = {}
    for rank in ranks:
        if rank in rank_counts:
            rank_counts[rank] += 1
        else:
            rank_counts[rank] = 1


    for count in rank_counts.values():
        if count == 2:
            return True

    return False

def check_three_of_a_kind(cards):
    ranks = [extract_rank(card) for card in cards]

    rank_counts = {}
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    return 3 in rank_counts.values()




def check_flush(cards):
    suits = []

    for card in cards:
        suit = extract_suit(card)
        suits.append(suit)


    unique_suits = set(suits)

    if len(unique_suits) == 1:
        return True
    else:
        return False
    

def check_straight(cards):
    rank_order = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
    ranks = []
    for c in cards:
        rank = extract_rank(c)
        ranks.append(rank)

    indices = []
    for r in ranks:
        if r in rank_order:
            index = rank_order.index(r)
            indices.append(index)
        else:
            return False

    indices.sort()

    for i in range(len(indices) - 1):
        if indices[i] + 1 != indices[i + 1]:
            return False

    return True






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
    # #basic poker hands
    "Three of a Kind": check_three_of_a_kind,
    "Pair": check_pair,
    "Straight": check_straight,
    "Flush": check_flush

}



