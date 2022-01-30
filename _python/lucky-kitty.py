#!/usr/bin/env python
# -*- coding: utf-8 -*-
# raspberry pi, fullscreen
# python3 lucky-kitty.py -p -f
# OSX Testing
# python3 lucky-kitty.py -d
# Override forcewin = None to force a particular winstate for testing

import pygame
from pygame.locals import *
from random import randrange
from sys import argv
from getopt import getopt, GetoptError

##new lucky kitty specific stuff
import serial
from gpiozero import Button

VERSION = "0.1"

# the game###########################
class Game:
    def __init__(self, dbg, fw):
        self.wins = None
        self.show = {}
        self.debug = dbg
        self.forcewin = fw
        
        self.screen = screen
        self.xoffsets = [0, 214, 428]
        self.yoffsets = [0, 160, 320]
        # COMMENT OUT ON OSX FOR TESTING
        if not self.debug:
            self.handle = Button(4)
        
        self.bsound = pygame.mixer.Sound("_assets/_sounds/CLICK10A.WAV")
        
        # Default
        self.oneup = pygame.mixer.Sound("_assets/_sounds/1up16.wav")
        self.coin = pygame.mixer.Sound("_assets/_sounds/coin16.wav")
        self.loss = pygame.mixer.Sound("_assets/_sounds/loss16.wav")
        self.reel = pygame.mixer.Sound("_assets/_sounds/reel16.wav")
        self.rstop = pygame.mixer.Sound("_assets/_sounds/rstop16.wav")
        
#         self.cheesy = pygame.mixer.Sound("_assets/_sounds/cheesy16.wav")
#         self.hth = pygame.mixer.Sound("_assets/_sounds/hth16.wav")
#         self.nyan = pygame.mixer.Sound("_assets/_sounds/nyan16.wav")
#         self.pinchy = pygame.mixer.Sound("_assets/_sounds/pinchy16.wav")
#         self.scream = pygame.mixer.Sound("_assets/_sounds/scream16.wav")
#         self.jackpot = pygame.mixer.Sound("_assets/_sounds/nyan16.wav")
        
        # Arno
        self.bast = pygame.mixer.Sound("_assets/_sounds/bast.wav")
        self.poutine = pygame.mixer.Sound("_assets/_sounds/poutine.wav")
        
        # Emma
        self.shera = pygame.mixer.Sound("_assets/Emma Theme/Sounds/shera.wav")
        self.nitrous = pygame.mixer.Sound("_assets/Emma Theme/Sounds/nitrous.wav")
        self.jabba = pygame.mixer.Sound("_assets/Emma Theme/Sounds/jabba.wav")
        self.cheese = pygame.mixer.Sound("_assets/Emma Theme/Sounds/cheese.wav")
        self.gremlin = pygame.mixer.Sound("_assets/Emma Theme/Sounds/gremlin.wav")
#         self.insurance = pygame.mixer.Sound("_assets/Emma Theme/Sounds/nyan16.wav")
        self.moar = pygame.mixer.Sound("_assets/Emma Theme/Sounds/moar.wav")
#         self.princess = pygame.mixer.Sound("_assets/Emma Theme/Sounds/reel16.wav")
        self.cats = pygame.mixer.Sound("_assets/Emma Theme/Sounds/nixnq.wav")
        
        # Default
        self.cmdLoss = b'\x07'
        self.cmdDone = b'\x09'
#         self.winNyan = b'\x00'
#         self.winTentacle = b'\x01'
#         self.winCoin = b'\x02'
#         self.winFire = b'\x03'
#         self.winCheese = b'\x04'
#         self.winPinchy = b'\x05'
#         self.winJackpot = b'\x06'

        # Arno
#         self.winBast = b'\x20'
#         self.winPoutine = b'\x21'

        # Emma
        self.winShera = b'\x30'
        self.winNitrous = b'\x31'
        self.winJabba = b'\x32'
        self.winCheese = b'\x33'
        self.winGremlin = b'\x34'
#         self.winInsurance = b'\x35'
        self.winMoar = b'\x36'
#         self.winPrincess = b'\x37'
        self.winCats = b'\x38'
        
        # Maybe change this to just be the one black line across
        self.windowlayer = pygame.image.load("_assets/_images/gradient.png")
        
        # Default + Arno
#         self.imgpaths = ["_assets/_images/0004_nyan.png", "_assets/_images/0002_tentacle.png", "_assets/_images/0007_coin.png", "_assets/_images/0006_fireflower.png", "_assets/_images/0008_cheese-ball.png", "_assets/_images/0003_pinchy.png", "_assets/_images/0005_lucky-kitty.png", "_assets/_images/0000_bast.png", "_assets/_images/0001_poutine.png"]
#         self.imgnyan = pygame.image.load(self.imgpaths[0])
#         self.imgtent = pygame.image.load(self.imgpaths[1])
#         self.imgcoin = pygame.image.load(self.imgpaths[2])
#         self.imgfire = pygame.image.load(self.imgpaths[3])
#         self.imgcheese = pygame.image.load(self.imgpaths[4])
#         self.imgpinchy = pygame.image.load(self.imgpaths[5])
#         self.imgjackpot = pygame.image.load(self.imgpaths[6])
#         self.imgbast = pygame.image.load(self.imgpaths[7])
#         self.imgpoutine = pygame.image.load(self.imgpaths[8])

#         self.img = [self.imgnyan,
#                     self.imgtent,
#                     self.imgcoin,
#                     self.imgfire,
#                     self.imgcheese,
#                     self.imgpinchy,
#                     self.imgjackpot,
#                     self.imgbast,
#                     self.imgpoutine]

        # Emma
        self.imgpaths = ["_assets/Emma Theme/Images/0001_shera.png",
                         "_assets/Emma Theme/Images/0004_nitrous.png",
                         "_assets/Emma Theme/Images/0000_jabba.png",
                         "_assets/Emma Theme/Images/0002_cheese.png",
                         "_assets/Emma Theme/Images/gremlin.png",
                         "_assets/Emma Theme/Images/0006_insurance.png",
                         "_assets/Emma Theme/Images/0007_moar.png",
                         "_assets/Emma Theme/Images/0005_brat.png",
                         "_assets/Emma Theme/Images/0003_nixnq.png"]
        self.imgShera = pygame.image.load(self.imgpaths[0])
        self.imgNitrous = pygame.image.load(self.imgpaths[1])
        self.imgJabba = pygame.image.load(self.imgpaths[2])
        self.imgCheese = pygame.image.load(self.imgpaths[3])
        self.imgGremlin = pygame.image.load(self.imgpaths[4])
        self.imgInsurance = pygame.image.load(self.imgpaths[5])
        self.imgMoar = pygame.image.load(self.imgpaths[6])
        self.imgBrat = pygame.image.load(self.imgpaths[7])
        self.imgCats = pygame.image.load(self.imgpaths[8])
        
        self.img = [self.imgShera,
                    self.imgNitrous,
                    self.imgJabba,
                    self.imgCheese,
                    self.imgGremlin,
                    self.imgInsurance,
                    self.imgMoar,
                    self.imgBrat,
                    self.imgCats]

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
            
        ##todo(mje): tweak the odds for outcomes
        rand = randrange(1, 100)
        outcome = None
        if 1 <= rand <= 8:
            outcome = self.imgpaths[0]
        elif 9 <= rand <= 15:
            outcome = self.imgpaths[1]
        elif 16 <= rand <= 22:
            outcome = self.imgpaths[2]
        elif 23 <= rand <= 29:
            outcome = self.imgpaths[3]
        elif 30 <= rand <= 36:
            outcome = self.imgpaths[4]
        elif 37 <= rand <= 43:
            outcome = self.imgpaths[5]
        elif 44 <= rand <= 50:
            outcome = self.imgpaths[6]
        elif 51 <= rand <= 57:
            outcome = self.imgpaths[7]
        elif 58 <= rand <= 65:
            outcome = self.imgpaths[8]
        
        #DEBUG: Uncomment this line and comment the rest to test a specific outcome
        if self.forcewin is not None:
            outcome = self.imgpaths[self.forcewin]
            
        for i in range(9):
            idx = randrange(7)
            self.show[i] = self.imgpaths[idx]
            
            # Most of this code is to ensure we don't display too many matching symbols regardless of win condition
            #todo(mje): Nicer - pick an outcome, then for each of the other slots randomize until they dont match the middle ones
            if outcome is None and i == 4 and idx == self.show[1]:
                newIdx = idx % 6
                self.show[i] = self.imgpaths[newIdx]
            elif outcome is not None and i in {1, 4, 7}:
                self.show[i] = outcome
            elif outcome is not None and i in {0, 3, 6} and self.show[i] == outcome:
                self.show[i] = self.imgpaths[(idx + 1) % 6]
            elif outcome is not None and i in {2, 5, 8} and self.show[i] == outcome:
                self.show[i] = self.imgpaths[(idx + 2) % 6]
   
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
                # Default + Arno
#                 if index == 0:
#                     self.nyan.play()
#                     self.sendandwait(self.winNyan)
#                     self.sendandwait(self.cmdDone) #maybe a reset instead, no need to wait?
#                 elif index == 1:
#                     self.scream.play()
#                     self.sendandwait(self.winTentacle)
#                     self.sendandwait(self.cmdDone)
#                 elif index == 2:
#                     self.coin.play()
#                     self.sendandwait(self.winCoin)
#                     self.oneup.play()
#                     
#                     while pygame.mixer.get_busy():
#                         pass
#                     
#                     self.sendandwait(self.cmdDone)
#                 elif index == 3:
#                     self.hth.play()
#                     self.sendandwait(self.winFire)
#                     self.sendandwait(self.cmdDone)
#                 elif index == 4:
#                     self.cheesy.play()
#                     self.sendandwait(self.winCheese)
#                     self.sendandwait(self.cmdDone)
#                 elif index == 5:
#                     self.pinchy.play()
#                     self.sendandwait(self.winPinchy)
#                     self.sendandwait(self.cmdDone)
#                 elif index == 6:
#                     self.jackpot.play()
#                     # Do all the lights and fire
#                     self.sendandwait(self.winJackpot) 
#                     
#                     ser.write(self.cmdDone)
#                     # play the coin sound and dispense a coin 3 times
#                     for _ in range(3):
#                         self.coin.play()
#                         while pygame.mixer.get_busy():
#                             pass
# 
#                     self.oneup.play()
#                     while pygame.mixer.get_busy():
#                         pass
# 
#                     self.sendandwait(self.cmdDone)
#                 elif index == 7:
#                     self.bast.play()
#                     self.sendandwait(self.winBast)
#                     
#                     ser.write(self.cmdDone)
#                     self.coin.play()
#                     while pygame.mixer.get_busy():
#                         pass
#                     
#                     self.sendandwait(self.cmdDone)
#                 elif index == 8:
#                     self.poutine.play()
#                     self.sendandwait(self.winPoutine)
#     
#                     ser.write(self.cmdDone)
#                     self.coin.play()
#                     while pygame.mixer.get_busy():
#                         pass
#                     
#                     self.sendandwait(self.cmdDone)

                # Emma
                if index == 0:
                    self.shera.play()
                    print("sending win shera")
                    self.sendandwait(self.winShera)
                    print("sending done")
                    self.sendandwait(self.cmdDone) 
                elif index == 1:
                    self.nitrous.play()
                    self.sendandwait(self.winNitrous)
                    self.sendandwait(self.cmdDone)
                elif index == 2:
                    self.jabba.play()
                    self.sendandwait(self.winJabba)
                    self.sendandwait(self.cmdDone)
                elif index == 3:
                    self.cheese.play()
                    self.sendandwait(self.winCheese)
                    self.sendandwait(self.cmdDone)
                elif index == 4:
                    self.gremlin.play()
                    # Do all the lights and fire
                    self.sendandwait(self.winGremlin) 
                    
                    ser.write(self.cmdDone)
                    # play the coin sound and dispense a coin 3 times
                    for _ in range(3):
                        self.coin.play()
                        while pygame.mixer.get_busy():
                            pass

                    self.oneup.play()
                    while pygame.mixer.get_busy():
                        pass

                    self.sendandwait(self.cmdDone)
                elif index == 5:
                    self.loss.play()
                    self.sendandwait(self.cmdLoss)
                    self.sendandwait(self.cmdDone)
                elif index == 6:
                    self.moar.play()
                    self.sendandwait(self.winMoar)
    
                    ser.write(self.cmdDone)
                    self.coin.play()
                    while pygame.mixer.get_busy():
                        pass
                    
                    self.sendandwait(self.cmdDone)
                elif index == 7:
                    self.loss.play()
                    self.sendandwait(self.cmdLoss)
                    self.sendandwait(self.cmdDone)
                elif index == 8:
                    self.cats.play()
                    self.sendandwait(self.winCats)
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
            
        byte = ser.read(1);
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
    print("Contact: everson.mike@gmail.com")

if __name__ == "__main__":
    fullscreen = False
    pi = False
    debug = False
    
    try:
        short = "hvfpd"
        long = ["help", "version", "fullscreen", "pi", "debug"]
        opts = getopt(argv[1:], short, long)[0]
    except GetoptError:
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
    #TODO(MJE): How will this work when we boot up the pi cold, will we need to wait?
    # COMMENT OUT ON OSX FOR TESTING
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
    
    # Override this to test a specific win state, 0-8
    forcewin = None
    plc = Game(debug, forcewin) 
    pygame.display.update()
