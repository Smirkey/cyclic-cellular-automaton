import pygame
import math
import random
import numpy as np
from pygame.locals import *
import pickle
import matplotlib.pyplot as plt
from PIL import Image
Colors = [[255,0,0], [0,255,0], [0,0,255], [0, 255, 255]]

size = 1
numIters = 500
windowX = 700
windowY = 700
startIter = 3000
         


def createGrid(x,y):
     return np.zeros(shape=(x,y))

def initialGrid(x,y):
    grid = createGrid(x, y)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i][j] = random.choice([i for i in range(len(Colors))])
    grid = grid.astype(int)
    return grid

def isEqual(tab1, tab2):
    count = 0
    for i in range(len(tab1)):
        if tab1[i] == tab2[i]:
            count += 1
    if count == len(tab1):
        return True
    else:
        return False

def colorToNextColorInCycleIndex(color):
    nextIndex = 0
    if color == len(Colors) - 1:
        nextIndex = 0
    else:
        nextIndex = color + 1

    return nextIndex

def colorToIndex(color):
     index = 0
     for i in range(len(Colors)):
          if isEqual(color, Colors[i]):
               index = i
               break
     return index

def getNeighboursToCheck(i, j, gridShape):
    NeighboursToCheck = [[i, j -1], [i, j+1], [i-1, j], [i+1,j]]
    if i == gridShape[0] - 1:
        NeighboursToCheck.pop(3)
    if i == 0:
        NeighboursToCheck.pop(2)
    if j == gridShape[1] - 1:
        NeighboursToCheck.pop(1)
    if j == 0:
        NeighboursToCheck.pop(0)
    return NeighboursToCheck

def getNeighboursToCheckv2(i , j, gridShape):
     NeighboursToCheck = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1], [i, j - 1], [i, j + 1], [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]
     checkList = [1 for i in range(len(NeighboursToCheck))]
     listOfNeighbours = []
     if i == gridShape[0] - 1:
        checkList[7] = 0
        checkList[6] = 0
        checkList[5] = 0
     if i == 0:
        checkList[0] = 0
        checkList[1] = 0
        checkList[2] = 0
     if j == gridShape[1] - 1:
        checkList[7] = 0
        checkList[4] = 0
        checkList[2] = 0
     if j == 0:
        checkList[5] = 0
        checkList[3] = 0
        checkList[0] = 0
     for i in range(len(NeighboursToCheck)):
          if checkList[i] == 1:
               listOfNeighbours.append(NeighboursToCheck[i])
     return listOfNeighbours
        
def take_a_step(grid):
    nextColorInTheCycle = 0
    newGrid = createGrid(grid.shape[0], grid.shape[1])
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            nextColorInTheCycle = colorToNextColorInCycleIndex(grid[i][j])
            neighboursToCheck = getNeighboursToCheckv2(i,j, [grid.shape[0], grid.shape[1]])
            numNextCycleNeighbours = 0
            for n in neighboursToCheck:
                if grid[n[0]][n[1]] == nextColorInTheCycle:
                    numNextCycleNeighbours += 1

            if numNextCycleNeighbours > 2:
                newGrid[i][j] = nextColorInTheCycle
            else:
                newGrid[i][j] = grid[i][j]

    newGrid = newGrid.astype(int)     
    return newGrid

def toImage(grid):
    newGrid = np.zeros(shape=(grid.shape[0], grid.shape[1], 3))
    for i in range(newGrid.shape[0]):
        for j in range(newGrid.shape[1]):
            for k in range(newGrid.shape[2]):
                newGrid[i][j][k] = Colors[grid[i][j]][k]
    
    return newGrid
            
def FromImageToGrid(image):
     newGrid = np.zeros(shape=(image.shape[0],image.shape[1]))
     for i in range(image.shape[0]):
          for j in range(image.shape[1]):
               newGrid[i][j] = colorToIndex(image[i][j])
     newGrid = newGrid.astype(int)
     return newGrid
               
def createData(numIters, grid):
    data = []
    print('started...')
    for i in range(numIters):
        im = Image.fromarray(toImage(grid).astype(np.uint8))
        im.save("{}.png".format(i + startIter))
        np.save("{}.npy".format(i + startIter), toImage(grid))
        print("saved")
        grid = take_a_step(grid)
            
        print('iter {}/{}'.format(i + 1 + startIter, numIters + startIter))
        
    print('...ended')

def showGrid(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            pygame.draw.rect(window, Colors[grid[i][j]], [i * size, j * size, size, size], 0)
            
def showGrid2(grid):
    surf = pygame.surfarray.make_surface(grid)
    window.blit(surf, (0, 0))
    
def showData(numIters):
    for k in range(numIters):
        showGrid2(np.load("{}.npy".format(startIter + k)))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def showData2(data):
    for k in range(len(data)):
        showGrid2(data[k])


Grid = FromImageToGrid(np.load("{}.npy".format(startIter - 1)))
data = createData(numIters, Grid)

pygame.init()
window = pygame.display.set_mode((windowX,windowY))
window.fill((0,0,0))


while 1:
    showData(numIters)
    firstTime = False
"""
while 1:
    Grid = take_a_step(Grid)
    showGrid(Grid)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
"""
