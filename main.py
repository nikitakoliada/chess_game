import pygame 
import chess

WIDTH = HEIGHT = 512
SQUARE_SIZE = WIDTH // 8 # 8 is dimension 8x8
PIECES_IMG = {}
DIM = 8

def load_images():
    for color in ('black', 'white'):
        for name in ('king', 'queen', 'rook', 'bishop', 'knight', 'pawn'):
            filename = f'images/{color}_{name}.png'
            PIECES_IMG[color + "_" + name] = pygame.transform.scale(pygame.image.load(filename), (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen, board):
    for row in range(DIM):
        for col in range(DIM):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = pygame.Color("gray") if (row + col) % 2 == 0 else pygame.Color("white")
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece != "empty":
                color = "black" if (row + col) % 2 == 0 else "white"
                screen.blit(PIECES_IMG[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



# def draw_pieces(screen, board):
#         for row in range(DIM):
#             for col in range(DIM):
                

#draw gamestate and resp for all graphics
def draw_gs(screen, game_state):
    draw_board(screen, game_state.board)
    # draw_pieces(screen, gs.board)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_state = chess.GameState()
    clock = pygame.time.Clock()
    load_images()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        draw_gs(screen, game_state)
        clock.tick(15)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()