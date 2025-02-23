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

# Track window scaling
scale_factor_x = 1
scale_factor_y = 1 

#create surface to draw on (base resolution)
base_surface = pygame.Surface([BASE_WIDTH, BASE_HEIGHT])

# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 1 # prevent cardcounting

fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)
smaller_font = pygame.font.Font('freesansbold.ttf', 25)
active = False

records = [0, 0, 0] # win, loss, tie
player_score = 0
dealer_score = 0

initial_deal = False # if yes, 2 cards should be drawn
game_deck = copy.deepcopy(decks * one_deck) # make sure only copy gets modified and not original cards list
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'Player busted! :(', 'Player wins :)', 'Dealer wins!', 'Tie game!']

# sound effects
lose_sound = pygame.mixer.Sound("loss.wav")
win_sound = pygame.mixer.Sound("win.wav")
click_sound = pygame.mixer.Sound("click.wav")

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
        pygame.draw.rect(base_surface, 'white', [47 + (47 * i), 307 + (3 * i), 80, 147], 0, 3)
        base_surface.blit(font.render(player[i], True, 'black'),(75 + 47 * i, 310 + 3 * i )) 
        base_surface.blit(font.render(player[i], True, 'black'),(75 + 47 * i, 423 + 3 * i )) 
        pygame.draw.rect(base_surface, 'red', [47 + (47 * i), 307 + (3 * i), 80, 147], 3, 3)
        
    # if player hasn't finished turn, dealer hides one card
    for i in range (len(dealer)):
        pygame.draw.rect(base_surface, 'white', [47 + (47 * i), 107 + (3 * i), 80, 147], 0, 3)
        if i != 0 or reveal:
            base_surface.blit(font.render(dealer[i], True, 'black'),(50 + 47 * i, 110 + 3 * i )) 
            base_surface.blit(font.render(dealer[i], True, 'black'),(50 + 47 * i, 223 + 3 * i ))
        else:
            base_surface.blit(font.render('???', True, 'black') ,(50 + 47 * i, 110 + 3 * i )) 
            base_surface.blit(font.render('???', True, 'black') ,(50 + 47 * i, 223 + 3 * i ))
             
        pygame.draw.rect(base_surface, 'blue', [47 + (47 * i), 107 + (3 * i), 80, 147], 3, 3)

# pass in hand and get best possible score
def calculate_score(hand):
    #calculate new score evnery time and check how many aces
    hand_score = 0
    aces_count = hand.count('A')
    # for loop check wwat highest possible score is
    for i in range (len(hand)):
        # for 2-9 just add number (int) to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, check to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
        # determine how many aces need to be 1 instead of 11 to be under 21
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

#declare game conditions and buttons
def draw_game(act, records, result):
    button_list = []
    #initially on startup - only option is deal new hand
    if not act:
        deal = pygame.draw.rect(base_surface, 'white', [100, 13, 200, 66], 0, 3)
        pygame.draw.rect(base_surface, 'green', [100, 13, 200, 66], 2, 3)
        deal_text = font.render('DEAL HAND', True, 'black')
        base_surface.blit(deal_text, (110, 33))
        button_list.append(deal)
    # once game started, put hit and stand buttons + win/loss records
    else:
        hit = pygame.draw.rect(base_surface, 'white', [0, 467, 200, 66], 0, 3)
        pygame.draw.rect(base_surface, 'green', [0, 467, 200, 66], 2, 3)
        hit_text = font.render('HIT ME', True, 'black')
        base_surface.blit(hit_text, (37, 490))
        button_list.append(hit)

        stand = pygame.draw.rect(base_surface, 'white', [200, 467, 200, 66], 0, 3)
        pygame.draw.rect(base_surface, 'green', [200, 467, 200, 66], 2, 3)
        stand_text = font.render('STAND', True, 'black')
        base_surface.blit(stand_text, (237, 490))
        button_list.append(stand)

        score_text = smaller_font.render(f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}', True, 'white')
        base_surface.blit(score_text, (10, 560))
    # if there is outcome for hand played, display restart button
    if result != 0:
        base_surface.blit(font.render(results[result], True, 'white'), (10, 17))
        deal = pygame.draw.rect(base_surface, 'white', [100, 147, 200, 66], 0, 3)
        pygame.draw.rect(base_surface, 'green', [100, 147, 200, 66], 2, 3)
        pygame.draw.rect(base_surface, 'black', [102, 149, 196, 63], 2, 3)
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
                totals[2] += 1
            add = False
    return result, totals, add

# main game loop
run = True
while run:
    # run game at framerate and fill screen with background color
    timer.tick(fps)
    screen.fill('black')
    base_surface.fill('black')

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

    # Adjust button positions based on the scaling factor**
    scaled_buttons = []  
    for button in buttons:
        scaled_rect = pygame.Rect(button)
        scaled_rect.x *= scale_factor_x  
        scaled_rect.y *= scale_factor_y  
        scaled_rect.width *= scale_factor_x  
        scaled_rect.height *= scale_factor_y  
        scaled_buttons.append(scaled_rect)  

    # event handling, if quit pressed, exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

            scale_factor_x = new_width / BASE_WIDTH  
            scale_factor_y = new_height / BASE_HEIGHT  
        

        if event.type == pygame.MOUSEBUTTONUP:
            click_sound.play()
            if not active:
                if scaled_buttons[0].collidepoint(event.pos): # Deal button
                    active = True
                    initial_deal = True # 2 cards drawn
                    game_deck = copy.deepcopy(decks * one_deck) # make sure only copy gets modified and not original cards list
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
                        game_deck = copy.deepcopy(decks * one_deck) # make sure only copy gets modified and not original cards list
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