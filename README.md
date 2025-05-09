# pygameGUI
A custom GUI library for pygame.

## Classes

### pygameGUI.Text(text,font,color, (x,y))
creates a text object that can be added to a menu
ARGS:
- text (string): the text displayed
- font (pygame.font.Font object): text font
- color (3 tuple, string, hex code): text color
- (x,y): position of the center of the text  
**In order to make a button, use the following code in the events poll:**
```
if event.type == pygame.MOUSEBUTTONUP:     
  pos = pygame.mouse.get_pos()     
  clickedSprites = [s for s in self.all_sprites if s.rect.collidepoint(pos)]    
  if <YOUR BUTTON> in clickedSprites:     
    <CODE TO RUN ON BUTTON PRESS>
```

### pygameGUI.Menu(color, title, titlecolor, font, width, height, image = None, pos = (0,0),hrcolor="black"):
creates a menu object  
ARGS:  
- color (3 tuple, string, hex code): the background color (overriden by image)
- title (string): menu title
- titlecolor (3 tuple, string, hex code): the title color
- font (pygame.font.Font object): title font
- width (num): menu width
- height (num): menu height
- image (image link): background image
- pos (2 tuple): top left corner of the menu
- hrcolor (3 tuple, string, hex code): the color of the horizontal rule under the title

### Here is an example of this code:
```
font = pygame.font.Font('freesansbold.ttf', 70)
menu = pygameGUI.Menu("Choose Game", "white", font, 500, 600, image="menuBG.png",pos=(100,60))

chessB = pygameGUI.Text("Chess", font, (255, 255, 255))
tetrisB = pygameGUI.Text("Tetris", font, (255, 255, 255))
quitB = pygameGUI.Text("Quit", font, (255, 255, 255))

menu.add(chessB)
menu.add(tetrisB)
menu.add(quitB)
```
First, we create the menu object with the title "Choose Game" with white text and the free sans bold font. The menu has a width of 500 and a height of 600 placed at 100,60 and the menuBG as its background image:
```
font = pygame.font.Font('freesansbold.ttf', 70)
menu = pygameGUI.Menu("Choose Game", "white", font, 500, 600, image="menuBG.png",pos=(100,60))
```
Then, we create three text objects, each with the free sans bold font and a white text color:
```
chessB = pygameGUI.Text("Chess", font, (255, 255, 255))
tetrisB = pygameGUI.Text("Tetris", font, (255, 255, 255))
quitB = pygameGUI.Text("Quit", font, (255, 255, 255))
```
Lastly, we add the text objects to the menu:
```
menu.add(chessB)
menu.add(tetrisB)
menu.add(quitB)
```
Now, we have to draw the menu. To do this, just call the draw function on the menu object in your game loop:
```
running = True
while running:
    for event in pg.event.get(): 
        if event.type == pg.QUIT: 
            running = False               

    screen.fill((0, 0, 0))
    menu.draw(screen) #draws the menu to the screen
    pg.display.flip()

pg.quit()
```
**IMPORTANT:** Adding the menu to a group and drawing it that way will not draw the menu elements.