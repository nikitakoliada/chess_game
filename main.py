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
    clock = pygame.time.Clock()
    square_sel = () # the square that user selected
    prev_sel = ()   
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_state = chess.GameState()
    #gets all possible valid moves
    valid_moves = game_state.get_valid_moves()
    #bool for regeneratint valid moves
    move_made = False
    load_images()
    running = True
    while running:
        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #gets the col and row of the figure
                loc = pygame.mouse.get_pos()
                col = loc[0]//SQUARE_SIZE
                row = loc[1]//SQUARE_SIZE
                if square_sel == (row, col):
                    square_sel = () # desselect the
                    prev_sel = ()
                    #TODO light the square up
                else:
                    
                    if len(square_sel) != 0:
                        #if we are ready to move 
                        prev_sel = square_sel
                        square_sel = (row, col)
                        #makes move
                        move = chess.Move(prev_sel , square_sel,  game_state.board)
                        print(prev_sel + square_sel)
                        if move in valid_moves:
                            game_state.make_move(move)
                            move_made = True
                        square_sel = () 
                        prev_sel = ()
                    else:
                        #checks for legal selecting of the squate
                        if game_state.check_for_right_move(row, col) == True :
                            square_sel = (row, col)
            #undo click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: 
                game_state.undo_move()
                move_made = True
        #regenerate valid moves 
        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        # draw again every 15 fps
        draw_gs(screen, game_state)
        clock.tick(15)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()