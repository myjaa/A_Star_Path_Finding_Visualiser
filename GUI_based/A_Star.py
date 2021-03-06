#the algorithm
# the most efficient form of this is written in GUI_based_improved/GUI_presentable

import math

# to store each node of the graph
class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.g_cost, self.h_cost = None, 0
        self.f_cost = 0
        self.way = True
        self.obstacle = False
        self.source = False
        self.target = False
        self.path = False
        self.root_parent = None

    # function to calculate f_cost
    def calculate_fcost(self):
        self.f_cost = self.g_cost + self.h_cost

#Data structure to store nodes according to their F-cost or H-cost as needed
class PriorityQ:
    def __init__(self):
        self.Q = []
        self.Q_copy=[]

    #  Q= [(node.f_cost,node),(),(), .....]
    def add(self, node, closed,thrown_out_of_closed):
        if node not in closed and node not in thrown_out_of_closed and node.obstacle==False:
            if len(self.Q) == 0:
                self.Q.append((node.f_cost, node))
            else:
                self.Qsort(node)

    def Qsort(self, node):
        for i in range(len(self.Q)):

            # if F-costs are equal then the one with the lowest H-cost gets priority
            if self.Q[i][0] == node.f_cost:
                if self.Q[i][1].h_cost > node.h_cost:
                    self.Q.insert(i, (node.f_cost, node))
                    break

            # The lowest F-cost gets priority
            if self.Q[i][0] > node.f_cost:
                self.Q.insert(i, (node.f_cost, node))
                break

            # if the F-Cost to be added is the largest in the Q
            if i == len(self.Q) - 1:
                self.Q.append((node.f_cost, node))

    # Pop the first element, i.e. the one with the lowest F-cost
    def popQ(self):
        if len(self.Q)!=0:
            lowest=self.Q.pop(0)
            return lowest

    # append all the remaining elements of Q to Q_copy and then clear the Q.
    def copyQ(self):
        if len(self.Q)!=0:
            for i in self.Q:
                self.Q_copy.append(i)
            self.Q.clear()

# function to display grid
def show_grid():
    for i in grid:
        for j in i:
            if j.way:
                print("-", end=" ")
            elif j.obstacle:
                print("O", end=" ")
            elif j.source:
                print("S", end=" ")
            elif j.target:
                print("T", end=" ")
            elif j.path:
                print("x", end=" ")
        print()


# function to set source node
def set_source(row, column):
    grid[row][column].source, grid[row][column].way = True, False


# function to set target node
def set_target(row, column):
    grid[row][column].target, grid[row][column].way = True, False

#function to set obstacle
def set_obstacle():
    for coordinate in obstacle_list:
        cell=grid[coordinate[0]][coordinate[1]]
        cell.obstacle, cell.way = True, False


# calculate h_cost for all nodes
def set_cost(currentrow, currentcol, target_r, target_c, parent, distance=1):
    dx = abs(target_r - currentrow)
    dy = abs(target_c - currentcol)
    # got this formula from Stanford's website on A* path finding
    grid[currentrow][currentcol].h_cost = (dx + dy) + ((1.4 - 2) * min(dx, dy))
    grid[currentrow][currentcol].g_cost =parent.g_cost + distance
    grid[currentrow][currentcol].calculate_fcost()

# function to add to open list/Q
def add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed,distance=1 ):
    if to_enter_row>=0 and to_enter_col>=0:
        set_cost(to_enter_row, to_enter_col, target_r, target_c, parent,distance)
        open.add(grid[to_enter_row][to_enter_col],closed,thrown_out_of_closed)


def test_print():
    print('source-r',source_r,'source_c',source_c)
    print('target-r',target_r,'target_c',target_c)
    print(obstacle_list)
    print(len(obstacle_list))


def calculate():
    # Pinning source and target
    set_source(source_r, source_c)
    set_target(target_r, target_c)
    set_obstacle()

    source = grid[source_r][source_c]
    source.g_cost = 0

    open = PriorityQ()
    closed = []
    thrown_out_of_closed=[]
    closed.append(source)
    parent = source
    dd=math.sqrt(2)  # diagonal distance , approx=1.4(root 2)
    break_counter=0

    while True:

        # top left
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col - 1
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed,dd )
        except IndexError:
            pass

        # top
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed)
        except IndexError:
            pass

        # top right
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col + 1
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed,dd )
        except IndexError:
            pass
        # ------------------------bottom-----------------------------------------
        # bottom left
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col - 1
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed,dd )
        except IndexError:
            pass

        # bottom
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed)
        except IndexError:
            pass

        # bottom right
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col + 1
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed,dd )
        except IndexError:
            pass
        # ----------------------------------sides---------------------
        # left
        try:
            to_enter_row, to_enter_col = parent.row, parent.col - 1
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed)
        except IndexError:
            pass

        # right
        try:
            to_enter_row, to_enter_col = parent.row, parent.col + 1
            add_to_open(to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,thrown_out_of_closed)
        except IndexError:
            pass

        # if len(Q)==0 then no path exists
        if len(open.Q)==0:
            if parent!=source:
                parent.way,parent.path=True,False
                thrown_out_of_closed.append(parent)
                closed.remove(parent)
                parent=parent.root_parent
            else:
                break_counter+=1
        else:
            # gives the element with the lowest f_cost
            parent.way,parent.path=False,True
            to_be_parent=open.popQ()[1]
            to_be_parent.root_parent=parent
            parent=to_be_parent
            closed.append(parent)

        if break_counter==2:
            print('no valid path')
            break

        open.copyQ()

        # checking if the current node is the target node
        if parent.target:
            break

    source.path=False
    # display grid
    show_grid()

def reset():
    for i in grid:
        for j in i:
            if j.obstacle:
                j.obstacle,j.way=False,True
            elif j.source:
                j.source,j.way=False,True
            elif j.target:
                j.target,j.way=False,True
            elif j.path:
                j.path,j.way=False,True
    obstacle_list.clear()


# ----------------------------------------------------main------------------------------------------------------------------


# a grid of 100x100(99x99)
# (RESOLVED) 0th column shouldn't be used, if the input recieved from GUI contains col=0 add +1 to both cols.  PLOT EVRYTHING WITH col+1
grid = [[Node(i, j) for j in range(50)] for i in range(50)]

# enter the coordinates of source and target
source_r, source_c = None,None
target_r, target_c = None,None
obstacle_list=set()

