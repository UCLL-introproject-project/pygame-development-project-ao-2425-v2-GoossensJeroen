import copy
import random
import pygame

pygame.init()

# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 1 # prevent cardcounting

# setting up pygame-window
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack 21')

# game variables
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False

records = [0, 0, 0] # win, loss, tie
player_score = 0
dealer_score = 0

initial_deal = False # if yes, 2 cards should be drawn
game_deck = copy.deepcopy(decks * one_deck) # make sure only copy gets modified and not original cards list
my_hand = []
dealer_hand = []
outcome = 0

# deal cards randomly from deck, one at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    print(current_hand, current_deck)
    return current_hand, current_deck

#declare game conditions and buttons:
def draw_game(act, records):
    button_list = []
    #initially on startup - only option is deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    # once game started, put hit and stand buttons + win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)

        score_text = smaller_font.render(f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}', True, 'white')
        screen.blit(score_text, (15, 840))

    return button_list

# main game loop
run = True
while run:
    # run game at framerate and fill screen with background color
    timer.tick(fps)
    screen.fill('black')

    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        print(my_hand, dealer_hand)
    initial_deal = False

    # once game if activated and dealt, calculate scores and display cards


    buttons = draw_game(active, records)

    # event handling, if quit pressed, exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True # 2 cards drawn
                    game_deck = copy.deepcopy(decks * one_deck) # make sure only copy gets modified and not original cards list
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
    
    pygame.display.flip()
pygame.quit()