#!/usr/bin/env python
# -*- coding: utf-8 -*-
# raspberry pi, fullscreen
# python3 lucky-kitty.py -p -f
# OSX Testing
# python3 lucky-kitty.py -d
# Override forcewin = None to force a particular winstate for testing
# Runs on startup via ~/.config/autostart/lk.desktop

import pygame
import random
from pygame.locals import *
from random import randrange
from sys import argv
from getopt import getopt, GetoptError

##new lucky kitty specific stuff
import serial
from gpiozero import Button

VERSION = "0.2"

# the game###########################
class Game:
    def __init__(self, dbg, fw):
        self.initial_render = True
        self.wins = None
        self.show = {}
        self.debug = dbg
        self.forcewin = fw
        
        self.screen = screen
        self.xoffsets = [-6, 214, 434]
        self.yoffsets = [-2, 160, 322]
        # COMMENT OUT ON OSX FOR TESTING
        if not self.debug:
            self.handle = Button(4)
        
        self.bsound = pygame.mixer.Sound("assets/_sounds/CLICK10A.WAV")
        
        # Default
        self.oneup = pygame.mixer.Sound("assets/_sounds/1up16.wav")
        self.coin = pygame.mixer.Sound("assets/_sounds/coin16.wav")
        self.loss = pygame.mixer.Sound("assets/_sounds/loss16.wav")
        self.reel = pygame.mixer.Sound("assets/_sounds/reel16.wav")
        self.rstop = pygame.mixer.Sound("assets/_sounds/rstop16.wav")

        # Demma Wedding
        self.emma = pygame.mixer.Sound("assets/themes/demma_wedding/sounds/1-emma.wav")
        self.dom = pygame.mixer.Sound("assets/themes/demma_wedding/sounds/2-dom.wav")
        self.belltent = pygame.mixer.Sound("assets/themes/demma_wedding/sounds/3-belltent.wav")
        self.cheesy = pygame.mixer.Sound("assets/themes/demma_wedding/sounds/4-cheesypotatoes.wav")
        self.nix = pygame.mixer.Sound("assets/themes/demma_wedding/sounds/5-nixandq.wav")
        self.tarna = pygame.mixer.Sound("assets/themes/demma_wedding/sounds/6-tarna.wav")
        self.penrose = pygame.mixer.Sound("assets/themes/demma_wedding/sounds/7-penrose.wav")
        
        # Default
        self.cmdLoss = b'\x07'
        self.cmdDone = b'\x09'

        # Demma Wedding
        self.winEmma = b'\x40'
        self.winDom = b'\x41'
        self.winBelltent = b'\x42'
        self.winCheesy = b'\x43'
        self.winNix = b'\x44'
        self.winTarna = b'\x45'
        self.winPenrose = b'\x46'
        
        # Maybe change this to just be the one black line across
        self.windowlayer = pygame.image.load("assets/_images/gradient.png")

        # Demma Wedding
        self.imgpaths = ["assets/themes/demma_wedding/images/1-emma.png",
                        "assets/themes/demma_wedding/images/2-dom.png",
                        "assets/themes/demma_wedding/images/3-belltent.png",
                        "assets/themes/demma_wedding/images/4-cheesypotatoes.png",
                        "assets/themes/demma_wedding/images/5-nixandq.png",
                        "assets/themes/demma_wedding/images/6-tarna.png",
                        "assets/themes/demma_wedding/images/7-penrose.png"]
        self.imgEmma = pygame.image.load(self.imgpaths[0])
        self.imgDom = pygame.image.load(self.imgpaths[1])
        self.imgBelltent = pygame.image.load(self.imgpaths[2])
        self.imgCheesy = pygame.image.load(self.imgpaths[3])
        self.imgNix = pygame.image.load(self.imgpaths[4])
        self.imgTarna = pygame.image.load(self.imgpaths[5])
        self.imgPenrose = pygame.image.load(self.imgpaths[6])
        
        self.img = [self.imgEmma,
                    self.imgDom,
                    self.imgBelltent,
                    self.imgCheesy,
                    self.imgNix,
                    self.imgTarna,
                    self.imgPenrose]

        # Randomize and update the images without actually doing the roll 
        self.randi()
        self.screen.fill([0, 0, 0])
        self.drawl()
        self.screen.blit(self.windowlayer, (0, 0))
        pygame.display.update()
        
        # mainloop
        while True:
            # COMMENT OUT ON OSX FOR TESTING
            if not self.debug and self.handle.is_pressed:
                self.playgame()
                print("Starting new round!")
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        self.bsound.play()
                        if event.key == pygame.K_LEFT:
                            self.playgame()
                            print("Starting new round!")

    def playgame(self):
        self.randi()
        self.roll(self.img)
        #reused
        self.drawl()
        self.screen.blit(self.windowlayer, (0, 0))
        #/reused
        pygame.display.update()
        self.winner()

    # Does the actual scrolling thing
    #Todo(mje): Make it so the top and bottom images are partially cut off
    #Todo: Make the images roll slower
    # Make the window border the full size we want it to be,
    # or else draw it manually
    def roll(self, img):
        szam = 0
        self.reel.play(loops=-1)
        
        # roll time
        #Todo: understand what this timing actually is (higher number is longer)
        rolla = randrange(30, 50)
        rollb = randrange(rolla+1, rolla+5)
        rollc = randrange(rollb+1, rollb+5)
        
        # a column
        rollaf = []
        rollaf.append(img[self.imgpaths.index(self.show[0])-1])
        rollaf.append(img[self.imgpaths.index(self.show[1])-1])
        rollaf.append(img[self.imgpaths.index(self.show[2])-1])
        while szam <= rolla:
            rollaf.append(img[randrange(0, 7)])
            szam = szam + 1
            
        szam = 0
        
        # b column
        rollbf = []
        rollbf.append(img[self.imgpaths.index(self.show[3])-1])
        rollbf.append(img[self.imgpaths.index(self.show[4])-1])
        rollbf.append(img[self.imgpaths.index(self.show[5])-1])
        while szam <= rollb:
            rollbf.append(img[randrange(0, 7)])
            szam = szam +1
            
        szam = 0
        
        # c column
        rollcf = []
        rollcf.append(img[self.imgpaths.index(self.show[6])-1])
        rollcf.append(img[self.imgpaths.index(self.show[7])-1])
        rollcf.append(img[self.imgpaths.index(self.show[8])-1])
        while szam <= rollc:
            rollcf.append(img[randrange(0, 7)])
            szam = szam +1
        
        szama = len(rollaf)-1
        szamb = len(rollbf)-1
        szamc = len(rollcf)-1
        
        #TODO: this is probably about where we need to do the slowdown
        while szamc > 2:
            self.screen.fill([0, 0, 0])
#             self.screen.blit(self.background, (0, 0))
            
            if szama > 2:
                self.screen.blit(rollaf[len(rollaf)-3], (self.xoffsets[0], self.yoffsets[0]))
                self.screen.blit(rollaf[len(rollaf)-2], (self.xoffsets[0], self.yoffsets[1]))
                self.screen.blit(rollaf[len(rollaf)-1], (self.xoffsets[0], self.yoffsets[2]))
                szama = szama - 1
                del(rollaf[len(rollaf)-1])
            else:
                self.screen.blit(rollaf[len(rollaf)-3], (self.xoffsets[0], self.yoffsets[0]))
                self.screen.blit(rollaf[len(rollaf)-2], (self.xoffsets[0], self.yoffsets[1]))
                self.screen.blit(rollaf[len(rollaf)-1], (self.xoffsets[0], self.yoffsets[2]))
                
            if szamb > 2:
                self.screen.blit(rollbf[len(rollbf)-3], (self.xoffsets[1], self.yoffsets[0]))
                self.screen.blit(rollbf[len(rollbf)-2], (self.xoffsets[1], self.yoffsets[1]))
                self.screen.blit(rollbf[len(rollbf)-1], (self.xoffsets[1], self.yoffsets[2]))
                szamb = szamb - 1
                del(rollbf[len(rollbf)-1])
            else:
                self.screen.blit(rollbf[len(rollbf)-3], (self.xoffsets[1], self.yoffsets[0]))
                self.screen.blit(rollbf[len(rollbf)-2], (self.xoffsets[1], self.yoffsets[1]))
                self.screen.blit(rollbf[len(rollbf)-1], (self.xoffsets[1], self.yoffsets[2]))
                
            if szamc > 2:
                self.screen.blit(rollcf[len(rollcf)-3], (self.xoffsets[2], self.yoffsets[0]))
                self.screen.blit(rollcf[len(rollcf)-2], (self.xoffsets[2], self.yoffsets[1]))
                self.screen.blit(rollcf[len(rollcf)-1], (self.xoffsets[2], self.yoffsets[2]))
                szamc = szamc - 1
                del(rollcf[len(rollcf)-1])
            else:
                self.screen.blit(rollcf[len(rollcf)-3], (self.xoffsets[2], self.yoffsets[0]))
                self.screen.blit(rollcf[len(rollcf)-2], (self.xoffsets[2], self.yoffsets[1]))
                self.screen.blit(rollcf[len(rollcf)-1], (self.xoffsets[2], self.yoffsets[2]))
            
            self.screen.blit(self.windowlayer, (0, 0))
            pygame.display.update()
            rollc = rollc - 1
        self.reel.stop()
        self.rstop.play()
    
    def drawl(self):
        #blit(image, (x,y to load it in)
        self.screen.blit(pygame.image.load(self.show[0]), (self.xoffsets[0], self.yoffsets[0]))
        self.screen.blit(pygame.image.load(self.show[1]), (self.xoffsets[0], self.yoffsets[1]))
        self.screen.blit(pygame.image.load(self.show[2]), (self.xoffsets[0], self.yoffsets[2]))
        self.screen.blit(pygame.image.load(self.show[3]), (self.xoffsets[1], self.yoffsets[0]))
        self.screen.blit(pygame.image.load(self.show[4]), (self.xoffsets[1], self.yoffsets[1]))
        self.screen.blit(pygame.image.load(self.show[5]), (self.xoffsets[1], self.yoffsets[2]))
        self.screen.blit(pygame.image.load(self.show[6]), (self.xoffsets[2], self.yoffsets[0]))
        self.screen.blit(pygame.image.load(self.show[7]), (self.xoffsets[2], self.yoffsets[1]))
        self.screen.blit(pygame.image.load(self.show[8]), (self.xoffsets[2], self.yoffsets[2]))

    # random images
    def randi(self):
        self.show = {}    
            
        # Outcome odds
        rand = randrange(1, 100)
        outcome = None

        if not self.initial_render:
            if 1 <= rand <= 10:
                outcome = self.imgpaths[0]
            elif 11 <= rand <= 20:
                outcome = self.imgpaths[1]
            elif 21 <= rand <= 30:
                outcome = self.imgpaths[2]
            elif 31 <= rand <= 40:
                outcome = self.imgpaths[3]
            elif 41 <= rand <= 50:
                outcome = self.imgpaths[4]
            elif 51 <= rand <= 60:
                outcome = self.imgpaths[5]
            elif 61 <= rand <= 70:
                outcome = self.imgpaths[6]

        self.initial_render = False

        if self.forcewin is not None:
            outcome = self.imgpaths[self.forcewin]

        # Display the correct slots without duplication
        left_slot = [0, 1 ,2]
        middle_slot = [3, 4 ,5]
        right_slot = [6, 7 ,8]

        used_win_index = [outcome] if outcome else []

        for slot in [left_slot, middle_slot, right_slot]:
            used_slot_index = []

            for index, space in enumerate(slot):
                possible_options = [v for v in range(len(self.imgpaths)) if v not in used_win_index and v not in used_slot_index]

                if index == 1:
                    #win_slot
                    val = self.imgpaths.index(outcome) if outcome else random.choice(possible_options)
                    self.show[space] = outcome if outcome else self.imgpaths[val]
                    used_win_index.append(val)
                else:
                    val = random.choice(possible_options)
                    self.show[space] = self.imgpaths[val]
                    used_slot_index.append(val)

    # Checks if any of your lines have won
    def check(self):
        if self.show[1] == self.show[4] == self.show[7]:
            pygame.draw.line(self.screen, [255, 20, 147], (self.xoffsets[0], 239), (self.xoffsets[2] + 213, 239), 8)
            self.wins = self.show[1]
        else:
            self.wins = None
   
    def winner(self):
        while pygame.mixer.get_busy():
            pass
        
        self.check()
        pygame.display.update()
        
        print("WIN STATE:")
        print(self.wins)
            
        if not self.debug:
            if self.wins is not None:
                index = self.imgpaths.index(self.wins)
                # Demma wedding
                if index == 0:
                    self.emma.play()
                    self.sendandwait(self.winEmma)

                    ser.write(self.cmdDone)
                    self.coin.play()
                    while pygame.mixer.get_busy():
                        pass

                    self.sendandwait(self.cmdDone)
                elif index == 1:
                    self.dom.play()
                    self.sendandwait(self.winDom)

                    ser.write(self.cmdDone)
                    self.coin.play()
                    while pygame.mixer.get_busy():
                        pass

                    self.sendandwait(self.cmdDone)
                elif index == 2:
                    self.belltent.play()
                    self.sendandwait(self.winBelltent)

                    # Wait for belltent track to finish
                    while pygame.mixer.get_busy():
                        pass
                    ser.write(self.cmdDone)

                    self.coin.play()
                    while pygame.mixer.get_busy():
                        pass

                    self.sendandwait(self.cmdDone)
                elif index == 3:
                    self.cheesy.play()
                    self.sendandwait(self.winCheesy)
                    self.sendandwait(self.cmdDone)
                elif index == 4:
                    self.nix.play()
                    self.sendandwait(self.winNix)
                    self.sendandwait(self.cmdDone)
                elif index == 5:
                    self.tarna.play()
                    self.sendandwait(self.winTarna)

                    ser.write(self.cmdDone)
                    self.coin.play()
                    while pygame.mixer.get_busy():
                        pass

                    self.sendandwait(self.cmdDone)
                elif index == 6:
                    self.penrose.play()
                    self.sendandwait(self.winPenrose)
                    self.sendandwait(self.cmdDone)
            else:
                self.loss.play()
                self.sendandwait(self.cmdLoss)
                self.sendandwait(self.cmdDone)
            
        print("Finished doing WINstate!")
    
    # Sends a command and waits for both thread and play to stop, eg. #b"Hello from Raspiberry Pi!\n"
    def sendandwait(self, cmd):
        ser.write(cmd)
        #TODO(mje): Might need to make sure we're flushing our buffer whenever we send something here
        print("Waiting for music to finish")
        while pygame.mixer.get_busy():
            pass
        print("Waiting for arduino")        
        while not (ser.in_waiting > 0):
            pass
            
        byte = ser.read(1)
        if not byte == self.cmdDone:
            print("Got an unexpected command")
        print("Arduino finished!")
        print(byte)
        
def help():
    print("Lucky Kitty help: eg. python3 lucky-kitty.py -p -f")
    print("Options:")
    print("-h, --help        display this help message")
    print("-v, --version     display game version")
    print("-f, --fullscreen  run in fullscreen mode")
    print("-p, --pi          run in raspberry pi mode")
    print("-d, --debug       run in debug mode")
    print("-w, --win         force winstate")
    print("Contact: everson.mike@gmail.com")

if __name__ == "__main__":
    fullscreen = False
    pi = False
    debug = False
    # Override this to test a specific win state, 0-8
    forcewin = None
    
    try:
        short = "hvfpd"
        long = ["help", "version", "fullscreen", "pi", "debug"]
        opts = getopt(argv[1:], short, long)[0]
    except GetoptError as e:
        print("Problem getting the options")
        print(e)
        help()
        exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            exit()
        if opt in ("-v", "--version"):
            print("Lucky Kitty - version: "+ VERSION)
            exit()
        if opt in ("-f", "--fullscreen"):
            fullscreen = True
        if opt in ("-p", "--pi"):
            pi = True
        if opt in ("-d", "--debug"):
            debug = True
                
         
    # Setup serial communication
    if not debug:
        if pi:
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
        else:        
            ser = serial.Serial('/dev/cu.usbmodem85842801', 9600, timeout=5)
        ser.flush()
            
    # pygame init, set display
    pygame.init()
    
    if not fullscreen:
        screen = pygame.display.set_mode([640, 480], 0, 24)
    else:
        screen = pygame.display.set_mode([640, 480], pygame.FULLSCREEN)

    pygame.display.set_caption("Lucky Kitty MkII")
    pygame.mouse.set_visible(False)

    plc = Game(debug, forcewin) 
    pygame.display.update()
