# Reduces rows individually.
# Note that this is *not* the same as conventional row reduction in linear algebra.
def rowReduce(matrix):
    for row in matrix:
        # find the minimum in the list
        minimum = row[0]
        for element in row:
            if(element < minimum):
                minimum = element
                
        #reduce each row by mn
        for i in range(0, len(row)):
            row[i] -= minimum

    return matrix
