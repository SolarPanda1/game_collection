import pygame
from os import path
from copy import deepcopy
import StandardPiece as sp
img_dir = path.join(path.dirname(__file__), 'images')
pygame.init()
mainClock = pygame.time.Clock()
WINDOWWIDTH = 400
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Chess')
COLOR1 = (102, 51, 0)
COLOR2 = (204, 102, 0)
WHITE = (255,255,255)
BLACK = (0,0,0)
font1 = pygame.font.SysFont('comicsans', 30, True)
text_image = [None, 0]
FPS = 27


class Board(list):
    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            super().__init__(args[0])
        else:
            super().__init__(args)
    def copy(self):
        return deepcopy(self)
    def __getitem__(self, index):
        if type(index) == int:           
           return super().__getitem__(index)
        else:
            return super().__getitem__(index[0]).__getitem__(index[1])
    def __setitem__(self,key,value):
        super().__getitem__(key[0]).__setitem__(key[1], value)
    def pretty_print(self):
        for i in self:
            print(i)

class Color:
    def __init__(self, color1, turn):
        self.color = color1
        self.pieces = {}
        self.selection_phase = True
        self.destination_phase = False
        self.selected_piece = None
        self.destination = None
        self.turn = turn
        self.enemy = None
    
    def add_pieces(self, piece):
        self.pieces[piece.name] = piece

    def move(self, selection):
        selected_piece = board[selection]
        if self.selection_phase:
            if not isinstance(selected_piece, sp.Piece):
                print_text('No piece selected. Please reselect')
            elif getattr(selected_piece, "color") != self.color:
                print_text('Wrong color. Please reselect')
            else:
                if self.selected_piece is not None:
                    self.selected_piece.shrink()
                self.selected_piece = selected_piece
                self.selected_piece.expand()
                self.selection_phase = False
                self.destination_phase = True

        elif self.destination_phase:
            if getattr(selected_piece, "color", None) == self.color:
                if self.selected_piece is not None:
                    self.selected_piece.shrink()
                self.selected_piece = selected_piece
                self.selected_piece.expand()
            elif selection in self.selected_piece.get_list_of_moves():
                self.destination = selection
                self.selection_phase = True
                self.destination_phase = False
                self.selected_piece.move(self.destination)
                self.selected_piece.shrink()
                self.turn = False
                self.enemy.turn = True
            else:
                print_text("Invalid move")

    def checked(self):
        for j in self.enemy.pieces.values():
            if (self.pieces["king"].y, self.pieces["king"].x) in j.get_list_of_moves():
                return True
        return False
    
    def check_all_moves(self):
        #checks for all moves by all pieces, whether valid or not
        for piece in self.pieces.values():
            for possible_position in piece.get_list_of_moves():
                yield piece, possible_position

    def check_filter(self, piece, possible_position):
        #Returns true if move by a piece results in a check
        eaten, name_of_eaten_piece, initial_state, initial_position = piece.remember_move(possible_position)
        am_i_checked = self.checked()
        piece.restore_move(eaten, name_of_eaten_piece, initial_state, initial_position)
        return am_i_checked
        
    def checkmate(self):
        for piece, possible_position in self.check_all_moves():
            if not self.check_filter(piece, possible_position):          
                return False
        return True

# Graphics
def print_text(text):
    global text_image
    text_image[0] = font1.render(text, False, BLACK)
    text_image[1] = 0

def redrawGameWindow():
    global text_image
    windowSurface.fill(WHITE)
    for j in range(0, 350, 100):
        for i in range(0, 350, 100):
            pygame.draw.rect(windowSurface, COLOR1, (i, j, 50, 50))
            pygame.draw.rect(windowSurface, COLOR2, (i + 50, j, 50, 50))
    for j in range(50, 400, 100):
        for i in range(0, 350, 100):
            pygame.draw.rect(windowSurface, COLOR1, (i + 50, j, 50, 50))
            pygame.draw.rect(windowSurface, COLOR2, (i, j, 50, 50))
    for player in [black, white]:
        for piece in player.pieces.values():
            windowSurface.blit(piece.display, (piece.x * 50, piece.y * 50))
    if isinstance(text_image[0], pygame.Surface):
        if text_image[1] == 50:
            text_image = [None, 0]
        else:
            windowSurface.blit(text_image[0], (0, 400))
            text_image[1] += 1
    pygame.display.update()
    
board = Board([[0 for j in range(8)] for i in range(8)])
sp.board = board
black = Color("black", False)
white = Color("white", True)
black.enemy = white
white.enemy = black

for i in range(8):
    black.add_pieces(sp.Pawn("pawn"+str(i+1), i, 1, "black", "black-pawn.png", white))
    white.add_pieces(sp.Pawn("pawn"+str(i+1), i, 6, "white", "white-pawn.png", black))
for color, player, y, enemy in [['white', white, 7, black], ['black', black, 0, white]]:
    player.add_pieces(sp.King("king", 4, y, color, color + "-king.png", enemy))
    player.add_pieces(sp.Rook("rook1", 0, y, color, color + "-rook.png", enemy))
    player.add_pieces(sp.Rook("rook2", 7, y, color, color + "-rook.png", enemy))
    player.add_pieces(sp.Queen("queen", 3, y, color, color + "-queen.png", enemy))
    player.add_pieces(sp.Bishop("bishop1", 2, y, color, color + "-bishop.png", enemy))
    player.add_pieces(sp.Bishop("bishop2", 5, y, color, color + "-bishop.png", enemy))
    player.add_pieces(sp.Knight("knight1", 1, y, color, color + "-knight.png", enemy))
    player.add_pieces(sp.Knight("knight2", 6, y, color, color + "-knight.png", enemy))


for i in black.pieces.values():
    board[i.y][i.x] = i
for j in white.pieces.values():
    board[j.y][j.x] = j

while True:
    mainClock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if 0<mouse_position[0]<400 and 0<mouse_position[1]<400:
                selected_square = (mouse_position[1] // 50, mouse_position[0] // 50)
                if white.turn:
                    if not white.checkmate():
                        white.move(selected_square)
                    else:
                        print_text("Checkmate, black win")
                        white.turn, black.turn = False, False
                elif black.turn:
                    if not black.checkmate():
                        black.move(selected_square)
                    else:
                        print_text("Checkmate, white win")
                        white.turn, black.turn = False, False
    redrawGameWindow()
