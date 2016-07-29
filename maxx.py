#!/usr/bin/env python2.7
import pygame
import pygame.camera
from pygame.locals import *
import time
import RPi.GPIO as GPIO
import time

logf = open("log", "w")
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


DEVICE = '/dev/video0'
SIZE = (1280, 720)
#SIZE = (1366, 768)

def camstream():
    pygame.init()
    pygame.camera.init()
    STARTCOUNTER=0
    TIMER=0
    TIMERNOW=0
    display = pygame.display.set_mode(SIZE, FULLSCREEN)
    camera = pygame.camera.Camera(DEVICE, SIZE,"RGB")
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True
    TAKEN=0
    cheese="cheese.png"
    font = pygame.font.SysFont("comicsansms", 400)
    font2 = pygame.font.SysFont("comicsansms", 200)
    TAKING=0
    pygame.mouse.set_visible(0)
    LASTIMAGE=""
    while capture:
        screen = camera.get_image(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    capture = False
            elif event.type == pygame.MOUSEBUTTONUP:
                TIMER=time.time()
		STARTCOUNTER=1;
        if STARTCOUNTER==1:
                print "TAKEN: " + str(TAKEN)
                TIMERNOW=time.time() - TIMER
                TIMERNOW=round(TIMERNOW)
                if TIMERNOW == 0:
                    text = font.render("3", True, (255,255,255))
		    screen.blit(text,(640 - text.get_width() // 2, 240 - text.get_height() // 2))
                if TIMERNOW == 1:
                    text = font.render("2", True, (255,255,255))
		    screen.blit(text,(640 - text.get_width() // 2, 240 - text.get_height() // 2))
                if TIMERNOW == 2:
                    text = font.render("1", True, (255,255,255))
		    screen.blit(text,(640 - text.get_width() // 2, 240 - text.get_height() // 2))
                if (TIMERNOW >= 3) and (TIMERNOW < 10):
                    if TAKEN == 0:
                        TAKEN = 1
		        TIME=str(time.time()) + ".jpg"
		        TIME="images/"+TIME
                        print "Image: " + TIME
                        pygame.image.save(screen, TIME)
                        LASTIMAGE=TIME
                    bg = pygame.image.load(LASTIMAGE)
                    text = font2.render("CHEESE!!!", True, (255,255,255))
                    img=pygame.image.load(cheese)
                    screen.blit(bg,(0,0))
                    screen.blit(img,(540,440)) 
		    screen.blit(text,(640 - text.get_width() // 2, 240 - text.get_height() // 2))
                if TIMERNOW > 10:
                    TAKING=0
                    STARTCOUNTER=0
                    TAKEN=0
                print TIMERNOW

        display.blit(screen, (0,0))
        pygame.display.flip()
	input_state = GPIO.input(18)
        if input_state == False:
            if TAKING == 0:
                print "Button Pushed!!"
                TIMER=time.time()
                STARTCOUNTER=1
                TAKING=1
    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
