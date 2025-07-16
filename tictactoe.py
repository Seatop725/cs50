"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def print_board(board):
    """
    Take as input the board, then prints out the board as a string
    """
    board_string=""
    for r in range(len(board)):
        for c in range(len(board[0])):
            board_string+=f"{board[r][c]} "
        board_string+="\n"
    print(board_string)


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    
    elif terminal(board):
        return None
    
    else:
        numX = 0
        numO = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board [i][j] == X:
                    numX += 1
                if board[i][j] == O:
                    numO += 1
        if numX > numO:
            return O
        
        else:
            return X
        
                     
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionsList = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == EMPTY:
                actionsList.append((r, c))
    if terminal(board):
        return None
    else:
        return actionsList
    
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    duplicate = copy.deepcopy(board)
    print(f"Player {player(board)}: {action}")
    if actions(board)==None or action==[]:
        raise Exception("There are not actions left. Try again.")
    elif action[0]>2 or action[1]>2:
        raise Exception("The attempted action is not permissable. Try again.")    
    i, j = action[0], action[1]
    duplicate[i][j] = player(board)
    print(f"Terminal state?: {terminal(duplicate)}")
    print_board(duplicate)
    return duplicate
    
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board == initial_state():
        return None
    '''
    Horizontal solution
    '''
    for r in range(len(board)):
        if board[r][0] == X and board[r][1] == X and board[r][2] == X:
            return X
        
        if board[r][0] == O and board[r][1] == O and board[r][2] == O:
            return O
    '''
    Vertical Solution
    '''
    for c in range(len(board[0])):
        if board[0][c] == X and board [1][c] == X and board[2][c] == X:
            return X
        
        if board[0][c] == O and board [1][c] == O and board[2][c] == O:
            return O
    '''
    Diagonal solutions
    '''
    # This may not work, may need to debug
    diagCheckX = 0
    diagCheckO = 0
    for r in range(len(board)):
        if board[r][r] == X:
            diagCheckX += 1   
            if diagCheckX == 3:
                return X
        if board[r][r] == O:
            diagCheckO += 1  
            if diagCheckO == 3:
                return O 
    '''
    Need to reset the variables counting how many are on the diagonal
    '''
    diagCheckX = 0
    diagCheckO = 0
    for r in range(len(board)):
        if board[r][2-r] == X:
            diagCheckX += 1
            if diagCheckX == 3:
                return X
        if board[r][2-r] == O:
            diagCheckO += 1
            if diagCheckO == 3:
                return O 
            

    '''No solution'''
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    t=0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c]==X or board[r][c]==O:
                t+=1
    if winner(board) is not None:
        return True
    elif t==9:
        return True
    
    else:
        return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    utility = -math.inf
    if winner(board)==X:
        utility = 1
    elif winner(board)==O:
        utility = -1
    elif winner(board)==None:
        utility = 0
        
    return utility
    raise NotImplementedError
    
    
def minfinder(board):
    '''
    Returns the value of a state based on whether or not it will lead to 
    a victory state for the player seeking to minimize utility
    (here predetermined as player O)
    
    Recursively calls upon maxfinder to determine the minimum utility of the 
    actions the max player could take
    
    Possible returns: -1, 0, 1
    '''
    if terminal(board) == True:
            return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxfinder(result(board, action)))
    
    return v
    raise NotImplementedError
    
def maxfinder(board):
    '''
    Returns the value of a state based on whether or not it will lead to 
    a victory state for the player seeking to maximize utility
    (here predetermined as player X)
    
    Recursively calls upon minfinder to determine the maximum utility of the 
    actions the min player could take
    
    Possible returns: -1, 0, 1
    '''
    if terminal(board) == True:
            return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minfinder(result(board, action)))
        
    return v
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    else:
        maxUtil=maxfinder(board)
        minUtil=minfinder(board)
        if player(board)==X:
            for action in actions(board):
                    if maxfinder(result(board, action)) == maxUtil:
                        return action
        if player(board)==O:
            for action in actions(board):
                    if minfinder(result(board, action)) == minUtil:
                        return action
            
                
                    
        # if action==[]:
        #     raise Exception("Minimax has failed, please debug")
    
    
    raise NotImplementedError
