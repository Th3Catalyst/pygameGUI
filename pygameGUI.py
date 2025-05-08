import pygame

# window setup
debug = False
if debug:
    pygame.init()
    screen = pygame.display.set_mode((1280, 900))
    running = True
    pygame.display.set_caption("Menu")
    all_sprites = pygame.sprite.Group()
    font = pygame.font.Font('freesansbold.ttf', 70)


class Background(pygame.sprite.Sprite): #class for the board squares

    def __init__(self,color,width,height,image = None, defaultC = ""): 
        # Call the parent class (Sprite) constructor
        super().__init__()

        # fill the surface of the sprite with a color
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
        
        #creates the bounding box of the sprite
        self.rect = self.image.get_rect()

    def draw(self, screen): #function that can draw the sprite so i can draw them individually
        screen.blit(self.image, self.rect)





class Text(pygame.sprite.Sprite):
    def __init__(self, text, font, color, xy):
        super().__init__()
        self.font = font
        self.text = text
        self.color = color
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(xy[0], xy[1]))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Menu(Background):
    def __init__(self, color, title, titlecolor, font, width, height, image = None, pos=(0,0),defaultC = ""):
        super().__init__(color, width, height, image, defaultC)
        self.title = title
        self.font = font
        self.width = width
        self.height = height
        self.sprites = pygame.sprite.Group()
        self.titlecolor = titlecolor
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        titleT = self.font.render(self.title, True, self.titlecolor)
        titleTRect = titleT.get_rect(center=(self.rect.x + self.width/2, self.rect.y + 50))
        screen.blit(titleT, (self.rect.x +self.width/2 - titleTRect.width/2, self.rect.y + 50 - titleTRect.height/2.5))
        pygame.draw.line(screen, "black", (self.rect.x + 20, self.rect.y + 60 + titleTRect.height / 2), (self.rect.x + self.width - 20, self.rect.y + 60 + titleTRect.height / 2), width=5)
        self.sprites.draw(screen)
    
    def add(self, sprite):
        self.sprites.add(sprite)
        sprite.rect.x = self.rect.x + (self.width - sprite.rect.width) / 2
        sprite.rect.y = self.rect.y + 70*(len(self.sprites)+1) -30

if debug:
    test_button = Text("Test", font, (255, 255, 255), (640, 450))

    bg = Menu("red", "You Lose!", "white", font, 600, 600)
    bg.rect.x = 300
    bg.rect.y = 200
    all_sprites.add(bg)

    bg.add(test_button)
    bg.add(Text("Test", font, (255, 255, 255), (640, 450)))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                clickedSprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
                if test_button in clickedSprites:  
                    print("test")     
        
        screen.fill((0, 0, 0))
        bg.draw(screen)
        #test_button.draw(screen)
        pygame.display.flip()



    pygame.quit()
