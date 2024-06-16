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
    # return pygame.font.Font('assets/static/font.ttf', size)
    return pygame.font.Font('assets/static/Teko-Medium.ttf', size)

def interference():
    pygame.display.set_caption('Interferencia: Simulación')
    wave_sources = []
    amplitude = 100
    wavelength = 20
    speed = 1
    time = 0
    def calculate_amplitude(x, y, sources, t):
        total_amplitude = 0
        for sx, sy, start_time in sources:
            distance = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
            elapsed_time = t - start_time
            # Solo calcular si la onda ha alcanzado el punto
            if distance <= elapsed_time * speed:
                wave_amplitude = amplitude * math.sin(2 * math.pi * (distance / wavelength - elapsed_time)) + 20
                total_amplitude += wave_amplitude
        return total_amplitude

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220,80), text_input='Menú principal', font=get_font(20),
                                  base_color='#d7fcd4', hovering_color='Green')
    
        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                wave_sources.append((mouse_x, mouse_y, time))

        SCREEN.fill('Black')
        for x in range(0, 800):
            for y in range(0, 600):
                amplitude_at_point = calculate_amplitude(x, y, wave_sources, time)
                color_value = 127.5 * (1 + math.sin(amplitude_at_point / amplitude))
                color_value = int(max(0, min(255, color_value)))  # Limitar el valor entre 0 y 255
                color = (color_value, color_value, color_value)
                SCREEN.set_at((x, y), color)

        time += 1
        pygame.display.flip()
        clock.tick(60)

def wave():
    pygame.display.set_caption('Ondas: Simulación')
    amplitude = 40
    frequency = 0.1
    speed = 1
    start_x = 0

    waves = []

    while True:
        SCREEN.fill('Black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220,80), text_input='Menú principal', font=get_font(20),
                                  base_color='#d7fcd4', hovering_color='Green')
    
        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)

        # for x in range(0, 320):
        #     y = int(amplitude * math.sin(frequency * (x + start_x)) + 40)
        #     pygame.draw.circle(SCREEN, (255, 255, 255), (x, y), 2)
        # start_x += speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                waves.append((mouse_x, mouse_y, 0))
        
        for i, wave in enumerate(waves):
            x, y, radius = wave
            if radius < 300:
                pygame.draw.circle(SCREEN, (0, 0, 255), (x, y), radius, 2)
                waves[i] = (x, y, radius + 1)
        clock.tick(60)
        pygame.display.update()


def equipotencial_surface(charge):
    pygame.display.set_caption('Superficies equipotenciales: Simulación')

    while True:
        SCREEN.fill('Black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220,80), text_input='Menú principal', font=get_font(20),
                                  base_color='#d7fcd4', hovering_color='Green')
        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)

        # ========================================================= #
        ### Particle ###
        pygame.draw.line(SCREEN, 'Green', (250, 360), (1030, 360), 2)
        pygame.draw.line(SCREEN, 'Green', (640, 20), (640, 700), 2)
        pygame.draw.line(SCREEN, 'Green', (250, 20), (1030, 700), 2)
        pygame.draw.line(SCREEN, 'Green', (250, 700), (1030, 20), 2)



        if charge == 'positive':
            pygame.draw.circle(SCREEN, (255, 0, 0), (640, 360), 20)
            pygame.draw.line(SCREEN, 'Green', (820,350), (830, 360), 2)
            pygame.draw.line(SCREEN, 'Green', (820,370), (830, 360), 2)

            pygame.draw.line(SCREEN, 'Green', (460,350), (450, 360), 2)
            pygame.draw.line(SCREEN, 'Green', (460,370), (450, 360), 2)

            pygame.draw.line(SCREEN, 'Green', (630,180), (640, 170), 2)
            pygame.draw.line(SCREEN, 'Green', (650,180), (640, 170), 2)

            pygame.draw.line(SCREEN, 'Green', (630,540), (640, 550), 2)
            pygame.draw.line(SCREEN, 'Green', (650,540), (640, 550), 2)

            charge_text = '+'
        if charge == 'negative':
            pygame.draw.circle(SCREEN, (0, 0, 255), (640, 360), 20)
            pygame.draw.line(SCREEN, 'Green', (820,350), (810, 360), 2)
            pygame.draw.line(SCREEN, 'Green', (820,370), (810, 360), 2)

            pygame.draw.line(SCREEN, 'Green', (460,350), (470, 360), 2)
            pygame.draw.line(SCREEN, 'Green', (460,370), (470, 360), 2)

            pygame.draw.line(SCREEN, 'Green', (630,180), (640, 190), 2)
            pygame.draw.line(SCREEN, 'Green', (650,180), (640, 190), 2)

            pygame.draw.line(SCREEN, 'Green', (630,540), (640, 530), 2)
            pygame.draw.line(SCREEN, 'Green', (650,540), (640, 530), 2)
            charge_text = '-'


        text_surface = get_font(25).render(charge_text, True, 'White')
        SCREEN.blit(text_surface, (635, 346))
        pygame.draw.circle(SCREEN, (255, 255, 255), (640, 360), 40, width=1)
        pygame.draw.circle(SCREEN, (255, 255, 255), (640, 360), 80, width=1)
        pygame.draw.circle(SCREEN, (255, 255, 255), (640, 360), 160, width=1)
        pygame.draw.circle(SCREEN, (255, 255, 255), (640, 360), 320, width=1)
        pygame.draw.circle(SCREEN, (255, 255, 255), (640, 360), 500, width=1)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def charge():
    pygame.display.set_caption('Superficies equipotenciales: Carga')

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('Black')
        TEXT = get_font(45).render("Carga de la partícula", True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        POSITIVE = Button(image=None, pos=(440,460), text_input='Positiva', font=get_font(25), base_color='White', hovering_color='Red')
        NEGATIVE = Button(image=None, pos=(840,460), text_input='Negativa', font=get_font(25), base_color='White', hovering_color='Blue')

        POSITIVE.changeColor(MOUSE_POS)
        POSITIVE.update(SCREEN)
        NEGATIVE.changeColor(MOUSE_POS)
        NEGATIVE.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if POSITIVE.checkForInput(MOUSE_POS):
                    equipotencial_surface(charge='positive')
                if NEGATIVE.checkForInput(MOUSE_POS):
                    equipotencial_surface(charge='negative')
        pygame.display.update()


def shm(length, angle):
    pygame.display.set_caption('Movimiento armónico simple: Simulación')

    x = 0
    y = 0
    gravity = 10
    time_elapsed = 0
    pendulum_length = length
    pendulum_angle = math.radians(angle)
    av = 0
    trajectory = []

    while True:
        SCREEN.fill('Black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos = (1220, 80), text_input='Menú principal', font=get_font(20),
                                  base_color='#d7fcd4', hovering_color='Green')
        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)

        acc = ( - gravity / pendulum_length ) * math.sin( pendulum_angle )
        av += acc * ( 1 / 1000 )
        pendulum_angle += av
        x = pendulum_length * math.sin( pendulum_angle ) + 200
        y = pendulum_length * math.cos( pendulum_angle ) + 40

        pygame.draw.line(SCREEN, 'White', (200, 40), (x, y), 1)
        pygame.draw.circle(SCREEN, 'Red', ( x,  y), 8)

        # ========================================================= #
        ### Trayectory ###
        trajectory.append( (x, y) )
        if len(trajectory) > 1:
            pygame.draw.lines(SCREEN, 'Pink', False, trajectory, 1)

        # ========================================================= #
        ### Variables in screen ###
        initial_angle_text = 'Ángulo inicial(°): %s' % ( angle )
        text_surface = get_font(20).render(initial_angle_text, True, 'White')
        SCREEN.blit(text_surface, (640, 80))

        initial_length_text = 'Longitud del péndulo(m): %s' % ( pendulum_length )
        text_surface = get_font(20).render(initial_length_text, True, 'White')
        SCREEN.blit(text_surface, (640, 120))

        position_x_text = 'Posición x: %s' % ( round(x - 200, 2) )
        text_surface = get_font(20).render(position_x_text, True, 'White')
        SCREEN.blit(text_surface, (640, 160))

        position_y_text = 'Posición y: %s' % ( round(y - 39, 2) )
        text_surface = get_font(20).render(position_y_text, True, 'White')
        SCREEN.blit(text_surface, (640, 200))

        x_axis_text = 'x'
        text_surface = get_font(20).render(x_axis_text, True, 'White')
        SCREEN.blit(text_surface, (620, 15))

        y_axis_text = 'y'
        text_surface = get_font(20).render(y_axis_text, True, 'White')
        SCREEN.blit(text_surface, (210, 680))

        # Lines of the axis
        pygame.draw.line(SCREEN, 'Green', (10, 40), (640, 40), 2)
        pygame.draw.line(SCREEN, 'Green', (200, 40), (200, 720), 2)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def pendulum_initial_angle(pendulum_length):
    pygame.display.set_caption('Movimiento armónico simple: condiciones iniciales - Ángulo')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    pendulum_initial_angle = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((485,300), (300,80)),
        manager=manager,
        object_id='#pendulum_initial_angle',
    )
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('black')

        TEXT = get_font(45).render('Ángulo(°)', True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        BACK = Button(image=None, pos=(540,460), text_input='Atrás', font=get_font(25), base_color='White', hovering_color='Green')
        NEXT = Button(image=None, pos=(740,460), text_input='Adelante', font=get_font(25), base_color='White', hovering_color='Green')

        BACK.changeColor(MOUSE_POS)
        BACK.update(SCREEN)
        NEXT.changeColor(MOUSE_POS)
        NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#pendulum_initial_angle':
                pendulum_angle_value = float(event.text)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    main_menu()
                if NEXT.checkForInput(MOUSE_POS):
                    shm(pendulum_length, pendulum_angle_value)

            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(SCREEN)
        pygame.display.update()


def pendulum_length():
    pygame.display.set_caption('Movimiento armónico simple: condiciones iniciales - Longitud')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    pendulum_length = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((485,300), (300,80)),
        manager=manager,
        object_id='#pendulum_length',
    )
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('black')

        TEXT = get_font(45).render('Longitud del péndulo(m)', True, 'white')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        BACK = Button(image=None, pos=(540,460), text_input='Atrás', font=get_font(25), base_color='White', hovering_color='Green')
        NEXT = Button(image=None, pos=(740,460), text_input='Adelante', font=get_font(25), base_color='White', hovering_color='Green')

        BACK.changeColor(MOUSE_POS)
        BACK.update(SCREEN)
        NEXT.changeColor(MOUSE_POS)
        NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#pendulum_length':
                pendulum_length_value = float(event.text)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    main_menu()
                if NEXT.checkForInput(MOUSE_POS):
                    pendulum_initial_angle(pendulum_length_value)

            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(SCREEN)
        pygame.display.update()


def parabolic_movement(initial_velocity, initial_angle):
    pygame.display.set_caption('Movimiento parabólico: Simulación')

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
        BACK_MENU_BUTTON = Button(image=None, pos = (1220, 80), text_input='Menú principal', font=get_font(20),
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
            pygame.draw.lines(SCREEN, 'White', False, trajectory, 1)


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
        position_x_text = 'Posición x: %s' % ( round( position_x - 20, 2 ) )
        text_surface = get_font(20).render(position_x_text, True, 'White')
        SCREEN.blit(text_surface, (20,10))

        position_y_text = 'Posición y: %s' % ( round( 700 - position_y, 2 ) )
        text_surface = get_font(20).render(position_y_text, True, 'White')
        SCREEN.blit(text_surface, (20,50))

        velocity_x_text = 'Velocidad x: %s' % ( round( initial_velocity_x, 2 ) )
        text_surface = get_font(20).render(velocity_x_text, True, 'White')
        SCREEN.blit(text_surface, (300,10))

        velocity_y_text = 'Velocidad y: %s' % ( round( initial_velocity_y - gravity * time_elapsed, 2 ) )
        text_surface = get_font(20).render(velocity_y_text, True, 'White')
        SCREEN.blit(text_surface, (300, 50))

        initial_angle_text = 'Ángulo inicial(°): %s' % ( initial_angle )
        text_surface = get_font(20).render(initial_angle_text, True, 'White')
        SCREEN.blit(text_surface, (580, 10))

        time_text = 'Tiempo: %s' % ( round( time_elapsed, 2 ) )
        text_surface = get_font(20).render(time_text, True, 'White')
        SCREEN.blit(text_surface, (580, 50))

        if max_height_arrived:
            max_height_text = 'Altura máxima: %s' % ( round( height_max, 2 ) )
            text_surface = get_font(20).render(max_height_text, True, 'White')
            SCREEN.blit(text_surface, (920, 10))

        if max_width_arrived:
            max_width_text = 'Alcance máximo: %s' % ( round( width_max, 2 ))
            text_surface = get_font(20).render(max_width_text, True, 'White')
            SCREEN.blit(text_surface, (920, 50))

        x_axis_text = 'x'
        text_surface = get_font(20).render(x_axis_text, True, 'White')
        SCREEN.blit(text_surface, (1180, 680))

        y_axis_text = 'y'
        text_surface = get_font(20).render(y_axis_text, True, 'White')
        SCREEN.blit(text_surface, (20, 120))

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
    pygame.display.set_caption('Movimiento parabólico: condiciones iniciales - ángulo')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    initial_angle = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((485,300), (300, 80)),
        manager=manager,
        object_id='#initial_angle'
    )
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('black')
        TEXT = get_font(45).render('Ángulo inicial(°)', True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        BACK = Button(image=None, pos=(540,460), text_input='Atrás', font=get_font(25), base_color='White', hovering_color='Green')
        NEXT = Button(image=None, pos=(740,460), text_input='Adelante', font=get_font(25), base_color='White', hovering_color='Green')

        BACK.changeColor(MOUSE_POS)
        BACK.update(SCREEN)
        NEXT.changeColor(MOUSE_POS)
        NEXT.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#initial_angle':
                initial_angle_value = float(event.text) or None
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
    pygame.display.set_caption('Movimiento parabólico: condiciones iniciales - velocidad')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    initial_velocity = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((485,300), (300,80)),
        manager=manager,
        object_id='#initial_velocity',
    )
    while True:
        MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill('black')

        TEXT = get_font(45).render('Velocidad inicial(m/s)', True, 'white')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        BACK = Button(image=None, pos=(540,460), text_input='Atrás', font=get_font(25), base_color='White', hovering_color='Green')
        NEXT = Button(image=None, pos=(740,460), text_input='Siguiente', font=get_font(25), base_color='White', hovering_color='Green')

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

        MENU_TEXT = get_font(100).render('EXPERIMENTOS DE FÍSICA', True, '#b68f40')
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PARABOLIC_BUTTON = Button(image=pygame.image.load('assets/static/images/options.png'),
                            pos=(280, 250), text_input='MOVIMIENTO PARABÓLICO', font=get_font(35),
                            base_color='#d7fcd4', hovering_color='White'
                        )
    
        SHM_BUTTON = Button(image=pygame.image.load('assets/static/images/options.png'),
                            pos=(280,400), text_input='MOVIMIENTO ARMÓNICO SIMPLE', font=get_font(35),
                            base_color='#d7fcd4', hovering_color='White'
                        )
        
        EQUIPOTENTIALS_BUTTON = Button(image=pygame.image.load('assets/static/images/options.png'),
                            pos=(280,550), text_input='SUPERFICIES EQUIPOTENCIALES', font=get_font(35),
                            base_color='#d7fcd4', hovering_color='White'
                        )

        WAVES_BUTTON = Button(image=pygame.image.load('assets/static/images/options.png'),
                            pos=(1000, 250), text_input='ONDAS', font=get_font(35),
                            base_color='#d7fcd4', hovering_color='White'
                        )

        INTERFERENCE_BUTTON = Button(image=pygame.image.load('assets/static/images/options.png'),
                            pos=(1000, 400), text_input='INTERFERENCIA', font=get_font(35),
                            base_color='#d7fcd4', hovering_color='White'
                        )

        MILEVA_BUTTON = Button(image=None, pos=(1200,680), text_input='MilevaDot', font=get_font(20), base_color='#b68f40', hovering_color='Green')

        for button in [PARABOLIC_BUTTON,SHM_BUTTON,EQUIPOTENTIALS_BUTTON,WAVES_BUTTON,INTERFERENCE_BUTTON,MILEVA_BUTTON]:
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
                if SHM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pendulum_length()
                if EQUIPOTENTIALS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    charge()
                if WAVES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    wave()
                if INTERFERENCE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    interference()
        pygame.display.update()


main_menu()
