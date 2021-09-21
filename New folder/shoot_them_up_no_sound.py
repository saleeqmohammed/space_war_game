#Shoot them up GAME
#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
#Art from Kenney.nl
import pygame
import random
from os import path 

img_dir = path.join(path.dirname(__file__),'img')
snd_dir  = path.join(path.dirname(__file__),'snd')
#Color pallet
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED=(255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
#configurations
HEIGHT=546 #SVGA res
WIDTH = 500
FPS = 60
WINDOW_TITLE = "Shoot 'em up"

#Initialize pygame and create window
pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

ship_speed = 5
POWERUP_TIME = 5000
font_name = pygame.font.match_font('arial')
def draw_text(surface, text,size, x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop=(x,y)
    surface.blit(text_surface,text_rect)
def spawn_mobs():
    m =Mob()
    all_sprites.add(m)
    mobs.add(m)
def draw_shield_bar(surface,x,y,pct):
    if pct <0:
        pct =0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface,GREEN,fill_rect)
    pygame.draw.rect(surface,WHITE,outline_rect,2)

def draw_lives(surface,x,y,lives,img):
    for i in range(lives):
        img.set_colorkey(BLACK)
        img_rect = img.get_rect()
        img_rect.x = x +30*i 
        img_rect.y = y
        surface.blit(img,img_rect)
def show_start():
    screen.blit(background, background_rect)
    draw_text(screen,"SPACE BLAST",64, WIDTH/2,HEIGHT/4)
    draw_text(screen,"Arrow keys to move, space to fire",22, WIDTH/2,HEIGHT/2)
    draw_text(screen,"press any key to begin",18,WIDTH/2,HEIGHT*0.75)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_go_screen(last_score):
    screen.blit(background, background_rect)
    draw_text(screen,"GAME OVER!",64, WIDTH/2,HEIGHT/4)
    draw_text(screen,"Arrow keys to move, space to fire",22, WIDTH/2,HEIGHT/2)
    draw_text(screen,"Last score: "+str(last_score),22,WIDTH/2,HEIGHT*0.6)
    draw_text(screen,"press any key to play again",18,WIDTH/2,HEIGHT*0.75)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0 
        self.sheild = 100
        self.shoot_delay = 250 #ms
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer =  pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
    def update(self):
        #time out for powerups
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -=1
            self.power_time = pygame.time.get_ticks()
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -ship_speed
        if keystate[pygame.K_RIGHT]:
            self.speedx = ship_speed
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0 :
            self.rect.left = 0
    def powerup(self):
        self.power +=1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                #shoot_snd.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                #shoot_snd.play()
    def hide(self):
        #temporaryly hide the player
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2 , HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.85/2)
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot  = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now -self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed)%360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = new_image.get_rect()
            self.rect.center = old_center
 
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -120 or self.rect.right > WIDTH + 120 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 8
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update =pygame.time.get_ticks()
        self.frame_rate = 75
    
    def update(self):
        now =pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image =  explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center 
            


#Load all graphics 
background = pygame.image.load(path.join(img_dir,'bg.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,'ship.png')).convert()
player_mini =pygame.transform.scale(player_img,(25,19))
meteor_img = pygame.image.load(path.join(img_dir,'meteor.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir,'laser.png')).convert()
meteor_images = []
meteor_list = [
    'meteor.png',
    'm1.png',
    'm2.png',
    'm3.png',
    'm4.png',
    'm5.png',
    'm6.png',
    'm7.png',
    'm8.png',
    'm9.png',
    'm10.png',
    'm11.png',
    'm12.png',
    'm13.png',
    'm14.png',
    'm15.png',
    'm16.png',
    'm17.png',
    'm18.png',
    'm19.png',
]
explosion_anim = {}
explosion_anim['lg']=[]
explosion_anim['sm']=[]
explosion_anim['player']=[]
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    img_lg =pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img= pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())
powerup_images={}
powerup_images['shield']=pygame.image.load(path.join(img_dir,'shield.png'))
powerup_images['gun']= pygame.image.load(path.join(img_dir,'gun.png'))

show_start()
game_over = False
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
poweups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):
    spawn_mobs()

score = 0

#Game loop
EXEC_STATUS =True
while EXEC_STATUS:
    if game_over:
        last_score = score
        show_go_screen(last_score)
        game_over =False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        poweups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            spawn_mobs()
        
        score = 0

    clock.tick(FPS)

    #process input(events)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EXEC_STATUS = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    #update

    all_sprites.update()
    #Chek if any bullet hits a mob
    hits =  pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 50- hit.radius
        #random.choice(explosion_sounds).play()
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random()<0.1:
            pow= Pow(hit.rect.center)
            all_sprites.add(pow)
            poweups.add(pow)
        spawn_mobs()

    #check if any mob hit the player sprite
    hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.sheild -= hit.radius*2
        #hurt_snd.play()
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        spawn_mobs()
        if player.sheild <= 0:
            death_explosion = Explosion(player.rect.center,'player')
            all_sprites.add(death_explosion)
            #player_explosion.play()
            player.hide()
            player.lives -=1
            player.sheild = 100
    #check if player hit a powerup
    hits = pygame.sprite.spritecollide(player,poweups,True)
    for hit in hits:
        if hit.type == 'shield':
            sheild_snd.play()
            player.sheild += random.randrange(10,30)
            if player.sheild >= 100:
                player.sheild = 100
        if hit.type == 'gun':
            #power_snd.play()
            player.powerup()



    #if player is dead and explosion over, finish game
    if player.lives ==0 and not death_explosion.alive():
        game_over = True



    #Render/Draw
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_shield_bar(screen,5,5,player.sheild)
    draw_lives(screen,WIDTH-100,5,player.lives,player_mini)
    #double buffering to be performed at the end
    pygame.display.flip()
print("Exiting...")
pygame.quit()
