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

### pygameGUI.Menu(color, title, titlecolor, font, width, height, image = None, pos = (0,0)):
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

### Here is an example of this code:
```
menu = pygameGUI.Menu("red", "Choose Game", "white", font, 500, 664, image="menuBG.png",pos=(screen.get_width()/2 - 210,screen.get_height()/2 - 332))

chessB = pygameGUI.Text("Chess", font, (255, 255, 255))
tetrisB = pygameGUI.Text("Tetris", font, (255, 255, 255))
quitB = pygameGUI.Text("Quit", font, (255, 255, 255))

menu.add(chessB)
menu.add(tetrisB)
menu.add(quitB)
```
First, we create the menu object with 