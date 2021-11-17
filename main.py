'''
Demo gif:
https://media.giphy.com/media/odillRIcapYxhSsIhY/giphy.gif

How to use:

Please press enter when prompted with "Go?"

Enter how many frames you want the simulation to run for when prompted with "iterations" 

A high number is usually more interesting!

Press space to unpause and begin the simulation, LEFT clicks in the simulation allow you to add lit-up/living squares!

RIGHT clicks delete squares!

You can pause it again with space to add squares with more precision. 

Creator: HanqiXiao / The Inscrutable

'''


import pygame
from game_of_life_base import Base
import sys

from theme_colors import WHITE, BLACK, GREY, RED

'''Script Components:
inits

main()

alter_grid()

draw()

run prevention
'''

##global constants
WIDTH, HEIGHT = 900, 450
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A recreation of John Conway's game of life")
FPS = 50
Base = Base()


##fonts
pygame.init()
pygame.mouse.set_visible = True

##game state
state = "running"

def main():
    ##member vars import global
    global state
    global square_size
    ##member vars
    run = True
    new_senario = True
    n_rl_match = True
    clock = pygame.time.Clock()

    ##match counter dictionaries
    counter = {'match0':0,'match1':0}
    m_tracker0 = {}

    ##pause handling
    held = False

    while run == True:

        ##fps
        clock.tick(FPS)

        ##exit loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        ##create input objects
        keys_pressed = pygame.key.get_pressed()

        if True:
            ##input rl_match
            if n_rl_match == True and False:
                match0 = Base.read_grid('rl_match_inputs.txt')
                m_cols = Base.cols
                m_rows = Base.rows
                square_size = HEIGHT/m_rows if m_cols <= m_rows else WIDTH/m_cols
                print('square_size', square_size, 'pixels')
                ##font for flexibility
                SQUARE_FONT = pygame.font.SysFont('Corbel', int(square_size))
                draw(match0)
                #print(match0)
                state = "paused"
                placeholder = "running"
                input()
                n_rl_match = False

            ##startup/restart
            if new_senario == True:
                grid0 = Base.read_grid('input.txt')
                cols = Base.cols
                rows = Base.rows
                square_size = HEIGHT/rows if cols < rows else WIDTH/cols
                print('square_size', square_size, 'pixels')
                ##font for flexibility
                SQUARE_FONT = pygame.font.SysFont('Corbel', int(square_size))
                draw(grid0)
                input('''

How to use :)

Press enter to start after you finish reading this quick guide!

You should then be prompted with text asking you for the number of iterations you want -- A high number is usually more interesting!

Press space to unpause and begin the simulation, LEFT clicks in the simulation allow you to add lit-up/living squares! RIGHT clicks delete squares!

Link to gif demo:
https://media.giphy.com/media/odillRIcapYxhSsIhY/giphy.gif
''')
                iterations = int(input('How long do you want the simulation to run? (in frames) ', ))
                new_senario = False
                state = "paused"
                placeholder = "running"
                continue

            ##progress simulation
            elif state == "running":
                if iterations > 0:
                    ## optional reinforcement learning helper code

                    #m_id = 0
                    #for yp in range(rows):
                    #    for xp in range(cols):
                    #        m_id += 1
                    #        match_n, target0 = Base.rl_match(m_cols, m_rows, match0, grid0, cols, rows, xp, yp)
                            #print(match, target)
                    #        if match_n == target0:
                    #            if not [xp,yp] in m_tracker0.values():
                    #                counter['match0'] = counter['match0']+1
                    #                print('match0','detected count', counter['match0'])
                    #                m_tracker0[m_id] = [xp,yp]
                    #            else: 
                    #                pass
                    #        else:
                    #            for i in m_tracker0.keys():
                    #                if [xp,yp] == m_tracker0[i]:
                    #                    m_tracker0[i] = 'null'
                    grid0 = Base.Calculatenextgrid(grid0).copy()
                    iterations -= 1
                    #time.sleep(.1)
                    ##end of simulation
                    if iterations == 1:
                        pass

        ##handle pauses
        toggle_p, held = button_down(pygame.K_SPACE, held, keys_pressed)
        if toggle_p == 1:
            state, placeholder = placeholder, state

        ##make changes to the grid
        grid0, pos = alter_grid(grid0, keys_pressed, SQUARE_FONT)
        draw(grid0)

        ##highllight
        pygame.draw.rect(WIN, GREY, (pos[0]*square_size, pos[1]*square_size, square_size, square_size), 0)

        ##stat blocks
        WIN.blit(SQUARE_FONT.render(state, False, RED), (0,0))
        WIN.blit(SQUARE_FONT.render(str(pos), False, RED), (250,0))
        pygame.display.update()


        ##restart
        if keys_pressed[pygame.K_r]:
          new_senario = True
        ##add iterations
        if keys_pressed[pygame.K_i]:
          iterations = int(input('How long do you want the simulation to run?  (in frames) ', ))
          state = "paused"
          placeholder = "running"

    pygame.quit()



def alter_grid(inputgrid, keys_pressed, font, pos=0):
    global state

    ##get grid pos
    pos = pygame.mouse.get_pos()
    y = int(pos[1]//square_size)
    x = int(pos[0]//square_size)
    gridpos = x,y

    ##alter grid
    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2] == True:
        if pygame.mouse.get_pressed()[0]:
            click = 1
        else:
            click = 0
        #print(pygame.mouse.get_pressed())

        if state == "running":
            inputgrid[y][x] = click
            inputgrid[((y + 1)+Base.rows)%Base.rows][x] = click
            inputgrid[y][((x + 1)+Base.cols)%Base.cols] = click
        elif state == "paused":
            inputgrid[y][x] = click

    return inputgrid, gridpos

def draw(input_grid, font = None):
    WIN.fill(WHITE)
    for y,i in enumerate(input_grid):
        for x,i in enumerate(input_grid[y]):
            if i == 0:
                pygame.draw.rect(WIN, BLACK, ((x)*square_size, y*square_size, square_size, square_size), 0)
                pass
            else:
                pygame.draw.rect(WIN, WHITE, (x*square_size, y*square_size, square_size, square_size), 0)
                pass
    pygame.display.update()

def button_down(button, held, keys_pressed):
    ##do button K_SPACE, held is the previous pressed_down
    if keys_pressed[button]:
        pressed_down = True
        pressed = 1
    elif keys_pressed[button] == False:
        pressed_down = False
        pressed = 0

    if held and pressed_down:
        pressed = 0

    return pressed, pressed_down

if __name__ == "__main__":
    main()
    for i in range(1):
     print('simulation end!')