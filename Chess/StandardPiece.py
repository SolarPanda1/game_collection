import pygame
import os
from movements2 import *
board = []
img_dir = os.path.join(os.path.dirname(__file__), 'images')

def get_square_color(place):
        return getattr(board[place], "color", None)

class Piece:
    def __init__(self, name, type, x, y, color, display, enemy, state=True):
        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.state = state
        self.color = color
        self.display = pygame.transform.scale(pygame.image.load(os.path.join(img_dir,display)), (50,50))
        self.enemy = enemy
    
    def __repr__(self):
        return self.color[0] + self.name

    def expand(self):
        self.display = pygame.transform.smoothscale(self.display, (60, 60))

    def shrink(self):
        self.display = pygame.transform.smoothscale(self.display, (50, 50))

    def move(self, destination):
        temp = [self.y, self.x]
        self.y, self.x = destination[0], destination[1]
        if getattr(board[destination], "color", None) == self.enemy.color:
            self.enemy.pieces.pop(board[destination].name)
        board[destination] = self
        board[temp] = 0
        self.state = False

    def remember_move(self, destination):
        initial_state = self.state
        initial_position = [self.y, self.x]
        self.y, self.x = destination[0], destination[1]
        if getattr(board[destination], "color", None) == self.enemy.color:
            name_of_eaten_piece = board[destination].name
            eaten = self.enemy.pieces.pop(board[destination].name)
        else:
            eaten, name_of_eaten_piece = 0, None
        board[destination] = self
        board[initial_position] = 0
        self.state = False
        return eaten, name_of_eaten_piece, initial_state, initial_position
    
    def restore_move(self, eaten, name_of_eaten_piece, initial_state, initial_position):
        self.state = initial_state
        if getattr(eaten, "color", None) == self.enemy.color:
            self.enemy.pieces[name_of_eaten_piece] = eaten
        board[self.y][self.x] = eaten
        self.y, self.x = initial_position[0], initial_position[1]
        board[initial_position] = self

    def valid_move_filter(self, place):
        if place[0] in range(8) and place[1] in range(8):
                target = board[place]
                condition1= hasattr(target, "color") and target.color != self.color
                condition2 = target == 0
                if condition1 or condition2:
                    return True
        return False


class Pawn(Piece):
    def __init__(self, name, x, y, color, display, enemy, state=True):
        super().__init__(name, 'pawn', x, y, color, display, enemy, state)

    def get_list_of_moves(self):
        # process to check square:
        # 1) First Square is empty: yield position
        # 2) First and second squares are empty and self.state == True:yield position
        # 3) Diagonal Square is empty or piece of diff color: yield position 

        temp = list(pawn_move(self))

        if 7 >= temp[0][0] >= 0 and 7 >= temp[0][1] >= 0:
            if get_square_color(temp[0]) == None:
                yield temp[0]
        if 7 >= temp[1][0] >= 0 and 7 >= temp[1][1] >= 0:
            if get_square_color(temp[1]) == self.enemy.color:
                yield temp[1]
        if 7 >= temp[2][0] >= 0 and 7 >= temp[2][1] >= 0:
            if get_square_color(temp[2]) == self.enemy.color:
                yield temp[2]
        if self.state:
            if 7 >= temp[3][0] >= 0 and 7 >= temp[3][1] >= 0:
                if get_square_color(temp[3]) == None:
                    yield temp[3]


class Rook(Piece):
    def __init__(self, name, x, y, color, display, enemy, state=True):
        super().__init__(name, 'rook', x, y, color, display, enemy, state)
    
    def get_list_of_moves(self):

        temp = rook_move(self)

        for position in temp:
            # process to check square:
            # 1) sqaure is out of bounds: send("BREAK")
            # 2) square has piece with same colour: send("BREAK")
            # 3) square is empty: yield position            
            # 4) sqaure has piece with different colour: yield position and send("BREAK")           
            #condition1 = position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0
            #condition2 = get_square_color(position) == self.color
            #condition3 = get_square_color(position) == None           
            #condition4 = not condition3 and not condition2
            if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
                try:
                    temp.send("BREAK")
                except StopIteration:
                    break
            elif get_square_color(position) == self.color:
                try:
                    temp.send("BREAK")
                except StopIteration:
                    break
            else:
                yield position
                if not get_square_color(position) == None :
                    try:
                        temp.send("BREAK")
                    except StopIteration:
                        break


class Bishop(Piece):
    def __init__(self, name, x, y, color, display, enemy, state=True):
        super().__init__(name, 'bishop', x, y, color, display, enemy, state)

    def get_list_of_moves(self):

        temp = bishop_move(self)

        for position in temp:
            if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
                try:
                    temp.send("BREAK")
                except StopIteration:
                    break
            elif get_square_color(position) == self.color:
                try:
                    temp.send("BREAK")
                except StopIteration:
                    break
            else:
                yield position
                if not get_square_color(position) == None :
                    try:
                        temp.send("BREAK")
                    except StopIteration:
                        break

        
class Queen(Piece):
    def __init__(self, name, x, y, color, display, enemy, state=True):
        super().__init__(name, 'queen', x, y, color, display, enemy, state)
    
    def get_list_of_moves(self):

        temp = queen_move(self)

        for position in temp:
            if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
                try:
                    temp.send("BREAK")
                except StopIteration:
                    break
            elif get_square_color(position) == self.color:
                try:
                    temp.send("BREAK")
                except StopIteration:
                    break
            else:
                yield position
                if not get_square_color(position) == None :
                    try:
                        temp.send("BREAK")
                    except StopIteration:
                        break


class Knight(Piece):
    def __init__(self, name, x, y, color, display, enemy, state=True):
        super().__init__(name, 'knight', x, y, color, display, enemy, state)

    def get_list_of_moves(self):
        temp = knight_move(self)
        for position in temp:
            if 7 >= position[0] >= 0 and 7 >= position[1] >= 0:
                if not get_square_color(position) == self.color:
                    yield position


class King(Piece):
    def __init__(self, name, x, y, color, display, enemy, state=True):
        super().__init__(name, 'king', x, y, color, display, enemy, state)

    def get_list_of_moves(self):
        temp = king_move(self)
        for position in temp:
            if 7 >= position[0] >= 0 and 7 >= position[1] >= 0:
                if not get_square_color(position) == self.color:
                    yield position
