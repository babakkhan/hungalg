import copy

class solver:

    def __init__(self, matrix):
        self.mat = copy.deepcopy(matrix)
        self.flipped = False
        
        # create 2 nxn matrices of booleans
        self.lines = [[False for y in range(0, len(self.mat))]
                             for x in range(0, len(self.mat))]
        self.assignement = copy.deepcopy(self.lines)

    def minsum(self):
                
        while(True):
            # reduce rows and columns 
            self.rowreduce()
            self.transpose()
            self.rowreduce() # after transposing this reduces the columns
            self.transpose() # and transpose back

            #
            
    
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
        r = 0
        for i in range(0, len(self.mat)):
            r += (self.mat[i][column] == 0)
            r -= (self.mat[row][i] == 0)
        return r
    
    # print the matrix
    # (useful for debugging)
    def printmatrix(self, offset):    
        for row in self.mat:
            formatted = [str(element).rjust(offset) for element in row]
            print(" ".join(formatted))
