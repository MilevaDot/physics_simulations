import pygame
import pygame_gui
import math
import sys
from button import Button

pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 220
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Physics Experiments')
clock = pygame.time.Clock()
UI_REFRESH_RATE = clock.tick(FPS)/1000
BACKGROUND = pygame.image.load('assets/static/background/main_menu.png')


def get_font(size):
    return pygame.font.Font('assets/static/font.ttf', size)


def parabolic_movement(initial_velocity, initial_angle):
    pygame.display.set_caption('Parabolic movement: The simulation')

    # ========================================================= #
    ### Particle ###
    gravity = 10
    x_initial = 20
    y_initial = 700
    time_elapsed = 0
    theta = math.radians(initial_angle)
    flight_time = ( 2 * initial_velocity * math.sin(theta) ) / gravity
    max_height_start = (0,0)
    max_height_end = (0,0)
    max_width_start = (0,0)
    max_width_end = (0,0)
    max_height_arrived = False
    max_width_arrived = False
    trajectory = []


    while True:
        SCREEN.fill('black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos = (1220, 80), text_input='Main menu', font=get_font(10),
                                  base_color='#d7fcd4', hovering_color='Green')
        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)


        # ========================================================= #
        ### Particle movement ###
        initial_velocity_x = initial_velocity * math.cos(theta)
        initial_velocity_y = initial_velocity * math.sin(theta)
        time_elapsed += 1 / FPS
        if time_elapsed > flight_time:
            time_elapsed = 0
        position_x = x_initial + initial_velocity_x * time_elapsed
        position_y = y_initial - ( initial_velocity_y * time_elapsed - 0.5 * gravity * time_elapsed**2 )
        pygame.draw.circle(SCREEN, (255, 0, 0), (position_x, position_y), 10)


        # ========================================================= #
        ### Trayectory ###
        trajectory.append((position_x, position_y))
        if len(trajectory) > 1:
            pygame.draw.lines(SCREEN, 'Green', False, trajectory, 1)


        # ========================================================= #
        ### Velocity vector ###
        velocity_x_start_0 = 20
        velocity_x_start_1 = 700
        velocity_x_start = (velocity_x_start_0 + initial_velocity_x * time_elapsed, velocity_x_start_1 - ( initial_velocity_y * time_elapsed - 0.5 * gravity * time_elapsed**2 ))
        velocity_x_end_0 = 70
        velocity_x_end_1 = 700
        velocity_x_end = (velocity_x_end_0 + initial_velocity_x * time_elapsed, velocity_x_end_1 - ( initial_velocity_y * time_elapsed - 0.5 * gravity * time_elapsed**2 ))

        velocity_y_start_0 = 20
        velocity_y_start_1 = 700
        velocity_y_start = (velocity_y_start_0 + initial_velocity_x * time_elapsed, velocity_y_start_1 - ( initial_velocity_y * time_elapsed - 0.5 * gravity * time_elapsed**2 ))
        velocity_y_end_0 = 20
        velocity_y_end_1 = 650
        velocity_y_end = (velocity_y_end_0 + initial_velocity_x * time_elapsed, velocity_y_end_1 - ( initial_velocity_y * time_elapsed - 0.5 * gravity * time_elapsed**2 ) + 50 * ( 1 -  round( initial_velocity_y - gravity * time_elapsed, 2 ) / initial_velocity_y ) )

        pygame.draw.line(SCREEN, 'White', velocity_x_start, velocity_x_end, 2)  # Velocity X
        pygame.draw.line(SCREEN, 'White', velocity_y_start, velocity_y_end, 2)  # Velocity Y


        # ========================================================= #
        ### Height max ###
        if round( initial_velocity_y - gravity * time_elapsed, 1 ) == 0.0:
            max_height_start = ( int( position_x ), int( HEIGHT - 10 )) # The lower
            max_height_end = ( int( position_x ), int( position_y) )    # The upper
            max_height_arrived = True
            height_max = 700 - position_y
        pygame.draw.line(SCREEN, 'Blue', max_height_start, max_height_end, 2)


        # ========================================================= #
        ### Range max ###
        if round( position_x - 20 , 2) >= ( initial_velocity**2 / gravity ) * math.sin( 2 * theta ) - 0.5:
            max_width_start = ( 10, HEIGHT - 15 )
            max_width_end = ( position_x, HEIGHT - 15 )
            max_width_arrived = True
            width_max = position_x - 20
        pygame.draw.line(SCREEN, 'Blue', max_width_start, max_width_end, 2)


        # ========================================================= #
        ### Variables in screen ###
        position_x_text = 'Position x: %s' % ( round( position_x - 20, 2 ) )
        text_surface = get_font(15).render(position_x_text, True, 'White')
        SCREEN.blit(text_surface, (20,10))

        position_y_text = 'Position y: %s' % ( round( 700 - position_y, 2 ) )
        text_surface = get_font(15).render(position_y_text, True, 'White')
        SCREEN.blit(text_surface, (20,50))

        velocity_x_text = 'Velocity x: %s' % ( round( initial_velocity_x, 2 ) )
        text_surface = get_font(15).render(velocity_x_text, True, 'White')
        SCREEN.blit(text_surface, (300,10))

        velocity_y_text = 'Velocity y: %s' % ( round( initial_velocity_y - gravity * time_elapsed, 2 ) )
        text_surface = get_font(15).render(velocity_y_text, True, 'White')
        SCREEN.blit(text_surface, (300, 50))

        initial_angle_text = 'Initial angle(°): %s' % ( initial_angle )
        text_surface = get_font(15).render(initial_angle_text, True, 'White')
        SCREEN.blit(text_surface, (580, 10))

        time_text = 'Time: %s' % ( round( time_elapsed, 2 ) )
        text_surface = get_font(15).render(time_text, True, 'White')
        SCREEN.blit(text_surface, (580, 50))

        if max_height_arrived:
            max_height_text = 'Max height: %s' % ( round( height_max, 2 ) )
            text_surface = get_font(15).render(max_height_text, True, 'White')
            SCREEN.blit(text_surface, (920, 10))

        if max_width_arrived:
            max_width_text = 'Max width: %s' % ( round( width_max, 2 ))
            text_surface = get_font(15).render(max_width_text, True, 'White')
            SCREEN.blit(text_surface, (920, 50))


        ### Lines of the axis ###
        pygame.draw.line(SCREEN, 'Green', (10, HEIGHT-10), (WIDTH, HEIGHT-10),2)
        pygame.draw.line(SCREEN, 'Green', (10, HEIGHT-10), (10, 0),2)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def initial_angle(initial_velocity):
    pygame.display.set_caption('Parabolic movement: initial conditions - angle')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    initial_angle = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((485,300), (300, 80)),
        manager=manager,
        object_id='#initial_angle'
    )
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('black')
        TEXT = get_font(45).render('Initial angle(°)', True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        BACK = Button(image=None, pos=(540,460), text_input='Back', font=get_font(25), base_color='White', hovering_color='Green')
        NEXT = Button(image=None, pos=(740,460), text_input='Next', font=get_font(25), base_color='White', hovering_color='Green')

        BACK.changeColor(MOUSE_POS)
        BACK.update(SCREEN)
        NEXT.changeColor(MOUSE_POS)
        NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#initial_angle':
                initial_angle_value = float(event.text)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    initial_velocity()
                if NEXT.checkForInput(MOUSE_POS):
                    parabolic_movement(initial_velocity,initial_angle_value)
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(SCREEN)
        pygame.display.update()


def initial_velocity():
    pygame.display.set_caption('Parabolic movement: initial conditions - velocity')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    initial_velocity = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((485,300), (300,80)),
        manager=manager,
        object_id='#initial_velocity',
    )
    while True:
        MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill('black')

        TEXT = get_font(45).render('Initial velocity(m/s)', True, 'white')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        BACK = Button(image=None, pos=(540,460), text_input='Back', font=get_font(25), base_color='White', hovering_color='Green')
        NEXT = Button(image=None, pos=(740,460), text_input='Next', font=get_font(25), base_color='White', hovering_color='Green')

        BACK.changeColor(MOUSE_POS)
        BACK.update(SCREEN)
        NEXT.changeColor(MOUSE_POS)
        NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#initial_velocity':
                initial_velocity_value = float(event.text)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    main_menu()
                if NEXT.checkForInput(MOUSE_POS):
                    initial_angle(initial_velocity_value)

            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(SCREEN)
        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BACKGROUND, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render('PHYSICS EXPERIMENTS', True, '#b68f40')
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PARABOLIC_BUTTON = Button(image=pygame.image.load('assets/static/images/options.png'),
                            pos=(640, 250), text_input='PARABOLIC MOVEMENT', font=get_font(20),
                            base_color='#d7fcd4', hovering_color='white'
                    )
        MIELVA_BUTTON = Button(image=None, pos=(1200,680), text_input='MilevaDot', font=get_font(10), base_color='#b68f40', hovering_color='Green')

        for button in [PARABOLIC_BUTTON,MIELVA_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if PARABOLIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                    initial_velocity()
        pygame.display.update()


main_menu()
