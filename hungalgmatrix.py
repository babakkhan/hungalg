import copy

class solver:

    def __init__(self, matrix):
        self.mat = copy.deepcopy(matrix)
        self.flipped = False

        # prepare the output list
        self.output = [0 for x in range(0, len(self.mat))]
        self.inuse = [False for x in range(0, len(self.mat))]

    def maxsum(self):
        for x in range(0, len(self.mat)):
            for y in range(0, len(self.mat)):
                self.mat[x][y] = -self.mat[x][y]
        return self.minsum()

    def minsum(self):
        # reduce rows and columns 
        self.rowreduce()
        self.transpose()
        self.rowreduce() # after transposing this reduces the columns
        self.transpose() # and transpose back
        
        while(True):
            # create 2 nxn matrices
            self.zeroes = [[0 for y in range(0, len(self.mat))]
                              for x in range(0, len(self.mat))]
            self.lines = copy.deepcopy(self.zeroes)

            # loop through the zeroes matrix, and for each element
            # that is zero, scan horizontally and vertically for
            # more zeroes and save the result
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(self.mat[x][y] == 0):
                        self.zeroes[x][y] = self.dirmax(x, y)
                    else:
                        self.zeroes[x][y] = 0
                        
            #print()
            #print("Reduced matrix")
            #self.printmatrix(self.mat, 3)
            #print()
            #print("Zeroes matrix")
            #self.printmatrix(self.zeroes, 2)

            # reset lines counter
            lines = 0

            # todo: comment
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    # clear according to sign
                    if(self.zeroes[x][y] > 0):
                        lines += 1
                        for i in range(0, len(self.mat)):
                            if(self.zeroes[i][y] > 0):
                                self.zeroes[i][y] = 0
                            self.lines[i][y] += 1
                    elif(self.zeroes[x][y] < 0):
                        lines += 1
                        for i in range(0, len(self.mat)):
                            if(self.zeroes[x][i] < 0):
                                self.zeroes[x][i] = 0
                            self.lines[x][i] += 1

            #print()
            #print("Lines matrix")
            #self.printmatrix(self.lines, 2)
            #print()
            #print(str(lines)+" lines")

            # If we covered all elements (by using as many lines as there are rows),
            # we are done. Otherwise, more reduction is necessary.
            if(lines >= len(self.mat)):
                break

            # loop through the matrix to find the lowest, non-struck value
            minvalue,found = 0,False
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(self.lines[x][y] == 0):
                        minvalue = (self.mat[x][y] if ((minvalue > self.mat[x][y]) or not found) else minvalue)
                        found = True

            print("lowest: "+str(minvalue))

            # loop through the matrix one more time
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(self.lines[x][y] == 0):
                        self.mat[x][y] -= minvalue
                    elif(self.lines[x][y] == 2):
                        self.mat[x][y] += minvalue

        # Find the optimal permutation
        self.findpermutation(0)
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

    # todo: comment
    def dirmax(self, row, column):
        h,v = 0,0
        for i in range(0, len(self.mat)):
            v += (self.mat[i][column] == 0)
            h += (self.mat[row][i] == 0)
        return (-h if (h > v) else v)
    
    # print the matrix
    # (useful for debugging)
    def printmatrix(self, toprint, offset):    
        for row in toprint:
            formatted = [str(element).rjust(offset) for element in row]
            print(" ".join(formatted))
