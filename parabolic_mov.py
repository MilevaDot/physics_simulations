import pygame
import math

WIDTH = 1280
HEIGHT = 720
FPS = 30

all_inital_velocity = 100
all_initial_angle = 53

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
        # Position
        self.rect = pygame.Rect(10, HEIGHT-30, 20, 20)
        self.image = pygame.Surface((50,50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (10, 10), 10)
        self.initial_velocity = all_inital_velocity
        self.initial_angle = all_initial_angle
        self.gravity = 10
        self.x_initial = 10
        self.y_initial = HEIGHT - 30
        self.time_elapsed = 0
        self.max_range = False


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
            self.max_range = True


class VelocityY(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 60), pygame.SRCALPHA)
        pygame.draw.line(self.image, (0, 0, 255), (15, 60), (15, 0), 2)
        self.rect = self.image.get_rect()
        self.initial_velocity = all_inital_velocity
        self.initial_angle = all_initial_angle
        self.gravity = 10
        self.x_initial = 4
        self.y_initial = HEIGHT - 80
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

        self.rect.x = self.x_initial + initial_velocity_x * self.time_elapsed
        self.rect.y = self.y_initial - (initial_velocity_y * self.time_elapsed - 0.5 * self.gravity * self.time_elapsed**2)

        if self.rect.left > WIDTH:
            self.rect.right = 30
            self.rect.bottom = HEIGHT - 10


class VelocityX(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60,30), pygame.SRCALPHA)
        pygame.draw.line(self.image, (0, 0, 255), (0, 15), (60, 15), 2)
        self.rect = self.image.get_rect()
        self.initial_velocity = all_inital_velocity
        self.initial_angle = all_initial_angle
        self.gravity = 10
        self.x_initial = 20
        self.y_initial = HEIGHT - 35
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

        self.rect.x = self.x_initial + initial_velocity_x * self.time_elapsed
        self.rect.y = self.y_initial - (initial_velocity_y * self.time_elapsed - 0.5 * self.gravity * self.time_elapsed**2)

        if self.rect.left > WIDTH:
            self.rect.right = 30
            self.rect.bottom = HEIGHT - 10

pygame.init()

font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Parabolic movement')
clock = pygame.time.Clock()
running = True
paused = False
sprites = pygame.sprite.Group()
particle = Particle()
velocity_x = VelocityX()
velocity_y = VelocityY()
sprites.add(particle)
sprites.add(velocity_x)
sprites.add(velocity_y)

# For the max height
height_list = [-1]
max_height_line_pos = (0, 0)
max_height_line_end = (0, 0)
max_height_arrive = False

# For the max range
width_list = [-1]
max_width_list_pos = (0,0)
max_width_list_end = (0,0)


while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                paused = not paused

    if not paused:
        sprites.update()
        # For the max height
        if len( height_list ) <= 2:
            height_list.append( 690 - particle.rect.y )

        if height_list[0] > height_list[1] and len( height_list ) <= 2 :
            max_height_line_pos = ( int( particle.rect.x ), int( HEIGHT - 10 ) )
            max_height_line_end = ( int( particle.rect.x ), int( particle.rect.y + 5 ) )
            pygame.draw.line(screen, 'green', max_height_line_pos, max_height_line_end, 2)
            max_height_arrive = True

        if height_list[0] <= height_list[1] and len( height_list ) <= 2:
            height_list.remove(height_list[0])

        # For the max width
        if len( width_list ) <= 2:
            width_list.append( particle.rect.x )

        if width_list[0] <= width_list[1] and len( width_list ) <= 2:
            max_width_list_pos = ( 10, HEIGHT - 20 )
            max_width_list_end = ( int( particle.rect.x ), HEIGHT - 20 )

        if width_list[0] <= width_list[1] and len(width_list) <= 2:
            width_list.remove(width_list[0])

    screen.fill('black')
    sprites.draw(screen)

    # Range max of the particle
    pygame.draw.line(screen, 'white', max_width_list_pos, max_width_list_end, 2)
    width_max = width_list

    # Height max of the particle
    pygame.draw.line(screen, 'white', max_height_line_pos, max_height_line_end, 2)
    height_max = height_list

    pygame.draw.line(screen, 'green', (10, HEIGHT-10),(WIDTH, HEIGHT-10),2)
    pygame.draw.line(screen, 'green', (10, HEIGHT-10), (10, 0), 2)

    # ========================================================= #
    ##### Start text in screen #####
    position_x_text = 'Position x: %s' % ( particle.rect.x - 10 )
    text_surface = font.render(position_x_text, True, text_color)
    screen.blit(text_surface, (20, 10))

    position_y_text = 'Position y: %s' % ( 690 - particle.rect.y)
    text_surface = font.render(position_y_text, True, text_color)
    screen.blit(text_surface, (20, 50))

    velocity_x_text = 'Velocity x: %s' % ( round( velocity_x.initial_velocity * math.cos(math.radians(velocity_x.initial_angle)), 4 ) )
    text_surface = font.render(velocity_x_text, True, text_color)
    screen.blit(text_surface, (210, 10))

    velocity_y_text = 'Velocity y: %s' % ( round( velocity_y.initial_velocity * math.sin(math.radians(velocity_y.initial_angle)) - velocity_y.gravity * velocity_y.time_elapsed, 4 ) )
    text_surface = font.render(velocity_y_text, True, text_color)
    screen.blit(text_surface, (210, 50))

    header_initial_angle = 'Initial angle(°): %s' % ( particle.initial_angle )
    text_surface = font.render(header_initial_angle, True, text_color)
    screen.blit(text_surface, (450, 10))

    time_text = 'Time: %s' % ( round( particle.time_elapsed, 2 ) )
    text_surface = font.render(time_text, True, text_color)
    screen.blit(text_surface, (450, 50))

    if max_height_arrive:
        height_text = 'Max height: %s' % ( max( height_max ) )
        text_surface = font.render(height_text, True, text_color)
        screen.blit(text_surface, (690, 10))

    # if particle.max_range:
    width_text = 'Max width: %s' % ( max( width_max ) )
    text_surface = font.render(width_text, True, text_color)
    screen.blit(text_surface, (690, 50))

    ##### End text in screen #####
    # ========================================================= #

    pygame.display.flip()

pygame.quit()
