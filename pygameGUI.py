import pygame
import asyncio


#set to false by default, true allows me to test features
debug = False
if debug and __name__=="__main__":
    #make a new screen
    pygame.init()
    screen = pygame.display.set_mode((1280, 900))
    running = True
    pygame.display.set_caption("Menu")
    all_sprites = pygame.sprite.Group()
    font = pygame.font.Font('freesansbold.ttf', 70)



class Menu(pygame.sprite.Sprite): #base menu class
    def __init__(self, title, titlecolor, font, width, height, color="red", image = None, pos=(0,0),hrcolor="black", anchor="nw"):
        super().__init__() #makes the menu a sprite
        
        #makes a rectangle the size of the sprite and fills it with the specified color if the user requested it
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        if image != None: #sets the menu background to an image if it was in the function
            self.image = pygame.image.load(image).convert_alpha()

        self.image = pygame.transform.scale(self.image, (width,height)) #scales the image to the size of the sprite
        
        
        self.rect = self.image.get_rect() #makes a collision box fgor the menu

        self.title = title #menu title
        self.font = font #menu font
        self.width = width #width of the menu
        self.height = height #height of the menu
        self.sprites = Manager() #group that all the objects of the menu are in
        self.titlecolor = titlecolor #color of the menu ttitle


        self.margin = 10
        self.padding = 0
        match anchor.lower():
            case "nw":
                self.anchor = (0,0)
            case "ne":
                self.anchor = (-self.rect.width,0)
            case "n":
                self.anchor = (-self.rect.width/2,0)
            case "w":
                self.anchor = (-self.rect.width/2,0)
            case "center":
                self.anchor = (-self.rect.width/2,-self.rect.height/2)
            case "e":
                self.anchor = (-self.rect.width,-self.rect.height/2)
            case "sw":
                self.anchor = (0,-self.rect.height)
            case "s":
                self.anchor = (-self.rect.width/2,-self.rect.height)
            case "se":
                self.anchor = (-self.rect.width,-self.rect.height)
        
        self.rect.x, self.rect.y = pos[0] +self.anchor[0], pos[1]+self.anchor[1]
        self.hrcolor = hrcolor #color of he line separtating the title from the menu elements
        
        #text input variables
        self.selectedInput = None #text input that is selected
        self.caps = False #capslock variable

        self.listHeight = 0

        self.titleT = self.font.render(self.title, True, self.titlecolor) 
        self.titleTRect = self.titleT.get_rect(center=(self.rect.x + self.width/2, self.rect.y + 50))

    def draw(self, screen): #draw function
        screen.blit(self.image, self.rect) #draws the menu background
        #renders the title text

        screen.blit(self.titleT, (self.rect.x +self.width/2 - self.titleTRect.width/2, self.rect.y + 50 - self.titleTRect.height/2.5))
        #draws the separating line from the title to the menu elements
        pygame.draw.line(screen, self.hrcolor, (self.rect.x + 20, self.rect.y + 60 + self.titleTRect.height / 2), (self.rect.x + self.width - 20, self.rect.y + 60 + self.titleTRect.height / 2), width=5)
        
        #draws all the menu elements to the screen
        for s in self.sprites:
            if not isinstance(s,Button) or (isinstance(s,Button) and not s.isdropdown): #makes sure i dont always draw the dropdown menu, as i couldnt close it otherwise
                #checks if the element has a special draw function
                try:
                    s.draw(screen) 
                except Exception:
                     screen.blit(s.image, s.rect)
     

    
    def add(self, sprite): #function to add an element to a menu
        self.sprites.add(sprite)
        #puts the element below the previous one
        if not sprite.pos:
            sprite.rect.x = self.rect.x + (self.width - sprite.rect.width) / 2
            sprite.rect.y = self.rect.y + (self.listHeight) + self.titleTRect.height +40 + sprite.padding +sprite.margin
            self.listHeight += sprite.rect.height + sprite.padding*2 +sprite.margin*2
            try:
                self.listHeight += sprite.borderWidth*2
            except Exception:
                pass
        else:
            sprite.rect.x = self.rect.x + sprite.pos[0] + sprite.anchor[0] + sprite.padding 
            sprite.rect.y = self.rect.y + sprite.pos[1] + sprite.anchor[1] + sprite.padding 
    
    def click(self): #function that handles menu element clicks for buttons
        #mkaes a list of the sprites that were clicked
        pos = pygame.mouse.get_pos()
        clickedSprites = [s for s in self.sprites if s.rect.collidepoint(pos)]

        for s in self.sprites:
            if isinstance(s,Button) and s in clickedSprites: #runs if the clicked sprite was a button
                try:
                    #runs the buttons specified function
                    func = s.command
                    if not s.isdropdown:
                        func()
                    else:
                        func(s.text) #the dropdown buttons need their text as a function argument, so the code must be different
                except Exception as e:
                    print(e)
            if isinstance(s,Dropdown) and s in clickedSprites: #runs if a dropdown was clicked
                s.selected = not s.selected #tells the dropdown its selected
            
            if isinstance(s,TextInput) and s in clickedSprites: #runs if the clicked sprite was a text input
                self.selectedInput = s #sets the selected input to be the clicked one
                s.selected = True #tells the text input its selected
    
    async def hover(self):
        pos = pygame.mouse.get_pos()
        for s in self.sprites:
            if isinstance(s,Button) and s.rect.collidepoint(pos):
                print("hover")


    def input(self,event): #function that handles all inputs for the menu elements

        if event.type == pygame.MOUSEBUTTONUP: #runs when the user clicks their mouse
            if self.selectedInput: #deselects a text input if it is selected
                self.selectedInput.selected = False
                self.selectedInput = None
            self.click() #runs the click input
        if event.type == pygame.KEYDOWN and self.selectedInput: #key presses for the text input
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE: #deselects the text input if enter or escape is pressed
                self.selectedInput.selected = False
                self.selectedInput = None
            else:
                try:
                    if event.key == pygame.K_BACKSPACE: #deletes a character from the text input string 
                        self.selectedInput.text = self.selectedInput.text[0:-1]
                        char = None
                    elif not self.caps and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        char = chr(event.key) #stores a lowercase letter
                    else: 
                        char = chr(event.key).upper() #stores an uppercase letter
                    self.selectedInput.text += char if char else "" #adds the character to the text input string
                    #rerenders the textinput with the new string
                    self.selectedInput.image = self.selectedInput.font.render(self.selectedInput.text, True, self.selectedInput.color)
                    temprect = self.selectedInput.image.get_rect()
                    self.selectedInput.rect.width = temprect.width
                    self.selectedInput.rect.height = temprect.height

                except:
                    if event.key == pygame.K_CAPSLOCK: #capslock functionality
                        self.caps = not self.caps

class Manager(pygame.sprite.Group): #input manager class
    def __init__(self,name=None):

        super().__init__()
        self.name = name
        #functionality for text inputs
        self.selectedInput = None
        self.caps = False
    
    def click(self): #click function (same as from menu)
        pos = pygame.mouse.get_pos()
        clickedSprites = [s for s in self.sprites() if s.rect.collidepoint(pos)]
        for s in self.sprites():
            if isinstance(s,Button) and s in clickedSprites:
                try:
                    func = s.command
                    if not s.isdropdown:
                        func()
                    else:
                        func(s.text)
                except Exception as e:
                    print(e)
            if isinstance(s,Dropdown) and s in clickedSprites:
                s.selected = not s.selected
            if isinstance(s,TextInput) and s in clickedSprites:
                self.selectedInput = s
                s.selected = True
    
    def input(self,event): #input function (same as from menu)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.selectedInput:
                self.selectedInput.selected = False
                self.selectedInput = None
            self.click()
        if event.type == pygame.KEYDOWN and self.selectedInput:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.selectedInput.selected = False
                self.selectedInput = None
            else:
                try:
                    if event.key == pygame.K_BACKSPACE:
                        self.selectedInput.text = self.selectedInput.text[0:-1]
                        char = None
                    elif not self.caps and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        char = chr(event.key)
                    else: 
                        char = chr(event.key).upper()
                    self.selectedInput.text += char if char else ""
                    self.selectedInput.image = self.selectedInput.font.render(self.selectedInput.text, True, self.selectedInput.color)
                    temprect = self.selectedInput.image.get_rect()
                    self.selectedInput.rect.width = temprect.width
                    self.selectedInput.rect.height = temprect.height

                except:
                    if event.key == pygame.K_CAPSLOCK:
                        self.caps = not self.caps


class Text(pygame.sprite.Sprite): #text object class
    def __init__(self, text, font, color, pos=None, anchor="nw"):
        super().__init__() #mkaes it a sprite
        self.font = font #text font
        self.text = text #the text string
        self.color = color #text color
        #renders the text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()


        self.margin = 10
        self.padding = 0

        match anchor.lower():
            case "nw":
                self.anchor = (0,0)
            case "ne":
                self.anchor = (-self.rect.width,0)
            case "n":
                self.anchor = (-self.rect.width/2,0)
            case "w":
                self.anchor = (-self.rect.width/2,0)
            case "center":
                self.anchor = (-self.rect.width/2,-self.rect.height/2)
            case "e":
                self.anchor = (-self.rect.width,-self.rect.height/2)
            case "sw":
                self.anchor = (0,-self.rect.height)
            case "s":
                self.anchor = (-self.rect.width/2,-self.rect.height)
            case "se":
                self.anchor = (-self.rect.width,-self.rect.height)
        try:
            self.rect.x, self.rect.y = pos[0] +self.anchor[0], pos[1]+self.anchor[1]
        except Exception:
            pass
        self.pos = pos

    def draw(self, surface): #draw function
        surface.blit(self.image, self.rect)

class Button(pygame.sprite.Sprite): #button object class
    def __init__(self, text, font, color, pos=None,command=None,bordercolor="black",bgcolor="grey",bgcolorHover="#cccccc",anchor="nw", isdropdown=False): #isdropdown is not used by users
        super().__init__() #makes it a sprite
        self.font = font # text font
        self.text = text #text string
        self.color = color #text color
        self.command = command #button function
        self.isdropdown = isdropdown #if the button is a dropdown element
        self.borderColor = bordercolor
        self.bgcolor = bgcolor
        self.bgcolorHover = bgcolorHover
        #renders the button
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        self.margin = 10
        self.padding = 5

        self.borderWidth = 5
        match anchor.lower():
            case "nw":
                self.anchor = (0,0)
            case "ne":
                self.anchor = (-self.rect.width,0)
            case "n":
                self.anchor = (-self.rect.width/2,0)
            case "w":
                self.anchor = (-self.rect.width/2,0)
            case "center":
                self.anchor = (-self.rect.width/2,-self.rect.height/2)
            case "e":
                self.anchor = (-self.rect.width,-self.rect.height/2)
            case "sw":
                self.anchor = (0,-self.rect.height)
            case "s":
                self.anchor = (-self.rect.width/2,-self.rect.height)
            case "se":
                self.anchor = (-self.rect.width,-self.rect.height)
        try:
            self.rect.x = pos[0] + self.anchor[0]
            self.rect.y = pos[1] + self.anchor[1]
            
        except Exception:
            print(self.text)
            pass
        #self.rect.width += 10; self.rect.height += 10
        self.pos = pos


    def draw(self, surface): #draw function
        width = self.borderWidth
        #draws the border rectangle around the text input
        pygame.draw.line(surface,self.borderColor,(int(self.rect.x- self.padding),int(self.rect.y- self.padding)),(int(self.rect.x+ self.padding) + self.rect.width,int(self.rect.y- self.padding)), width=width)
        pygame.draw.line(surface,self.borderColor,(int(self.rect.x+ self.padding) + self.rect.width,int(self.rect.y- self.padding)),(int(self.rect.x+ self.padding) + self.rect.width,int(self.rect.y+ self.padding) + self.rect.height), width=width)
        pygame.draw.line(surface,self.borderColor,(int(self.rect.x+ self.padding) + self.rect.width,int(self.rect.y+ self.padding) + self.rect.height),(int(self.rect.x - self.padding),int(self.rect.y + self.padding) + self.rect.height), width=width)
        pygame.draw.line(surface,self.borderColor,(int(self.rect.x - self.padding),int(self.rect.y + self.padding) + self.rect.height),(int(self.rect.x - self.padding),int(self.rect.y - self.padding)), width=width)

        pygame.draw.rect(surface,self.bgcolor, (self.rect.x - self.padding,self.rect.y - self.padding, self.rect.width + self.padding*2,self.rect.height + self.padding*2))
        surface.blit(self.image, self.rect)

class Dropdown(pygame.sprite.Sprite): #dropdown class
    def __init__(self, text, font, color,bgcolor="white", pos=None,values=[],scaleFactor=1,anchor="nw"):
        super().__init__() #makes it a sprite
        self.font = font #font for dropdown object and th emenu objects
        self.text = text #placeholder text string
        self.color = color #text color
        self.scaleFactor = scaleFactor #how much smaller the menu elements are from the dropdown menu title
        self.selected = False
        self.bgcolor = bgcolor #dropdown menu bg color
        #renders the dropdown
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        self.margin = 10
        self.padding = 0

        match anchor.lower():
            case "nw":
                self.anchor = (0,0)
            case "ne":
                self.anchor = (-self.rect.width,0)
            case "n":
                self.anchor = (-self.rect.width/2,0)
            case "w":
                self.anchor = (-self.rect.width/2,0)
            case "center":
                self.anchor = (-self.rect.width/2,-self.rect.height/2)
            case "e":
                self.anchor = (-self.rect.width,-self.rect.height/2)
            case "sw":
                self.anchor = (0,-self.rect.height)
            case "s":
                self.anchor = (-self.rect.width/2,-self.rect.height)
            case "se":
                self.anchor = (-self.rect.width,-self.rect.height)
        try:
            self.rect.x, self.rect.y = pos[0] +self.anchor[0], pos[1]+self.anchor[1]
        except Exception:
            pass
        self.pos = pos
        #mkaes the entries in the dropdown menu
        self.entries = []
        
        self.maxwidth = self.rect.width #this will store the width the rectangle behind the menu entries needs to be
        for t in values:
            #renders a menu entry
            text= Button(t, font, (255, 255, 255), command=self.selectItem,isdropdown=True)
            
            text.image = pygame.transform.scale(text.image, (int(text.rect.width*scaleFactor), int(text.rect.height*scaleFactor)))
            text.rect = text.image.get_rect()
            self.maxwidth = text.rect.width if text.rect.width > self.maxwidth else self.maxwidth #makes the maxwidth larger if a text element is longer than the rectangle
            self.entries.append(text) #adds the button to a llist of all the dropdown menu sprites
            

    def selectItem(self,item): #function for the dropdown buttons that updates the dropdown title/placeholder text
        self.text = item
        self.image = self.font.render(self.text, True, self.color)

    def draw(self, surface): #draw function for the dropdown
        surface.blit(self.image, self.rect)#draws the placeholder/title text
        if self.selected: #draws this part if the dropdown is selected
            i=0
            pygame.draw.rect(surface,self.bgcolor,(int(self.rect.x),int(self.rect.y+self.rect.height+5),self.maxwidth,int(20+(self.rect.height+10)*self.scaleFactor*(len(self.entries)))))
            for t in self.entries:
                #positions the menu entries
                t.rect.x = self.rect.x +20
                t.rect.y = self.rect.y+80 + i*(t.rect.height*self.scaleFactor+10)
                surface.blit(t.image, t.rect) #draws the menu entry to the screen
                i+=1
            for group in self.groups(): #adds the menu entries to any input managers the dropdown is part of
                if isinstance(group,Manager):
                    
                    for e in self.entries:
                        group.add(e)

class TextInput(pygame.sprite.Sprite): #text input class
    def __init__(self, text, font, color, pos=None, anchor="nw"):
        super().__init__() #makes it a sprite
        self.font = font #font color
        self.text = text #placeholder string
        self.color = color #text color
        self.selected = False
        #renders the text input
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        self.margin = 10
        self.padding = 0

        self.borderWidth = 1
        self.borderFocused = 5

        match anchor.lower():
            case "nw":
                self.anchor = (0,0)
            case "ne":
                self.anchor = (-self.rect.width,0)
            case "n":
                self.anchor = (-self.rect.width/2,0)
            case "w":
                self.anchor = (-self.rect.width/2,0)
            case "center":
                self.anchor = (-self.rect.width/2,-self.rect.height/2)
            case "e":
                self.anchor = (-self.rect.width,-self.rect.height/2)
            case "sw":
                self.anchor = (0,-self.rect.height)
            case "s":
                self.anchor = (-self.rect.width/2,-self.rect.height)
            case "se":
                self.anchor = (-self.rect.width,-self.rect.height)
        try:
            self.rect.x, self.rect.y = pos[0] +self.anchor[0], pos[1]+self.anchor[1]
        except Exception:
            pass
        self.pos = pos

    def draw(self, surface): #draw function
        if self.selected: #makes the border thicker if its selected
            width = self.borderFocused
        else:
            width = self.borderWidth
        #draws the border rectangle around the text input
        pygame.draw.line(surface,self.color,(int(self.rect.x-10),int(self.rect.y-10)),(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10)), width=width)
        pygame.draw.line(surface,self.color,(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10)),(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10) + self.rect.height +10), width=width)
        pygame.draw.line(surface,self.color,(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10) + self.rect.height +10),(int(self.rect.x-10),int(self.rect.y-10) + self.rect.height +10), width=width)
        pygame.draw.line(surface,self.color,(int(self.rect.x-10),int(self.rect.y-10) + self.rect.height +10),(int(self.rect.x-10),int(self.rect.y-10)), width=width)


        surface.blit(self.image, self.rect) #draws the text input text



if debug and __name__ == "__main__": #runs if im debugging
    test_button = Button("Test", font, (255, 255, 255), command=lambda: print("test")) #test button

    #test menu
    bg = Menu("You Lose!", "white", font, 600, 600,"red")
    bg.rect.x = 300
    bg.rect.y = 100
    all_sprites.add(bg)

    #adds the test button and a test text object to the menu
    bg.add(test_button)
    bg.add(Text("Test", font, (255, 255, 255), (300, 600), anchor="s"))

    man = Manager() #makes a test input manager 

    d = Dropdown("dropdown", font, "white", "black",values=["test","test2","test3","test4"], scaleFactor=0.5) #makes a test dropdown
    ti = TextInput("Test", font, (255, 255, 255)) #test text inoput
    #adds the text input and dropdown to the menu
    bg.add(ti)
    bg.add(d)
    while running: #game loop
        for event in pygame.event.get(): #polls for events
            bg.input(event) #runs the input function for the menu
            asyncio.run(bg.hover())
            #man.input(event) #runs the input function for the manager
            if event.type == pygame.QUIT: #runs when the user presses the "x"
                running = False

            if event.type == pygame.MOUSEBUTTONUP: #runs when th euser clicks
                #testing click functions for menu and manager
                #bg.click() 
                #man.click() 
                pass
        

        screen.fill((0, 0, 0)) #makes the screen black
        #draws the menu to the screen
        #d.draw(screen)
        #ti.draw(screen)
        bg.draw(screen)
        #test_button.draw(screen)
        pygame.display.flip() #updates the display



    pygame.quit() #quits pygame
