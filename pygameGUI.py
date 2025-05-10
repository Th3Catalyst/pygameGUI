import pygame

# window setup
debug = True
if debug:
    pygame.init()
    screen = pygame.display.set_mode((1280, 900))
    running = True
    pygame.display.set_caption("Menu")
    all_sprites = pygame.sprite.Group()
    font = pygame.font.Font('freesansbold.ttf', 70)


class Background(pygame.sprite.Sprite): 

    def __init__(self,color,width,height,image = None, defaultC = ""): 
        
        super().__init__()

        
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.color = color

        self.pieceIndex = ""

        match defaultC:
                case "red":
                    self.image = pygame.image.load("school/blocks/redTile.png").convert_alpha()
                case "green":
                    self.image = pygame.image.load("school/blocks/greenTile.png").convert_alpha()
                case "orange":
                    self.image = pygame.image.load("school/blocks/orangeTile.png").convert_alpha()
                case "purple":
                    self.image = pygame.image.load("school/blocks/purpleTile.png").convert_alpha()
                case "blue":
                    self.image = pygame.image.load("school/blocks/blueTile.png").convert_alpha()
                case "teal":
                    self.image = pygame.image.load("school/blocks/tealTile.png").convert_alpha()
                case "yellow":
                    self.image = pygame.image.load("school/blocks/yellowTile.png").convert_alpha()
                case "grey":
                    self.image = pygame.image.load("school/blocks/greyTile.png").convert_alpha()
        

        if image != None:
            self.image = pygame.image.load(image).convert_alpha()

        self.image = pygame.transform.scale(self.image, (width,height))
        
        
        self.rect = self.image.get_rect()

    def draw(self, screen): 
        screen.blit(self.image, self.rect)


class Menu(Background):
    def __init__(self, title, titlecolor, font, width, height, color="red", image = None, pos=(0,0),hrcolor="black",defaultC = ""):
        super().__init__(color, width, height, image, defaultC)
        self.title = title
        self.font = font
        self.width = width
        self.height = height
        self.sprites = Manager(title)
        self.titlecolor = titlecolor
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.hrcolor = hrcolor
        
        self.selectedInput = None
        self.caps = False
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        titleT = self.font.render(self.title, True, self.titlecolor)
        titleTRect = titleT.get_rect(center=(self.rect.x + self.width/2, self.rect.y + 50))
        screen.blit(titleT, (self.rect.x +self.width/2 - titleTRect.width/2, self.rect.y + 50 - titleTRect.height/2.5))
        pygame.draw.line(screen, self.hrcolor, (self.rect.x + 20, self.rect.y + 60 + titleTRect.height / 2), (self.rect.x + self.width - 20, self.rect.y + 60 + titleTRect.height / 2), width=5)
        #self.sprites.draw(screen)
        for s in self.sprites:
            if not isinstance(s,Button) or (isinstance(s,Button) and not s.isdropdown):
                s.draw(screen)  
     

    
    def add(self, sprite):
        self.sprites.add(sprite)
        sprite.rect.x = self.rect.x + (self.width - sprite.rect.width) / 2
        sprite.rect.y = self.rect.y + 70*(len(self.sprites)+1) -30
    
    def click(self):
        pos = pygame.mouse.get_pos()
        clickedSprites = [s for s in self.sprites if s.rect.collidepoint(pos)]
        for s in self.sprites:
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
                print(s.selected)
            
            if isinstance(s,TextInput) and s in clickedSprites:
                self.selectedInput = s
                s.selected = True
    
    def input(self,event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.selectedInput:
                self.selectedInput.selected = False
                self.selectedInput = None
            self.click()
        if event.type == pygame.KEYDOWN and self.selectedInput:
            print(event.key)
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.selectedInput.selected = False
                self.selectedInput = None
            else:
                try:
                    if event.key == pygame.K_BACKSPACE:
                        self.selectedInput.text = self.selectedInput.text[0:-1]
                        char = None
                    elif not self.caps and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        print(chr(event.key))
                        char = chr(event.key)
                    else: 
                        print(chr(event.key).upper())
                        char = chr(event.key).upper()
                    self.selectedInput.text += char if char else ""
                    self.selectedInput.image = self.selectedInput.font.render(self.selectedInput.text, True, self.selectedInput.color)
                    temprect = self.selectedInput.image.get_rect()
                    self.selectedInput.rect.width = temprect.width
                    self.selectedInput.rect.height = temprect.height

                except:
                    if event.key == pygame.K_CAPSLOCK:
                        self.caps = not self.caps

class Manager(pygame.sprite.Group):
    def __init__(self,name=None):
        super().__init__()
        self.name = name
        self.selectedInput = None
        self.caps = False
    
    def click(self):
        pos = pygame.mouse.get_pos()
        clickedSprites = [s for s in self.sprites() if s.rect.collidepoint(pos)]
        print(clickedSprites)
        print("===")
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
                print(s.selected)
            if isinstance(s,TextInput) and s in clickedSprites:
                self.selectedInput = s
                s.selected = True
    
    def input(self,event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.selectedInput:
                self.selectedInput.selected = False
                self.selectedInput = None
            self.click()
        if event.type == pygame.KEYDOWN and self.selectedInput:
            print(event.key)
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.selectedInput.selected = False
                self.selectedInput = None
            else:
                try:
                    if event.key == pygame.K_BACKSPACE:
                        self.selectedInput.text = self.selectedInput.text[0:-1]
                        char = None
                    elif not self.caps and not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        print(chr(event.key))
                        char = chr(event.key)
                    else: 
                        print(chr(event.key).upper())
                        char = chr(event.key).upper()
                    self.selectedInput.text += char if char else ""
                    self.selectedInput.image = self.selectedInput.font.render(self.selectedInput.text, True, self.selectedInput.color)
                    temprect = self.selectedInput.image.get_rect()
                    self.selectedInput.rect.width = temprect.width
                    self.selectedInput.rect.height = temprect.height

                except:
                    if event.key == pygame.K_CAPSLOCK:
                        self.caps = not self.caps


class Text(pygame.sprite.Sprite):
    def __init__(self, text, font, color, pos=(0,0)):
        super().__init__()
        self.font = font
        self.text = text
        self.color = color
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Button(pygame.sprite.Sprite):
    def __init__(self, text, font, color, pos=(0,0),command=None, isdropdown=False):
        super().__init__()
        self.font = font
        self.text = text
        self.color = color
        self.command = command
        self.isdropdown = isdropdown
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Dropdown(pygame.sprite.Sprite):
    def __init__(self, text, font, color,bgcolor="white", pos=(0,0),values=[],scaleFactor=1):
        super().__init__()
        self.font = font
        self.text = text
        self.color = color
        self.scaleFactor = scaleFactor
        self.selected = False
        self.bgcolor = bgcolor
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.entries = []
        i=0
        self.maxwidth = self.rect.width
        for t in values:
            text= Button(t, font, (255, 255, 255), (pos[0] +20,pos[1]+self.rect.height+5), command=self.selectItem,isdropdown=True)
            #text.command = lambda: print(text.text)
            
            text.rect.y += i*(text.rect.height*scaleFactor+10)
            text.image = pygame.transform.scale(text.image, (int(text.rect.width*scaleFactor), int(text.rect.height*scaleFactor)))
            text.rect = text.image.get_rect()
            self.maxwidth = text.rect.width if text.rect.width > self.maxwidth else self.maxwidth
            self.entries.append(text)
            i+=1

    def selectItem(self,item):
        print(item)
        self.text = item
        self.image = self.font.render(self.text, True, self.color)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            i=0
            pygame.draw.rect(surface,self.bgcolor,(int(self.rect.x),int(self.rect.y+self.rect.height+5),self.maxwidth,int(20+(self.rect.height+10)*self.scaleFactor*(len(self.entries)))))
            for t in self.entries:
                t.rect.x = self.rect.x +20
                t.rect.y = self.rect.y+80 + i*(t.rect.height*self.scaleFactor+10)
                surface.blit(t.image, t.rect)
                i+=1
            for group in self.groups():
                if isinstance(group,Manager):
                    #print(group)
                    
                    for e in self.entries:
                        group.add(e)

class TextInput(pygame.sprite.Sprite):
    def __init__(self, text, font, color, pos=(0,0)):
        super().__init__()
        self.font = font
        self.text = text
        self.color = color
        self.selected = False
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]

    def draw(self, surface):
        if self.selected:
            width = 5
        else:
            width = 1
        pygame.draw.line(surface,self.color,(int(self.rect.x-10),int(self.rect.y-10)),(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10)), width=width)
        pygame.draw.line(surface,self.color,(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10)),(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10) + self.rect.height +10), width=width)
        pygame.draw.line(surface,self.color,(int(self.rect.x-10) + self.rect.width +20,int(self.rect.y-10) + self.rect.height +10),(int(self.rect.x-10),int(self.rect.y-10) + self.rect.height +10), width=width)
        pygame.draw.line(surface,self.color,(int(self.rect.x-10),int(self.rect.y-10) + self.rect.height +10),(int(self.rect.x-10),int(self.rect.y-10)), width=width)


        surface.blit(self.image, self.rect)



if debug:
    test_button = Button("Test", font, (255, 255, 255), (640, 450), lambda: print("test"))


    bg = Menu("You Lose!", "white", font, 600, 600,"red")
    bg.rect.x = 300
    bg.rect.y = 200
    all_sprites.add(bg)

    bg.add(test_button)
    bg.add(Text("Test", font, (255, 255, 255), (640, 450)))

    man = Manager("man")

    d = Dropdown("dropdown", font, "white", "black", (300,300),["test","test2","test3","test4"], scaleFactor=0.5)
    ti = TextInput("Test", font, (255, 255, 255), (640, 450))
    bg.add(ti)
    bg.add(d)
    while running:
        for event in pygame.event.get():
            bg.input(event)
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                #bg.click() 
                #man.click() 
                pass
        screen.fill((0, 0, 0))
        d.draw(screen)
        ti.draw(screen)
        bg.draw(screen)
        #test_button.draw(screen)
        pygame.display.flip()



    pygame.quit()
