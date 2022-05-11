from cmu_112_graphics import *
import random


def appStarted(app):
    app.label = "Tetris!"
    app.color = "orange"
    app.size = 0
    app.rows = gameDimensions()[0]
    app.cols = gameDimensions()[1]
    app.cellSize = gameDimensions()[2]
    app.margin = gameDimensions()[3]
    app.emptyColor = "blue"
    app.board = [([app.emptyColor] * app.cols) for row in range(app.rows)]
    app.isGameOver = False
    app.score = 0
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[True, True, True, True]]
    jPiece = [[True, False, False], [True, True, True]]
    lPiece = [[False, False, True], [True, True, True]]
    oPiece = [[True, True], [True, True]]
    sPiece = [[False, True, True], [True, True, False]]
    tPiece = [[False, True, False], [True, True, True]]
    zPiece = [[True, True, False], [False, True, True]]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.tetrisPieceColors = [
        "red",
        "yellow",
        "magenta",
        "pink",
        "cyan",
        "green",
        "orange",
    ]
    newFallingPiece(app)


def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)


def drawBoard(app, canvas):
    rows = gameDimensions()[0]
    cols = gameDimensions()[1]
    for row in range(rows):
        for col in range(cols):
            drawCell(app, canvas, row, col, app.board[row][col])


def cellCoords(margin, row, col, size):
    x0 = margin + (col * size)
    y0 = margin + (row * size)
    x1 = margin + ((1 + col) * size)
    y1 = margin + ((1 + row) * size)
    return (x0, y0, x1, y1)


def drawCell(app, canvas, row, col, color):
    x0, y0, x1, y1 = cellCoords(app.margin, row, col, app.cellSize)
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=4)


def newFallingPiece(app):
    """
    It creates a new falling piece by randomly selecting one of the pieces in the `tetrisPieces` list,
    and then setting the `fallingPiece` variable to that piece, the `fallingPieceColor` variable to the
    corresponding color, the `fallingPieceRow` variable to 0, the `fallingPieceCol` variable to the
    middle of the board minus half the width of the piece, the `fallingPieceRows` variable to the number
    of rows in the piece, and the `fallingPieceCols` variable to the number of columns in the piece
    
    :param app: the app object
    """
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow = 0
    app.fallingPieceCol = app.cols // 2 - len(app.fallingPiece[0]) // 2
    app.fallingPieceRows = len(app.fallingPiece)
    app.fallingPieceCols = len(app.fallingPiece[0])


def drawFallingPiece(app, canvas):
    """
    For each row and column in the falling piece, if the cell is True, draw the cell.
    
    :param app: the app object
    :param canvas: the canvas to draw on
    """
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col] == True:
                drawCell(
                    app,
                    canvas,
                    app.fallingPieceRow + row,
                    app.fallingPieceCol + col,
                    app.fallingPieceColor,
                )


def fallingPieceIsLegal(app):
    """
    If the falling piece is outside the board or if it overlaps with a non-empty cell, then the falling
    piece is not legal
    
    :param app: the TetrisApp object
    :return: a boolean value.
    """
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[0])):
            if app.fallingPiece[i][j] == True:
                row = int(app.fallingPieceRow + i)
                col = int(app.fallingPieceCol + j)
                if row < 0 or row >= app.rows or col < 0 or col >= app.cols:
                    return False
                if app.board[row][col] != app.emptyColor:
                    return False
    return True


def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    return True


def rotateFallingPiece(app):
    """
    The above function rotates the falling piece by 90 degrees clockwise
    
    :param app: the app object
    :return: the new piece, the new number of rows and columns, and the new row and column.
    """
    oldPiece = app.fallingPiece
    oldRows, oldCols = app.fallingPieceRows, app.fallingPieceCols
    oldy, oldx = app.fallingPieceRow, app.fallingPieceCol
    newNumRows, newNumCols = oldCols, oldRows
    newlst = [([None] * newNumCols) for row in range(newNumRows)]
    for i in range(oldRows):
        for j in range(oldCols):
            newlst[oldCols - 1 - j][i] = oldPiece[i][j]

    newRow = oldy + oldRows // 2 - newNumRows // 2
    newCol = oldx + oldCols // 2 - newNumCols // 2
    app.fallingPieceRow = newRow
    app.fallingPieceCol = newCol
    app.fallingPiece = newlst
    app.fallingPieceRows = newNumRows
    app.fallingPieceCols = newNumCols

    if not fallingPieceIsLegal(app):
        app.fallingPiece = oldPiece
        app.fallingPieceRows = oldRows
        app.fallingPieceCols = oldCols
        app.fallingPieceRow = oldy
        app.fallingPieceCol = oldx
    return


def placeFallingPiece(app):
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[0])):
            if app.fallingPiece[i][j] == True:
                row = i + app.fallingPieceRow
                col = j + app.fallingPieceCol
                app.board[row][col] = app.fallingPieceColor
    removeFullRows(app)


def keyPressed(app, event):
    """
    If the game is over, and the user presses the "r" key, then the game restarts. 
    If the game is not over, and the user presses the "r" key, then the game restarts. 
    If the user presses the "Left" key, then the falling piece moves left. 
    If the user presses the "Right" key, then the falling piece moves right. 
    If the user presses the "Down" key, then the falling piece moves down. 
    If the user presses the "Up" key, then the falling piece rotates. 
    If the user presses the "Space" key, then the falling piece moves down until it hits the bottom.
    
    :param app: the TetrisApp object
    :param event: the event object
    :return: the value of the variable "app.isGameOver"
    """
    if app.isGameOver:
        if event.key == "r":
            appStarted(app)
        return
    if event.key == "r":
        appStarted(app)
    if event.key == "Left":
        moveFallingPiece(app, 0, -1)
    if event.key == "Right":
        moveFallingPiece(app, 0, 1)
    if event.key == "Down":
        moveFallingPiece(app, 1, 0)
    if event.key == "Up":
        rotateFallingPiece(app)
    if event.key == "Space":
        while fallingPieceIsLegal(app):
            if moveFallingPiece(app, 1, 0) == False:
                placeFallingPiece(app)
                break
            moveFallingPiece(app, 1, 0)


def timerFired(app):
    """
    If the game is over, do nothing. Otherwise, increase the size of the falling piece by 10 pixels, and
    if the falling piece can't move down, place it, and create a new falling piece. If the new falling
    piece is not legal, end the game
    
    :param app: the TetrisApp object
    :return: the value of the function moveFallingPiece.
    """
    if app.isGameOver == True:
        return
    app.size += 10
    if not moveFallingPiece(app, 1, 0):
        placeFallingPiece(app)
        newFallingPiece(app)
    if not fallingPieceIsLegal(app):
        app.isGameOver = True


def isFullRow(app, row):
    for e in row:
        if e == app.emptyColor:
            return False
    return True


def removeFullRows(app):
    """
    It removes full rows from the board and adds empty rows to the top of the board
    
    :param app: the TetrisApp object
    """
    emptyRow = [app.emptyColor] * len(app.board[0])
    rowsRemoved = 0
    for row in range(len(app.board)):
        if isFullRow(app, app.board[row]):  # reconstruct current board
            app.board.remove(app.board[row])
            app.board.insert(0, emptyRow)
            rowsRemoved += 1
    app.score += rowsRemoved**2


def drawScore(app, canvas):
    canvas.create_text(
        app.width / 2,
        app.margin / 2,
        text="Score: " + str(app.score),
        font="Helvetica 15 bold",
        fill="white",
    )


def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="orange")
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    if app.isGameOver:
        canvas.create_text(
            app.width / 2,
            app.height / 2,
            text="GAME OVER",
            font="Helvetica 20 bold",
            fill="white",
        )
        canvas.create_text(
            app.width / 2,
            app.height - app.margin / 2,
            text="Press r key to restart :D",
            font="Helvetica 10 bold",
            fill="white",
        )


def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    width = (cols * cellSize) + (2 * margin)
    height = (rows * cellSize) + (2 * margin)
    runApp(width=width, height=height)


playTetris()
