# Reduces rows individually.
# Note that this is *not* the same as conventional row reduction in linear algebra.
def rowreduce(matrix):
    for row in matrix:
        # find the minimum in the row
        minimum = row[0]
        for element in row:
            if(element < minimum):
                minimum = element
                
        #reduce each row by mn
        for i in range(0, len(row)):
            row[i] -= minimum

#transpose the matrix
def transpose(matrix):
    for x in range(0, len(matrix)):
        for y in range(x + 1, len(matrix)):
            matrix[x][y],matrix[y][x] = matrix[y][x],matrix[x][y]


# print the matrix
# (useful for debugging)
def printmatrix(matrix, offset):    
    for row in matrix:
        formatted = [str(element).rjust(offset) for element in row]
        print(" ".join(formatted))
