"""
A Python module for the Othello game.
TODO:   An in-console implementation of the Othello/Reversi game for two players or one player vs computer. Keyboard-only control.

        Basic instructions: run play() to begin game, follow instructions on screen.

        Key functions:
            newGame         : creating a new game
            printBoard      : printing the game board
            loadGame        : loading an existing game from a text file called game.txt
            getValidMoves   : finding all valid moves for a player
            makeMove        : making a move on the board
            scoreBoard      : calculating game score
            suggestMove1    : suggesting best move for computer to make
            suggestMove2    : -//-, but more advanced
            play            : main function, running the game itself
            
        Globals:
            compMoveDelay   : integer, number of seconds for computer (suggestMove1) to wait before making its move.
            
Full name: Dmitrii Odintcov
"""

from copy import deepcopy # you may use this for copying a board

import time, re

global directions, charToNum, computerMoveDelay
directions = [(1,0),(1,1),(0,1),(-1,0),(-1,-1),(0,-1),(1,-1),(-1,1)]
charToNum = "abcdefgh"
compMoveDelay = 1

def newGame(player1,player2):
     """
     Returns a new instance of the game dictionary, with names of player 1 and 2 as arguments, and the standard Othello starting board.
     
     Arguments:
         player1: string
         player2: string
         
     Returns:
         game: dict
     """ 
     game = {
             'player1' : player1,
             'player2' : player2,
             'who' : 1,
             'board' : [[0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,2,1,0,0,0],
                        [0,0,0,1,2,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0]]
             }
     return game

# TODO: All the other functions of Tasks 2-12 go here.
# USE EXACTLY THE PROVIDED FUNCTION NAMES AND VARIABLES!
     
def printBoard(board):
    """
    Prints the Othello game board with boundaries and row/column names, and the positions of players 1 and 2 as X and O respectively.
    
    Arguments:
        board: list of lists
    
    Returns:
        None
    """    
    def cellEval(n):
        if (n==1):
            return 'X'
        elif (n==2):
            return 'O'
        else:
            return ' '
        
    divLine = ' +' + '-+'*8
    print(' |a|b|c|d|e|f|g|h|')
    print(divLine)
    
    for index, line in enumerate(board):
        print(str(index+1)+'|', end='')
        [list(map(lambda cell: print(cellEval(cell)+'|', end=''), line))]
        print()
    
    print(divLine)
    
    return

def strToIndex(s):
    """
    Converts a string describing a position on the board such as C4 to its tuple equivalent.
    
    Arguments:
        s: string
        
    Returns:
        None
    """
    s = str().join((re.findall("\w", s.lower())))
    row = re.findall("[1-8]", s)
    column = re.findall("[a-h]", s)
    
    if (len(s) == 2) and (len(row) == len(column) == 1):
        return((int(row[0])-1, charToNum.index(column[0])))
    else:
        raise ValueError()
        
    return
        
        
def indexToStr(tup):
    """
    Converts the board position coordinates as a tuple to a string with the respective column letter and row number, e.g. C4.
    
    Arguments:
        tup: tuple
        
    Return:
        --: string
    """
    return (charToNum[tup[1]] + str(tup[0]+1))
    
    
def loadGame():
    """
    Attempts to open a local game.txt file containing data of a previous game, and return the respective instance of the game dictionary.
    
    Returns:
        game: dict, the game data extracted
        
    Handles:
        ValueError()
    """
    
    try:
        f = open("game.txt", mode="rt", encoding="utf8")
    except FileNotFoundError:
        raise FileNotFoundError()
    
    try:
        data = f.read().splitlines()
        
        game = {
                 'player1' : data[0],
                 'player2' : data[1],
                 'who' : data[2],
                 'board' : [list(map(int, i.split(','))) for i in data[3:]]
                }
        
        if (
            type(game['player1']) == type(game['player2']) == type(game['who']) == str
            and
            0 not in (len(game['player1']), len(game['player2']), len(game['who']))
            and
            all (len(line) == len(game['board']) == 8 for line in game['board'])
            ):
            
            return game
        
        else:
            raise ValueError()
            
    except:
        raise ValueError()
        

def getLine(board, who, pos, dir):
    """
    Returns the coordinates of board positions lying on a straight line 
        from the supplied empty starting point 
        to the nearest (first-encountered) position under the supplied player's control, 
        in the supplied direction. 
    
    Arguments:
        board: list of lists,
        who: integer, the player id
        pos: tuple, the starting point
        dir: tuple, the straight line direction
        
    Returns:
        []: list, empty
        giveLine: list, the positions
    """
    dir = tuple(map(lambda x: int(x/abs(x)) if (x != 0) else 0, dir))
    giveLine = []
    
    while True:
        pos = tuple(map(sum, zip(pos, dir)))
        if ((-1 in pos) or (8 in pos)):
            return []
        elif (board[pos[0]][pos[1]] == 3-who):
            giveLine.append(pos)
        elif (board[pos[0]][pos[1]] == who):
            return giveLine
        else:
            return []
        

def getValidMoves(board, who):      
    """
    Returns a list of all valid moves for the supplied player on the suppled board.
    
    Arguments:
        board: list of lists,
        who: integer, the player id
        
    Returns:
        moves: list, the valid moves
        
    Handles:
        ValueError
    """
    def inverseGetLine(board, who, pos, dir):
        """
        Same functionality as getLine(), but starting from a position occupied by the supplied player, and ending on an empty position. 
    
        Arguments:
            board: list of lists,
            who: integer, the player id
            pos: tuple, starting the point
            dir: tuple, the straight line direction
            
        Returns:
            []: list, empty
            giveLine: list, the positions
        """
        dir = tuple(map(lambda x: int(x/abs(x)) if (x != 0) else 0, dir))
        lineCount = 0
        
        while True:
            pos = tuple(map(sum, zip(pos, dir)))
            if ((-1 in pos) or (8 in pos)):
                return []
            elif (board[pos[0]][pos[1]] == 3-who):
                lineCount += 1
            elif (lineCount > 0 and board[pos[0]][pos[1]] == 0):
                return pos
            else:
                return []
    
    moves=[]
    
    for row in range(0,7,1):
        if (board[row] != [0, 0, 0, 0, 0, 0, 0, 0]) and (who in board[row]):
            for column in range(0,7,1):
                if board[row][column] == who:
                    for dirct in directions:
                        moves.append(inverseGetLine(board, who, (row, column), dirct))
    
    #Clean up moves[]
    try:
        while True: moves.remove([])
    except ValueError:
        pass
    
    return list(set(moves))


def makeMove(board, move, who):
    
    """
    Makes supplied player's move to supplied board position, replacing valid enemy positions.
    
    Arguments:
        board: list of lists,
        move: tuple, position of move,
        who: integer, the player id
        
    Returns:
        board: list of lists, the new board
    """
    moves=[]
    
    for dirct in directions:
        moves.append(getLine(board, who, move, dirct))
       
    moves = sum(moves, 
                [move])

    for cell in (moves):
        if cell != []:
            board[cell[0]][cell[1]] = who    
    
    return board


def scoreBoard(board):
    """
    Evaluates the current score by calculating (number of player1's positions - player2's positions)
    
    Arguments:
        board, list of lists
        
    Returns:
        --: integer, the score
    """
    values = sum(board,[])
    return (values.count(1)-values.count(2))


def suggestMove1(board, who):
    """
    Suggests the best move for supplied player on the supplied board based on the potential score after the move.
    
    Arguments:
        board: list of lists,
        who: integer, the player id
    
    Returns:
        potentialMove: tuple, the best-scoring move
    """
    potentialScore = scoreBoard(board)
    potentialMove = ()
    
    validMoves = getValidMoves(board, who)
    
    for mvt in validMoves:
        tempBoard = deepcopy(board)
        newScore = scoreBoard(makeMove(tempBoard, mvt, who))
        if (((-1)**(who+1))*newScore + ((-1)**who)*potentialScore) >= 0:
            potentialScore = newScore
            potentialMove = mvt
            
    return potentialMove


def suggestMove2(board, who):
    """
    Suggests the best move for supplied player on the supplied board based on:
        1) Move value (wrt the goal of capturing a corner)
        2) Post-move mobility of players (maximising the potential number of valid moves for the supplied player, and minimising for the enemy)
        3) Post-move score
    
    Arguments:
        board: list of lists,
        who: integer, the player id
        
    Returns:
        potentialMove: tuple, the optimal move   
    """
    values = [[6,-5,5,3,3,5,-5,6],
              [-5,-6,-2,-1,-1,-2,-6,-5],
              [5,-2,4,2,2,4,-2,5],
              [3,-1,2,0,0,2,-1,3],
              [3,-1,2,0,0,2,-1,3],
              [5,-2,4,2,2,4,-2,5],
              [-5,-6,-2,-1,-1,-2,-6,-5],
              [6,-5,5,3,3,5,-5,6]]

    curBoard = deepcopy(board)
    potentialScore = scoreBoard(board) 
    validMoves = getValidMoves(board, who)
    
    def tryMove(board, move, who):
        """
        Makes supplied move  by the supplied player on a temporary copy of the supplied board.
        
        Arguments:
            board: list of lists
            move: tuple, the move to make
            who: integer, the player id
            
        Returns:
            tempBoard: list of lists, copy of the supplied board with the move made
        """
        tempBoard = deepcopy(board)
        makeMove(tempBoard, move, who)
        return tempBoard

    def evalMove(validMove): 
        """
        Evaluates the supplied move with respect to the goal of capturing a corner of the board.
        
        Arguments:
            validMove: tuple, the move to be evaluated
            
        Returns:
            validMove: list, contains the supplied move and its value
        """
        validMove = [validMove]
        validMove.append(values[validMove[0][0]][validMove[0][1]]) #Move value
        return validMove
    
    def mobility(validMove):
        """
        Calculates the post-move (mobility of the current player - the mobility of the other player) for the supplied list containing a move and its value - after evalMove().
        
        Arguments:
            validMove: list, the move and its value
            
        Returns:
            validMove: list, the move, its value, the post-move board, and the mobility change
        """
        validMove.append(tryMove(curBoard, validMove[0], who)) #Add would-be-board
        validMove.append(len(getValidMoves(validMove[2], who)) - 
                         len(getValidMoves(validMove[2], 3-who))) #Check mobility improvement or lack thereof
        return validMove
    
    def futureScore(validMove): 
        """
        Evaluates the score on the post-move board in the supplied list containing a move, its value, the post-move board, and the mobility change - after validMove().
    
        Arguments:
            validMove: tuple, the move
        
        Returns:
            potentialMove: list, the move, its value, the post-move board, the mobility change, and the score of the post-move board
        """
        validMove.append(((-1)**(who+1))*scoreBoard(validMove[2]) + ((-1)**who)*potentialScore) #Add would-be-score improvement
        return validMove
    
    approach = [[evalMove, 1], [mobility, 3], [futureScore, 4]]
    
    cycle = 0
    while (len(validMoves) > 1) and (cycle <= 2):
        func = approach[cycle][0]
        param = approach[cycle][1]
        
        validMoves[:] = map(func, validMoves) #Evaluate all valid moves
        validMoves.sort(key=lambda validMove: validMove[param], reverse=True) #Descending sort by move value
        validMoves = list(filter(lambda validMove: validMove[param]==validMoves[0][param], validMoves)) #Multiple moves of equal value
        cycle += 1
        
    if validMoves == []:
        return None
    elif type(validMoves[0]) == tuple:
        return validMoves[0]
    
    return validMoves[0][0]

# ------------------- Main function --------------------
def play():
    """
    Outputs the game greeting message, asks for player names, and prompts move inputs until the end of the game.
    """
    print("*"*65)
    print("***"+" "*8+"WELCOME TO DMITRII'S FABULOUS OTHELLO GAME!"+" "*8+"***")
    print("*"*65,"\n")
    print("Enter the players names, or 'C' to play against the computer. Enter 'L' to load a previously saved game.\n")
    # TODO: Game flow control starts here
    
    def myInput(string):
        """
        Normal input(), lowercased and capitalised.
        """
        while True:
            val = input(string).lower().capitalize()
            if val: break
        return val
     
    players = [myInput("Player 1: "), myInput("Player 2: ")]
     
    global game, board, who
    
    if 'L' in players:
        game = loadGame()
    else:
        game = newGame(*players)
    
    board = game['board'] #Quick names, for convenience
    who = int(game['who'])
    
    
    def playerToName(who, sign=0):
        """
        Converts the player id (1 or 2) to the respective player name.
        
        Arguments:
            who: integer, the player id
            sign=0: integer, 0 by default or 1, whether to also print out the player's position sign (X or O)
        """
        return (game['player'+str(who).strip()]  + sign*[' (X)',' (O)'][who - 1]).strip()
    
    skipped = False
    
    while True:
        printBoard(board)
        validMoves = getValidMoves(board, who)
        
        if validMoves == []:          
            if skipped:       
                score = scoreBoard(board)
                if score == 0:
                    print("Draw. Friendship wins!")
                else:
                    winner = int(1.5-0.5*(score/abs(score)))
                    print(playerToName(winner, 1)+
                          " wins with a score of "+
                          str(abs(score)))
                break
            
            print("No valid moves for " + playerToName(who, 1) + ", skipping")
            skipped = True
        else:
            if playerToName(who) == 'C':
                compMove = suggestMove1(board, who)
                print("Computer" + [' (X)',' (O)'][who - 1] + " moves to ", end='')
                time.sleep(abs(compMoveDelay)) # For that dramatic effect
                print(indexToStr(compMove))
                makeMove(board, compMove, who)
                
            else:
                playerMove = strToIndex(input(str(playerToName(who, 1)) + " moves to: "))
                makeMove(board, playerMove, who)
            
        who = 3 - who
        
    return

# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
    play()