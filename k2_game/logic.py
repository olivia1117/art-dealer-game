# k2_game/logic.py

# Dictionary of pattern names mapped to checking functions
DEALER_PATTERNS = {
    "All Red": lambda card: card.endswith("hearts.png") or card.endswith("diamonds.png"),
    "All Black": lambda card: card.endswith("spades.png") or card.endswith("clubs.png"),
    "All Hearts": lambda card: card.endswith("hearts.png"),
    "All Diamonds": lambda card: card.endswith("diamonds.png"),
    "All Spades": lambda card: card.endswith("spades.png"),
    "All Clubs": lambda card: card.endswith("clubs.png"),
    "All Kings": lambda card: card.startswith("king"),
    "All Queens": lambda card: card.startswith("queen"),
    "All Jacks": lambda card: card.startswith("jack"),

}
