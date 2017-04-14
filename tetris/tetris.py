import pygame, sys, random,time
from enum import Enum
pygame.init()


class UserEvent(Enum):
	move = pygame.USEREVENT + 1

class Constant():
	block_size = 20

class Direction(Enum):
	up = 'w'
	down = 's'
	left = 'a' 
	right = 'd'

class Block:
	def __init__(self):
		self.image = pygame.Surface((20,20))
		self.center = self.image.get_rect()
		self.top = self.image.get_rect()
		self.bottom = self.image.get_rect()
		self.left = self.image.get_rect()
		self.right = self.image.get_rect()
		self.topleft = self.image.get_rect()
		self.topright = self.image.get_rect()
		self.bottomleft = self.image.get_rect()
		self.bottomright = self.image.get_rect()
		
		#~ self.center.centerx = back_rect.centerx
		self.center.centerx = 110
		self.top.bottomleft = self.center.topleft
		self.bottom.topleft = self.center.bottomleft
		self.left.topright = self.center.topleft
		self.right.topleft = self.center.topright
		self.topleft.bottomright = self.center.topleft
		self.topright.bottomleft = self.center.topright
		self.bottomleft.topright = self.center.bottomleft
		self.bottomright.topleft = self.center.bottomright
		
		self.direction = Direction.up
		self.all_blocks = [self.center, self.top, self.bottom, self.left, self.right, self.topleft, self.topright, self.bottomleft, self.bottomright]
		self.move = True
		
	def stop(self):
		for block in self.visible:
			for i in range(len(lines)-1,-1,-1):
				for image, rect in lines[i]:
					if block.bottomleft == rect.topleft:
						self.move = False
						return True
		return False
	
	def hard_drop(self):
		while not self.stop():
			self.move_down()
		for block in self.visible:
			lines[len(lines)-block.bottom//20].append((self.image,block))
		return
		
	def move_down(self):
		if self.stop():
			for block in self.visible:
				lines[len(line)-block.bottom//20].append((self.image,block))
			return
		if not self.move: return
		
		for block in self.all_blocks:
			block.move_ip(0,Constant.block_size)
	
	def move_left(self):
		if not self.move: return
		for block in self.visible:
			if block.left == back_rect.left:
				return
			for i in range(len(lines)-1,-1,-1):
				for image, rect in lines[i]:
					if block.topleft == rect.topright:
						return
						
		for block in self.all_blocks:
			block.move_ip(-Constant.block_size,0)
			
	def move_right(self):
		if not self.move: return
		for block in self.visible:
			if block.right == back_rect.right:
				return
			for i in range(len(lines)-1,-1,-1):
				for image, rect in lines[i]:
					if block.topright == rect.topleft:
						return
						
		for block in self.all_blocks:
			block.move_ip(Constant.block_size,0)
	
	def update(self):
		for block in self.visible:
			screen.blit(self.image,block.topleft)
			
class I(Block):
	def __init__(self):
		self.image = pygame.Surface((20,20))
		self.image.fill((255, 0, 255))
		pygame.draw.rect(self.image,(255,255,255),self.image.get_rect(),1)
		self.center = self.image.get_rect()
		self.top = self.image.get_rect()
		self.bot = self.image.get_rect()
		self.botbot = self.image.get_rect()
		self.left = self.image.get_rect()
		self.right = self.image.get_rect()
		self.rightright = self.image.get_rect()

		self.center.centerx = 130
		self.top.bottomleft = self.center.topleft
		self.left.topright = self.center.topleft
		self.right.topleft = self.center.topright
		self.rightright.topleft = self.right.topright
		self.bot.topleft = self.center.bottomleft
		self.botbot.topleft = self.bot.bottomleft

		self.direction = Direction.up	
		self.visible = [self.center,self.left,self.right,self.rightright]
		self.all_blocks = [self.center,self.top,self.left,self.bot,self.botbot,self.right,self.rightright]
		self.move = True
		
	def rotate(self):
		for block in self.all_blocks:
			if not back_rect.contains(block):
				return
		if self.direction == Direction.up:
			self.direction = Direction.left
			self.visible.remove(self.left)
			self.visible.remove(self.right)
			self.visible.remove(self.rightright)
			self.visible.append(self.top)
			self.visible.append(self.bot)
			self.visible.append(self.botbot)
		elif self.direction == Direction.left:
			self.direction = Direction.up
			self.visible.remove(self.top)
			self.visible.remove(self.bot)
			self.visible.remove(self.botbot)
			self.visible.append(self.left)
			self.visible.append(self.right)
			self.visible.append(self.rightright)
			
	def update(self):
		for block in self.visible:
			screen.blit(self.image,block.topleft)
			
class J(Block):
	def __init__(self):
		Block.__init__(self)
		self.image.fill((255, 0, 0))
		pygame.draw.rect(self.image,(255,255,255),self.image.get_rect(),1)
		screen.blit(self.image,self.center.topleft)
		screen.blit(self.image,self.left.topleft)
		screen.blit(self.image,self.right.topleft)
		screen.blit(self.image,self.bottomright.topleft)
		self.visible = [self.center,self.left,self.right,self.bottomright]
	def rotate(self):
		for block in self.all_blocks:
			if not back_rect.contains(block):
				return
		
		if self.direction == Direction.up:
			self.direction = Direction.left
			self.visible.remove(self.left)
			self.visible.remove(self.right)
			self.visible.remove(self.bottomright)
			self.visible.append(self.bottom)
			self.visible.append(self.bottomleft)
			self.visible.append(self.top)
			
		elif self.direction == Direction.left:
			self.direction = Direction.down
			self.visible.remove(self.bottom)
			self.visible.remove(self.bottomleft)
			self.visible.remove(self.top)
			self.visible.append(self.left)
			self.visible.append(self.topleft)
			self.visible.append(self.right)
			
		elif self.direction == Direction.down:
			self.direction = Direction.right
			self.visible.remove(self.left)
			self.visible.remove(self.topleft)
			self.visible.remove(self.right)
			self.visible.append(self.top)
			self.visible.append(self.topright)
			self.visible.append(self.bottom)
			
		elif self.direction == Direction.right:
			self.direction = Direction.up
			self.visible.remove(self.top)
			self.visible.remove(self.topright)
			self.visible.remove(self.bottom)
			self.visible.append(self.right)
			self.visible.append(self.bottomright)
			self.visible.append(self.left)
			

class L(Block):
	def __init__(self):
		Block.__init__(self)
		self.image.fill((255, 191, 0))
		pygame.draw.rect(self.image,(255,255,255),self.image.get_rect(),1)
		screen.blit(self.image,self.center.topleft)
		screen.blit(self.image,self.left.topleft)
		screen.blit(self.image,self.right.topleft)
		screen.blit(self.image,self.bottomleft.topleft)
		self.visible = [self.center,self.left,self.right,self.bottomleft]
	def rotate(self):
		for block in self.all_blocks:
			if not back_rect.contains(block):
				return
		if self.direction == Direction.up:
			self.direction = Direction.left
			self.visible.remove(self.left)
			self.visible.remove(self.right)
			self.visible.remove(self.bottomleft)
			self.visible.append(self.bottom)
			self.visible.append(self.topleft)
			self.visible.append(self.top)
			
		elif self.direction == Direction.left:
			self.direction = Direction.down
			self.visible.remove(self.bottom)
			self.visible.remove(self.topleft)
			self.visible.remove(self.top)
			self.visible.append(self.left)
			self.visible.append(self.topright)
			self.visible.append(self.right)
			
		elif self.direction == Direction.down:
			self.direction = Direction.right
			self.visible.remove(self.left)
			self.visible.remove(self.topright)
			self.visible.remove(self.right)
			self.visible.append(self.top)
			self.visible.append(self.bottomright)
			self.visible.append(self.bottom)
			
		elif self.direction == Direction.right:
			self.direction = Direction.up
			self.visible.remove(self.top)
			self.visible.remove(self.bottomright)
			self.visible.remove(self.bottom)
			self.visible.append(self.right)
			self.visible.append(self.bottomleft)
			self.visible.append(self.left)
			
			
class O(Block):
	def __init__(self):
		Block.__init__(self)
		self.image.fill((64, 255, 0))
		pygame.draw.rect(self.image,(255,255,255),self.image.get_rect(),1)
		screen.blit(self.image,self.center.topleft)
		screen.blit(self.image,self.right.topleft)
		screen.blit(self.image,self.bottom.topleft)
		screen.blit(self.image,self.bottomright.topleft)
		self.visible = [self.center,self.bottom,self.right,self.bottomright]
	def rotate(self):
		pass
		
class S(Block):
	def __init__(self):
		Block.__init__(self)
		self.image.fill((0, 191, 255))
		pygame.draw.rect(self.image,(255,255,255),self.image.get_rect(),1)
		screen.blit(self.image,self.center.topleft)
		screen.blit(self.image,self.right.topleft)
		screen.blit(self.image,self.bottom.topleft)
		screen.blit(self.image,self.bottomleft.topleft)
		self.visible = [self.center, self.right,self.bottom,self.bottomleft]
	def rotate(self):
		for block in self.all_blocks:
			if not back_rect.contains(block):
				return
		if self.direction == Direction.up:
			self.direction = Direction.left
			self.visible.remove(self.right)
			self.visible.remove(self.bottomleft)
			self.visible.append(self.left)
			self.visible.append(self.topleft)
		elif self.direction == Direction.left:
			self.direction = Direction.up
			self.visible.remove(self.left)
			self.visible.remove(self.topleft)
			self.visible.append(self.right)
			self.visible.append(self.bottomleft)
		
class T(Block):
	def __init__(self):
		Block.__init__(self)
		self.image.fill((0,0,255))
		pygame.draw.rect(self.image,(255,255,255),self.image.get_rect(),1)
		screen.blit(self.image,self.center.topleft)
		screen.blit(self.image,self.left.topleft)
		screen.blit(self.image,self.right.topleft)
		screen.blit(self.image,self.bottom.topleft)
		self.visible = [self.center,self.left,self.right,self.bottom]
	
	def rotate(self):
		for block in self.all_blocks:
			if not back_rect.contains(block):
				return
		if self.direction == Direction.up:
			self.direction = Direction.left
			self.visible.remove(self.right)
			self.visible.append(self.top)
			
		elif self.direction == Direction.down:
			self.direction = Direction.right
			self.visible.remove(self.left)
			self.visible.append(self.bottom)
			
		elif self.direction == Direction.left:
			self.direction = Direction.down
			self.visible.remove(self.bottom)
			self.visible.append(self.right)
			
		elif self.direction == Direction.right:
			self.direction = Direction.up
			self.visible.remove(self.top)
			self.visible.append(self.left)
			
class Z(Block):
	def __init__(self):
		Block.__init__(self)
		self.image.fill((191, 0, 255))
		pygame.draw.rect(self.image,(255,255,255),self.image.get_rect(),1)
		screen.blit(self.image,self.center.topleft)
		screen.blit(self.image,self.left.topleft)
		screen.blit(self.image,self.bottom.topleft)
		screen.blit(self.image,self.bottomright.topleft)
		self.visible = [self.center,self.left,self.bottom,self.bottomright]
		
	def rotate(self):
		for block in self.all_blocks:
			if not back_rect.contains(block):
				return
		if self.direction == Direction.up:
			self.direction = Direction.left
			self.visible.remove(self.left)
			self.visible.remove(self.bottomright)
			self.visible.append(self.right)
			self.visible.append(self.topright)
		elif self.direction == Direction.left:
			self.direction = Direction.up
			self.visible.remove(self.right)
			self.visible.remove(self.topright)
			self.visible.append(self.left)
			self.visible.append(self.bottomright)
		

			
screen = pygame.display.set_mode((240,480))
back_rect = screen.get_rect()
background = pygame.Surface(back_rect.size)
background.fill((20, 20, 20))
pygame.display.flip()

lines = [[] for i in range(0,25)]
base_surf = pygame.Surface((240,20))
base_line = pygame.Rect((0,0),(20,20))
base_line.topleft = back_rect.bottomleft
lines[0] = [ (base_surf,base_line.move(x,0)) for x in range(0,240,20)]

user_event_move = pygame.USEREVENT + 1

i = random.randrange(0,7)
if i == 0: block = I()
if i == 1: block = J()
elif i == 2: block = L()
elif i == 3: block = O()
elif i == 4: block = S()
elif i == 5: block = T()
elif i == 6: block = Z()

game_over = False
timer = 600
limit = 1000
score = 0

pygame.time.set_timer(user_event_move, timer)
clock = pygame.time.Clock()
pygame.key.set_repeat(50,50)


while 1:
	clock.tick(30)
	if block.move == False:
		i = random.randrange(0,7)
		if i == 0: block = I()
		if i == 1: block = J()
		elif i == 2: block = L()
		elif i == 3: block = O()
		elif i == 4: block = S()
		elif i == 5: block = T()
		elif i == 6: block = Z()
	
	for image, rect in lines[22]:
		if rect.topleft == (100,40)\
		or rect.topleft == (120,40)\
		or rect.topleft == (140,40):
			game_over = True
		
	for event in pygame.event.get():
		if event.type == user_event_move:
			block.move_down()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
			if event.key == pygame.K_UP:
				block.rotate()
			if event.key == pygame.K_SPACE:
				block.hard_drop()
			if event.key == pygame.K_LEFT:
				block.move_left()
			if event.key == pygame.K_RIGHT:
				block.move_right()
			if event.key == pygame.K_DOWN:
				block.move_down()
				pygame.time.set_timer(user_event_move,0)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				pygame.time.set_timer(user_event_move, timer)
	
	#~ if score > limit and timer > 200:
		#~ timer -= 20
		#~ limit += 1000
		#~ pygame.time.set_timer(user_event_move, timer)
	
	screen.blit(background,(0,0))
	block.update()
	
	k = 0
	for i in range(1,len(lines)):
		if len(lines[i]) == 12: k+=1
		elif len(lines[i]) != 12 and k!=0:
			for image, rect in lines[i]:
				rect.move_ip(0,k*Constant.block_size)
			lines[i-k] = lines[i]
			lines[i] = []
	#SCORING
	if k == 1: score+=100
	elif k == 2: score += 200
	elif k == 3: score += 300
	elif k == 4: score += 500
			
	for line in lines:
		for image,rect in line:
			screen.blit(image,rect.topleft)
	
	pygame.display.flip()
	
	if game_over:
		print("score:",score)
		sys.exit()
	
