import pygame, sys, time, copy, random

FPS = 20
RIGHT = pygame.K_RIGHT
LEFT = pygame.K_LEFT
UP = pygame.K_UP
DOWN = pygame.K_DOWN
DISPLAY = (640,480)
SIZE = (20,20)
global RESTART
RESTART = False

x_coords = [False for i in range(0,DISPLAY[0]//SIZE[0])]
y_coords = [False for i in range(0,DISPLAY[1]//SIZE[1])]

class SnakeBody(pygame.sprite.Sprite):
	def __init__(self, next = None):
		pygame.sprite.Sprite.__init__(self)
		self.limit = pygame.display.get_surface().get_rect()
		self.image = pygame.Surface(SIZE)
		self.image.fill((0,0,0))
		self.rect = self.image.get_rect()
		self.direction = RIGHT
		self.isHead = False
		self.isTail = False
		self.next = next
		
class Prey(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface(SIZE)
		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.reinit()
		
	def reinit(self):
		while 1:
			i = random.randrange(0,DISPLAY[0],SIZE[0])//SIZE[0]
			j = random.randrange(0,DISPLAY[1],SIZE[0])//SIZE[0]
			if x_coords[i] is True or y_coords[j] is True: continue
			self.rect.topleft = (i*SIZE[0],j*SIZE[0])
			updateCoords(self.rect.topleft,True)
			break
		
	def eaten(self):
		updateCoords(self.rect.topleft,False)
		self.reinit()
		
class Box(pygame.sprite.Sprite):
	def __init__(self,text,font,focused):
		pygame.sprite.Sprite.__init__(self)
		self.not_focused = font.render(text,1,(0,0,0))
		self.focused = font.render(text,1,(255,0,0))
		self.focus = focused
		self.reinit()
		self.rect = self.image.get_rect()
	
	def update(self):
		self.reinit()
	
	def reinit(self):
		if self.focus: self.image = self.focused
		else: self.image = self.not_focused
	
		
def updateCoords(coords,to_state):
	x_coords[coords[0]//SIZE[0]] = to_state
	y_coords[coords[1]//SIZE[0]] = to_state
		

def updateSnake():
	global head,score,prey, RESTART
	sprite_list = snakeSprite.sprites()
	
	for s in sprite_list:
		if s.isHead:
			offsets = (0,0)
			if s.direction is UP: 		offsets = (0,-s.rect.w)
			elif s.direction is DOWN: 	offsets = (0,s.rect.w)
			elif s.direction is LEFT : 	offsets = (-s.rect.w,0)
			elif s.direction is RIGHT: 	offsets = (s.rect.w,0)
			
			temp = SnakeBody()
			temp.rect = s.rect.move(offsets)
			
			#collision detection
			if pygame.sprite.spritecollideany(temp, snakeSprite)\
			or not temp.limit.contains(temp.rect):
				RESTART = True
				return
			updateCoords(temp.rect.topleft,True)
			temp.isHead = True
			temp.isTail = False
			temp.direction = s.direction
			
			s.isHead = False
			s.next = temp
			head = temp
			
			snakeSprite.add(temp)
			
			if head.rect == prey.rect:
				score+=1
				prey.eaten()
				return
			break
			
	for s in sprite_list:
		if s.isTail:
			updateCoords(s.rect.topleft, False)
			s.next.isTail = True
			snakeSprite.remove(s)
			break
	
	pygame.event.pump()

#~ def replay():






#~ def main():
	#~ pygame.init()
	
	#~ screen = pygame.display.set_mode(DISPLAY)
	#~ background = pygame.Surface(screen.get_rect().size)
	#~ background.fill((255,255,255))
	#~ screen.blit(background,(0,0))
	#~ pygame.display.update()
	#~ return screen, background











def main():
	global RESTART, snakeSprite, head, prey, score
	global screen, background
	
	s1 = SnakeBody()
	s1.isHead = True
	s1.rect.topleft = s1.limit.topleft
	s2 = SnakeBody(s1)
	s2.isTail = True
	s2.rect.topright = s1.rect.topleft
	
	
	score = 0
	head = s1
	prey = Prey()
	
	preySprite = pygame.sprite.RenderPlain(prey)
	snakeSprite = pygame.sprite.RenderPlain(s1,s2)
	
	for s in snakeSprite.sprites():
		updateCoords(s.rect.topleft,True)
	updateCoords(prey.rect.topleft,True)
	
	pygame.key.set_repeat(100,100)
	clock = pygame.time.Clock()
	
	while 1:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type is pygame.MOUSEBUTTONDOWN:
				sys.exit()
			if event.type is pygame.KEYDOWN:
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_ESCAPE]:
					sys.exit()
				if pressed[pygame.K_UP] and head.direction is not DOWN:
					head.direction = UP
				if pressed[pygame.K_DOWN] and head.direction is not UP:
					head.direction = DOWN
				if pressed[pygame.K_LEFT] and head.direction is not RIGHT:
					head.direction = LEFT
				if pressed[pygame.K_RIGHT] and head.direction is not LEFT:
					head.direction = RIGHT
		if RESTART:
			print("RESTART")
			RESTART = False
			return score
		updateSnake()
		
		screen.blit(background,(0,0))
		preySprite.update()
		preySprite.draw(screen)
		snakeSprite.update()
		snakeSprite.draw(screen)
		pygame.display.update()

def replay(score):
	global screen,background
	backgroundCopy = background.copy()
	font = pygame.font.Font('../font/Pixeled.ttf',30)
	text = font.render("Score: "+str(score),1,(0,0,0))
	text_rect = text.get_rect(centerx=screen.get_rect().centerx)
	replay = font.render("PLAY AGAIN?",1,(0,0,0))
	replay_rect = replay.get_rect(centerx=text_rect.centerx)
	replay_rect.top = screen.get_rect().centery//2
	
	backgroundCopy.blit(text, text_rect.topleft)
	backgroundCopy.blit(replay,replay_rect.topleft)
	
	box_yes = Box('YES',font,True)
	box_no = Box('NO',font,False)
	
	box_yes.rect.right = replay_rect.centerx - 10
	box_yes.rect.top = replay_rect.bottom + 10
	box_no.rect.left = replay_rect.centerx + 10
	box_no.rect.top = replay_rect.bottom + 10
	
	boxSprites = pygame.sprite.RenderPlain(box_yes,box_no)
	
	while 1:
		for event in pygame.event.get():
			if event.type is pygame.KEYDOWN:
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_RIGHT]:
					box_no.focus = True
					box_yes.focus = False
				elif pressed[pygame.K_LEFT]:
					box_yes.focus = True
					box_no.focus = False
				elif pressed[pygame.K_RETURN]\
				or pressed[pygame.K_KP_ENTER]:
					if box_yes.focus: return True
					if box_no.focus: return False
					
		screen.blit(backgroundCopy,(0,0))
		boxSprites.update()
		boxSprites.draw(screen)
		
		pygame.display.update()
	
global screen ,background 
pygame.init()

screen = pygame.display.set_mode(DISPLAY)
background = pygame.Surface(screen.get_rect().size)
background.fill((255,255,255))

while 1:
	score = main()
	if replay(score):
		continue
	else:
		sys.exit()
	
