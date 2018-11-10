
import pygame
WHITE = (255,255,255) # white RGB
pad_width = 600
pad_height = 400


def runGame():
	global gamepad, clock
	x=pad_width*0.05
	y=pad_height*0.8
	x_change=5
	y_change=0
	crashed = False

	while not crashed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
		if x>360:
			x_change=-5
		elif x<10:
			x_change=5
		x += x_change
		gamepad.fill(WHITE)
		flower(x,y)
		pygame.display.update()
		clock.tick(60)
	pygame.quit()
def initGame():
	global gamepad, clock, flowere # use global var

	pygame.init() # lib init
	gamepad = pygame.display.set_mode((pad_width,pad_height)) # display use
	pygame.display.set_caption('Smart flower') # name
	flowere = pygame.image.load('pika.png')
	clock = pygame.time.Clock() # set frame
	runGame()

def flower(x,y):
	global gamepad, flowere
	gamepad.blit(flowere,(x,y))

initGame()
