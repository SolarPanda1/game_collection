import pygame
pygame.init()
golden = (1 + 5 ** 0.5) / 2

class Board:
    def __init__(self, axis, pixelSize):
        self.axis = axis
        self.pixelSize = pixelSize

    def draw(self):
        '''
        :param pixelSize: size of each point
        :return: None
        '''
        if self.pixelSize == 1:
            f = [i * self.pixelSize * self.axis / 400 - self.axis for i in range(800)]
            g = [self.axis - j * self.pixelSize * self.axis / 400 for j in range(800)]

            for a, x in enumerate(f):
                for b, y in enumerate(g):
                    if julia(complex(x,y), quadraticPolynomial, 2):
                        screen.set_at((a, b), RED)
        else:
            f = [i * self.pixelSize * self.axis / 400 - self.axis for i in range(int(800 / self.pixelSize))]
            g = [self.axis - j * self.pixelSize * self.axis / 400 for j in range(int(800 / self.pixelSize))]

            for a, x in enumerate(f):
                for b, y in enumerate(g):
                    if julia(complex(x,y), quadraticPolynomial, 2):
                        pygame.draw.rect(screen, RED, (a * self.pixelSize, b * self.pixelSize, self.pixelSize,
                                                       self.pixelSize))

def mandelbrot(num, c):
    for i in range(80):
        num = num**2 + c
        if abs(num) > 2:
            return False
    return True


def quadraticPolynomial(arg):
    return arg**2 + 1 - golden


def julia(z, func, bound):
    for i in range(80):
        z = func(z)
        if abs(z) > bound:
            return False
    return True


'''
Failed code
board = []
for i in range(400):
    board.append([])
    for j in range(400):
        board[i].append([i/100 - 2, 2 - j/100])
'''

# -------- Main Program Loop -----------
if __name__ == "__main__":
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    mainClock = pygame.time.Clock()

    board = Board(axis = 2, pixelSize= 1)
    board.draw()
    pygame.display.flip()
    while True:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        mainClock.tick(40)

