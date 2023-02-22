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
            if piece != "empty" and piece != "en passant":
                color = "black" if (row + col) % 2 == 0 else "white"
                screen.blit(PIECES_IMG[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def light_square(screen, game_state, valid_moves, square_sel):
    if square_sel != ():
        row, col = square_sel
        if ("white" in game_state.board[row][col] and game_state.white_move) or ("black" in game_state.board[row][col] and not game_state.white_move):
            surf = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
            surf.set_alpha(100)
            surf.fill(pygame.Color("yellow"))
            screen.blit(surf, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            surf.fill("green")
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                     screen.blit(surf, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

        


#draw gamestate and resp for all graphics
def draw_gs(screen, game_state, valid_moves, square_sel):
    draw_board(screen, game_state.board)
    light_square(screen, game_state, valid_moves, square_sel)
    
def draw_text(screen, text):
    font = pygame.font.SysFont("Arial", 38, True, False)
    text_obj = font.render(text, 0, pygame.Color("Red"))
    text_loc = pygame.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - text_obj.get_width()/2, HEIGHT/2 - text_obj.get_height()/2)
    screen.blit(text_obj, text_loc)

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

                if len(square_sel) != 0:
                    #if we are ready to move 
                    prev_sel = square_sel
                    square_sel = (row, col)
                    #makes move
                    move = chess.Move(prev_sel , square_sel,  game_state.board)
                    if move in valid_moves:
                        print(prev_sel + square_sel)
                        game_state.make_move(move)
                        move_made = True
                        square_sel = () 
                        prev_sel = ()
                    else:
                        #reselects
                        square_sel = (row, col)
                
                else:
                    #checks for legal selecting of the squate
                    # if game_state.check_for_right_move(row, col) == True :
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
        draw_gs(screen, game_state, valid_moves, square_sel)
        if game_state.checkmate:
            if game_state.white_move:
                draw_text(screen, "Black wins")
            else:
                draw_text(screen, "White wins")
        elif game_state.stalemate:
            draw_text(screen, "Stalemate")



        clock.tick(15)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()