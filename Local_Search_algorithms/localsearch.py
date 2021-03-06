"""
localsearch.py

author: Anil Poriya

description: localsearch program will perform different local search algorithms for a given 2D matrix of
elevations. The algorithms will try to find a 5 x 5 region within the matrix that performs a maximization of
the variation which is defined as the difference of the maximum value and minimum value in the region. The algorithms
covered are hill climb, random restart hill climb, simulated annealing and random restart simulated annealing

Note: We need to have elevation.txt in the same folder as this code since the file name is hard-coded

Also, for simulated annealing algorithms, some random locations we may have to wait for slightly more seconds for output
to be displayed.
The format of the output displayed is described in the corresponding functions.


"""
import math
from random import randint
from random import randrange
class Pixel:
    """
    Pixel class is used to describe Pixel objects wherein each pixel instance will have the following information:
    row - row of the pixel
    col - column of the pixel
    value - value of the pixel in the original matrix.
    """
    __slots__ = 'row','col','value'


    def __init__(self,row,col,val):

        self.row = row
        self.col = col
        self.value = val


    def __str__(self):

        return ' ( X: ' + str(self.row) + ', Y: ' + str(self.col) + ' )  Pixel Value ->'+ str(self.value)

class CurrentState:

    __slots__ = 'value','pixel','grid'

    def __int__(self):
        self.value  = 0

    def convertToNodes(self,arr):
        """
        Converts elevation values to pixel objects
        :param arr: 2D matrix of elevations provided with the problem
        :return: 2D array -> grid, array of pixel objects
        """

        elevation = []

        for row in range(len(arr)):
            elerow = []
            for col in range(len(arr[0])):
                elerow.append(Pixel(row,col,arr[row][col]))
            elevation.append(elerow)

        return elevation

    def hillclimb(self,node):
        """
        Performs the Hill Climbing algorithm with the node that is provided. It finds the local max variance value
        by considering the neighbors of the current node. For each neighbor, it calculates the variance value for
        the 5 x 5 region generated by that neighbor and compare it with the existing variance value. If it is
        greater than the current variance value, we switch the current variance value and the current state accordingly
        and continue with the algorithm.
        This process continues until we find a state wherein none of its neighbors is able to produce a better variance
        value in which case, the function returns the current max variance value and the current state(node).

        The output for the Hill Climb when called is as follows:

        Variance Value , Pixel Point from where the region was generated which had this value

        5 x 5 grid for that Pixel Point.


        :param node: the start node which is randomly generated
        :return: fval,currentstate --> fval is the maximum variance value
        and currentstate is the node from which the region was obtained that
        contained this maximum variance value
        """
        #print("Hill Climbing")
        rowcurr = node.row
        colcurr = node.col
        valcurrent = node.value
        #print(rowcurr, ' ', colcurr, ' ', valcurrent)


        currentstate = node
        fval = self.initialvariation(node)

        #print(fval,'fval')

        while True:
            check = fval
            neighbors = self.findsuccessors(currentstate)
            for node in neighbors:
                fstate = self.initialvariation(node)
                #print('fstate',fstate)
                if fstate > fval:
                    currentstate = node
                    fval = fstate
            if fval == check:
                break

        #print('Hill Climbing Max Variance Value: ',fval)
        #self.printgrid(currentstate)

        return fval,currentstate


    def printgrid(self,node):
        """
        Prints the grid for the current node. The grid is 5 x 5 region where the node
        is the top-left most point in the region.
        :param node: The starting point from which the grid needs to be printed. The node represents
         the top-left most point of the grid.
        :return: None
        """

        r = node.row
        c = node.col
        matrix = []
        for row in range(r,r+5):
            trow = []
            for col in range(c,c+5):
                trow.append(self.grid[row][col].value)
            matrix.append(trow)

        for l in matrix:
            print(*l)

    def findsuccessors(self,curr):
        """
        Finds the neighbors of the current node. Neighbors include the four-pixel point moves possible
        from the current node. It checks whether each of these neighbors is valid and appends only
        the valid neighbors to the list and returns this list of valid neighbors.

        :param curr: the current node
        :return: list of valid neighbors for the current node
        """

        rowcurr = curr.row
        colcurr = curr.col

        neighbors = []
        if self.isValid(self.grid[rowcurr + 1][colcurr]):
            neighbors.append(self.grid[rowcurr + 1][colcurr])
        if self.isValid(self.grid[rowcurr - 1][colcurr]):
            neighbors.append(self.grid[rowcurr - 1][colcurr])
        if self.isValid(self.grid[rowcurr][colcurr + 1]):
            neighbors.append(self.grid[rowcurr][colcurr + 1])
        if self.isValid(self.grid[rowcurr][colcurr - 1]):
            neighbors.append(self.grid[rowcurr][colcurr - 1])

        return neighbors


    def initialvariation(self,node):
        """
        This function calculates the variance value which needs to be maximized
        for our algorithms. The node provided forms the top-left most point of the
        5 x 5 grid that is formed from this point. The variance is then calcualted
        by finding the difference of the maximum and minimum pixel value of this region.
        :param node: current node to form the grid and find the variance value
        :return: variance value (difference of max and min value)
        """

        row = node.row
        col = node.col
        minval = None
        maxval = None

        for r in range(row,row + 5):
            for c in range(col,col + 5):
                temp = float(self.grid[r][c].value)
                if minval is None or temp < minval:
                    minval = temp
                if maxval is None or temp > maxval:
                    maxval = temp

        #print('minval', minval, ' maxval ',maxval)
        return maxval - minval



    def randomrestartHC(self):
        """
        randomrestartHC performs the Hill Climbing algorithm 50 times
        and finds the average variance value of the 50 runs and also the
        maximum variance value among these 50 runs.

        The output format of Random Restart Hill Climbing algorithm is :

        Max variance value, Average variance value, finalstate or node which maximizes the variance value

        5 x 5 grid for the finalstate or node(with finalstate as the top-left most point of the region)

        :return: the finalstate or pixel node which gives the maximum variance value
         within the region formed by that node.
        """
        print("Random Restart Hill Climbing")
        fval = 0
        totalval = 0
        finalstate = None
        for _ in range(50):

            row,col = self.generateRandomStatePos(len(self.grid),len(self.grid[0]))
            val,state = self.hillclimb(self.grid[row][col])
            totalval += val
            #print('val ->',val,'state ->',state)
            if fval is None or val > fval:
                fval = val
                finalstate = state


        print('Max resulting value -> ',fval,'  Average resulting value -> ',totalval/50,'final ',finalstate)
        return finalstate




    def simulatedann(self,node):
        """
        performs the simulated annealing algorithm which is a variant of stochastic hill climbing algorithm.
        In simulated annealing, if a move improves the variance value, it is always accepted. However, if it does
        not improve the variance, we simply do not discard the move or pixel node. The algorithm instead calculates
        the probability for the move and if it satisfies a certain constraint, the move of pixel node is accepted.
        We evaluate this badness or goodness of the move using the formula provided below in the code.
        It uses a temperature T, current max variance value fval, variance value of the pixel to be considered fstate.

        We start with T = 2 and after every iteration, we decrease T by some factor. Going by the formula, the bad
        moves are more likely to be allowed only at the start when the temperature is high and less likely as T drops.

        When T drops to 0.1 or below, we simply perform hill climb with the current state which gives
        better convergence value.

        The output for the Simulated Annealing when called is as follows:

        Variance Value , Pixel Point from where the region was generated which had this value

        5 x 5 grid for that Pixel Point.

        :param node: the start node which is randomly generated
        :return: hillclimb(currenstate) function which gives fval,currentstate --> fval is the maximum variance value
        and currentstate is the node from which the region was obtained that
        contained this maximum variance value
        """
        #print("Simulated Annealing")

        currentstate = node
        fval = self.initialvariation(currentstate)
        T = 2
        while True:

            neighbors = self.findsuccessors(currentstate)
            state = self.findrandom(neighbors)

            fstate = self.initialvariation(state)
            if fstate > fval:
                fval = fstate
                currentstate = state
            else:
                num = randint(0,1)
                exponent = (fstate - fval)/T
                compval = math.pow(math.e,exponent)
                #print('num ->',num,' exponent ->',exponent,'compval ->',compval)
                if num < compval:
                    currentstate = state
                    fval = fstate
            T *= 0.999

            #print(T)
            if T <= 0.1:
                return self.hillclimb(currentstate)


    def randomrestartSA(self):

        """
        randomrestartSA performs the simulated annealing algorithm 50 times
        and finds the average variance value of the 50 runs and also the
        maximum variance value among these 50 runs.

        The output format of Random Restart Simulated Annealing algorithm is :

        Max variance value, Average variance value, finalstate or node which maximizes the variance value

        5 x 5 grid for the finalstate or node(with finalstate as the top-left most point of the region)

        :return:
        """
        print("Random Restart Simulated Annealing")

        fval = 0
        totalval = 0
        finalstate = None

        for _ in range(50):
            row, col = self.generateRandomStatePos(len(self.grid), len(self.grid[0]))
            val, state = self.simulatedann(self.grid[row][col])
            totalval += val
            #print('val ->', val, 'state ->', state)
            if fval is None or val > fval:
                fval = val
                finalstate = state

        print('Max resulting value -> ', fval, '  Average resulting value -> ', totalval / 50, 'final ', finalstate)
        return finalstate



    def isValid(self,node):
        """
        checks whether the given node is valid or not. It is valid if from the given
        node, we can create a 5 x 5 region of pixels with the given node as the top-left most
        pixel in the region.
        :param node: the node to check the validity for
        :return: True if the node is valid or False if it is not
        """

        row = node.row
        col = node.col
        #print('isvalid ',row,' ',col)
        #valid = False
        if row + 4 < len(self.grid) and col + 4 < len(self.grid[0]):
            return True
        else:
            return False

        #print('isvalid ',row,' ',col,valid)
        #return valid

    def findrandom(self,nodelist):
        """
        selects a random pixelnode from the given list of pixelnodes
        :param nodelist: the list of nodes
        :return: a random node selected from the list
        """

        random_index = randrange(0,len(nodelist))
        return nodelist[random_index]

    def generateRandomStatePos(self,r,c):
        """
        generates a random row and column location within the given
        matrix and checks whether this location of row,column is valid
        or not and return these values which will be used for generating
        a random startnode for hillclimb and simulatedannealing algorithms.

        The locations would be valid if form these given row and col values,
        we can create a 5 x 5 region.

        :param r: the max number of rows in the matrix
        :param c: the max number of colums in the matrix
        :return: randomly generated row and column positions.
        """

        while True:

            row = randint(0,r-1)
            col = randint(0,c-1)

            if row + 4 < r and col + 4 < c:
                return row,col
            else:
                continue

def main():
    matrix = []
    try:
        with open('elevation.txt') as handle:
            for line in handle:
                arr = []
                arr = line.strip().split()
                matrix.append(arr)
    except:
        print("Enter a valid file name")
    #print(arr)
    lsearch = CurrentState()
    lsearch.grid = lsearch.convertToNodes(matrix)

    maxwrows = len(lsearch.grid)
    maxcols = len(lsearch.grid[0])


    row, col = lsearch.generateRandomStatePos(maxwrows,maxcols)
    #print(row,' ',col)




    print("Select type of algorithm to run :")
    print("1. Hill Climbing \n2. Random Restart Hill Climbing")
    print("3. Simulated Annealing \n4. Random Restart Simulated Annealing")

    while(True):

        try:
            inp = int(input("Enter your choice "))
        except:
            print("Enter a number")
            continue

        if inp == 1:
            #print("random point taken :",row,' ',col)
            fval,currentstate = lsearch.hillclimb(lsearch.grid[row][col])
            print('Hill Climbing Max Variance Value: ', fval,' Pixel Point : ',currentstate)
            lsearch.printgrid(currentstate)
            break
        elif inp == 2:
            currentstate = lsearch.randomrestartHC()
            lsearch.printgrid(currentstate)
            break
        elif inp == 3:
            fval,currentstate = lsearch.simulatedann(lsearch.grid[row][col])
            print('Simulated Annealing Max Variance Value: ',fval,' Pixel Point : ',currentstate)
            lsearch.printgrid(currentstate)
            break
        elif inp == 4:
            currentstate = lsearch.randomrestartSA()
            lsearch.printgrid(currentstate)
            break
        else:
            print("Enter a valid number")
            continue




if __name__ == '__main__':
    main()

