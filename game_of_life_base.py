import re
#import turtle
import copy
#import pandas as pd

class Base(object):

    def __init__(self):

        self.rows = 0
        self.cols = 0
        self.layers = 0
    ##read file, produce 2d array
    def read_grid(self, filename):

        ##open file
        #global f
        with open(filename,'r') as f:
            f = f.readlines()

        ##read file into gridsize
        gridsize = f[0]
        #print('the first line in "input":', gridsize)
        ##read inputs and assaign inputs into variables cols and rows
        if re.match(r'C(.*) R(.*)', gridsize):
            self.cols = int(re.search(r'C(.*) R(.*)', gridsize).group(1))
            self.rows = int(re.search(r'C(.*) R(.*)', gridsize).group(2))

        ##create grid
        inputgrid = [[[0] for i in range(self.cols)] for i in range(self.rows)]
        ##fill grid
        gridvalues = f[1:self.rows+1]
        for y,i in enumerate(inputgrid):
            gridvalues[y] = gridvalues[y].replace(' ', '')
            for x,i in enumerate(inputgrid[y]):
                inputgrid[y][x] = int(list(gridvalues[y])[x])
                '''try:
                    inputgrid[y][x] = int(list(gridvalues[y])[x])
                except:
                    print('input grid smaller than indicated size')
                exit()'''
        return inputgrid

    ##code to iterate through every grid block
    '''
      for y,i in enumerate(grid0):
          for x,i in enumerate(grid0[y]):
    '''

    def LiveNCount(self, y, x, inputgrid):
      ##iterate through neighbors
      Nsum = 0
      ## y is an index, self.rows is a count, this calculates a weird donnut world wraparound, 3x3 spaces will not behave if the borders are expected
      for a in range(-1,2):
          for b in range(-1,2):
            c = ((y + a)+self.rows)%self.rows
            d = ((x + b)+self.cols)%self.cols
            Nsum += inputgrid[c][d]
      Nsum -= inputgrid[y][x]
      return Nsum

    def Calculatenextgrid(self, inputgrid):
      ##create grid1 with actual braket iterable deepcopy
      grid1 = copy.deepcopy(inputgrid)

      for y,i in enumerate(inputgrid):
          for x,i in enumerate(inputgrid[y]):

            count = self.LiveNCount(y, x, inputgrid)
            #could replace with grid1:

            if (inputgrid[y][x] == 0 and count == 3):
              grid1[y][x] = 1
            if (inputgrid[y][x] == 1 and (count < 2 or count > 3)):
              grid1[y][x] = 0
      return grid1

    def draw(inputgrid):
      string = ''
      for y,i in enumerate(inputgrid):
        for x,i in enumerate(inputgrid[y]):
          if inputgrid[y][x] == 0:
            string = string + '-'
          else:
            string = string + '@'
            #print('@+')
        else:
          string = string + '\n'
      #print(string)


    ##Reinforcement Learning Modules
    def rl_match(self, x, y, key, inputgrid, x1, y1, xp, yp):
        match = 0
        target = x*y
        for a in range(0,y):
          for b in range(0,x):
            c = ((yp + a)+y1)%y1
            d = ((xp + b)+x1)%x1
            #print(a, b, key[a][b], 'grid', c, d, inputgrid[c][d])
            #print(type(key))
            if key[a][b] == inputgrid[c][d]:
                match += 1
        return match, target
        
    def count_g(inputgrid):
        count = 0
        for y in inputgrid:
            for x in inputgrid[y]:
                count += inputgrid[y][x]

#Creator: HanqiXiao / The Inscrutable

class match_store(object):
    def __init__(self):
        self.name = 0
        self.counter = 0
        self.reward = 1
        pass

    