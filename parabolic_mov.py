import pygame
import math

WIDTH = 1280
HEIGHT = 720
FPS = 30

'''
    Parabolic movement equation:
    r(t) = ( x_0 + v_0x(t) )i + ( -(g(t)^2)/2 + v_0yt + y_0 )j
    x(t) = x_0 + v_0x(t)
    y(t) = y_0 + v_0yt - (g(t)^2)/2
'''

def time_generator(start, end, step):
    numbers = []
    while start < end:
        numbers.append(start)
        start += step
    return numbers

class Particle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(10, HEIGHT-30, 20, 20)
        self.image = pygame.Surface((50,50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (10, 10), 10)
        self.initial_velocity = 100
        self.initial_angle = 53
        self.gravity = 10
        self.x_initial = 10
        self.y_initial = HEIGHT - 30
        self.time_elapsed = 0

    def flight_time(self, initial_velocity, initial_angle, gravity):
        theta = math.radians(initial_angle)
        time = ( 2 * initial_velocity * math.sin(theta) ) / gravity
        return time

    def update(self):
        initial_angle = math.radians(self.initial_angle)
        initial_velocity_x = self.initial_velocity * math.cos(initial_angle)
        initial_velocity_y = self.initial_velocity * math.sin(initial_angle)
        self.time_elapsed += 1 /FPS

        if self.time_elapsed > self.flight_time(self.initial_velocity, self.initial_angle, self.gravity):
            self.time_elapsed = 0
        '''
            x(t) = x_0 + v_0x(t)
            y(t) = y_0 + v_0yt - (g(t)^2)/2
        '''
        self.rect.x = self.x_initial + initial_velocity_x * self.time_elapsed
        self.rect.y = self.y_initial - (initial_velocity_y * self.time_elapsed - 0.5 * self.gravity * self.time_elapsed**2)
        if self.rect.left > WIDTH:
            self.rect.right = 30
            self.rect.bottom = HEIGHT - 10

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Parabolic movement')
clock = pygame.time.Clock()
running = True
sprites = pygame.sprite.Group()
particle = Particle()
sprites.add(particle)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    sprites.update()
    screen.fill('purple')
    sprites.draw(screen)
    pygame.draw.line(screen, 'green', (10, HEIGHT-10),(WIDTH, HEIGHT-10),2)
    pygame.draw.line(screen, 'green', (10, HEIGHT-10), (10, 0), 2)
    pygame.display.flip()
pygame.quit()