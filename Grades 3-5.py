def get_card_info(card_filename):
    base= card_filename.replace('.png', ' ')
    rank,suit= base.split('_')
    return rank.lower(), suit.lower()


#Dealer Patterns for Grades 3-5

DEALER_PATTERNS = {
    #All Red Cards
    "All Red Cards": lambda card: get_card_info(card)[1] in ['hearts', 'diamonds'],

    #All Black cards
    "All Black Cards": lambda card: get_card_info(card)[1] in ['spades', 'clubs'],

    #All cards that are prime numbers
    "Single Digit Primes": lambda card: get_card_info(card)[0].isdigit() and int(get_card_info(card)[0]) in [2,3,5,7],

    #Cards that add to 9
    "Cards Adding to 9": lambda card: get_card_info(card)[0].isdigit() and int(get_card_info(card)[0]) ==9,

    #Ace or Black Jack

    "Ace and Black Jack": lambda card: (
        get_card_info(card)[0] == 'ace' or
        (get_card_info(card)[0]== 'jack' and get_card_info(card)[1] in ['spades', 'clubs']) 
        
    ),



}

