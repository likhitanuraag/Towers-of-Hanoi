# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 17:46:57 2020

@author: Likhit
"""

import sys
import random 
from array import array

class Board:
    
    def __init__(self, numRods, numDisks, targetRod):
        self.rods = []
        self.numDisks = numDisks
        
        if(numRods < 9):
            self.numRods = numRods
        else:
            raise ValueError("Number of rods must be 8 or less")
            
        if(targetRod < numRods):
            self.targetRod = targetRod
        else:
            raise ValueError("Target rod must be < number of rods")
            
        for i in range(numRods):
            self.rods.append(array('b'))
            
        for disk in range(numDisks, 0, -1):
            self.rods[0].append(disk)
            
    def isFinished(self):
        return len(self.rods[self.targetRod]) == self.numDisks
    
    def makeMove(self, fromRodIndex, toRodIndex):
        
        fRod = self.rods[fromRodIndex]
        
        if len(fRod):
            disk = fRod.pop()
        else:
            return -2
        
        tRod = self.rods[toRodIndex]
        if not len(tRod) or tRod[len(tRod) - 1] > disk:
            tRod.append(disk)
        else:
            fRod.append(disk)
            return -1
        
        return (disk, fromRodIndex, toRodIndex)
    
    def hash(self):
        output = 0
        for i, rod in enumerate(self.rods):
            for disk in rod:
                output += i << (3 * (disk - 1))
        return output
    
    def makeCopy(self):
        new = Board(self.numRods, self.numDisks, self.targetRod)
        new.rods = []
        for rod in self.rods:
            new.rods.append(array('b', rod))
        return new
    
    def printBoard(self):
        output = ""
        for rod in self.rods:
            output += "|"
            for disk in rod:
                output += str(disk) + " "
            output += "\n"
        output += "\n"
        sys.stdout.write(output)
        sys.stdout.flush()
        
    def successors(self):
        succ = []
        
        child = self.makeCopy()
        
        for fromRod in range(self.numRods):
            for toRod in range(self.numRods):
                
                if fromRod == toRod:
                    continue
                
                moveResults = child.makeMove(fromRod, toRod)
                
                if moveResults == -1:
                    continue
                elif moveResults == -2:
                    break
                else:
                    succ.append((child, moveResults))
                    child = self.makeCopy()
        return succ
    
    def heuristic(self):
        val = 0
        largestNotOn = -1
        
        for i in range(self.numDisks, 0, -1):
            if i not in self.rods[self.targetRod]:
                largestNotOn = i
                break
            
        if largestNotOn == -1:
            return 0 
        
        for rod in self.rods:
            if largestNotOn in rod:
                largestNotOnLocation = rod
                
        val += len(largestNotOnLocation) * 2 - 1
        
        val += largestNotOn - len(largestNotOnLocation)
        
        return val
    
    def randomShuffle(numRods, numDisks, targetRod):
        new = Board(numRods, numDisks, targetRod)
        
        for i in range(len(new.rods)):
            new.rods[i] = array('b')
            
        for disk in range(numDisks, 0, -1):
            random.choice(new.rods).append(disk)
            
        return new
    
    def constructTargetBoard(numRods, numDisks, targetRod):
        new = Board(numRods, numDisks, targetRod)
        for i in range(len(new.rods)):
            new.rods[i] = array('b')
            
        for i in range(numDisks, 0, -1):
            new.rods[targetRod].append(i)
            
        return new
    
    def constructBoard(hash, numRods, numDisks, targetRod):
        new = Board(numRods, numDisks, targetRod)
        
        for i in range(len(new.rods)):
            new.rods[i] = array('b')
            
        for i in range(numDisks, 0, -1):
            bit1 = (hash >> (3 * (i - 1))) & 1
            bit2 = (hash >> (3 * (i - 1) + 1)) & 1
            bit3 = (hash >> (3 * (i - 1) + 2)) & 2
            
            rodNum = bit1 + (bit2 * 2) + (bit3 * 4)
            new.rods[rodNum].append(i)
            
        return new
            
            
            
            
            
            
            
            
            
            
            
            