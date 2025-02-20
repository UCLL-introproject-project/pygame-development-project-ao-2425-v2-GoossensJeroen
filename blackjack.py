import copy
import random
import pygame

# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 1 # prevent cardcounting
game_deck = copy.deepcopy(decks * one_deck) # make sure only copy gets modified and not original cards list

# setting up pygame-window
WIDTH = 600
HEIGHT = 900
pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack 21')

# game variables
fps = 60
pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
