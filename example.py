import pygameGUI
import pygame
#imports my tetris and chess gamesh
pygame.init()
screen = pygame.display.set_mode((1280, 900))
running = True
pygame.display.set_caption("Menu")
all_sprites = pygame.sprite.Group()
font = pygame.font.Font('example/8bitFONT.ttf', 70)

test_button = pygameGUI.Button("Button", font, (255, 255, 255), (640, 450), lambda: print("test"))


bg = pygameGUI.Menu("You Lose!", "white", font, 600, 600,image="example/menuBG.png")
bg.rect.x = 300
bg.rect.y = 200
all_sprites.add(bg)

bg.add(test_button)
bg.add(pygameGUI.Text("Text", font, (255, 255, 255), (640, 450)))

man = pygameGUI.Manager("man")

d = pygameGUI.Dropdown("dropdown", font, "white", "black", (300,300),["test","test2","test3","test4"], scaleFactor=0.5)
ti = pygameGUI.TextInput("Input", font, (255, 255, 255), (640, 450))
bg.add(ti)
bg.add(d)
while running:
    for event in pygame.event.get():
        bg.input(event)
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    d.draw(screen)
    ti.draw(screen)
    bg.draw(screen)
    #test_button.draw(screen)
    pygame.display.flip()



pygame.quit()
