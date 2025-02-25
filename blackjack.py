#!/usr/bin/env python3

import copy
import random
import pygame

pygame.init()

# setting up pygame-window
BASE_WIDTH = 400
BASE_HEIGHT = 600
ASPECT_RATIO = BASE_WIDTH/BASE_HEIGHT

screen = pygame.display.set_mode([BASE_WIDTH, BASE_HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption('Blackjack 21')

# allow window scaling
scale_factor_x = 1
scale_factor_y = 1 

#create surface to draw on (base resolution)
base_surface = pygame.Surface([BASE_WIDTH, BASE_HEIGHT])

# game variables
cards = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC', 
         '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',
         '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',
         '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
decks = 1 # prevent cardcounting

# load card images
card_images = {
    '2C': pygame.image.load("img/2C.png"),
    '3C': pygame.image.load("img/3C.png"),
    '4C': pygame.image.load("img/4C.png"),
    '5C': pygame.image.load("img/5C.png"),
    '6C': pygame.image.load("img/6C.png"),
    '7C': pygame.image.load("img/7C.png"),
    '8C': pygame.image.load("img/8C.png"),
    '9C': pygame.image.load("img/9C.png"),
    '10C': pygame.image.load("img/10C.png"),
    'JC': pygame.image.load("img/JC.png"),
    'QC': pygame.image.load("img/QC.png"),
    'KC': pygame.image.load("img/KC.png"),
    'AC': pygame.image.load("img/AC.png"),

    '2D': pygame.image.load("img/2D.png"),
    '3D': pygame.image.load("img/3D.png"),
    '4D': pygame.image.load("img/4D.png"),
    '5D': pygame.image.load("img/5D.png"),
    '6D': pygame.image.load("img/6D.png"),
    '7D': pygame.image.load("img/7D.png"),
    '8D': pygame.image.load("img/8D.png"),
    '9D': pygame.image.load("img/9D.png"),
    '10D': pygame.image.load("img/10D.png"),
    'JD': pygame.image.load("img/JD.png"),
    'QD': pygame.image.load("img/QD.png"),
    'KD': pygame.image.load("img/KD.png"),
    'AD': pygame.image.load("img/AD.png"),

    '2H': pygame.image.load("img/2H.png"),
    '3H': pygame.image.load("img/3H.png"),
    '4H': pygame.image.load("img/4H.png"),
    '5H': pygame.image.load("img/5H.png"),
    '6H': pygame.image.load("img/6H.png"),
    '7H': pygame.image.load("img/7H.png"),
    '8H': pygame.image.load("img/8H.png"),
    '9H': pygame.image.load("img/9H.png"),
    '10H': pygame.image.load("img/10H.png"),
    'JH': pygame.image.load("img/JH.png"),
    'QH': pygame.image.load("img/QH.png"),
    'KH': pygame.image.load("img/KH.png"),
    'AH': pygame.image.load("img/AH.png"),

    '2S': pygame.image.load("img/2S.png"),
    '3S': pygame.image.load("img/3S.png"),
    '4S': pygame.image.load("img/4S.png"),
    '5S': pygame.image.load("img/5S.png"),
    '6S': pygame.image.load("img/6S.png"),
    '7S': pygame.image.load("img/7S.png"),
    '8S': pygame.image.load("img/8S.png"),
    '9S': pygame.image.load("img/9S.png"),
    '10S': pygame.image.load("img/10S.png"),
    'JS': pygame.image.load("img/JS.png"),
    'QS': pygame.image.load("img/QS.png"),
    'KS': pygame.image.load("img/KS.png"),
    'AS': pygame.image.load("img/AS.png")
}

for key in card_images:
    card_images[key] = pygame.transform.scale(card_images[key], (100, 140))

# load background
background = pygame.image.load("img/background.jpg")
background = pygame.transform.scale(background, (BASE_WIDTH, BASE_HEIGHT))

fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)
smaller_font = pygame.font.Font('freesansbold.ttf', 25)
smallest_font = pygame.font.Font('freesansbold.ttf', 14)
active = False

records = [0, 0, 0] # win, loss, tie
player_score = 0
dealer_score = 0

initial_deal = False # if yes, 2 cards should be drawn
game_deck = copy.deepcopy(decks * cards) # make sure only copy gets modified and not original cards list
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'Player busted! :(', 'Player wins :)', 'Dealer wins!', 'It\'s a draw!']

# sound effects
lose_sound = pygame.mixer.Sound("loss.wav")
win_sound = pygame.mixer.Sound("win.wav")
click_sound = pygame.mixer.Sound("click.wav")
draw_sound = pygame.mixer.Sound("draw.wav")

# define functions
# deal cards randomly from deck, one at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck)-1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck

# draw scores on scaled_surface
def draw_scores(player, dealer):
    base_surface.blit(font.render(f'Score [{player}]', True, 'white'), (233, 266))
    if reveal_dealer:
        base_surface.blit(font.render(f'Score [{dealer}]', True, 'white'), (233, 66))

# draw cards visually on screen
def draw_cards(player, dealer, reveal):
    for i in range (len(player)):
        base_surface.blit(card_images[player[i]], (47 + (47 * i), 307 + (3 * i), 100, 140))
        pygame.draw.rect(base_surface, 'black', [47 + (47 * i), 307 + (3 * i), 100, 140], 2, 3)
        
    # if player hasn't finished turn, dealer hides one card
    for i in range (len(dealer)):   
        if i != 0 or reveal:
            base_surface.blit(card_images[dealer[i]], (47 + (47 * i), 107 + (3 * i), 100, 140))
        else:
            pygame.draw.rect(base_surface, 'white', [47 + (47 * i), 107 + (3 * i), 100, 140], 0, 3)
            base_surface.blit(font.render('?', True, 'black') ,(50 + 47 * i, 110 + 3 * i )) 
            base_surface.blit(font.render('?', True, 'black') ,(50 + 47 * i, 210 + 3 * i ))
            
        pygame.draw.rect(base_surface, 'black', [47 + (47 * i), 107 + (3 * i), 100, 140], 2, 3)

# pass in hand and get best possible score
def calculate_score(hand):
    #calculate new score evnery time and check how many aces
    hand_score = 0
    aces_count = 0
    
    for card in hand:
        card_value = card[:-1] # slices last char and removes the suit 
        # for values 2-10
        if card_value.isdigit():
            hand_score += int(card_value)
        # for 10 and face cards add 10
        elif card_value in ['J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, check to reduce afterwards
        elif card_value == 'A':
            hand_score += 11
            aces_count += 1
        # determine how many aces need to be 1 instead of 11 to be under 21
    while hand_score > 21 and aces_count > 0:
        hand_score -= 10
        aces_count -= 1
    return hand_score

#declare game conditions and buttons
def draw_game(act, records, result):
    button_list = []
    #initially on startup - only option is deal new hand
    if not act:
        deal = pygame.draw.rect(base_surface, 'white', [100, 13, 200, 66], 0, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        base_surface.blit(deal_text, (110, 33))
        button_list.append(deal)
        esc_text = smaller_font.render('Press Esc to quit', True, 'white')
        base_surface.blit(esc_text, (90, 475))
        disclaimer = smallest_font.render('Image by Freepik.com', True, 'white')
        base_surface.blit(disclaimer, (110, 580))
    # once game started, put hit and stand buttons + win/loss records
    else:
        hit = pygame.draw.rect(base_surface, 'white', [0, 467, 200, 66], 0, 5)
        pygame.draw.rect(base_surface, 'black', [0, 467, 200, 66], 2, 3)
        hit_text = font.render('HIT ME', True, 'black')
        base_surface.blit(hit_text, (37, 490))
        button_list.append(hit)

        stand = pygame.draw.rect(base_surface, 'white', [200, 467, 200, 66], 0, 5)
        pygame.draw.rect(base_surface, 'black', [200, 467, 200, 66], 2, 3)
        stand_text = font.render('STAND', True, 'black')
        base_surface.blit(stand_text, (237, 490))
        button_list.append(stand)

        score_text = smaller_font.render(f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}', True, 'white')
        base_surface.blit(score_text, (10, 560))
    # if there is outcome for hand played, display restart button
    if result != 0:
        base_surface.blit(font.render(results[result], True, 'white'), (10, 17))
        deal = pygame.draw.rect(base_surface, 'white', [100, 147, 200, 66], 0, 3)
        pygame.draw.rect(base_surface, 'black', [100, 147, 200, 66], 2, 3)
        deal_text = font.render('NEW HAND', True, 'black')
        base_surface.blit(deal_text, (110, 170))
        button_list.append(deal)
    return button_list

# check endgame conditions functions
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check endgame scenarios: stood, busted or blackjacked
    # result 1-bust 2-win 3-loss 4-tie
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or dealer_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                lose_sound.play()
                totals[1] += 1
            elif result == 2:
                win_sound.play()
                totals[0] += 1
            else:
                draw_sound.play()
                totals[2] += 1
            add = False
    return result, totals, add


# main game loop
run = True
while run:
    # run game at framerate and fill screen with background color
    timer.tick(fps)
    base_surface.blit(background, (0, 0))

    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
    initial_deal = False

    # once game if activated and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)

    # Adjust button positions based on the scaling factor
    scaled_buttons = []  
    for button in buttons:
        scaled_rect = pygame.Rect(button)
        scaled_rect.x *= scale_factor_x  
        scaled_rect.y *= scale_factor_y  
        scaled_rect.width *= scale_factor_x  
        scaled_rect.height *= scale_factor_y  
        scaled_buttons.append(scaled_rect)  

    # event handling
    for event in pygame.event.get():

        # handle quiting
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        # reset dimensions when resizing
        elif event.type == pygame.VIDEORESIZE:
            # get new window size
            new_width, new_height = event.w, event.h
            if new_width / new_height > ASPECT_RATIO:
                new_width = int(new_height * ASPECT_RATIO)
            else:
                new_height = int(new_width / ASPECT_RATIO)
            # resize the window
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            base_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

            # Scales to make UI responsive
            scale_factor_x = new_width / BASE_WIDTH  
            scale_factor_y = new_height / BASE_HEIGHT  

            # Resize background dynamically
            background = pygame.transform.scale(background, (BASE_WIDTH, BASE_HEIGHT))  
                       
        if event.type == pygame.MOUSEBUTTONUP:
            click_sound.play()
            if not active:
                if scaled_buttons[0].collidepoint(event.pos): # Deal button
                    active = True
                    initial_deal = True # 2 cards drawn
                    game_deck = copy.deepcopy(decks * cards) # make sure only copy gets modified and not original cards list
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
            else:
                # if player can hit, allow to draw card
                if scaled_buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # end turn (stand)
                elif scaled_buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(scaled_buttons) == 3:
                    if scaled_buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True # 2 cards drawn
                        game_deck = copy.deepcopy(decks * cards) # make sure only copy gets modified and not original cards list
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        dealer_score = 0
                        player_score = 0
                        reveal_dealer = False
                        add_score = True

    # Scale the base surface to fit the window while maintaining the aspect ratio
    scaled_surface = pygame.transform.smoothscale(base_surface, screen.get_size())

    # Blit to the screen
    screen.blit(scaled_surface, (0, 0))

    # if player busts or blackjacks end turn automaticly
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    pygame.display.flip()
pygame.quit()