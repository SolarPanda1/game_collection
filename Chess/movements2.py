# Gnenerators that generate all possible moves for each chess piece. Does not check if move is valid (if the destination 
# sqaure is within bounds, is occupied or not)
# A queen piece can move in 8 directions, but cannot move beyond a black or white piece. To stop the queen from checking 
# further in the same direction, use send("BREAK")

def pawn_move(self):
    if self.color == "white":
        e = -1
    else:
        e = 1
    yield (self.y + e, self.x)

    for i in [-1,1]:
        yield (self.y + e, self.x + i)
    
    if self.state: # if pawn has been moved, self.state = False
        yield (self.y + 2*e, self.x)



def king_move(self):
    for i in [-1, 1]:
        yield (self.y + i, self.x)
        yield (self.y , self.x + i)
    for i in [-1, 1]:
        for j in [-1, 1]:
            yield (self.y + i, self.x + j)

def rook_move(self):
    final_value = False
    for j in [0, 1]:
        for k in [range(-1, -8, -1), range(1, 8)]:
            for i in k:
                if final_value == True:
                    yield None
                    final_value = False               
                position = [self.y, self.x].copy()
                position[j] += i
                should_i_break = yield tuple(position)
                if should_i_break == "BREAK":
                    final_value = True
                    break

def bishop_move(self):
    final_value = False
    for a in [range(-1, -8, -1), range(1, 8)]:
        for b in [range(-1, -8, -1), range(1, 8)]:
            for c, d in zip(a, b):
                if final_value == True:
                    yield None
                    final_value = False
                position = [self.y, self.x].copy()
                position[0] += c
                position[1] += d
                should_i_break = yield tuple(position)
                if should_i_break == "BREAK":
                    final_value = True
                    break

def knight_move(self):  
    for i in [-2, 2, 1, -1]:
        for j in [x for x in [-2, 2, 1, -1] if abs(x) != abs(i)]:
            position = [self.y, self.x].copy()
            position[0] += j
            position[1] += i
            yield tuple(position)

def test():
    for i in range(1,10):
        print('{} from generator'.format(i))
        num = yield i
        print("num is {}". format(num))
        if num == 'BREAK':
            break
    yield None

def add_movements(*args):
    def new_func(piece):
        for i in args:
            final_value = False
            temp = i(piece)
            for moves in temp:
                if final_value:
                    yield None
                    final_value = False
                should_i_break = yield moves
                if should_i_break == 'BREAK':
                    final_value = True
                    try:
                        temp.send("BREAK")
                    except StopIteration:
                        break
    return new_func

#Custom moves below
queen_move = add_movements(bishop_move, rook_move)

# See how it works below
class _TEST_UNIT:
    pass
if __name__ == "__main__":
    piece = _TEST_UNIT()
    piece.x = 2
    piece.y = 6
    piece.state= True
    piece.color = 'white'
    queen = queen_move(piece)
    pawn = pawn_move(piece)
    rook = rook_move(piece)

    for i in queen:
        if i[0] > 7 or i[0] < 0 or i[1] > 7 or i[1] < 0:
            try:
                queen.send("BREAK")
            except StopIteration:
                break
        else:
            print(i)
    print(list(rook))