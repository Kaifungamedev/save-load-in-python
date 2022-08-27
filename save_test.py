# Imports
import sys
import pygame
import tkinter as tk
from tkinter import filedialog
import json
from pygame.locals import *
from pygame_Textinput import *
root = tk.Tk()
root.withdraw()

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height), NOFRAME ,32)
pygame.display.set_caption("import export test")
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
font = pygame.font.SysFont('Arial', 40)
textinputX = 10
textinputY = 430
objects = []
importedText = "example text"


class Button():

    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


class Rect(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface(
            (width, textinputY))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=pos)


fontsize = 25
font = pygame.font.SysFont("Consolas", fontsize)
manager = TextInputManager(validator=lambda input: len(input) <= 35)
textinput_custom = TextInputVisualizer(manager=manager, font_object=font)


def open_file():
    global importedText
    importedText = filedialog.askopenfilename(filetypes=(
        ("Lil brute save file", "*.json"), ("All Files", "*.*")))
    import_text()


def import_text():
    global importedText
    f = open(importedText)
    data_load = json.load(f)
    importedText = data_load['Text']['text']


def export():
    data = {}

    data['Text'] = {'text': f"{textinput_custom.value}"}

    with open('data.json', 'w') as f:
        json.dump(data, f)


export_button = Button(540, 420, 100, 60, 'export', export)
quit_button = Button(540, 0, 100, 50, 'QUIT', sys.exit)
import_button = Button(0, 0, 100, 50, 'import', open_file)

pygame.key.set_repeat(200, 25)
player = pygame.sprite.GroupSingle()
# Game loop.
while True:
    screen.fill((20, 20, 20))

    # Feed it with events every frame
    textinput_custom.update(pygame.event.get())

    # Get its surface to blit onto the screen
    player_sprite = Rect((0, textinputY - 10))
    player.add(player_sprite)
    player.draw(screen)
    screen.blit(textinput_custom.surface,
                (textinputX, textinputY))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(
                f"User pressed enter! Input so far: {textinput_custom.value}")

    text = font.render(importedText, True, green, blue)
    instructions = pygame.font.SysFont("Consolas", 18).render(
        "first type a message in the text box below then press export.", True, white)
    instructions2 = pygame.font.SysFont("Consolas", 18).render(
        "then press import and then import data.json", True, white)
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    for object in objects:
        object.process()
    screen.blit(text, (width / len(importedText), 390))
    screen.blit(instructions,  (10, (height // 2) + 2))
    screen.blit(instructions2,  (10, (height // 2) + (2 * 18)))
    pygame.display.flip()
    pygame.display.update()
    fpsClock.tick(fps)
