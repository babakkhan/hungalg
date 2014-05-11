# Written by Timon Knigge, 2014
# Implements the Hungarian Algorithm.
# http://en.wikipedia.org/wiki/Hungarian_algorithm

import copy

class solver:

    def __init__(self, matrix):
        self.mat = copy.deepcopy(matrix)
        self.flipped = False

        # prepare the output list
        self.output = [0] * len(self.mat)
        self.inuse = [False] * len(self.mat)
        

    def maxsum(self):
        # we can easily find the max sum by multiplying the matrix by -1,
        # and finding the min sum of the result.
        for x in range(0, len(self.mat)):
            for y in range(0, len(self.mat)):
                self.mat[x][y] = -self.mat[x][y]                
        return self.minsum()
    

    def minsum(self):
        # reduce rows and columns 
        self.rowreduce()
        self.transpose()
        self.rowreduce() # after transposing this reduces the columns
        
        while(True):
            # create 2 lists holding the no of zeroes per row/column
            zerosinrow = [0] * len(self.mat)
            zerosincol = [0] * len(self.mat)
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(self.mat[x][y] == 0):
                        zerosinrow[x] += 1
                        zerosincol[y] += 1
            
            # create a matrix to track lines we draw over the main matrix
            lines = [[0] * len(self.mat) for y in range(0, len(self.mat))]
            linesno = 0
            
            lastdir = -1    # whether our last line was vertical or horizontal (0 <=> v, 1 <=> h, -1 <=> not set)

            # while there are zeros we haven't crossed out yet
            while(self.zerosleft(zerosinrow, zerosincol)):            
                maxzeros = -1
                lindex = 0
                neworient = 1

                # find the best row to cross out
                for i in range(0, len(self.mat)):
                    if(zerosinrow[i] > maxzeros or (zerosinrow[i] == maxzeros and lastdir == 0)):
                        lindex = i
                        newdir = 1
                        maxzeros = zerosinrow[i]

                # same for columns
                for j in range(0, len(self.mat)):
                    if(zerosincol[j] > maxzeros or (zerosincol[j] == maxzeros and lastdir == 1)):
                        lindex = j
                        newdir = 0
                        maxzeros = zerosincol[j]

                if(newdir == 1):
                    for i in range(0, len(self.mat)):   # for each element to be crossed out
                        if(self.mat[lindex][i] == 0):   # if it is a zero
                            zerosincol[i] -= 1          # update the zerosinrow/zerosincol arrays it was part of
                            zerosinrow[lindex] -= 1
                        lines[lindex][i] += 1           # draw the line
                else:
                    for i in range(0, len(self.mat)):   # see ^
                        if(self.mat[i][lindex] == 0):
                            zerosinrow[i] -= 1
                            zerosincol[lindex] -= 1
                        lines[i][lindex] += 1

                lastdir = newdir         # lastdir has to be saved to prevent a nasty edge case
                linesno += 1
            # end of inner while

            # see if we found a good permutation yet
            if(linesno >= len(self.mat)):
                if(self.findpermutation(0)):
                    break
            
            # else, reduce the matrix once more
            # find the lowest uncrossed element
            minvalue,found = 0,False
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(lines[x][y] == 0):
                        minvalue = (min(minvalue,self.mat[x][y]) if found else self.mat[x][y])
                        found = True

            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(lines[x][y] == 0):
                        self.mat[x][y] -= minvalue      # subtract the lowest uncrossed element from all uncrossed elements
                    elif(lines[x][y] == 2):
                        self.mat[x][y] += minvalue      # add the lowest uncrossed element to all double crossed elements
        # end of outer while

        # Return the result
        return self.output        
    #end of minsum()
    

    # attempts to find a suitable permutation using the reduced matrix.
    # returns true if a permutation is found.
    def findpermutation(self, row):
        if(row >= len(self.mat)): # no more rows to check
            return True

        # loop through the existing columns
        for i in range(0, len(self.mat)):
            if((self.mat[row][i] == 0) and not self.inuse[i]):  # if the column is unused, and the intersection with our row is a 0
                self.output[row] = i                            # save/mark it
                self.inuse[i] = True                            
                if(self.findpermutation(row + 1)):              # and move to the next row
                    return True                                 # successful branch
                self.inuse[i] = False                           # no success in this branch
        return False
    

    # whether there are still rows/columns that should be crossed out
    def zerosleft(self, row, col):
        for x in row:
            if (x > 0):
                return True
        for y in col:
            if (y > 0):
                return True
        return False
    
    
    # Reduces rows individually.
    # Note that this is *not* the same as conventional row reduction in linear algebra.
    def rowreduce(self):
        for row in self.mat:
            # find the minimum in the row
            minimum = min(element for element in row)
                    
            # reduce each element in the row by the minimum
            if(minimum != 0):
                for i in range(0, len(row)):
                    row[i] -= minimum
                    
    
    #transpose the matrix
    def transpose(self):
        self.flipped = not self.flipped
        for x in range(0, len(self.mat)):
            for y in range(x + 1, len(self.mat)):
                self.mat[x][y], self.mat[y][x] = self.mat[y][x], self.mat[x][y]
                
    
    # print the matrix
    # (useful for debugging)
    def printmatrix(self, toprint, offset=1):    
        for row in toprint:
            formatted = [str(element).rjust(offset) for element in row]
            print(" ".join(formatted))
