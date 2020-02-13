"""
nim_board.py
created on: 01/12/2020
created by: Anna Branam
last modified: 02/12/2020

"""

############################################################################
#imports
############################################################################
import random

############################################################################
#classes
############################################################################

class Coin():
    def __init__(self, x=0, y=0):
        self.x = x#x coordiant on board
        self.y = y#y coordiant on board
        self.removed, self.selected = False, False
    def remove(self):
        self.removed = True
        self.selected = False
        return self.removed
    def inStack(self): return not self.removed
    def isSelected(self):return self.selected
    def select(self):
        if self.inStack():#only selectable if the coin is in the stack
            self.selected = not self.selected
    def getX(self):return self.x
    def getY(self):return self.y
        
class Stack():
    def __init__(self,stackID, coins):
        self.stackID = stackID#y coord of stack
        self.coins = []
        for i in range(coins):
            self.coins.append(Coin(i, stackID))
            self.coinCount = coins
    def getCoins(self):return self.coins
    def removeCoins(self, coins):
        if any(filter(lambda coinID: coinID>=len(self.coins) or self.coins[coinID].removed, coins)): return False#if any of the moves is illegal, return False
        #at this point, all selected coins are still in the stack
        for coinID in coins:
            self.coins[coinID].remove()#flag each coin as removed
        return True
    
class Board():
    def __init__(self, stacks):
        stacks.sort()
        self.stacks = []
        for i in range(len(stacks)):
            self.stacks.append(Stack(i, stacks[i]))
    def getStacks(self):return self.stacks
    def removeCoins(self, stack, coins):
        #check length of stack and attempt to remove coin from stack
        return self.stacks[stack].removeCoins(coins)
    def getMove(self, move):
        (stack, coins) = move
        #check move validity and remove coin
        return stack in range(len(self.stacks)) and self.removeCoins(stack, coins)
