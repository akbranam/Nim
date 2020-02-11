"""
nim.py
created on: 01/15/2020
created by: Anna Branam
last modified: 02/07/2020


Nim is a game that consists of stacks of coins
the numbers of stacks and the number of coins in each stack varies
each player can take any number of coins from a single stack
the last player to remove a coin loses
"""

############################################################################
#imports
############################################################################
import sys
import random
import nim_exceptions as exceptions
from nim_mechanics import *
from nim_graphics import *
############################################################################
#classes
############################################################################

class Game():
    def __init__(self):
        self.players = [Player("Player 1"), Player("Player 2")]
        self.board, self.graphics = None, None

    def genBoard(self, stacks=[]):
        if stacks == []:#If no coins are specified, randomize
            for i in range(random.randrange(2, 6)):
                stacks.append(random.randrange(1, 6))
        self.board = Board(stacks)
        
    def checkWin(self):
        coins = 0
        for stack in self.board.getStacks():
            coins+= sum(coin.inStack() for coin in stack.getCoins())#count coins that are still on the board
        return coins == 0 or coins == 1#if there are no coins on the board, the game is over
    
    def quit(self):
        pygame.quit()
        sys.exit()
            
    def play(self):
        ###INITS###
        ##################################
        self.genBoard()
        self.graphics = Graphics(self.board)
        turn = 0
        currentPlayer = self.players[0]
        ##################################

        self.graphics.displayBoard()#display the board

        ###MAIN GAME LOOP###
        #####################################################
        while (not self.checkWin()):
            #start the current player's turn#
            #########################
            if not currentPlayer.onTurn():
                self.graphics.showPlayer(currentPlayer.name)
                currentPlayer.startTurn()
                self.graphics.displayBoard()#display the board
            #########################
            
            #check for events#
            ##########################################
            e = pygame.event.get()
            for event in e:
                #check for exit#
                ########################
                if event.type == pygame.QUIT:
                    self.quit()
                ########################
                #Check for key Presses#
                ########################
                elif event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:#return/enter key presed
                        (stack, coins) = currentPlayer.move()
                        if self.board.getMove((stack, coins)):
                            for coin in coins:
                                self.graphics.removeCoin(self.board.getStacks()[currentPlayer.getStack()].getCoins()[coin])
                            currentPlayer.endTurn()#end current player's turn
                        else: print("invalid move")
                        break
                    elif event.key == pygame.K_ESCAPE:#escape key pressed
                        self.quit()
                    elif event.key == pygame.K_SPACE:#Space bar pressed
                        #bring up menu
                        break
                ########################
                
                #Check for mouse clicks#
                ########################
                elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:#Left mouse button pressed
                    (x, y) = event.pos
                    try:#set up break out excetption
                        for stack in self.board.getStacks():#go through the stacks
                            for coin in stack.getCoins():#go through the coins in each stack
                                mid_x, mid_y = self.graphics.getCoinPos(coin)
                                x_start, y_start = mid_x-COIN_SIZE, mid_y-COIN_SIZE
                                x_end, y_end = mid_x+COIN_SIZE, mid_y+COIN_SIZE
                                if x_end>=x and x_start<=x and y_end>=y and y_start<=y and coin.inStack():#Check if click is on coin
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
                                        #pygame.display.flip()
                                        raise exceptions.breakOutException#break out of the loops
                    except exceptions.breakOutException:pass#catches exception outside of the loops
                    break
            ########################
            #end checking for events#
            ##########################################
            #check for next turn
            if not currentPlayer.onTurn():
                turn+=1
                currentPlayer = self.players[turn%len(self.players)]
            pygame.display.flip()
        ###end of main game loop###
        #####################################################
        #display win
        self.graphics.displayWin(currentPlayer.name)
        return

############################################################################
#main function
############################################################################

if __name__=="__main__":
    g = Game()
    g.play()
    
