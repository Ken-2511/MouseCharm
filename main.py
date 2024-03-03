import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
FPS = 60
DELTA_T = 1 / FPS
CHARM_MASS = 10
energy_limit = -CHARM_MASS / 30
kinetic_energy_limit = 50


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos_x=0, pos_y=0, speed_x=0, speed_y=0):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.acc_x = 0
        self.acc_y = 0
        self.potential_energy = 0
        self.kinetic_energy = 0
        self.mass = 1

    def is_approaching(self):
        # check if the dot_product of the speed and the position vector is negative
        return self.speed_x * (get_charm_point()[0] - self.pos_x) + self.speed_y * (get_charm_point()[1] - self.pos_y) > 0

    def update(self):
        distance = ((get_charm_point()[0] - self.pos_x) ** 2 + (get_charm_point()[1] - self.pos_y) ** 2) ** 0.5 + 1
        # update the acceleration
        self.acc_x = CHARM_MASS / distance ** 2 * (get_charm_point()[0] - self.pos_x) / distance
        self.acc_y = CHARM_MASS / distance ** 2 * (get_charm_point()[1] - self.pos_y) / distance
        # update the speed
        self.speed_x += self.acc_x * DELTA_T
        self.speed_y += self.acc_y * DELTA_T
        # update the energy
        self.potential_energy = -CHARM_MASS * self.mass / distance
        self.kinetic_energy = 0.5 * self.mass * (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
        # limit the sum of potential and kinetic energy
        if self.kinetic_energy > kinetic_energy_limit:
            aim_kinetic_energy = kinetic_energy_limit
            # update the speed
            self.speed_x *= aim_kinetic_energy / self.kinetic_energy
            self.speed_y *= aim_kinetic_energy / self.kinetic_energy
        elif self.potential_energy + self.kinetic_energy > energy_limit and not self.is_approaching():
            self.speed_x *= 0.995
            self.speed_y *= 0.995
            self.speed_x += self.acc_x * DELTA_T
            self.speed_y += self.acc_y * DELTA_T
        # limit the position to the screen
        if self.pos_x > 40:
            self.speed_x = -abs(self.speed_x)
        if self.pos_x < -40:
            self.speed_x = abs(self.speed_x)
        if self.pos_y > 30:
            self.speed_y = -abs(self.speed_y)
        if self.pos_y < -30:
            self.speed_y = abs(self.speed_y)
        # update the position
        self.pos_x += self.speed_x * DELTA_T
        self.pos_y += self.speed_y * DELTA_T
        # draw the ball
        pygame.draw.circle(screen,
                           (255, 200, 200),
                           map_to_screen(self.pos_x, self.pos_y),
                           5)


def get_charm_point():
    x, y = pygame.mouse.get_pos()
    return map_to_world(x, y)


def map_to_screen(x, y):
    return round(x * 10 + 400), round(300 - y * 10)


def map_to_world(x, y):
    return (x - 400) / 10, (300 - y) / 10


if __name__ == '__main__':
    ball = Ball()
    balls = []
    for _ in range(500):
        ball = Ball()
        balls.append(ball)
        ball.pos_x = random.random() * 10 - 5
        ball.pos_y = random.random() * 10 - 5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        for ball in balls:
            ball.update()
        pygame.display.flip()
    pygame.quit()
