import pygame
import os
import random
from game_assets.game_items import Player, Enemy

pygame.font.init()  # need to initialize fonts before they can be used

# game setup (for pygame put game images in assets folder to load)
# use all caps for constants (immutable variables) in Python
WIDTH, HEIGHT = 650, 650
GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))  # first value is game dimensions, must be tuple
pygame.display.set_caption('Discount Space Invaders')

GAME_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))


# main game loop
def main():
    run = True
    lost = False
    lost_count = 0
    fps = 60  # frames per sec, higher number is faster game
    clock = pygame.time.Clock()

    level = 0
    lives = 3
    ship_vel = 6
    laser_vel = -4  # (needs to be neg to travel upwards, y increases as it goes down in pygame)
    main_font = pygame.font.SysFont("comicsans", 45)
    lost_font = pygame.font.SysFont("comicsans", 60)

    player1 = Player(300, 300)
    enemies = []
    wave_length = 3  # at each level we'll increase the number of ships in wave
    enemy_vel = 1

    # draw the game window
    def redraw_window():
        GAME_WINDOW.blit(GAME_BACKGROUND, (0, 0))  # draws selected image on location specified, (0,0 is top left)
        score = player1.score

        # add text variables to window
        level_label = main_font.render(f'Level: {level}', True, (255, 255, 255))
        lives_label = main_font.render(f'Lives: {lives}', True, (255, 255, 255))
        score_label = main_font.render(f'Score: {score}', True, (255, 255, 255))

        GAME_WINDOW.blit(level_label, (10, 10))
        GAME_WINDOW.blit(lives_label, ((WIDTH - level_label.get_width())/2.5 + 10, 10))  # get width of item + add padding
        last_width = WIDTH - level_label.get_width()/2 - lives_label.get_width() - 20
        GAME_WINDOW.blit(score_label, (last_width, 10))

        for enemy_ship in enemies:
            enemy_ship.draw(GAME_WINDOW)

        player1.draw(GAME_WINDOW)

        if lost:
            lost_label = lost_font.render('Uh oh. You lost.', True, (255, 255, 255))
            GAME_WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 325))

        pygame.display.update()  # update game window

    # playing the game
    while run:
        clock.tick(fps)
        redraw_window()

        if lives <= 0 or player1.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):
                if level > 3:
                    enemy = Enemy(random.randrange(75, WIDTH - 100), random.randrange(int(-1500*level/3), -100),
                                  random.choice(['red', 'blue', 'green']))
                    enemy_vel += 1
                else:
                    enemy = Enemy(random.randrange(75, WIDTH - 100), random.randrange(-1500, -100),
                                  random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        # determine if user wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # track movement keys, with constraints to keep user on the board
        keys = pygame.key.get_pressed()
        player_width = player1.get_width()
        player_height = player1.get_height()

        if keys[pygame.K_LEFT] and player1.x_pos - ship_vel > 0:
            player1.x_pos -= ship_vel
        elif keys[pygame.K_RIGHT] and player1.x_pos + ship_vel + player_width < WIDTH:
            player1.x_pos += ship_vel
        elif keys[pygame.K_UP] and player1.y_pos - ship_vel > 0:
            player1.y_pos -= 1
        elif keys[pygame.K_DOWN] and player1.y_pos + ship_vel + player_height < HEIGHT:
            player1.y_pos += 1
        elif keys[pygame.K_SPACE]:
            player1.shoot()

        # enemy play
        enemies_copy = enemies.copy()

        for enemy in enemies_copy:
            enemy.move(enemy_vel)
            enemy.move_lasers(abs(laser_vel), player1)

            # randomization of enemy shooting at player
            if random.randrange(0, 120) == 1:
                enemy.shoot()

            if enemy.collision(player1):
                player1.health -= 10
                player1.score += 10
                enemies.remove(enemy)
            elif enemy.y_pos + enemy.get_height() > HEIGHT and lives > 0:
                lives -= 1
                enemies.remove(enemy)

        player1.move_lasers(laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont('comicsans', 50)
    run = True

    while run:
        GAME_WINDOW.blit(GAME_BACKGROUND, (0, 0))
        title_label = title_font.render('Click your mouse to begin', True, (255, 255, 255))
        GAME_WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 325))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


if __name__ == '__main__':
    main_menu()
