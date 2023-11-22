import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        penny_1 = pygame.image.load("graphics/penny/penny1.png").convert_alpha()
        penny_2 = pygame.image.load("graphics/penny/penny2.png").convert_alpha()
        self.player_walk = [penny_1, penny_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/penny/penny_jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (90, 360))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audios/jump.flac")
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 360:
            self.gravity = -21
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 360:
            self.rect.bottom = 360

    def animation_state(self):
        if self.rect.bottom < 360:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "mouse":
            mouse_1 = pygame.image.load("graphics/mouse/mouse1.png").convert_alpha()
            mouse_2 = pygame.image.load("graphics/mouse/mouse2.png").convert_alpha()
            mouse_3 = pygame.image.load("graphics/mouse/mouse3.png").convert_alpha()
            mouse_4 = pygame.image.load("graphics/mouse/mouse4.png").convert_alpha()
            self.frames = [mouse_1, mouse_2, mouse_3, mouse_4]
            y_pos = 360
        elif type == "bird":
            bird_1 = pygame.image.load("graphics/bird/red_bird1.png").convert_alpha()
            bird_2 = pygame.image.load("graphics/bird/red_bird2.png").convert_alpha()
            bird_3 = pygame.image.load("graphics/bird/red_bird3.png").convert_alpha()
            bird_4 = pygame.image.load("graphics/bird/red_bird4.png").convert_alpha()
            bird_5 = pygame.image.load("graphics/bird/red_bird4.png").convert_alpha()
            self.frames = [bird_1, bird_2, bird_3, bird_4, bird_5]
            rand_pos = choice([210, 385, 200])
            y_pos = rand_pos
        else:
            dog_1 = pygame.image.load("graphics/dog/jayce_run1.png").convert_alpha()
            dog_2 = pygame.image.load("graphics/dog/jayce_run2.png").convert_alpha()
            dog_3 = pygame.image.load("graphics/dog/jayce_run3.png").convert_alpha()
            dog_4 = pygame.image.load("graphics/dog/jayce_run4.png").convert_alpha()
            self.frames = [dog_1, dog_2, dog_3, dog_4]
            y_pos = 365

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1400, 1700), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def speed(self):
        if self.rect.bottom == 360:
            rand_speed = randint(9,10)
        elif self.rect.bottom == 365:
            rand_speed = randint(12,14)
        else:
            rand_speed = randint(11,13)
        self.rect.x -= rand_speed

    def update(self):
        self.animation_state()
        self.speed()
        self.checkOver()
    
    def checkOver(self):
        if self.rect.x <= 0:
            return True
        return False

    def destroy(self):
        global score
        if self.rect.bottomright <= 0:
            score += 1
            self.kill()
    
def display_score():
    global score
    score_surf = test_font.render(f'Score: {score}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (500, 50))
    screen.blit(score_surf, score_rect)
    return score

def collisions():
    if pygame.sprite.spritecollide(penny.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

#Def vars
pygame.init()
screen = pygame.display.set_mode((1000,500))
pygame.display.set_caption("Cat Jumper")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf",50)
start = True
game_active = False
global score
score = 0
high_score = 0
hasPlayedGameOverSound = False
new_round = True

#Music
bg_music = pygame.mixer.Sound("audios/bit.mp3")
bg_music.set_volume(0.5)
game_over_music = pygame.mixer.Sound("audios/game_over.mp3")
game_over_music.set_volume(0.7)
bg_music.play(loops= -1)

#Groups
penny = pygame.sprite.GroupSingle()
penny.add(Player())
obstacle_group = pygame.sprite.Group()

#Sky
sky_surf = pygame.image.load("graphics/backgrounds/Sky.png").convert_alpha()
sky_idx = 0
sky_width = 1000

#Ground
ground_surf = pygame.image.load("graphics/backgrounds/ground.png").convert_alpha()
ground_idx = 0
ground_width = 1350

#Game over text
game_over_surf = test_font.render("GAME OVER", False, (64,64,64))
game_over_surf = pygame.transform.scale2x(game_over_surf)
game_over_rect = game_over_surf.get_rect(center = (500,50))

#Intro screen
player = pygame.image.load("graphics/penny/penny.png")
player = pygame.transform.scale2x(player)
player_rect = player.get_rect(center= (500, 280))

game_name1 = test_font.render("Cat Jumper:", True, (111, 196, 169))
game_name1 = pygame.transform.scale2x(game_name1)
game_name2 = test_font.render("Penny's Quest", False, (111, 196, 169))
game_name_rect1 = game_name1.get_rect(center = (500, 60))
game_name_rect2 = game_name2.get_rect(center = (500, 110))

game_mess = test_font.render("Press space to start", False, (111, 196, 169))
game_mess_rect = game_mess.get_rect(center = (500, 450))

#Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1499)

mouse_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(mouse_animation_timer, 300)

bird_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bird_animation_timer, 200)

dog_animation_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(dog_animation_timer, 150)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["mouse", "bird", "dog", "mouse", "mouse", "bird"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start = False

    if game_active:
        hasPlayedGameOverSound = False
        if new_round: score = 0
        #Sky animation
        screen.blit(sky_surf, (sky_idx,0))
        screen.blit(sky_surf, (sky_width + sky_idx, 0))
        sky_idx -= 1
        if sky_idx == -sky_width: sky_idx = 0

        #Ground animation
        screen.blit(ground_surf,(ground_idx,280))
        screen.blit(ground_surf, (ground_width + ground_idx, 280))
        ground_idx -= 1
        if ground_idx == -ground_width: ground_idx = 0

        #Sprite classes
        penny.draw(screen)
        penny.update()

        obstacle_group.draw(screen) 
        obstacle_group.update()
        for obstacle in obstacle_group:
            if obstacle.checkOver():
                score += 1
        game_active = collisions()

        #Score
        score = display_score()
        high_score_mess_game = test_font.render(f"High Score: {high_score}", True, "#aaaaaa")
        high_score_mess_game = pygame.transform.rotozoom(high_score_mess_game, 0, .7)
        high_score_mess_game_rect = high_score_mess_game.get_rect(center = (900, 40))
        if score > high_score: high_score = score
        screen.blit(high_score_mess_game, high_score_mess_game_rect)

    else:
        screen.fill((94, 129, 162))
        screen.blit(game_mess, game_mess_rect)
        penny_gravity = 0
        ground_idx = 0
        sky_idx = 0

        if start:
            screen.blit(player, player_rect)
            screen.blit(game_name1, game_name_rect1)
            screen.blit(game_name2, game_name_rect2)
        else:
            if not hasPlayedGameOverSound:
                game_over_music.play(loops=0)
                hasPlayedGameOverSound = True
            new_round = True

            player_rect.center = (500, 250)
            screen.blit(player, player_rect)
            screen.blit(game_over_surf, game_over_rect)
            score_mess = test_font.render(f'Your score: {score}', False, (111, 196, 169))
            score_mess_rect = score_mess.get_rect(center = (500, 410))
            screen.blit(score_mess, score_mess_rect)

            high_score_mess = test_font.render(f"High Score: {high_score}", False, (64,64,64))
            high_score_mess_rect = high_score_mess.get_rect(center = (500, 90))
            if score > high_score: high_score = score
            screen.blit(high_score_mess, high_score_mess_rect)

    pygame.display.update()
    clock.tick(60)