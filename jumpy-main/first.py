import pygame
import random


pygame.init()
SCREEN_WIDTH=400
SCREEN_HEIGHT=600
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("jumpy jump")
icon=pygame.image.load("icon.png")
pygame.display.set_icon(icon)
# pygame.display.set_icon("icon.png")
clock=pygame.time.Clock()
FPS=60

gravity=1
white=(255,255,255)
maxplatform=10
jumpy_image=pygame.image.load("jump.png").convert_alpha()
bg_img=pygame.image.load("bg.png").convert_alpha()
platform_img=pygame.image.load("wood.png").convert_alpha()

# player
class player:
    def __init__(self,x,y):
        self.image=pygame.transform.scale(jumpy_image,(45,45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.flip = False
        self.vel_y=0

    def move(self):
		#reset variables
        dx = 0
        dy = 0

		#process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
          dx = -10
          self.flip = True
        if key[pygame.K_d]:
          dx = 10
          self.flip = False
        #gravity
        self.vel_y+=gravity
        dy+=self.vel_y
		#ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
          dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
          dx = SCREEN_WIDTH - self.rect.right
        #ground
        if self.rect.bottom+dy>SCREEN_HEIGHT:
            dy=0
            self.vel_y=-20
        #collision of platform
        for p in platform_group:
           if p.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
              if self.rect.bottom<p.rect.centery:
                 if self.vel_y>0:
                    self.rect.bottom=p.rect.top
                    dy=0
                    self.vel_y=-20

		#update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
       screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
       pygame.draw.rect(screen, white, self.rect, 2)


class platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(platform_img,(width,10))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#platform instance
platform_group=pygame.sprite.Group()
for p in range(maxplatform):
    p_w=random.randint(40,60)
    p_x=random.randint(0,SCREEN_WIDTH-p_w)
    p_y=p*random.randint(80,120)
    plat=platform(p_x,p_y,p_w)
    platform_group.add(plat)





jumpy = player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
run = True
while run:
    platform_group.draw(screen)
    clock.tick(FPS)
    jumpy.move()
	#draw background
    screen.blit(bg_img, (0, 0))
	#draw sprites
    platform_group.draw(screen)
    jumpy.draw()
	#event handler
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
            #update display window
    pygame.display.update()



pygame.quit()