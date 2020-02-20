"""
nim_mechanics.py
created on:01/16/2020
created by: Anna Branam
last modified: 02/20/2020

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
    def isAI(self):return False
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
    def move(self): return (self.stack, self.coins)
    def getStack(self): return self.stack
    def setStack(self, stack):self.stack = stack
    def getName(self):return self.name
    
class AI(Player):#random moves
    def __init__(self, name, board, diff = 0):
        super(AI, self).__init__(name)
        self.board = board
        self.diff = diff
    def isAI(self):return True
    def move(self):
        self.coins = []
        self.stack = random.randrange(len(self.board.getStacks()))
        coin_list = self.board.getStacks()[self.stack].getCoins()
        coins = [coin for coin in coin_list if coin.inStack]
        random.shuffle(coins)
        if len(coins)>1: coin_range = random.randrange(len(coins))
        else: coin_range = 1
        for i in range(coin_range):
            self.addCoin(coins[i].getX())
        print((self.stack, self.coins))
        return (self.stack, self.coins)

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
            if self.board.getMove((stack, coins)):#move was valid
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
        return True
    
class CoinClickEvent(GameEvent):
    def __init__(self, board, graphics, event):
        super(CoinClickEvent, self).__init__( board, graphics)
        (self.x, self.y) = event.pos#the position of the mouse click
    def handle(self, currentPlayer):
        for stack in self.board.getStacks():#go through the stacks
            for coin in stack.getCoins():#go through the coins in each stack
                mid_x, mid_y = self.graphics.getCoinPos(coin)#find the midpoint of the coin shape
                x_start, y_start = mid_x-COIN_SIZE, mid_y-COIN_SIZE#find the starting point of the coin shape
                x_end, y_end = mid_x+COIN_SIZE, mid_y+COIN_SIZE#find the end point of the coin shape
                if x_end>=self.x and x_start<=self.x and y_end>=self.y and y_start<=self.y and coin.inStack():#Check if click is on coin
                    if currentPlayer.getStack()<0:#check if a stack has been selected
                        currentPlayer.setStack(coin.getY())#set the selected stack to this stack
                    if currentPlayer.getStack()==coin.getY():#check if coin is in selected stack
                        coin.select()#select or disselect a coin
                        if coin.isSelected():currentPlayer.addCoin(coin.getX())#add coin to player's selected coin list if the coin is selected
                        else: currentPlayer.removeCoin(coin.getX())#remove the coin from the players seleceted coin list
                        if not(any(filter(lambda coin: coin.isSelected(), self.board.getStacks()[currentPlayer.getStack()].getCoins()))):#check if there are no coins currently selected
                            currentPlayer.setStack(-1)#if there are no selected coins unselect the stack
                        self.graphics.animateCoin(coin)#redraw coin
                        return True
class menuClickEvent(GameEvent):
    def __init__(self):
        pass
    
##############################
##Game Runner
##############################
class Runner():
    def __init__(self, board, graphics, players):
        self.board = board
        self.graphics = graphics
        self.players = players
    def quit(self):
        pygame.quit()
        sys.exit()    
    def checkEvent(self, event, currentPlayer):
        if event.type == pygame.QUIT:#check for exit#
            self.quit()
        elif event.type ==pygame.KEYDOWN:#Check for key Presses#
            return KeyDownEvent(self.board, self.graphics, event).handle(currentPlayer)
        elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:#Check for mouse left mouse click
            return CoinClickEvent(self.board, self.graphics, event).handle(currentPlayer)
        return False
         
    def checkWin(self):
        coins = 0
        for stack in self.board.getStacks():
            coins+= sum(coin.inStack() for coin in stack.getCoins())#count coins that are still on the board
        return coins#if there are no coins on the board, the game is over
    
    def run(self):
        turn = -1
        currentPlayer = None
        while True:#main game loop
            
            if self.checkWin()==1: return turn
            elif self.checkWin()==0: return turn+1
            #start the current player's turn#
            ######################### 
            if currentPlayer == None or not currentPlayer.onTurn():
                turn+=1
                currentPlayer = self.players[turn%len(self.players)]
                self.graphics.showPlayer(currentPlayer.name)
                currentPlayer.startTurn()
                self.graphics.displayBoard()#display the board
            #########################

            if currentPlayer.isAI():
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
            #check for events#
            e = pygame.event.get()
            for event in e:
                if self.checkEvent(event, currentPlayer):break
            pygame.display.flip()
            
