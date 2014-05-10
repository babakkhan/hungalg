import copy

class solver:

    def __init__(self, matrix):
        self.mat = copy.deepcopy(matrix)
        self.flipped = False
        
        # create 2 nxn matrices
        self.zeroes = [[0 for y in range(0, len(self.mat))]
                          for x in range(0, len(self.mat))]
        self.lines = [[False for y in range(0, len(self.mat))]
                             for x in range(0, len(self.mat))]

    def minsum(self):
                
        while(True):
            # reduce rows and columns 
            self.rowreduce()
            self.transpose()
            self.rowreduce() # after transposing this reduces the columns
            self.transpose() # and transpose back

            # loop through the zeroes matrix, and for each element
            # that is zero, scan horizontally and vertically for
            # more zeroes and save the result
            for x in range(0, len(self.mat)):
                for y in range(0, len(self.mat)):
                    if(self.mat[x][y] == 0):
                        self.zeroes[x][y] = self.dirmax(x, y)

            # todo: comment
            
            

            print()
            print("Reduced matrix")
            self.printmatrix(self.zeroes, 2)
            print()
            print("Zeroes matrix")
            self.printmatrix(self.mat, 3)
            
    
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
