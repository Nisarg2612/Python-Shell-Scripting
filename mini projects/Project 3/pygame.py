import pygame
from pygame.locals import *
import random

# Intialize the pygam
pygame.init()

# refresh rate to 60
clock = pygame.time.Clock()
FPS = 60

width = 600
height = 800

# create the scree
screen = pygame.display.set_mode((width, height))

# Screen Caption
pygame.display.set_caption('Space Invanders')

# Screen icon
icon = pygame.image.load("img/ufo.png")
pygame.display.set_icon(icon)

#define font
font = pygame.font.SysFont('Arial', 30)


#define game variables
level = 1 # level initialize to 1
lives = 5 # lives set to 5
rows = 5
cols = 5
alien_cooldown = 1000 # bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0 #0 is no game over, 1 means player has won, -1 means player has lost
score_value = 0 # score value initilize to 0



#define colours
red = [255, 0, 0]
green = [0, 255, 0]
white = [255, 255, 255]



# Background load image
background = pygame.image.load("img/background.png")


#define function for creating text
def draw_text(text, font, text_col, x, y):
	textsurface = font.render(text, True, text_col)
	screen.blit(textsurface, (x, y))


#create spaceship class
class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, life, score):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/spaceship.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.life = life
		self.score = score
		self.last_shot = pygame.time.get_ticks()


	def update(self):
		#set movement speed
		speed = 5
		#set a cooldown variable
		cooldown = 500 #milliseconds
		game_over = 0


		#check if key was pressed
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < width:
			self.rect.x += speed

		#record current time
		time_now = pygame.time.get_ticks()
		#shoot
		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			bullet = Bullets(self.rect.centerx, self.rect.top, 0)
			bullet_group.add(bullet)
			self.last_shot = time_now


		#update mask
		self.mask = pygame.mask.from_surface(self.image)

		return game_over


#create Bullets class
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y, score):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		
		

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):
			self.kill()
			spaceship.score += 10
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			explosion_group.add(explosion)


#create Aliens class
class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction



#create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien_bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y += 2
		if self.rect.top > height:
			self.kill()
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			self.kill()
			#reduce spaceship life
			spaceship.life -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)




#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"img/exp{num}.png")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			#add the image to the list
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0


	def update(self):
		explosion_speed = 3
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, delete explosion
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

# create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


# create player
spaceship = Spaceship(int(width / 2), height - 100, 5, 0)
# add the spaceship to the spaceship group
spaceship_group.add(spaceship)

def create_aliens():
	# generate aliens
	for row in range(rows):
		for item in range(cols):
			alien = Aliens(100 + item * 100, 100 + row * 70)
			alien_group.add(alien)

create_aliens()



run = True
# game loop
while run:

	pygame.display.flip()
	clock.tick(FPS)

	#draw background
	screen.blit(background, (0, 0))

	#draw level and lives 
	level_label = font.render(f"Level: {level}",1, (white))
	lives_label = font.render(f"Lives: {spaceship.life}", 1, (white))
	score_label = font.render(f"Score: {spaceship.score}", 1, (white))


	screen.blit(level_label, (width - level_label.get_width() - 10, 10))
	screen.blit(lives_label, (10, 10))
	screen.blit(score_label, (width / 2 - 50, 10))


	if countdown == 0:
		#create random alien bullets
		#record current time
		time_now = pygame.time.get_ticks()
		#shoot
		if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
			attacking_alien = random.choice(alien_group.sprites())
			alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
			alien_bullet_group.add(alien_bullet)
			last_alien_shot = time_now

		#Check Player Life Count
		if spaceship.life <= 0:
			game_over = -1

		#check if all the aliens have been killed
		if len(alien_group) == 0:
			game_over = 1

		if game_over == 0:
			#update spaceship
			game_over = spaceship.update()

			#update sprite groups
			bullet_group.update()
			alien_group.update()
			alien_bullet_group.update()
		else:
			if game_over == -1:
				draw_text('GAME OVER!', font, white, int(width / 2 - 100), int(height / 2 + 40))
			if game_over == 1:
				draw_text('YOU WIN!', font, white, int(width / 2 - 100), int(height / 2 + 40))

	if countdown > 0:
		draw_text('GET READY!', font, white, int(width / 2 - 110), int(height / 2 + 50))
		draw_text(str(countdown), font, white, int(width / 2 - 10), int(height / 2 + 100))
		count_timer = pygame.time.get_ticks()
		if count_timer - last_count > 1000:
			countdown -= 1
			last_count = count_timer


	#update explosion group	
	explosion_group.update()


	#draw sprite groups
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alien_bullet_group.draw(screen)
	explosion_group.draw(screen)

	#for now it only checks for the quit event
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	pygame.display.update()

pygame.quit()
