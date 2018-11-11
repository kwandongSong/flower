import serial
import pygame
import threading
from time import sleep
import datetime
import os
#from PIL import Image

WHITE = (255,255,255) # white RGB
pad_width = 1500
pad_height = 900

def gainsensorval():
	global temsenval, soilsenval, getsuccessflag
	getsuccessflag=0
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1.5)
	sumoutput = ser.readline()
	output= str(sumoutput)
	output= output.replace("b'","")
	output= output.replace("\\r\\n'","")
	finaldata= output.split("*")
	print(finaldata)
	if finaldata[0] == " ":
		finaldata[0] = 24
	if finaldata[0] != "'":
		temsenval =float(finaldata[0])
		soilsenval =int(finaldata[1])
		getsuccessflag=1
		print(temsenval)
		print(soilsenval)
def runGame():
	global back, gamepad, clock, getsuccessflag, speakflag, mind, Y_angry, Y_bad, Y_perfect, A_angry, A_bad, A_perfect
	mind=2
	speakflag=0
	count=0
	x=pad_width*0.5
	y=pad_height*0.2
	x_change=5
	y_change=-30
	crashed = False
	gainsensorval()

	while not crashed:
		getsuccessflag=0
		count = count+1
		now=datetime.datetime.now()
		nowhour= now.strftime('%M')
		nowsec= now.strftime('%S')
		nowhour=int(nowhour)
		nowsec=int(nowsec)
		if nowhour%1 ==0 and nowsec%10 == 0: #2minute
			while getsuccessflag != 1:
				gainsensorval()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL:
					crashed = True
		if x>1100:
			x_change= -5
			Y_perfect = pygame.image.load('pic/good.png')
			Y_angry = pygame.image.load('pic/angry.png')
			Y_bad = pygame.image.load('pic/bad.png')
			A_angry = pygame.image.load('pic/Flower_angry.png')
			A_bad = pygame.image.load('pic/Flower_bad.png')
			A_perfect = pygame.image.load('pic/Flower_good.png')
		elif x<10:
			x_change= 5
			Y_perfect = pygame.image.load('pic/goodR.png')
			Y_angry = pygame.image.load('pic/angryR.png')
			Y_bad = pygame.image.load('pic/badR.png')
			A_angry = pygame.image.load('pic/Flower_angryR.png')
			A_bad = pygame.image.load('pic/Flower_badR.png')
			A_perfect = pygame.image.load('pic/Flower_good.png')
		x += x_change
		if count%30 == 0:
			y += y_change
			y_change=-y_change
		if count == 100:
			count=0

	#	gamepad.fill(WHITE)
		background(0,0)
		getlength(x,y)

		statusmessage(x+250,y-150)
		if mind == 0 and speakflag != 1:
				os.system('omxplayer badbad.wav')
				speakflag = 1
		if mind == 2 and speakflag != 2:
				os.system('omxplayer verygood.wav')
				speakflag = 2
		#sleep(0.1)
		pygame.display.update()
		clock.tick(60)
	pygame.quit()
def background(x,y):
	global gamepad, back
	gamepad.blit(back,(x,y))
def initGame():
	global back,gamepad, clock, M_temhigh, M_temlow, M_all_bad, M_humidlow, M_allgood, Y_perfect, Y_angry, Y_bad, A_angry, A_bad, A_perfect # use global var

	pygame.init() # lib init
	gamepad = pygame.display.set_mode((pad_width,pad_height),pygame.FULLSCREEN) # display use
	pygame.display.set_caption('Smart flower') # name
	M_temhigh = pygame.image.load('pic/hot.png')
	M_temlow = pygame.image.load('pic/cold.png')
	M_all_bad=pygame.image.load('pic/coldhot.png')
	M_humidlow=pygame.image.load('pic/water.png')
	M_allgood=pygame.image.load('background.png')
	Y_perfect = pygame.image.load('pic/goodR.png')
	Y_angry = pygame.image.load('pic/angryR.png')
	Y_bad = pygame.image.load('pic/badR.png')
	A_angry = pygame.image.load('pic/Flower_angryR.png')
	A_bad = pygame.image.load('pic/Flower_badR.png')
	A_perfect = pygame.image.load('pic/Flower_goodR.png')
	back = pygame.image.load('pic/colorbackground.png')
	clock = pygame.time.Clock() # set frame
	runGame()
def getlength(x,y):
	global gamepab, length, whatgrow, Y_perfect, Y_bad, Y_angry, A_perfect, A_bad, A_angry, mind
	length=5
	if length >0 and length <= 10:
		whatgrow=0
		if mind == 2:
			gamepad.blit(Y_perfect,(x,y))
		elif mind == 1:
			gamepad.blit(Y_bad,(x,y))
		elif mind == 0:
			gamepad.blit(Y_angry,(x,y))
		 #baby
	elif length >10 and length <= 20:
		whatgrow=1
		if mind == 2:
			gamepad.blit(A_perfect,(x,y))
		elif mind == 1:
			gamepad.blit(A_bad,(x,y))
		elif mind == 0:
			gamepad.blit(A_angry,(x,y))
		 #adult

#	elif length >20 and length <=30:
#		gamepad.blit(grown,(x,y))
def statusmessage(x,y):
	global gamepad, whatgrow, temsenval, soilsenval, speakflag, M_temhigh, M_temlow, M_all_bad, M_humidlow, Y_perfect, Y_angry, Y_bad, A_angry, A_bad, A_perfect, mind
		#mind 2good  1bad  0angry
	if temsenval <10: #tem low
		if soilsenval <400: #humid low
			gamepad.blit(M_all_bad,(x,y)) #tem low & humid low
	#		speakflag =1
			mind=0
		else:
			gamepad.blit(M_temlow,(x,y)) #only tem low
	#		speakflag =1
			mind=1
	elif temsenval >25: #tem high
		if soilsenval <400: #humid low
			gamepad.blit(M_all_bad,(x,y)) #tem high & humid low
	#		speakflag =2
			mind=0
		else:
			gamepad.blit(M_temhigh,(x,y)) #only tem high
	#		speakflag =2
			mind=1
	elif 10 <= temsenval:
		if soilsenval <400: #humid low
			gamepad.blit(M_humidlow,(x,y)) #only humid low
	#		speakflag =3
			mind=1
	#		os.system('omxplayer Y_cold.wav')
		elif soilsenval >= 400:
			gamepad.blit(M_allgood,(x,y)) #both good~!
	#		speakflag =3
			mind=2
initGame()
