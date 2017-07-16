# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 17:12:53 2017

@author: Mauro
"""

#==============================================================================
# # Imports
#==============================================================================

from tkinter import (Tk, Label, Frame, Button, PhotoImage, Menu, StringVar, 
                     Toplevel)
from random import choice

#==============================================================================
# # AI
#==============================================================================

class AI:
    ''' Small random based AI that plays after the player'''
    
    def __init__(self, cellboard, gl):
        ''' the AI requires to know the game logic and the access to <press>
        the required cell in the game
        '''
        
        self.cellboard = cellboard
        self.gl = gl
    
    def check_board(self, coords):
        ''' Retrive the next possible cells, returns a list of cells '''
        bix, smx = divmod(coords[0], 3)
        biy, smy = divmod(coords[1], 3)    
        possibilities = []         
        # if the next square is full, gather all non occupied cells
        if self.gl.board.get_big_cell_bc(smx, smy).isfull():
            for cell in self.cellboard.cell_matrix:
                # check for every cell if is still unoccupied
                if self.gl.board.get_cell(cell.coords[0],cell.coords[1]).value is None:
                    possibilities.append(cell)
        else:
            # gather the next non full big cell and append the free cells
            bc = self.cellboard.get_big_cell_bc(smx, smy) 
            for cell in bc:
                if self.gl.board.get_cell(cell.coords[0],cell.coords[1]).value is None:
                    possibilities.append(cell)
        return possibilities
        
    def make_move(self, coord):
        ''' given the free cells, chose one option randomly'''
        p = self.check_board(coord)
        c = choice(p)
        # simulates the player button press
        c.press()

#==============================================================================
# # Helper functions
#==============================================================================

def check_values(cells):
    ''' checks if the cells have been filled by the same player
    returns True if all cells have the same value.
    '''
    first_element = cells[0].value
    
    # if the first element is None means that either they are all None or have
    # different values
    if first_element is None:
        return False
    # if the value is not None, check the other values, if the value is
    # different from the first return False
    for cell in cells:
        if cell.value != first_element:
            return False
    # this means all the elements are not None and the same
    return True


def check_win(get_func, matrix):
    ''' The function checks rows, columns and diagonals for a win 
    (three same glyphs)
    get_func: is a cell getter depending on the 
              matrix of class SmallCell or BigCell
    matrix: is the matrix containing the cells
    '''
    # checks rows
    row = []
    for i in range(3):
        for j in range(3):
            row.append(get_func(i, j))
        if check_values(row):
            return row[0].value
        row =[]
    
    # check columns
    col = []    
    for j in range(3):
        for i in range(3):
            col.append(get_func(i, j))
        if check_values(col):
            return col[0].value
        col =[]
        
    # check the diagonals
    diag_idx = [(0,0), (1,1), (2,2)]
    diag = []
    for idx in diag_idx:
        diag.append(get_func(idx[0],idx[1]))
    
    if check_values(diag):
        return  diag[0].value  

    diag_idx = [(0,2), (1,1), (2,0)]
    diag = []
    for idx in diag_idx:
        diag.append(get_func(idx[0],idx[1]))
    
    if check_values(diag):
        return  diag[0].value    
    
    # return 2 if the game is tie, the routine just checks if the board is full
    # since the winning options where excluded before
    board_full = True
    for cell in matrix:
        if cell.value is None:
            board_full = False
            break
    if board_full:
        return 2

#==============================================================================
# # Game cell definition
#==============================================================================

class SmallCell:
    ''' This class stores the player value '''
    
    def __init__(self):
        self.value = None
    
    def set_value(self, player):
        if player == 1:
            self.value = 1
        else:
            self.value = 0

class BigCell:
    '''This class stores a matrix of SmallCell representing a Tic Tac Toe'''
    
    rows = 3
    cols = 3
    
    def __init__(self):
        self.value = None        
        self.cell_matrix = []
        
        # Initializate the matrix containing the small cells        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell_matrix.append(SmallCell())
    
    def get_cell(self, x, y):
        idx = x * self.rows + y
        return self.cell_matrix[idx]
    
    def set_cell(self, x, y, player):
        idx = x * self.rows + y
        self.cell_matrix[idx].set_value(player)
    
    def check_win(self):
        return check_win(self.get_cell, self.cell_matrix)
    
    def isfull(self):
        ''' returns true if all the value are either 0 or 1 '''
        cells = [False if cell.value is None else True for cell in self.cell_matrix]
        return all(cells)

class Board:
    ''' This is the game board, containg 3x3 big cells'''
    
    rows = 3
    cols = 3
    
    def __init__(self):       
        self.cell_matrix = []
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell_matrix.append(BigCell())  
    
    def get_board_coords_sc(self, x, y):
        ''' from the coordinates of the board gets the coordinates of big cell
        and small cells
        '''
        bix, smx = divmod(x, self.rows)
        biy, smy = divmod(y, self.cols)

        return (bix, biy, smx, smy)        
    
    def set_cell(self, x, y, player):
        ''' set the cell value with the board coordinates'''
        bix, biy, smx, smy = self.get_board_coords_sc(x, y)
        self.cell_matrix[bix *self.cols + biy].set_cell(smx, smy, player)
    
    def get_cell(self, x, y):
        bix, biy, smx, smy = self.get_board_coords_sc(x, y)
        return self.cell_matrix[bix *self.cols + biy].get_cell(smx, smy)        
        
    def check_win(self, x, y):
        bix, biy, smx, smy = self.get_board_coords_sc(x, y)
        return self.cell_matrix[bix *self.cols + biy].check_win()

    def set_big_cell(self, x, y, player):
        bix, biy, smx, smy = self.get_board_coords_sc(x, y)
        self.cell_matrix[bix *self.cols + biy].value = player
    
    def get_big_cell(self, x, y):
        ''' given small cell coordinates get the big cell'''
        bix, biy, smx, smy = self.get_board_coords_sc(x, y)
        return self.get_big_cell_bc(bix, biy)
    
    def get_big_cell_bc(self, bix, biy):
        ''' given the big cell coordinates, get the cell'''
        return self.cell_matrix[bix *self.cols + biy]
    
    def check_win_board(self):
        return check_win(self.get_big_cell_bc, self.cell_matrix)

#==============================================================================
# # Game Logic
#==============================================================================

class GameLogic:
    ''' Thi class manages how the players are initiated and chosen '''
    
    def __init__(self):
        # initialize the game board
        self.board = Board()
        
        # initialize the player
        self.player = 1
        self.turn = 0
    
    def next_player(self):
        self.player = self.turn % 2
        self.turn += 1

#==============================================================================
# # Graphics functions
#==============================================================================

class Cell:
    ''' this is the class that manages the real cell, any game logic should
    be delegated at the GameLogic class
    '''
    
    def __init__(self, frame, grid_position, coords, gl, images, cb, pi):
        # set up everything in a frame and gird it according to what 
        # CellBaoard says
        self.frame = Frame(frame)
        self.frame.grid(row = grid_position[0], column = grid_position[1])
        
        # the cell coordinates
        self.coords = coords        
        
        # this is the array containg the images is linked to the root
        self.images = images
        
        # create a button inside the frame representing one cell
        self.b = Button(self.frame, text = "-",
                        image = self.images["blank_glyph"],
                        relief = "groove", width = 50, height = 50,
                        command = self.press)
        self.b.pack()
        
        # game logic, cell board, player infos
        self.gl = gl
        self.cb = cb
        self.pi = pi
        
        # initialize the AI - change the AI to fit in the game logic
        # activate the press cell from the game logic.
        self.ai = AI(self.cb, self.gl)
    
    def press(self):
        ''' this function select the picture to assign to the button and
        checks if it's game end, moreover activates the AI
        '''
        
        # upload the according picture
        if gl.board.get_big_cell(self.coords[0], self.coords[1]).value is None:
            if self.gl.player == 1:  
                self.b.config(image = self.images["x_glyph"])
            else:
                self.b.config(image = self.images["o_glyph"])
        
        if gl.board.get_big_cell(self.coords[0], self.coords[1]).value == 1:
            if self.gl.player == 1:  
                self.b.config(image = self.images["x_blue_glyph"])
            else:
                self.b.config(image = self.images["o_blue_glyph"])
        
        if gl.board.get_big_cell(self.coords[0], self.coords[1]).value == 0:
            if self.gl.player == 1:  
                self.b.config(image = self.images["x_red_glyph"])
            else:
                self.b.config(image = self.images["o_red_glyph"])
        
        # set this button to nothing, even if pressed
        self.b["command"] = self.do_nothing    
        
        # set the cell value of the current player
        self.gl.board.set_cell(self.coords[0], self.coords[1], self.gl.player)
        
        # check for chance of winning or set the next possible big square
        if self.gl.board.get_big_cell(self.coords[0], self.coords[1]).value is None:
            # if the current BigCell doesn't have a winner
            win = self.gl.board.check_win(self.coords[0], self.coords[1])
            if win is None:
                # next player
                self.prepare_board()
                self.next_player()   
            else:
                # set the board value to win (0, 1, 2)
                self.gl.board.set_big_cell(self.coords[0], self.coords[1], win)
                
                #change the color of all cells according to winner
                self.cb.make_big_cell_color(self.coords[0], self.coords[1], self.gl.player)
                
                # check if all board win
                board_win = self.gl.board.check_win_board()
                winstr = ["Player 2 win", "Player 1 win", "Tie"]
                if board_win is not None:
                    print(winstr[win])
                    self.pi.set_win(win)
                    self.cb.make_all_inactives()
                    return
                    
                # next player
                self.prepare_board()
                self.next_player()
        else:
            # next player
            self.prepare_board()
            self.next_player()         
            
    def prepare_board(self):
        ''' this function prepares the next Big square'''
        bix, by, smx, smy = self.gl.board.get_board_coords_sc(self.coords[0], self.coords[1])
        if self.gl.board.get_big_cell_bc(smx, smy).isfull():
            self.cb.make_all_actives()
        else:
            self.cb.make_next_square_active(self.coords)        
        pass
    
    def next_player(self):
        ''' this function manages the next player action, by setting the new
        player and starting the AI
        '''
        self.gl.next_player() 
        self.pi.set_player(self.gl.player)
        if self.gl.player == 0:
            self.ai.make_move(self.coords)         

        
    def do_nothing(self):
        pass
    
    def make_active(self):
        self.b["state"] = "normal"
    
    def make_inactive(self):
        self.b["state"] = "disabled"
    
    def make_blue(self):
        ''' this function makes the cell background blue'''
        self.make_color("blue")

    def make_red(self):
        ''' this function makes the cell background blue'''
        self.make_color("red")  
    
    def make_color(self, color):
        ''' this function makes the background of the cells depending on color
        color = "red" | "blue". (could be player id instead of 1 or 0)
        '''
        if self.gl.board.get_cell(self.coords[0], self.coords[1]).value == 1:
            self.b.config(image = self.images["x_" + color + "_glyph"])
        elif self.gl.board.get_cell(self.coords[0], self.coords[1]).value == 0:
            self.b.config(image = self.images["o_" + color + "_glyph"])
        else:
            self.b.config(image = self.images["blank_" + color + "_glyph"])        
        

class CellBoard:
    ''' This class manages the list of Cell which are the graphic elements'''
    
    def __init__(self, frame, gl, images, pi):
        # grid the cell board as the 3rd element (row = 2)
        self.mainFrame = Frame(frame)
        
        # initialize the list that contains the cells
        self.cell_matrix = []
        
        rcount = 0 # true row counnt / different than the graphic row count
        ccount = 0 # true col counnt / different than the graphic col count
        
        for bj in range(3): # for big cell col
            for j in range(3): # for small cell col
                for bi in range(3): # for big row
                    if bi >= 1 and bi <= 2: 
                        #add a column separator 
                        separator = Frame(self.mainFrame, height=2, bd=1, relief="sunken")
                        separator.grid(row = rcount, column = ccount, padx=5, pady=5)
                        ccount += 1
                    for i in range(3):# for small row
                        # initialize a cell
                        self.cell_matrix.append(
                                Cell(self.mainFrame, 
                                     (rcount,ccount), # graphic coords
                                     (j + bj*3, i + bi*3), # game coords
                                     gl, # game logic
                                     images, # image list
                                     self, # the class itself
                                     pi # player indicator
                                     )
                                )
                        ccount += 1
                ccount = 0 # reset the columns
                rcount += 1
            if bj >= 0 and bj <= 2: 
               #add a row separator 
               separator = Frame(self.mainFrame, width=0 , height = 10, bd=3, relief="sunken")
               separator.grid(row = rcount, column = ccount, padx=5, pady=0)
               rcount += 1    
    
    def get_big_cell_bc(self, bigx, bigy):
        ''' get the cells of a big cell given its coordinates, as a list'''
        cellsofbig = []
        for i in range(3):
            for j in range(3):
                idxmatrix = bigx * 27 + i* 9 + bigy * 3 + j
                cellsofbig.append(self.cell_matrix[idxmatrix])
        return cellsofbig
    
    def make_big_cell_active(self, bigx, bigy):
        ''' make active all the cells of a big cell '''
        for i in range(3):
            for j in range(3):
                idxmatrix = bigx * 27 + i* 9 + bigy * 3 + j
                self.cell_matrix[idxmatrix].make_active()
                
    
    def make_big_cell_color(self, x, y, player):
        ''' change the backgroung of a big square given the x, y coordinates
        of a cell inside
        '''
        bix, smx = divmod(x, 3)
        biy, smy = divmod(y, 3)   
        
        for i in range(3):
            for j in range(3):
                idxmatrix = bix * 27 + i* 9 + biy * 3 + j
                if player == 1:
                    self.cell_matrix[idxmatrix].make_blue()  
                else:
                    self.cell_matrix[idxmatrix].make_red() 
                
    def make_next_square_active(self, coords):
        ''' given a cell coordinate calculates the next square'''
        self.make_all_inactives()
        
        bix, smx = divmod(coords[0], 3)
        biy, smy = divmod(coords[1], 3)   
        self.make_big_cell_active(smx, smy)
    
    def make_all_actives(self):
        for cell in self.cell_matrix:
            cell.make_active()

    def make_all_inactives(self):
        for cell in self.cell_matrix:
            cell.make_inactive()
    



class PlayerIndicator:
    '''create a label saying "player x" or "player o" depending on the player
    playing
    '''
    
    def __init__(self, frame, root):

        # the main frame, left grid positioning for later
        self.mainFrame = Frame(frame)
        
        # the images displayed near Player turn
        self.imageo = root.images["player_image_o"]
        self.imagex = root.images["player_image_x"]
        self.imageb = root.images["player_image_blank"]
        
        # label + PhotoImage
        self.str_label = StringVar()
        self.str_label.set("Trun for player: ")
        
        label = Label(self.mainFrame, textvariable = self.str_label)
        label.grid(row = 0, column = 0)
        
        self.imglabel = Label(self.mainFrame, image = self.imagex)
        self.imglabel.grid(row = 0, column = 1)
    
    def set_player(self, player):
        if player == 1:
            self.imglabel["image"] = self.imagex
        else:
            self.imglabel["image"] = self.imageo
    
    def set_win(self, win):
        if win == 0:
            self.str_label.set("WIN: ")
            self.imglabel["image"] = self.imageo
        if win == 1:
            self.str_label.set("WIN: ")
            self.imglabel["image"] = self.imagex
        if win == 2:
            self.str_label.set("TIE: ")
            self.imglabel["image"] = self.imageb    

def new_game():
    print("\n - new game -")
    ngl = GameLogic()
    
    npi = PlayerIndicator(root, root)
    npi.mainFrame.grid(row = 0, column = 0)
    ncb = CellBoard(root, ngl, root.images, npi)
    ncb.mainFrame.grid(row = 1, column = 0)
    

def help_cmd():
    top = Toplevel(root)
    
    l = Label(top, image = root.images["help_menu"])
    l.pack()
    
if __name__ == "__main__":
    print("Extended Tris")
    
    root = Tk()
    
    # create the images array
    root.images = {}
    root.images["blank_glyph"] = PhotoImage(file = "./data/blank_glyph.gif")   
    root.images["x_glyph"] = PhotoImage(file = "./data/x_glyph.gif")
    root.images["o_glyph"] = PhotoImage(file = "./data/o_glyph.gif")
    root.images["blank_blue_glyph"] = PhotoImage(file = "./data/blank_blue_glyph.gif") 
    root.images["x_blue_glyph"] = PhotoImage(file = "./data/x_blue_glyph.gif")
    root.images["o_blue_glyph"] = PhotoImage(file = "./data/o_blue_glyph.gif")
    root.images["blank_red_glyph"] = PhotoImage(file = "./data/blank_red_glyph.gif") 
    root.images["x_red_glyph"] = PhotoImage(file = "./data/x_red_glyph.gif")
    root.images["o_red_glyph"] = PhotoImage(file = "./data/o_red_glyph.gif")
    root.images["player_image_o"] = PhotoImage(file = "./data/o_player_glyph.gif")
    root.images["player_image_x"] = PhotoImage(file = "./data/x_player_glyph.gif")
    root.images["player_image_blank"] = PhotoImage(file = "./data/blank_player_glyph.gif")
    root.images["help_menu"] = PhotoImage(file = "./data/help_menu_res.gif")
    
    # Title to window
    root.wm_title("Extended Tris")

    #Initialize game
    gl = GameLogic()
    pi = PlayerIndicator(root, root)
    pi.mainFrame.grid(row = 0, column = 0)
    cb = CellBoard(root, gl, root.images, pi) 
    cb.mainFrame.grid(row = 1, column = 0)
    
    # Make the menu
    menubar = Menu(root)
    menubar.add_command(label="New Game (not working)", command = new_game )
    menubar.add_command(label="Help", command = help_cmd)
    menubar.add_command(label="Quit!", command=root.quit)    
    root.config(menu=menubar)
    
    # the classical main loop
    root.mainloop()