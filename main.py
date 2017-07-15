# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 17:12:53 2017

@author: Mauro
"""

from tkinter import Tk, Label, Frame, Button, PhotoImage, Menu, StringVar, Toplevel

from random import choice
import sys, os

class AI:
    
    def __init__(self, cellboard, gl):
        self.cellboard = cellboard
        self.gl = gl
    
    def check_board(self, coords):
        bix, smx = divmod(coords[0], 3)
        biy, smy = divmod(coords[1], 3)    
        possibilities = []         
        if self.gl.board.get_big_cell_bc(smx, smy).isfull():
            # get all non occupied cells
            for cell in self.cellboard.cell_matrix:
                if self.gl.board.get_cell(cell.coords[0],cell.coords[1]).value is None:
                    possibilities.append(cell)
        else:
            bc = self.cellboard.get_big_cell_bc(smx, smy) 
            for cell in bc:
                if self.gl.board.get_cell(cell.coords[0],cell.coords[1]).value is None:
                    possibilities.append(cell)
        return possibilities
        
    def make_move(self, coord):
        # chose random from the list
        p = self.check_board(coord)
        c = choice(p)
        c.press()

def check_values(l):
    first_element = l[0].value
    if first_element is None:
        return False
    for cell in l:
        if cell.value != first_element:
            return False
    return True


def check_win(get_func, matrix):
    print("Checking win..")
    row = []
    col = []
    
    
    print("checking rows")
    for i in range(3):
        for j in range(3):
            row.append(get_func(i, j))
        if check_values(row):
            return row[0].value
        row =[]
        
    print("checking columns")
    for j in range(3):
        for i in range(3):
            col.append(get_func(i, j))
        if check_values(col):
            return col[0].value
        col =[]
        
    print("checking diags")
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
    
    # return 2 if the game is tie
    board_full = True
    print("checking ties")
    for cell in matrix:
        if cell.value is None:
            board_full = False
            break
    if board_full:
        return 2

class SmallCell:
    
    def __init__(self):
        self.value = None
    
    def set_value(self, player):
        if player == 1:
            self.value = 1
        else:
            self.value = 0

class BigCell:
    
    def __init__(self):
        
        self.rows = 3
        self.cols = 3
        
        self.value = None
        
        self.cell_matrix = []
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell_matrix.append(SmallCell())
    
    def set_value(self, x, y, player):
        idx = x * self.rows + y
        self.cell_matrix[idx].value
    
    def get_cell(self, x, y):
        idx = x * self.rows + y
        return self.cell_matrix[idx]
    
    def set_cell(self, x, y, player):
        idx = x * self.rows + y
        self.cell_matrix[idx].set_value(player)
    
    def check_win(self):
        return check_win(self.get_cell, self.cell_matrix)
    
    def isfull(self):
        # returns true if all the value are either 0 or 1
        cells = [False if cell.value is None else True for cell in self.cell_matrix ]
        return all(cells)
            
            
    

class Board:
    
    def __init__(self):
        print(" init board ")
        self.rows = 3
        self.cols = 3
        
        self.cell_matrix = []

        for i in range(self.rows):
            for j in range(self.cols):
                self.cell_matrix.append(BigCell())  
    
    
    def set_cell(self, x, y, player):
        bix, smx = divmod(x, 3)
        biy, smy = divmod(y, 3)
        
        self.cell_matrix[bix *self.cols + biy].set_cell(smx, smy, player)
    
    def get_cell(self, x, y):
        bix, smx = divmod(x, 3)
        biy, smy = divmod(y, 3)
                
        return self.cell_matrix[bix *self.cols + biy].get_cell(smx, smy)        
        
    def check_win(self, x, y):
        bix, smx = divmod(x, 3)
        biy, smy = divmod(y, 3)    
        
        return self.cell_matrix[bix *self.cols + biy].check_win()

    def set_big_cell(self, x, y, player):
        bix, smx = divmod(x, 3)
        biy, smy = divmod(y, 3) 
        
        self.cell_matrix[bix *self.cols + biy].value = player
    
    def get_big_cell(self, x, y):
        bix, smx = divmod(x, 3)
        biy, smy = divmod(y, 3) 
        
        return self.cell_matrix[bix *self.cols + biy]
    
    def get_big_cell_bc(self, bix, biy):
        return self.cell_matrix[bix *self.cols + biy]
    
    def check_win_board(self):
        return check_win(self.get_big_cell_bc, self.cell_matrix)

class GameLogic:
    
    def __init__(self):

        
        self.board = Board()
        
        self.player = 1
        self.turn = 0
    
    def win(self, pos):
        # set the cell value = player
        
        
        # check for the win
        win = self.board.check_win(pos[0], pos[1])
        
        if win is not None:
            return win
        else:
            None
    
    def next_player(self):
        self.player = self.turn % 2
        
        print("Turn for player:", self.player)
        self.turn += 1
    
    def set_big_cell(self, x, y, player):
        self.board.set_big_cell(x, y, player)


class Cell:
    
    def __init__(self, frame, grid_position, coords, gl, images, cb, pi):
        self.frame = Frame(frame)
        self.frame.grid(row = grid_position[0], column = grid_position[1])
        
        self.coords = coords        

        self.images = images
            
        self.b = Button(self.frame, text = "-", image = self.images["blank_glyph"], relief = "groove", width = 50, height = 50, command = self.press)
        self.b.pack()
        
        self.gl = gl
        self.cb = cb
        self.pi = pi
        
        self.ai = AI(self.cb, self.gl)
    
    def press(self):
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
        
        self.b["command"] = self.do_nothing    
        
        self.gl.board.set_cell(self.coords[0], self.coords[1], self.gl.player)
        
        print("\n - Button is pressed - ")
        if self.gl.board.get_big_cell(self.coords[0], self.coords[1]).value is None:
            print("Nobody has won yet in this cell")
            win = self.gl.win(self.coords)
            if win is None:
                
                bix, smx = divmod(self.coords[0], 3)
                biy, smy = divmod(self.coords[1], 3)    
                print("next quadrant is:", smx, smy)
                print("is next quadrant full?", self.gl.board.get_big_cell_bc(smx, smy).isfull())
                if self.gl.board.get_big_cell_bc(smx, smy).isfull():
                    self.cb.make_all_actives()
                else:
                    self.cb.make_inactives(self.coords)
                # display inactives
                self.gl.next_player()
                self.pi.set_player(self.gl.player)
                if self.gl.player == 0:
                    self.ai.make_move(self.coords)
                
            else:
                print("Somebody won:", win)
                # set the board value to win
                self.gl.set_big_cell(self.coords[0], self.coords[1], win)
                self.cb.make_big_cell_color(self.coords[0], self.coords[1], self.gl.player)
                
                # check if all board win
                win = self.gl.board.check_win_board()
                if win == 1:
                    print("player 1 win")
                    self.pi.set_win(win)
                    self.cb.make_all_inactives()
                    return
                elif win == 0:
                    print("player 2 win")
                    self.pi.set_win(win)
                    self.cb.make_all_inactives()
                    return
                elif win == 2:
                    print("Tie")
                    self.pi.set_win(win)
                    self.cb.make_all_inactives()
                    return
                    
                # next player
                bix, smx = divmod(self.coords[0], 3)
                biy, smy = divmod(self.coords[1], 3)             
                if self.gl.board.get_big_cell_bc(smx, smy).isfull():
                    self.cb.make_all_actives()
                else:
                    self.cb.make_inactives(self.coords)
                self.gl.next_player() 
                self.pi.set_player(self.gl.player)
                if self.gl.player == 0:
                    self.ai.make_move(self.coords)
            
        else:
            print("somebody has won in this quadrant")
            # get next cell 
            bix, smx = divmod(self.coords[0], 3)
            biy, smy = divmod(self.coords[1], 3)             
            if self.gl.board.get_big_cell_bc(smx, smy).isfull():
                self.cb.make_all_actives()
            else:
                self.cb.make_inactives(self.coords)
            
            # display inactives
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
        
        if self.gl.board.get_cell(self.coords[0], self.coords[1]).value == 1:
            self.b.config(image = self.images["x_blue_glyph"])
        elif self.gl.board.get_cell(self.coords[0], self.coords[1]).value == 0:
            self.b.config(image = self.images["o_blue_glyph"])
        else:
            self.b.config(image = self.images["blank_blue_glyph"])

    def make_red(self):
        
        if self.gl.board.get_cell(self.coords[0], self.coords[1]).value == 1:
            self.b.config(image = self.images["x_red_glyph"])
        elif self.gl.board.get_cell(self.coords[0], self.coords[1]).value == 0:
            self.b.config(image = self.images["o_red_glyph"])
        else:
            self.b.config(image = self.images["blank_red_glyph"])        
        

class CellBoard:
    
    def __init__(self, frame, gl, images, pi):
        self.mainFrame = Frame(frame)
        self.mainFrame.grid(row = 2, column = 0)
        
        self.cell_matrix = []
        
        
        rcount = 0
        ccount = 0
        for bj in range(3):
            for j in range(3):
                
                for bi in range(3):
                    if bi >= 1 and bi <= 2:
                        #add a separator 
                        separator = Frame(self.mainFrame, height=2, bd=1, relief="sunken")
                        separator.grid(row = rcount, column = ccount, padx=5, pady=5)
                        ccount += 1
                    for i in range(3):
                        self.cell_matrix.append(
                                Cell(self.mainFrame,
                                     (rcount,ccount), 
                                     (j + bj*3, i + bi*3),
                                     gl,
                                     images,
                                     self, 
                                     pi
                                     )
                                )

                        ccount += 1
                ccount = 0
                rcount += 1
            if bj >= 0 and bj <= 2:
               #add a separator 
               separator = Frame(self.mainFrame, width=0 , height = 10, bd=3, relief="sunken")
               separator.grid(row = rcount, column = ccount, padx=5, pady=0)
               rcount += 1    
    
    def get_big_cell_bc(self, bigx, bigy):
        cellsofbig = []
        for i in range(3):
            for j in range(3):
                idxmatrix = bigx * 27 + i* 9 + bigy * 3 + j
                cellsofbig.append(self.cell_matrix[idxmatrix])
        return cellsofbig
    
    def make_big_cell_active(self, bigx, bigy):
        for i in range(3):
            for j in range(3):
                idxmatrix = bigx * 27 + i* 9 + bigy * 3 + j
                self.cell_matrix[idxmatrix].make_active()
                
    
    def make_big_cell_color(self, x, y, player):
        bix, smx = divmod(x, 3)
        biy, smy = divmod(y, 3)   
        
        for i in range(3):
            for j in range(3):
                idxmatrix = bix * 27 + i* 9 + biy * 3 + j
                if player == 1:
                    self.cell_matrix[idxmatrix].make_blue()  
                else:
                    self.cell_matrix[idxmatrix].make_red() 
                
                
    
    def make_inactives(self, coords):
        #make inactive all the cells

        bix, smx = divmod(coords[0], 3)
        biy, smy = divmod(coords[1], 3) 
        
        
        
        for cell in self.cell_matrix:
            cell.make_inactive()
            
        self.make_big_cell_active(smx, smy)
    
    def make_all_actives(self):
        for cell in self.cell_matrix:
            cell.make_active()

    def make_all_inactives(self):
        for cell in self.cell_matrix:
            cell.make_inactive()
    

def new_game():
    print("\n - new game -")
    ngl = GameLogic()
    
    npi = PlayerIndicator(root, root)
    npi.mainFrame.grid(row = 1, column = 0)
    CellBoard(root, ngl, root.images, npi)
    

class PlayerIndicator:

    def __init__(self, frame, root):
        # create a label saying player x or player o depending on the player
        # playing
        
        self.mainFrame = Frame(frame)
        
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
        # cambia la stinga
        if player == 1:
            self.imglabel["image"] = self.imagex
        else:
            self.imglabel["image"] = self.imageo
        # cambia l'immagine
    
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
            
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        print(e)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def help_cmd():
    top = Toplevel(root)
    
    l = Label(top, image = root.images["help_menu"])
    l.pack()
    
 

if __name__ == "__main__":
    print("Hello World")
    
    root = Tk()
    root.images = {}
    root.images["blank_glyph"] = PhotoImage(file = resource_path("./data/blank_glyph.gif"))     
    root.images["x_glyph"] = PhotoImage(file = resource_path("./data/x_glyph.gif"))
    root.images["o_glyph"] = PhotoImage(file = resource_path("./data/o_glyph.gif"))  
    root.images["blank_blue_glyph"] = PhotoImage(file = resource_path("./data/blank_blue_glyph.gif"))     
    root.images["x_blue_glyph"] = PhotoImage(file = resource_path("./data/x_blue_glyph.gif"))
    root.images["o_blue_glyph"] = PhotoImage(file = resource_path("./data/o_blue_glyph.gif"))
    root.images["blank_red_glyph"] = PhotoImage(file = resource_path("./data/blank_red_glyph.gif"))     
    root.images["x_red_glyph"] = PhotoImage(file = resource_path("./data/x_red_glyph.gif"))
    root.images["o_red_glyph"] = PhotoImage(file = resource_path("./data/o_red_glyph.gif"))
    root.images["player_image_o"] = PhotoImage(file = resource_path("./data/o_player_glyph.gif"))
    root.images["player_image_x"] = PhotoImage(file = resource_path("./data/x_player_glyph.gif"))   
    root.images["player_image_blank"] = PhotoImage(file = resource_path("./data/blank_player_glyph.gif"))
    root.images["help_menu"] = PhotoImage(file = resource_path("./data/help_menu_res.gif"))
    
    root.wm_title("Extended Tris")
    
    title_label = Label(root, text = " - Extended Tris - ")
    title_label.grid(row = 0, column = 0)

    #mycb = CellBoard(root, gl, root.images)
    gl = GameLogic()
    pi = PlayerIndicator(root, root)
    pi.mainFrame.grid(row = 1, column = 0)
    CellBoard(root, gl, root.images, pi) 
    
    menubar = Menu(root)
    menubar.add_command(label="New Game (not working)", command = new_game )
    menubar.add_command(label="Help", command = help_cmd)
    menubar.add_command(label="Quit!", command=root.quit)    
    
    root.config(menu=menubar)
    
    
    
    root.mainloop()