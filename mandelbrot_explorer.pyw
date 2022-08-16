'''
Mandelbot Explorer

Its mandelbrot!
Decided to do when I was bored, and slowly added more things

Controls:
Click - Set start and end of selection box
Space - zoom to selection box
I - set number of iterations
P - set pixel density (size of drawn pixels)
R - reset all parameters and zoom
F1 - save a screenshot

Enter - Confirm
Esc - Remove selection box / Cancel / Exit


History:

18/10/17 - Made program
31/08/19 - fixed a couple bugs
'''
import random
import pygame
import sys
import time

# -----------FUNCTIONS
sign = lambda x: (1, -1)[x < 0]

def leave():
    pygame.quit()
    sys.exit()

def save_mandelbrot(name):
    pygame.image.save(mandelbrot_s,"m"+str(name)+".png")

def move_to(coord1,coord2):
    global cameraX, cameraY, cameraZoom, update
    midx = (coord1[0] + coord2[0])/2
    midy = (coord1[1] + coord2[1])/2
    cameraX, cameraY = screen_to_coord(midx,midy)
    cameraZoom *= WIDTH/abs(coord2[0]-coord1[0])
    update = True    

def set_pixellation(number):
    global cameraZoom, SIZE_M, mandelbrot_s, update
    if number < 1 or number > 200:
        return 
    
    cameraZoom *= SIZE_M
    SIZE_M = number
    cameraZoom /= SIZE_M
    mandelbrot_s = pygame.Surface((WIDTH//SIZE_M, HEIGHT//SIZE_M))
    update = True

def set_iterations(number):
    global ITERATIONS, update
    ITERATIONS = number
    update = True

def reset_variables():
    global cameraX, cameraY, cameraZoom, ITERATIONS, SIZE_M,mandelbrot_s, update
    SIZE_M = 3
    ITERATIONS = 100
    cameraX = 0
    cameraY = 0
    cameraZoom = 200/SIZE_M

    mandelbrot_s = pygame.Surface((WIDTH//SIZE_M, HEIGHT//SIZE_M))
    update = True

def do_mandelbrot(real, imag):
    z = complex(real, imag)
    c = z
    for i in range(ITERATIONS):
        z = pow(z,2) + c
        if abs(z) > 2:
            return i/ITERATIONS * 255

    return -1

def get_mouse_pos():
    mousepos = pygame.mouse.get_pos()
    if drawingbox:
        boxwidth = (mousepos[0]-boxpos[0][0])/WIDTH
        boxheight = (mousepos[1]-boxpos[0][1])/HEIGHT

        if abs(boxwidth) > abs(boxheight):
            boxheight = sign(boxheight) * abs(boxwidth)
        else:
            boxwidth = sign(boxwidth) * abs(boxheight)

        boxwidth *= WIDTH
        boxheight *= HEIGHT

        mousepos = (boxpos[0][0]+ boxwidth, boxpos[0][1]+ boxheight)
    return mousepos

def screen_to_coord(x,y):
    x -= WIDTH/2
    y -= HEIGHT/2

    real = cameraX + x/cameraZoom/SIZE_M
    imag = cameraY - y/cameraZoom/SIZE_M

    return (real,imag)

def remove_box():
    global drawingbox, boxpos
    drawingbox = False
    boxpos = []

# -----------VARIABLES

pygame.init()
clock = pygame.time.Clock()

# Pygame
FULLSCREEN_MODE = True
monitor = pygame.display.Info()

if FULLSCREEN_MODE:
    WIDTH = monitor.current_w
    HEIGHT = monitor.current_h
    surface = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
else:
    WIDTH = 1000
    HEIGHT = 1000

    surface = pygame.display.set_mode((WIDTH,HEIGHT))
    

pygame.display.set_caption("Mandelbrot Explorer")


FONTSIZE = int(30/1920*WIDTH)
# -Text-
# Select the                 font to use,  size, bold, italics
font = pygame.font.SysFont("Century Gothic", FONTSIZE, False, False)
# Render the text. "True" means anti-aliased text. The list is the colour.
text = font.render("My text",True,(0,0,0))
# Put the image of the text on the screen at 250x250
# surface.blit(text, [250, 250])


#Program

reset_variables()

running = True
keypress = None
boxpos = []
drawingbox = False

textbox = None


while running:

    # ----------------------------------- INPUTS ----
    keypress = None
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                keypress = "escape"

            if event.key == pygame.K_BACKSPACE:
                keypress = "back"
                
            if event.key == pygame.K_SPACE:
                keypress= "space"

            if event.key == pygame.K_RETURN:
                keypress= "enter"

            if event.key == 282:
                keypress = "f1"

            #print(event.key)

            if 48 <= event.key <= 57:   # Number input
                keypress= event.key - 48
            
            if event.key == 105:
                keypress= "i"

            if event.key == 112:
                keypress= "p"
            
            if event.key == pygame.K_r:
                keypress = "r"

        if event.type == pygame.QUIT:
            leave()


        mousepos = get_mouse_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not drawingbox:
                boxpos = [mousepos,mousepos]
                drawingbox = True
            else:
                drawingbox = False
            

    # --------------------------------- DRAWING ----

    if drawingbox:
        boxpos[1] = mousepos

    if keypress == "space":
        if boxpos and not drawingbox:
            move_to(boxpos[0],boxpos[1])
    
    if keypress == "r":
        remove_box()
        reset_variables()

    if keypress == "i":
        remove_box()
        textbox = [("Maximum iterations:",str(ITERATIONS)+" -"),set_iterations]

    if keypress == "p":
        remove_box()
        textbox = [("Draw every x pixels:",str(SIZE_M)+" -"),set_pixellation]

    if keypress == "f1":
        drawingbox = False
        textbox = [("Give image a number:","  m"),save_mandelbrot]
        

    if update:
        x = int(-WIDTH/SIZE_M/2)
        y = int(-HEIGHT/SIZE_M/2)
        update = False
        textbox = None
        remove_box()


    surface.blit(pygame.transform.scale(mandelbrot_s,(WIDTH,HEIGHT)),(0,0))
    
    if x <= WIDTH//SIZE_M//2:  # If mandelbrot not fully generated yet
        x += 1
        for y in range(int(-HEIGHT/SIZE_M/2), int(HEIGHT/SIZE_M/2)+1):
            mandelbrotX = cameraX + x/cameraZoom
            mandelbrotY = -cameraY + y/cameraZoom
            output = do_mandelbrot(mandelbrotX, mandelbrotY)
            if output < 0:
                color = (0,0,0)
            else:
                color = (output,0,20)
            mandelbrot_s.set_at((x+int(WIDTH/SIZE_M/2), y+int(HEIGHT/SIZE_M/2)), color)

        text = font.render("Thinkifying"+"."*(x%3+1),True,(255,255,255))
        surface.blit(text, [HEIGHT*0.05, HEIGHT*0.95])
        text = font.render("_"*int(((x+WIDTH/SIZE_M/2)*SIZE_M*2)/FONTSIZE),True,(255,255,255))
        surface.blit(text, [0, HEIGHT*0.96])
            

    if textbox:
        
        pygame.draw.rect(surface, (20,20,20), ((WIDTH*0.70,HEIGHT*0.1),(WIDTH*0.2,WIDTH*0.06)), 0) # Whole box
        pygame.draw.rect(surface, (10,10,10), ((WIDTH*0.70,HEIGHT*0.1+WIDTH*0.06),(WIDTH*0.2,WIDTH*0.003)), 0) # Shadow
        pygame.draw.rect(surface, (40,40,40), ((WIDTH*0.77,HEIGHT*0.1+WIDTH*0.03),(WIDTH*0.125,WIDTH*0.025)), 0) # Input box
        pygame.draw.rect(surface, (30,30,30), ((WIDTH*0.77,HEIGHT*0.1+WIDTH*0.03),(WIDTH*0.125,WIDTH*0.003)), 0) # Input shadow
        
        for i,t in enumerate(textbox[0]):
            text = font.render(t,True,(0,0,0))
            surface.blit(text, [WIDTH*0.71, HEIGHT*0.1 + WIDTH*(0.005+0.0275*i)])

        num = 0
        for i in textbox[2:]:
            num *= 10
            num += i
        if num != 0:
            text = font.render(str(num),True,(0,0,0))
            surface.blit(text, [WIDTH*0.775, HEIGHT*0.1+WIDTH*0.0325])

        if isinstance(keypress,int):
            textbox.append(keypress)

        if keypress == "enter":
            if num != 0:
                textbox[1](num)
                
            textbox = None

        if keypress == "back":
            if len(textbox) > 2:
                del textbox[-1]

    
    if keypress == "escape":
        if boxpos or textbox:
            textbox = None
            remove_box()
        else:
            leave()

    if boxpos:

        boxwidth = boxpos[1][0]-boxpos[0][0]
        boxheight = boxpos[1][1]-boxpos[0][1]
        pygame.draw.rect(surface, (155,155,50), (boxpos[0],(boxwidth,boxheight)), 2)


    pygame.display.flip()


    # Find gamespeed
    gamespeed = max(  min(clock.tick() *0.25, 1000) ,200   ) * 0.2









