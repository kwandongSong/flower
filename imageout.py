
import pygame
WHITE = (255,255,255) # white RGB
pad_width = 600
pad_height = 400
def flower(x,y):
	global gamepad,aircraft
	gamepad.blit(aircraft,(x,y))

def runGame():
	global gamepad, clock
	x=pad_width*0.05
	y=pad_height*0.8
	y_change=0
	crashed = False

	while not crashed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
		gamepad.fill(WHITE)
		pygame.display.update()
		clock.tick(60)
	pygame.quit()
def initGame():
	global gamepad, clock # use global var
	pygame.init() # lib init
	gamepad = pygame.display.set_mode((pad_width,pad_height)) # display use
	pygame.display.set_caption('Smart flower') # name
	clock = pygame.time.Clock() # set frame
	runGame()
initGame()
