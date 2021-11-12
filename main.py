import pygame
import os
import random
pygame.font.init()

#game window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!")

#colors
GREEN = (0,128,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)

#Fonts
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
GO_FONT = pygame.font.SysFont('comicsans', 40 )

#apple
APPLE_WIDTH, APPLE_HEIGHT = 30, 30
APPLE_IMAGE = pygame.image.load(os.path.join('assets', 'apple.png'))
APPLE = pygame.transform.scale( APPLE_IMAGE, (APPLE_WIDTH, APPLE_HEIGHT))

#snake
SNAKE_WIDTH, SNAKE_HEIGHT = 15, 15
SNAKE_HEAD_IMAGE = pygame.image.load(os.path.join('assets', 'snake_head.png'))
SNAKE_HEAD = pygame.transform.scale( SNAKE_HEAD_IMAGE, (SNAKE_WIDTH, SNAKE_HEIGHT))
SNAKE_BODY_IMAGE = pygame.image.load(os.path.join('assets', 'snake_bod.png'))
SNAKE_BODY = pygame.transform.scale( SNAKE_BODY_IMAGE, (SNAKE_WIDTH, SNAKE_HEIGHT )) 

VEL = 5 #movement speed
FPS = 60 #fps control

def draw_window( snake_head, apple, snake_body, score, direction ):
    WIN.fill(BLACK)
    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE )
    WIN.blit(score_text, (10, 10))
    if direction == 'LEFT':
        WIN.blit(pygame.transform.rotate(SNAKE_HEAD, 270), (snake_head.x,snake_head.y))
    elif direction == 'RIGHT':
        WIN.blit(pygame.transform.rotate(SNAKE_HEAD, 90), (snake_head.x,snake_head.y))
    elif direction == 'UP':
        WIN.blit(pygame.transform.rotate(SNAKE_HEAD, 0), (snake_head.x,snake_head.y))
    elif direction == 'DOWN':
        WIN.blit(pygame.transform.rotate(SNAKE_HEAD, 180), (snake_head.x,snake_head.y))
    #pygame.draw.rect(WIN, GREEN, (snake_head.x, snake_head.y, SNAKE_WIDTH, SNAKE_HEIGHT))
    set_snake(snake_body )
    WIN.blit(APPLE, (apple.x,apple.y))
    pygame.display.update()

#movement handle
def snake_movement(direction, snake_head):
    if direction == 'LEFT':
        snake_head.x -= VEL
    elif direction == 'RIGHT':
        snake_head.x += VEL
    elif direction == 'UP':
        snake_head.y -= VEL
    elif direction == 'DOWN':
        snake_head.y += VEL

#collision handler
def apple_collision(snake_head, apple):
    if snake_head.colliderect(apple):
        return True
    return False

def body_collision( snake_body ):
    return snake_body[0] in snake_body[1:]

def border_collision( snake_head ):
    if snake_head.x > WIDTH or snake_head.x < 0:
        return True
    if snake_head.y > HEIGHT or snake_head.y < 0:
        return True
    return False

#length set
def set_snake( snake_body ):
    for part in snake_body:
        WIN.blit(SNAKE_BODY, part )
        #pygame.draw.rect(WIN, GREEN, (*part, SNAKE_WIDTH, SNAKE_HEIGHT ))

#game over
def end_game( score ):
    WIN.fill(BLACK)
    go_text = GO_FONT.render("GAME OVER!", 1, WHITE )
    WIN.blit( go_text, (WIDTH/2 - go_text.get_width()/2, HEIGHT/2 - go_text.get_height()/2 ) )
    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE )
    WIN.blit(score_text, (10,10) )
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    snake_head = pygame.Rect( 500,250, SNAKE_WIDTH, SNAKE_HEIGHT )
    snake_length = 1
    snake_body = []
    snake_body.append((snake_head.x,snake_head.y))
    direction = 'RIGHT'
    score = 0

    apple = pygame.Rect( random.randint(APPLE_WIDTH, WIDTH-APPLE_WIDTH),random.randint(APPLE_HEIGHT, HEIGHT-APPLE_HEIGHT), APPLE_WIDTH, APPLE_HEIGHT )
    clock = pygame.time.Clock()
    run = True
    while run: #run game
        clock.tick(FPS) #control speed of while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if user quit the game end the loop
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    direction = 'LEFT'
                elif event.key == pygame.K_d:
                    direction = 'RIGHT'
                elif event.key == pygame.K_w:
                    direction = 'UP'
                elif event.key == pygame.K_s:
                    direction = 'DOWN'
                    
        snake_body.append((snake_head.x, snake_head.y))

        #movement handling
        snake_movement( direction, snake_head )

        #collision
        if apple_collision(snake_head, apple):
            #new apple position
            apple.x = random.randint(APPLE_WIDTH, WIDTH-APPLE_WIDTH)
            apple.y = random.randint(APPLE_HEIGHT, HEIGHT-APPLE_HEIGHT)
            score+=1
            #increase snake_body
            snake_length += 1

        if len(snake_body) > snake_length:
            del snake_body[0]
        
        if body_collision(snake_body) or border_collision(snake_head):
            end_game( score )
            break

        draw_window( snake_head, apple, snake_body, score, direction )#window draw
    main()

if __name__ == "__main__":
    main()