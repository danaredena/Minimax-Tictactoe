import copy
import math

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

def print_board(board):
    for i in range(0,3):
        print("-------------")
        print("|", board[i][0], "|", board[i][1], "|", board[i][2], "|")
    print("-------------")

print("=== LET'S PLAY TIC TAC TOE == ")
print_board(board)
print("\n")

def is_win(board): #param: state
    for i in range(0, 3):
        if (board[i][0] == 'x' and board[i][1] == 'x' and board[i][2] == 'x'):
            return 'x' #can return cost instead
        if (board[i][0] == 'o' and board[i][1] == 'o' and board[i][2] == 'o'):
            return 'o'
        if (board[0][i] == 'x' and board[1][i] == 'x' and board[2][i] == 'x'):
            return 'x'
        if (board[0][i] == 'o' and board[1][i] == 'o' and board[2][i] == 'o'):
            return 'o'

    if (board[0][0] == 'x' and board[1][1] == 'x' and board[2][2] == 'x'):
        return 'x'
    if (board[0][2] == 'x' and board[1][1] == 'x' and board[2][0] == 'x'):
        return 'x'
    if (board[0][0] == 'o' and board[1][1] == 'o' and board[2][2] == 'o'):
        return 'o'
    if (board[0][2] == 'o' and board[1][1] == 'o' and board[2][0] == 'o'):
        return 'o'
    if (is_filled(board)):
        return 'draw'
    return '-'

def is_filled(board):
    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] == ' '):
                return False
    return True

def next_moves(board):
    next = []
    for i in range(3):
        for j in range(3):
            if (board[i][j] == ' '):
                next.append((i,j))
    return next

class State:
    def __init__(self, parent, board, depth, coord):
        self.alpha = float("-inf")
        self.beta = float("inf")
        self.parent = parent
        self.children = []
        self.depth = depth
        if (self.depth%2 == 0): #maximizer
            self.cost = float("-inf")
        else:
            self.cost = float("inf") #minimizer
        self.s_board = board
        self.next = next_moves(self.s_board)
        self.coord = coord
    def set_alpha(self, alpha):
        self.alpha = alpha
    def set_beta(self, beta):
        self.beta = beta
    def set_cost(self, cost):
        self.cost = cost
    def get_cost(self):
        return self.cost
    def get_alpha(self):
        return self.alpha
    def get_beta(self):
        return self.beta
    def get_parent(self):
        return self.parent
    def get_depth(self):
        return self.depth
    def get_board(self):
        return self.s_board
    def get_coord(self):
        return self.coord
    def min_or_max(self):
        return self.depth%2
    def next_op(self, op):
        if (op == 0):
            print(self.next)
        elif (op == 1): #len
            return len(self.next)
        else:
            return self.next.pop(0)
    def add_child(self, child):
        self.children.append(child)
    def get_childsol(self):
        for i in range(len(self.children)):
            if (self.children[i].get_cost() == self.cost):
                return self.children[i].get_board(), self.children[i].get_coord()

def next_move(move_char, board, coord):
    board[coord[0]][coord[1]] = move_char
    return board

def descend(parent):
    board = parent.get_board()
    s_board = copy.deepcopy(board)
    depth = parent.get_depth()

    is_terminal = is_win(s_board)

    #check if terminal before descend
    if (is_terminal != '-'):
        if (is_terminal == 'o'):
            parent.set_cost(10-depth)
        elif (is_terminal == 'x'):
            parent.set_cost(depth-10)
        else:
            parent.set_cost(0)
        if (parent.min_or_max() == 0): #max
            parent.set_alpha(parent.get_cost())
        else:
            parent.set_beta(parent.get_cost())
        return False #begin ascension

    #check for pruning
    if (parent.get_alpha() >= parent.get_beta()):
        return False #trigger ascend

    #check if no more children can be found
    if (parent.next_op(1) == 0):
        return False
    coord = parent.next_op(2)

    #Descend
    if (parent.min_or_max() == 0): #descend to min from max
        child = State(parent, next_move('o', s_board, coord), depth + 1, coord)
        child.set_alpha(parent.get_alpha())
        child.set_cost(child.get_beta())
        parent.add_child(child)

    else: #descend to max from min
        child = State(parent, next_move('x', s_board, coord), depth + 1, coord)
        child.set_beta(parent.get_beta())
        child.set_cost(child.get_alpha())
        parent.add_child(child)
    return child

def ascend(child):
    parent = child.get_parent()
    if (parent == None):
        return None

    if (parent.min_or_max() == 0): #ascend to max
        if (child.get_beta() != float("inf")):
            if (child.get_beta() > parent.get_alpha()):
                parent.set_alpha(child.get_beta())
                parent.set_cost(parent.get_alpha())

    else: #ascend to min
        if (child.get_alpha() != float("-inf")):
            if (child.get_alpha() < parent.get_beta()):
                parent.set_beta(child.get_alpha())
                parent.set_cost(parent.get_beta())
    return parent

def ai_move():
    print("Thinking of a move...")
    global board
    mm_board = copy.deepcopy(board)
    #root Node
    prev_state = None
    root = State(None, mm_board, 0, None)
    parent = root
    while (parent != None): #DONE
        next_state = parent
        prev_state = parent
        while (next_state != False):
            prev_state = next_state
            next_state = descend(next_state)
        #ascend
        parent = ascend(prev_state)
    solution, coord = root.get_childsol()
    print("Chose", coord)
    print_board(solution)
    return solution

def human_move():
    while(True):
        print("Take your move, human")
        x = int(input("x: "))
        y = int(input("y: "))
        if (board[y][x] == ' '):
            board[y][x] = 'x'
            print_board(board)
            break
        print("Invalid Move. Try Again")

#========== PROGRAM ==============
first = input("Human makes first move? (y/n) ")
while(True):
    if (first == 'y'):
        human_move()
        break
    elif (first != 'n'):
        print("Invalid key, try again")
    else:
        break
    first = input("Human makes first move? (y/n) ")

while(True):
    board = ai_move()
    if (is_win(board) != '-'):
        if (is_win(board) == 'x'):
            print("CONGRATULATIONS HUMAN, YOU WIN!")
        elif (is_win(board) == 'o'):
            print("SORRY HUMAN, I WIN!")
        else:
            print("IT'S A DRAW")
        break
    human_move()
    if (is_win(board) != '-'):
        if (is_win(board) == 'x'):
            print("CONGRATULATIONS HUMAN, YOU WIN!")
        elif (is_win(board) == 'o'):
            print("SORRY HUMAN, I WIN!")
        else:
            print("IT'S A DRAW")
        break
