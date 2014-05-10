import copy

class solver:

    def __init__(self, matrix):
        self.mat = copy.deepcopy(matrix)
        
    # Reduces rows individually.
    # Note that this is *not* the same as conventional row reduction in linear algebra.
    def rowreduce(self):
        for row in self.mat:
            # find the minimum in the row
            minimum = min(element for element in row)
                    
            #reduce each element in the row by the minimum
            for i in range(0, len(row)):
                row[i] -= minimum
    
    #transpose the matrix
    def transpose(self):
        for x in range(0, len(self.mat)):
            for y in range(x + 1, len(self.mat)):
                self.mat[x][y], self.mat[y][x] = self.mat[y][x], self.mat[x][y]
    
    
    # print the matrix
    # (useful for debugging)
    def printmatrix(self, offset):    
        for row in self.mat:
            formatted = [str(element).rjust(offset) for element in row]
            print(" ".join(formatted))
