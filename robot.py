import numpy as np

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim

        self.dir_sensors = {'up': ['left', 'up', 'right'], 'right': ['up', 'right', 'down'],
                       'down': ['right', 'down', 'left'], 'left': ['down', 'left', 'up']}

        self.dir_move = {'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}

        # Our target is to reach to the center of the maze. Here, we define two values that corrospond to the center
        # For example, if maze is 12x12, counting from 0 to 11 the center would be located in:
        # (5,5), (5,6), (6,5), (6,6)
        # For simplicity, we are going to define only the values that x and y should have in the center
        self.goal = [(maze_dim/2)-1, maze_dim/2] 
        self.heuristic = self.generate_heuristic()

        # Cost for moving one block in the maze
        self.cost = 1

        # g value which indicates the cost for reaching to the current block
        self.g_value = 0 

        # Track how many times each block was visited
        # 0 --> was not explored
        # >1 --> explored
        self.explored = np.array([[0 for col in range(maze_dim)] for row in range(maze_dim)])
        self.explored[self.location[0]][self.location[1]] = 1

        # Keep track of number of steps taken to reach each block
        # -1 indicates that the corrosponding cell has not been explored
        self.stepsMap = np.array([[-1 for col in range(maze_dim)] for row in range(maze_dim)])
        self.stepsCount = 0

        # Record available moves at each block
        #self.available_moves = [[self.g_value, location[0], location[1]]]


    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        rotation = 0
        movement = 0
        print "------------"
        print self.location

        

        if self.location[0] in self.goal and self.location[1] in self.goal:
            rotation = 'Reset'
            movement = 'Reset'
        else:
            validMoves = self.get_valid_next_moves(self.location, sensors)

            if len(validMoves) == 0:
                nextDirection = "stuck"
            else:
                costList = []
                # Calcluate the cost for every valid move
                for move in validMoves:
                    nextCost = self.g_value + self.cost
                    isExplored = self.explored[move["location"][0]][move["location"][1]]
                    costList.append({
                        "cost":nextCost + self.heuristic[move["location"][0]][move["location"][1]],
                        "location": move["location"],
                        "direction": move["direction"],
                        "isExplored": isExplored
                        })


                # Sort costList by total cost to get the least costly next move
                # If a cell has been explored, increase its cost by 999
                sortedCostList = sorted(costList, key=lambda x: x["cost"] + 999*(x["isExplored"]), reverse=False)

                lowestCostMove = sortedCostList[0]
                nextDirection = lowestCostMove["direction"]
                self.location = lowestCostMove["location"]


            movement, rotation = self.get_movement_rotation(nextDirection)

            # Update global variables
            self.g_value += movement
            if nextDirection == "stuck":
                self.heading = self.dir_sensors[self.heading][2]
            else:
                self.heading = nextDirection
            self.stepsMap[self.location[0]][self.location[1]] = self.g_value
            self.explored[self.location[0]][self.location[1]] += 1



            print self.heading
            self.print_cell_values(self.explored)


        return rotation, movement

    def print_cell_values(self, cellValues):
        '''
        Utility function used to visualize the maze cells for a given array
        Since the indexing in Python is different from the xy coordinates,
        whenever we need to visualize our cell values array we should transform
        the array by transposing first then inverting the y axis
        '''
        axes = np.transpose(cellValues)
        print axes[::-1]


    def generate_heuristic(self):
        '''
        Generate A* heuristic values for a given maze dimensions
        '''
        heuristic = [[-1 for col in range(self.maze_dim)] for row in range(self.maze_dim)]

        # Fill goal cells with a value of zero
        heuristic[self.goal[0]][self.goal[0]] = 0
        heuristic[self.goal[0]][self.goal[1]] = 0
        heuristic[self.goal[1]][self.goal[0]] = 0
        heuristic[self.goal[1]][self.goal[1]] = 0

        while True:
            # Condition for breaking the loop in case we reached to the grid boundaries
            cellModifiedCount = 0

            # Get indices for all maximum values occurrences
            maximumValue = np.amax(heuristic)
            maxIndices = np.argwhere(heuristic == maximumValue)

            # Loop through max cells to modify their adjacent cells
            for index in maxIndices:
                # Add one g-value to the adjacent cells to the maximum cell
                for direction in self.dir_move:
                    adjacentCell = self.make_a_move(index, direction, 1) # Pass a dummy value for distanceToWall to make this function work 
                    if adjacentCell != False and heuristic[adjacentCell[0]][adjacentCell[1]] == -1:
                        heuristic[adjacentCell[0]][adjacentCell[1]] = maximumValue + 1
                        cellModifiedCount += 1

            if cellModifiedCount == 0:
                break

        return heuristic




    def get_valid_next_moves(self, startingPosition, sensors):
        '''
        Return valid moves assuming we make a maximum of one step at a time
        The output is a list of valid xy coordinates and the direction of the move
        '''
        validMoves = []

        i = 0
        for direction in self.dir_sensors[self.heading]:
            nextMove = self.make_a_move(startingPosition, direction, sensors[i])
            i+=1

            if nextMove != False:
                validMoves.append({"location":nextMove, "direction":direction})

        return validMoves

    def make_a_move(self, startingPosition, direction, distanceToWall):
        '''
        Check whether a move can be made in the passed direction
        Two conditions are checked:
        1- Is the move inside the grid?
        2- Is there a wall in the direction we want to move?

        If a move is valid, return the xy coordinates. Otherwise, return False 
        '''

        if distanceToWall == 0:
            return False

        nextMove = [startingPosition[0] + self.dir_move[direction][0], startingPosition[1] + self.dir_move[direction][1]]
        if (nextMove[0] < 0) or (nextMove[0] > (self.maze_dim-1)) or (nextMove[1] < 0) or (nextMove[1] > (self.maze_dim-1)):
            return False

        return nextMove

    def get_movement_rotation(self, direction):
        '''
        For a given direction, return movement and rotation needed
        '''
        movement = 1
        if direction == "stuck":
            movement = 0
            rotation = 90

        else:
            if direction == self.dir_sensors[self.heading][0]:
                rotation = -90

            elif direction == self.dir_sensors[self.heading][1]:
                rotation = 0

            else:
                rotation = 90

        return movement, rotation


