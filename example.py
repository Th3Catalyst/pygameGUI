import pygameGUI
import pygame as pg
#imports my tetris and chess gamesh


#new pygame window
pg.init()
screen = pg.display.set_mode((1280, 900))
pg.display.set_caption("Launcher")

#important variables
all_sprites = pg.sprite.Group()
font = pg.font.Font('8bitFONT.ttf', 70)
squareWidth = 40

#makes th ebuttons for playing chess and tetris using my GUI lib
chessB = pygameGUI.Text("Chess", font, (255, 255, 255), (640, 450))
tetrisB = pygameGUI.Text("Tetris", font, (255, 255, 255), (640, 450))
all_sprites.add(chessB)
all_sprites.add(tetrisB)

#makes the quit button using my GUI lib
quitB = pygameGUI.Text("Quit", font, (255, 255, 255), (640, 450))
all_sprites.add(quitB)

#makes the menu base with my GUI lib
menu = pygameGUI.Menu( "Choose Game", "white", font, 12*squareWidth + 20, 16*squareWidth+24, image="menuBG.png",pos=(screen.get_width()/2 - 5*squareWidth -10,screen.get_height()/2 - 8*squareWidth -12))
all_sprites.add(menu)

#adds the buttons to the menu
menu.add(chessB)
menu.add(tetrisB)
menu.add(quitB)

#creates a main loop
running = True
while running:
    for event in pg.event.get(): #gets all the events
        if event.type == pg.QUIT: #runs when the user clicks the windows x button
            running = False #ends the loop

        if event.type == pg.MOUSEBUTTONUP: #runs when the user clicks their mouse 
            pos = pg.mouse.get_pos() #gets the mosue position

            clickedSprites = [s for s in all_sprites if s.rect.collidepoint(pos)] #makes a list of all sprites clicked
            if chessB in clickedSprites: #runs if the chess button was clicked
                print("chess")
            if tetrisB in clickedSprites: #runs if the tetris button is clicked
               print("tetris")

            if quitB in clickedSprites: #quits the game when the quit button is clicked
                running = False
                  
            
                
    #DRAWING THINGS TO THE SCREEN

    screen.fill((0, 0, 0)) #fills the screen with black (this covers the previous frame)
    menu.draw(screen) #draws the menu to the screen

    pg.display.flip() #updates the display



pg.quit() #quits pygame after closing the run loop