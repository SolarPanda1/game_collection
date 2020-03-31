import pygame
from os import path
img_dir = path.join(path.dirname(__file__), 'images')
pygame.init()
mainClock = pygame.time.Clock()
WINDOWWIDTH = 400
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Chess')
run = True
COLOR1 = (102, 51, 0)
COLOR2 = (204, 102, 0)
WHITE = (255,255,255)
BLACK = (0,0,0)
font1 = pygame.font.SysFont('comicsans', 30, True)
text_image = None
FPS = 27

print()
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

    def add_pieces(self, name, type, x, y, state, display):
        piece = Piece(name, type, x, y, state, self.color, display)
        self.pieces[name] = piece

    def move(self, selection):
        selected_piece = board[selection[0]][selection[1]]
        if self.selection_phase:
            if not isinstance(selected_piece, Piece):
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
                self.selected_piece.move(self.destination, self.enemy)
                self.turn = False
                self.enemy.turn = True
            else:
                print_text("Invalid move")

    def checked(self):
        for j in self.enemy.pieces.values():
            if [self.pieces["king"].y, self.pieces["king"].x] in j.get_list_of_moves():
                return True
        return False


class Piece:
    def __init__(self, name, type, x, y, state, color, display):
        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.state = state
        self.color = color
        self.display = pygame.transform.scale(pygame.image.load(path.join(img_dir,display)), (50,50))

    def expand(self):
        self.display = pygame.transform.smoothscale(self.display, (60, 60))

    def shrink(self):
        self.display = pygame.transform.smoothscale(self.display, (50, 50))

    def move(self, destination, enemy):
        temp = [self.y, self.x]
        self.y, self.x = destination[0], destination[1]
        if getattr(board[destination[0]][destination[1]], "color", None) == enemy.color:
            enemy.pieces.pop(board[destination[0]][destination[1]].name)
        board[destination[0]][destination[1]] = self
        board[temp[0]][temp[1]] = 0
        self.shrink()
        self.state = False

    def get_list_of_moves(self):
        list_of_moves = []
        position = [self.y, self.x].copy()

        def get_square_color(place):
            return getattr(board[place[0]][place[1]], "color", None)

        def append_moves(piece, place):
            if place[0] in range(8) and place[1] in range(8):
                target = board[place[0]][place[1]]
                if hasattr(target, "color") and target.color != piece.color:
                    list_of_moves.append(place)
                elif target == 0:
                    list_of_moves.append(place)
            return [piece.y, piece.x].copy()

        if self.type == "pawn":
            if self.color == "white":
                e = -1
            else:
                e = 1
            if self.state:
                position[0] += 2*e
                position = append_moves(self, position)
            position[0] += e
            position = append_moves(self, position)
            for i in [-1,1]:
                position[0] += e
                position[1] += i
                if position[0] in range(8) and position[1] in range(8):
                    diagonal_target = board[position[0]][position[1]]
                    if hasattr(diagonal_target, "color") and diagonal_target.color != self.color:
                        list_of_moves.append(position)
                    position = [self.y, self.x].copy()

        if self.type == "king":
            for i in [-1, 1]:
                for j in [0, 1]:
                    position[j] += i
                    position = append_moves(self, position)
            for i in [-1, 1]:
                for j in [-1, 1]:
                    position[0] += j
                    position[1] += i
                    position = append_moves(self, position)
        if self.type == 'rook' or self.type == 'queen':
            for j in [0, 1]:
                for k in [range(-1, -8, -1), range(1, 8)]:
                    for i in k:
                        position[j] += i
                        if position[j] > 7 or position[j] < -7:
                            position = [self.y, self.x].copy()
                            break
                        if get_square_color([position[0], position[1]]) == self.color:
                            position = [self.y, self.x].copy()
                            break
                        append_moves(self, position)
                        if board[position[0]][position[1]] != 0:
                            position = [self.y, self.x].copy()
                            break
                        position = [self.y, self.x].copy()
        if self.type == 'bishop' or self.type == "queen":
            for a in [range(-1, -8, -1), range(1, 8)]:
                for b in [range(-1, -8, -1), range(1, 8)]:
                    for c, d in zip(a, b):
                        position[0] += c
                        if position[0] > 7 or position[0] < -7:
                            position = [self.y, self.x].copy()
                            break
                        position[1] += d
                        if position[1] > 7 or position[1] < -7:
                            position = [self.y, self.x].copy()
                            break
                        if get_square_color([position[0], position[1]]) == self.color:
                            position = [self.y, self.x].copy()
                            break
                        append_moves(self, position)
                        if board[position[0]][position[1]] != 0:
                            position = [self.y, self.x].copy()
                            break
                        position = [self.y, self.x].copy()
        if self.type == "knight":
            for i in [-2, 2, 1, -1]:
                for j in [x for x in [-2, 2, 1, -1] if abs(x) != abs(i)]:
                    position[0] += j
                    if position[0] > 7 or position[0] < -7:
                        position = [self.y, self.x].copy()
                        break
                    position[1] += i
                    if position[1] > 7 or position[1] < -7:
                        position = [self.y, self.x].copy()
                        break
                    append_moves(self, position)
                    position = [self.y, self.x].copy()
        return list_of_moves


def checkmate(n):
    list = n.pieces.values()
    for piece in list:
        for possible_position in piece.get_list_of_moves():
            temp = board[possible_position[0]][possible_position[1]]
            pos = [piece.y, piece.x]
            piece.y, piece.x = possible_position[0], possible_position[1]
            board[possible_position[0]][possible_position[1]] = piece
            board[pos[0]][pos[1]] = 0
            check = n.checked()
            if not check:
                board[possible_position[0]][possible_position[1]] = temp
                piece.y, piece.x = pos[0], pos[1]
                board[pos[0]][pos[1]] = piece
                return False
            board[possible_position[0]][possible_position[1]] = temp
            piece.y, piece.x = pos[0], pos[1]
            board[pos[0]][pos[1]] = piece
    return True

# Graphics
def print_text(text):
    global text_image
    text_image = font1.render(text, False, BLACK)


def redrawGameWindow():
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
    if isinstance(text_image, pygame.Surface):
        windowSurface.blit(text_image, (0, 400))
    pygame.display.update()


board = []
for i in range(8):
    board.append([])
    for j in range(8):
        board[i].append(0)

black = Color("black", False)
white = Color("white", True)
black.enemy = white
white.enemy = black

for i in range(8):
    black.add_pieces("pawn"+str(i+1), "pawn", i, 1, True, "b-pawn.png")
    white.add_pieces("pawn"+str(i+1), "pawn", i, 6, True, "w-pawn.png")
for x, y, z in [[white, 7, "w"], [black, 0, "b"]]:
    x.add_pieces("king", "king", 4, y, True, z + "-king.png")
    x.add_pieces("queen", "queen", 3, y, False, z + "-queen.png")
    x.add_pieces("bishop1", "bishop", 2, y, False, z + "-bishop.png")
    x.add_pieces("bishop2", "bishop", 5, y, False, z + "-bishop.png")
    x.add_pieces("rook1", "rook", 0, y, True, z + "-rook.png")
    x.add_pieces("rook2", "rook", 7, y, True, z + "-rook.png")
    x.add_pieces("knight1", "knight", 1, y, False, z + "-knight.png")
    x.add_pieces("knight2", "knight", 6, y, False, z + "-knight.png")

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
                selected_square = [mouse_position[1] // 50, mouse_position[0] // 50]
                if white.turn:
                    if not checkmate(white):
                        white.move(selected_square)
                    else:
                        print_text("Checkmate, black win")
                        white.turn, black.turn = False, False
                elif black.turn:
                    if not checkmate(black):
                        black.move(selected_square)
                    else:
                        print_text("Checkmate, white win")
                        white.turn, black.turn = False, False
    redrawGameWindow()
