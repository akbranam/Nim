"""
nim_mechanics.py
created on:01/16/2020
created by: Anna Branam
last modified: 02/12/2020

TODO:
AI player

"""


############################################################################
#imports
############################################################################
import random
import pygame
from nim_globals import *


############################################################################
#classes
############################################################################

##############################
##Players
##############################

class Player():
    def __init__(self, name):
        self.name = name
        self.stack = -1
        self.isTurn = False
        self.coins = []
        pass
    def addCoin(self, coin):
        if coin not in self.coins:
            self.coins.append(coin)
    def removeCoin(self, coin):
        if coin in self.coins:
            self.coins.remove(coin)
    def getCoins(self):return self.coins
    def endTurn(self):
        self.isTurn = False
        self.stack = -1
        self.coins = []
    def startTurn(self): self.isTurn = True
    def onTurn(self): return self.isTurn
    def getStack(self): return self.stack
    def setStack(self, stack):self.stack = stack
    def move(self): return (self.stack, self.coins)

class AI(Player):
    def __init(self, name, board):
        super(AI, self).__init__(name)
    def move(self):
        #insert algorithm here
        pass

##############################
##Game Events
##############################
#parent class for all game events
class GameEvent():
    def __init__(self, board, graphics, event = None):
        self.board = board
        self.graphics = graphics
        pass

class KeyDownEvent(GameEvent):
    def __init__(self, board, graphics, event):
        super(KeyDownEvent, self).__init__(board, graphics)
        self.key = event.key
    def handle(self, currentPlayer):
        if self.key == pygame.K_RETURN:#return/enter key presed
            (stack, coins) = currentPlayer.move()
            if self.board.getMove((stack, coins)):
                for coin in coins:
                    self.graphics.removeCoin(self.board.getStacks()[currentPlayer.getStack()].getCoins()[coin])
                currentPlayer.endTurn()#end current player's turn
            else:#invalid move
                self.graphics.displayInvalidMove()
                print("invalid move")
        elif self.key == pygame.K_ESCAPE:#escape key pressed
            #self.quit()
            pass
        elif self.key == pygame.K_SPACE:#Space bar pressed
            pass#bring up menu
        return
    
class CoinClickEvent(GameEvent):
    def __init__(self, board, graphics, event):
        super(CoinClickEvent, self).__init__( board, graphics)
        (self.x, self.y) = event.pos
    def handle(self, currentPlayer):
        for stack in self.board.getStacks():#go through the stacks
            for coin in stack.getCoins():#go through the coins in each stack
                mid_x, mid_y = self.graphics.getCoinPos(coin)
                x_start, y_start = mid_x-COIN_SIZE, mid_y-COIN_SIZE
                x_end, y_end = mid_x+COIN_SIZE, mid_y+COIN_SIZE
                if x_end>=self.x and x_start<=self.x and y_end>=self.y and y_start<=self.y and coin.inStack():#Check if click is on coin
                    if currentPlayer.getStack()<0:
                        currentPlayer.setStack(coin.getY())
                    if currentPlayer.getStack()==coin.getY():#check if coin is in selected stack
                        coin.select()#select or disselect a coin
                        if coin.isSelected():currentPlayer.addCoin(coin.getX())
                        else: currentPlayer.removeCoin(coin.getX())
                        #check if there are no coins currently selected
                        if not(any(filter(lambda coin: coin.isSelected(), self.board.getStacks()[currentPlayer.getStack()].getCoins()))):
                            currentPlayer.setStack(-1)
                            #redraw coin
                        self.graphics.animateCoin(coin)
                        return
