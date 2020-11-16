import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,700))
    screen.blit(floor_surface, (floor_x_pos + 576,700))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos- 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if pipe in pipes:
            if bird_rect.colliderect(pipe):
                return False
    if bird_rect.top <= -100 or bird_rect.bottom >=750:
        return False 
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if(game_state == "main_game"):
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    if(game_state == "game_over"):
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 200))
        screen.blit(score_surface, score_rect)

        high_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_rect = high_surface.get_rect(center = (288, 600))
        screen.blit(high_surface, high_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)


# Game Varialbles
gravity = 0.1
bird_movement = 0
game_active = True
score = 0
high_score = 0


bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0 
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 500))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)  

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# # bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100, 500))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [400, 600, 700]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 300))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 500)
                bird_movement = 0
                score = 0


        if event.type == SPAWNPIPE: 
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if (bird_index < 2):
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0,0)),


    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement 
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # score
        score += 0.01
        score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")


    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    


    pygame.display.update()
    clock.tick(120)
