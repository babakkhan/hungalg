import copy

class solver:

    def __init__(self, matrix):
        self.mat = copy.deepcopy(matrix)
        self.flipped = False

        # prepare the output list
        self.output = [0 for x in range(0, len(self.mat))]
        self.inuse = [False for x in range(0, len(self.mat))]

    def maxsum(self):
        maxvalue = 0
        for x in range(0, len(self.mat)):
            for y in range(0, len(self.mat)):
                maxvalue = max(self.mat[x][y], maxvalue)
                
        for x in range(0, len(self.mat)):
            for y in range(0, len(self.mat)):
                self.mat[x][y] = - self.mat[x][y]
                
        return self.minsum()

    def minsum(self):
        # reduce rows and columns 
        self.rowreduce()
        self.transpose()
        self.rowreduce() # after transposing this reduces the columns
        
        while(True):
            # create 2 lists holding the no of zeroes per row/column
            zerosinrow = [0 for i in range(0, len(self.mat))]
            zerosincol = [0 for i in range(0, len(self.mat))]
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(self.mat[x][y] == 0):
                        zerosinrow[x] += 1
                        zerosincol[y] += 1
                        
            # create a matrix signifying where a line is running
            lines = [[0 for x in range(0, len(self.mat))] for y in range(0, len(self.mat))]
            linesno = 0
                    
            lastdir = -1

            while(self.zerosleft(zerosinrow, zerosincol)):
                linesno += 1
                
                maxzeros = -1
                lindex = 0
                neworient = 1
                
                for i in range(0, len(self.mat)):
                    if(zerosinrow[i] > maxzeros or (zerosinrow[i] == maxzeros and lastdir == 0)):
                        lindex = i
                        neworient = 1
                        maxzeros = zerosinrow[i]

                for j in range(0, len(self.mat)):
                    if(zerosincol[j] > maxzeros or (zerosincol[j] == maxzeros and lastdir == 1)):
                        lindex = j
                        neworient = 0
                        maxzeros = zerosincol[j]

                if(neworient == 1):
                    for i in range(0, len(self.mat)):
                        if(self.mat[lindex][i] == 0):
                            zerosincol[i] -= 1
                            zerosinrow[lindex] -= 1
                        lines[lindex][i] += 1
                else:
                    for i in range(0, len(self.mat)):
                        if(self.mat[i][lindex] == 0):
                            zerosinrow[i] -= 1
                            zerosincol[lindex] -= 1
                        lines[i][lindex] += 1

                lastdir = neworient

            # if we needed as many lines as there are rows, are done
            if(linesno >= len(self.mat)):
                if(self.findpermutation(0)):
                    break
            
            # else, reduce the matrix once more
            minvalue,found = 0,False
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(lines[x][y] == 0):
                        minvalue = (min(minvalue,self.mat[x][y]) if found else self.mat[x][y])
                        found = True

            # one more loop, subtract min from unmarked, add to double marked
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(lines[x][y] == 0):
                        self.mat[x][y] -= minvalue
                    elif(lines[x][y] >= 2):
                        self.mat[x][y] += minvalue

            #self.printmatrix(self.mat,4)
            #self.printmatrix(lines,1)

        # Find the optimal permutation
        print()
        print()
        print()
        print("Reduced matrix")
        self.printmatrix(self.mat, 3)
        print()
        print()
        return self.output
        
        #end of minsum()

    #  todo comment
    def findpermutation(self, row):
        if(row >= len(self.mat)): # done
            return True

        # loop through the existing columns
        for i in range(0, len(self.mat)):
            if((self.mat[row][i] == 0) and not self.inuse[i]):
                self.output[row] = i
                self.inuse[i] = True
                if(self.findpermutation(row + 1)):
                    return True
                self.inuse[i] = False
        return False

    def zerosleft(self, row, col):
        for x in row:
            if (x > 0):         # was !=
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
                    
            #reduce each element in the row by the minimum
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
    def printmatrix(self, toprint, offset):    
        for row in toprint:
            formatted = [str(element).rjust(offset) for element in row]
            print(" ".join(formatted))
