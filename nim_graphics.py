"""
graphics.py
cerated on: 01/16/2020
created by: Anna Branam
last modified: 02/07/2020
"""

############################################################################
#imports
############################################################################
import math
import pygame
from nim_mechanics import *
from nim_globals import *


############################################################################
#classes
############################################################################
class Graphics ():
    def __init__(self, board):
        self.board = board
        self.height = 700
        self.width = 1000
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
    def displayBoard(self):
        for stack in self.board.getStacks():
            for coin in stack.getCoins():#draw each coin in stack
                if coin.inStack():self.animateCoin(coin)
        pygame.display.flip()
    def getCoinPos(self, coin):#get screen position of specified coin
        return (coin.getX()*(COIN_SIZE+COIN_OFFSET)+COIN_BUFFER, coin.getY()*(COIN_SIZE+STACK_OFFSET)+STACK_BUFFER)
    def showPlayer(self, player):
        #display specified player
        pass
    def displayMove(self, move):
        pass
    def displayWin(self, player):
        #show winning player
        pass
    def animateCoin(self, coin):
        if coin.isSelected(): pygame.draw.circle(self.screen, WHITE, self.getCoinPos(coin), COIN_SIZE, 3)#draw selected coin at specified point
        else: pygame.draw.circle(self.screen, YELLOW, self.getCoinPos(coin), COIN_SIZE, 0)#draw a coin at specified point
    def removeCoin(self, coin):
        pygame.draw.circle(self.screen, BACKGROUND, self.getCoinPos(coin), COIN_SIZE+2, 0)#draw a coin at specified point
        
