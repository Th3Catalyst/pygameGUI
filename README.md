# pygameGUI
A custom GUI library for pygame.    
`pip install -i https://test.pypi.org/simple/ pygGUI`
## Classes

### pygameGUI.Text(text,font,color, pos = (0,0))
creates a text object that can be added to a menu
ARGS:
- text (string): the text displayed
- font (pygame.font.Font object): text font
- color (3 tuple, string, hex code): text color
- pos (2 tuple): top left corner of the text

### pygameGUI.Button(text,font,color, pos = (0,0), command=None)
creates a button object that can be added to a menu. In order to use it properly you must add the button to a [Manager](https://github.com/Th3Catalyst/pygameGUI?tab=readme-ov-file#pygameguimanager) or a menu.
ARGS:
- text (string): the text displayed
- font (pygame.font.Font object): text font
- color (3 tuple, string, hex code): text color
- pos (2 tuple): top left corner of the button
- command (function): code to run on click 

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


### pygameGUI.Dropdown(text, font, color,bgcolor="white", pos=(0,0),values=[],scaleFactor=1):
creates a dropdown that can be added to a menu. In order to use it properly you must add the dropdown to a [Manager](https://github.com/Th3Catalyst/pygameGUI?tab=readme-ov-file#pygameguimanager) or a menu.
ARGS:
- text (string): the placeholder text
- font (pygame.font.Font object): text font
- color (3 tuple, string, hex code): text color
- bgcolor (3 tuple, string, hex code): color of the background of the list
- pos (2 tuple): top left corner of the dropdown
- values (list of strings): the options in the dropdown
- scaleFactor (num): the size of the list objects relative to the main text

Use the `.text` attribute to get the value of the dropdown.

### pygameGUI.TextInput(text, font, color, pos=(0,0)):
creates a text input object that can be added to a menu. In order to use it properly you must add the dropdown to a [Manager](https://github.com/Th3Catalyst/pygameGUI?tab=readme-ov-file#pygameguimanager) or a menu. 
ARGS:
- text (string): the text displayed
- font (pygame.font.Font object): text font
- color (3 tuple, string, hex code): text color
- pos (2 tuple): top left corner of the text

Use the `.text` attribute to get the text input's value.


### Here is an example of this code:
```
font = pygame.font.Font('freesansbold.ttf', 70)
menu = pygameGUI.Menu("Choose Game", "white", font, 500, 600, image="menuBG.png",pos=(100,60))

chess = pygameGUI.Text("Chess", font, (255, 255, 255))
tetris = pygameGUI.Text("Tetris", font, (255, 255, 255))

menu.add(chess)
menu.add(tetris)
```
First, we create the menu object with the title "Choose Game" with white text and the free sans bold font. The menu has a width of 500 and a height of 600 placed at 100,60 and the menuBG as its background image:
```
font = pygame.font.Font('freesansbold.ttf', 70)
menu = pygameGUI.Menu("Choose Game", "white", font, 500, 600, image="menuBG.png",pos=(100,60))
```
Then, we create two text objects, each with the free sans bold font and a white text color:
```
chess = pygameGUI.Text("Chess", font, (255, 255, 255))
tetris = pygameGUI.Text("Tetris", font, (255, 255, 255))
```
Lastly, we add the text objects to the menu:
```
menu.add(chess)
menu.add(tetris)
```
Now, we have to draw the menu. To do this, just call the draw function on the menu object in your game loop:
```
running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False               

    screen.fill((0, 0, 0))
    menu.draw(screen) #draws the menu to the screen
    pygame.display.flip()

pygame.quit()
```
**IMPORTANT:** Adding the menu to a group and drawing it that way will not draw the menu elements.

### pygameGUI.Manager()

Used to handle inputs from elements in pygameGUI.
### Example:
```
import pygame
import pygameGUI
font = pygame.font.Font('freesansbold.ttf', 70)
man = Manager()

def test_func():
    print("test")

test_button = Button("Test", font, (255, 255, 255), (640, 450), lambda: print("test"))
test_button2 = Button("Test", font, (255, 255, 255), (640, 650), test_func)
man.add(test_button)
man.add(test_button2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        man.input(event)

    screen.fill((0, 0, 0))

    test_button.draw(screen)
    test_button2.draw(screen)

    pygame.display.flip()

pygame.quit()
```
First, we create the input manager we will be using, and one of the buttons' functions:  
**IMPORTANT:** Menu objects have a built-in input manager, so in this code, `man` could be replaced with a `pygameGUI.Menu()` object.  
```
import pygame
import pygameGUI
font = pygame.font.Font('freesansbold.ttf', 70)
man = Manager()

def test_func():
    print("test")
```
Then we create the two buttons and add them both to the input manager:
```
test_button = Button("Test", font, (255, 255, 255), (640, 450), lambda: print("test"))
test_button2 = Button("Test", font, (255, 255, 255), (640, 650), test_func)
man.add(test_button)
man.add(test_button2)
```
Next we start a game loop and start our event polling with `man.input(event)`:
```
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        man.input(event)
```
Finally, we draw the buttons to the screen and close our loop:
```
screen.fill((0, 0, 0))

    test_button.draw(screen)
    test_button2.draw(screen)

    pygame.display.flip()

pygame.quit()
```
The `input(event)` function tracks element clicking and typing when a text box is selected. Alternatively, you can use the `click()` function to only track mouse clicks:
```
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                man.click()

# ...
```

