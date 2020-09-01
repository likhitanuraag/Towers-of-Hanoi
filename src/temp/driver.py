# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:02:39 2020

@author: Likhit
"""
import sys
import random 
from array import array

import copy
import queue
#import Board
from priorityq import PQ

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
    
class Search:
    def __init__(self, start):
        self.parentTrace = {}
        self.start = start
        self.gamePath = []
        self.movePath = []
        self.numMoves = 0
        
        self.end = None
        
        
    def unwindPath(self):
        if self.end:
            target = self.end
        else:
            target = Board.constructTargetBoard(self.start.numRods, self.start.numDisks, self.start.targetRod)
            
        startHash = self.start.hash()
        nextHash = target.hash()
        
        self.gamePath = []
        self.movePath = []
        
        if not startHash == nextHash:
            while (True):
                self.gamePath.insert(0, Board.constructBoard(nextHash, self.start.numRods, self.start.numDisks, self.start.targetRod))
                if startHash == nextHash:
                    break
                else:
                    #break
                    moves = self.parentTrace[nextHash][1]
                    self.movePath.insert(0, moves)
                    nextHash = self.parentTrace[nextHash][0]
                    
        self.numMoves = len(self.movePath)
        
        
    def printPath(self, verbose = False):
        if verbose:
            counter = 0
            for i in range(len(self.gamePath)):
                if counter == 0:
                    print("Original")
                    print("Heuristic = " + str(self.gamePath[i].heuristic()) + " : Actual Dist = " + str(len(self.gamePath) - counter - 1))
                    self.gamePath[i].printBoard()
                else:
                    print("Move " + str(counter) + ": " + str(self.movePath[counter - 1]))
                    print("Heuristic = " + str(self.gamePath[i].heuristic()) + " : Actual Dist = " + str(len(self.gamePath) - counter - 1))
                    self.gamePath[1].printBoard()
                print("-----------------------------------------------")
                counter += 1
        else:
            for i in range(len(self.movePath)):
                print("Move " + str(i + 1) + ": " + str(self.movePath[i]))
                
                
class BFSSearch(Search):
    def __init__(self, start, end=None):
        super().__init__(start)
        
        if end is None:
            self.end = Board.constructTargetBoard(start.numRods, start.numDisks, start.targetRod)
        else:
            self.end = end
            
        self.endHash = self.end.hash()
        self.parentTrace = {}
        self.search()
        
        
    def search(self):
        self.parentTrace = {}
        
        q = queue.Queue()
        q.put((self.start, (0,0,0)))
        
        while(not q.empty()):
            game = q.get()[0]
            hash = game.hash()
            
            if game.isFinished():
                self.unwindPath()
                return
            
            successors = game.successors()
            successors[:] = filter(lambda x: x[0].hash() not in self.parentTrace, successors)
            
            for successor in successors:
                self.parentTrace[successor[0].hash()] = {hash, successor[1]}
                q.put(successor)
    
    
class AStarSearch(Search):
    def __init__(self, start, debug=False):
        super().__init__(start)
        
        self.end = Board.constructTargetBoard(start.numRods, start.numDisks, start.targetRod)
        self.endHash = self.end.hash()
        
        self.openSet = PQ()
        self.openSet.update(start)
        
        self.openSet.update(start)
        
        self.closedSet = {}
        
        self.temp_gScore = {start.hash():0}
        
        self.parentTrace[start.hash()] = {}
        
        self.latest_heuristic = {start.hash():start.heuristic()}
        
        self.snapshots = []
        self.debug = debug
        
        self.search()
        
    def search(self):
        pass
    
    
    def updateLatestHeuristic(self, board, newHeuristic, move):
        board_hash = board.hash()
        if board_hash not in self.latest_heuristic or newHeuristic != self.latest_heuristic[board_hash]:
            self.latest_heuristic[board_hash] = newHeuristic
            
            if self.debug:
                self.snapshots.append((copy.copy(self.latest_heuristic), copy.copy(self.parentTrace)))


if __name__ == "__main__":
    board = Board.randomShuffle(5, 3, 4)

    print("**************BFS*****************")
    BFSSearch(board).printPath(True)   

    print("**************A-STAR*****************")
    AStarSearch(board).printPath(True)                      
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
