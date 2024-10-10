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
score=0
scrool=0
scrool_thres=200
gravity=1
game_over=False
white=(255,255,255)
haicolor=(200,255,150)
maxplatform=10
font_small=pygame.font.SysFont("Lccida Sans",28)
font_big=pygame.font.SysFont("Lucida Sans",38)
font_again=pygame.font.SysFont("Lucida Sans",18)
bg_scroll=0
jumpy_image=pygame.image.load("jump.png").convert_alpha()
bg_img=pygame.image.load("bg.png").convert_alpha()
platform_img=pygame.image.load("wood.png").convert_alpha()
###########################################
def draw_bg(bg_scroll):
   screen.blit(bg_img, (0, 0+ bg_scroll))
   screen.blit(bg_img, (0,-600+ 0 + bg_scroll))

def draw_text(text,font,text_col,x,y):
   img=font.render(text,True,text_col)
   screen.blit(img,(x,y))
#########################################################3
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
        scrool=0
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
        # if self.rect.bottom+dy>SCREEN_HEIGHT:
        #     dy=0
        #     self.vel_y=-20
        
        #collision of platform
        for p in platform_group:
           if p.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
              if self.rect.bottom<p.rect.centery:
                 if self.vel_y>0:
                    self.rect.bottom=p.rect.top
                    dy=0
                    self.vel_y=-20
                    global score
                    score+=1
        #check top of screen
        if self.rect.top<=scrool_thres:
           if self.vel_y<0:
              scrool=-dy

		#update rectangle position
        self.rect.x += dx
        self.rect.y += dy +scrool
        return scrool
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
    def update(self,scrool):
       #update platform position
       self.rect.y+=scrool
       #check if platform platform go from screen
       if self.rect.top>SCREEN_HEIGHT:
          self.kill()

#platform instance
platform_group=pygame.sprite.Group()
# for p in range(maxplatform):
    # p_w=random.randint(40,60)
    # p_x=random.randint(0,SCREEN_WIDTH-p_w)
    # p_y=p*random.randint(80,120)
    # plat=platform(p_x,p_y,p_w)
    # platform_group.add(plat)
#initial platform
plat=platform(SCREEN_WIDTH//2-50,SCREEN_HEIGHT-100,100)
platform_group.add(plat)



jumpy = player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
run = True
while run:
    # platform_group.draw(screen)
    clock.tick(FPS)
    if game_over==False:
        scrool=jumpy.move()
        #draw background
        bg_scroll+=scrool
        if bg_scroll>=600:
            bg_scroll=0
        draw_bg(bg_scroll)
        ##draw scrool thesh
        # pygame.draw.line(screen,white,(0,scrool_thres),(SCREEN_WIDTH,scrool_thres))
        #generate platform
        if len(platform_group)<maxplatform:
            p_w=random.randint(50,80)
            p_x=random.randint(0,SCREEN_WIDTH-p_w)
            p_y=plat.rect.y-random.randint(80,120)
            plat=platform(p_x,p_y,p_w)
            platform_group.add(plat)
        
        
        platform_group.update(scrool)
        #draw sprites
        platform_group.draw(screen)
        jumpy.draw()
        #event handler
        #check gameover
        if jumpy.rect.top>SCREEN_HEIGHT:
            game_over=True
    else:
       draw_text("GAME OVER",font_big,white,130,200)
       draw_text("Score:"+str(score),font_small,haicolor,40,300)
       draw_text("Press SPACEBAR for play again",font_again,white,40,320)
       key=pygame.key.get_pressed()
       if key[pygame.K_SPACE]:
          game_over=False
          score=0
          scrool=0
          jumpy.rect.center=(SCREEN_WIDTH//2,SCREEN_HEIGHT-150)
          platform_group.empty()
          plat=platform(SCREEN_WIDTH//2-50,SCREEN_HEIGHT-100,100)
          platform_group.add(plat)
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
            #update display window
    pygame.display.update()



pygame.quit()