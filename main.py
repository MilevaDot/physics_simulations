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

favicon = pygame.image.load('assets/static/images/favicon.png')
pygame.display.set_icon(favicon)

def get_font(size):
    # return pygame.font.Font('assets/static/font.ttf', size)
    return pygame.font.Font('assets/static/Teko-Medium.ttf', size)


def lens_simulation():
    pygame.display.set_caption('Simulación de Lentes')

    CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    LENS_HEIGHT = int(0.8 * HEIGHT)
    MAX_OBJECT_HEIGHT = LENS_HEIGHT // 2
    FOCAL_LENGTH = 150

    # Colores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

    def draw_dotted_arrow(screen, color, start, end, arrow_size=10, dash_length=10, gap_length=5):
        total_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        angle = math.atan2(dy, dx)

        num_dashes = int(total_length // (dash_length + gap_length))
        for i in range(num_dashes):
            start_dash_x = start[0] + (i * (dash_length + gap_length)) * math.cos(angle)
            start_dash_y = start[1] + (i * (dash_length + gap_length)) * math.sin(angle)
            end_dash_x = start_dash_x + dash_length * math.cos(angle)
            end_dash_y = start_dash_y + dash_length * math.sin(angle)

            pygame.draw.line(screen, color, (start_dash_x, start_dash_y), (end_dash_x, end_dash_y), 2)

        arrow_points = [
            (end[0] - arrow_size * math.cos(angle - math.pi / 6), end[1] - arrow_size * math.sin(angle - math.pi / 6)),
            (end[0] - arrow_size * math.cos(angle + math.pi / 6), end[1] - arrow_size * math.sin(angle + math.pi / 6))
        ]
        pygame.draw.polygon(screen, color, [end, *arrow_points])


    def draw_arrow(screen, color, start, end, arrow_size=10):
        pygame.draw.line(screen, color, start, end, 2)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_points = [
            (end[0] - arrow_size * math.cos(angle - math.pi / 6), end[1] - arrow_size * math.sin(angle - math.pi / 6)),
            (end[0] - arrow_size * math.cos(angle + math.pi / 6), end[1] - arrow_size * math.sin(angle + math.pi / 6))
        ]
        pygame.draw.polygon(screen, color, [end, *arrow_points])

    class ObjectArrow:
        def __init__(self):
            self.x = CENTER_X - 300
            self.height = MAX_OBJECT_HEIGHT // 2
            self.dragging = False

        def draw(self):
            pygame.draw.line(SCREEN, YELLOW, (self.x, CENTER_Y), (self.x, CENTER_Y - self.height), 5)
            pygame.draw.polygon(SCREEN, YELLOW, [(self.x, CENTER_Y - self.height), (self.x - 10, CENTER_Y - self.height + 20), (self.x + 10, CENTER_Y - self.height + 20)])

        def update(self, mouse_x, mouse_y):
            if self.dragging:
                self.x = max(0, min(mouse_x, CENTER_X))
                self.height = min(max(CENTER_Y - mouse_y, 10), MAX_OBJECT_HEIGHT)

    class Lens:
        def __init__(self, converging=True):
            self.converging = converging

        def draw(self):
            pygame.draw.line(SCREEN, WHITE, (0, CENTER_Y), (WIDTH, CENTER_Y), 1)
            pygame.draw.line(SCREEN, WHITE, (CENTER_X, CENTER_Y - LENS_HEIGHT // 2), (CENTER_X, CENTER_Y + LENS_HEIGHT // 2), 5)
            if self.converging:
                pygame.draw.polygon(SCREEN, WHITE, [(CENTER_X, CENTER_Y - LENS_HEIGHT // 2), (CENTER_X - 20, CENTER_Y - LENS_HEIGHT // 2 + 20), (CENTER_X + 20, CENTER_Y - LENS_HEIGHT // 2 + 20)])
                pygame.draw.polygon(SCREEN, WHITE, [(CENTER_X, CENTER_Y + LENS_HEIGHT // 2), (CENTER_X - 20, CENTER_Y + LENS_HEIGHT // 2 - 20), (CENTER_X + 20, CENTER_Y + LENS_HEIGHT // 2 - 20)])
            else:
                pygame.draw.polygon(SCREEN, WHITE, [(CENTER_X, CENTER_Y - LENS_HEIGHT // 2 + 20), (CENTER_X + 20, CENTER_Y - LENS_HEIGHT // 2), (CENTER_X - 20, CENTER_Y - LENS_HEIGHT // 2)])
                pygame.draw.polygon(SCREEN, WHITE, [(CENTER_X, CENTER_Y + LENS_HEIGHT // 2 - 20), (CENTER_X + 20, CENTER_Y + LENS_HEIGHT // 2), (CENTER_X - 20, CENTER_Y + LENS_HEIGHT // 2)])

    def calculate_intersection(line1_start, line1_end, line2_start, line2_end):
        x1, y1 = line1_start
        x2, y2 = line1_end
        x3, y3 = line2_start
        x4, y4 = line2_end

        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return None

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
        return int(px), int(py)

    def draw_principal_rays(lens, obj, font):
        f1 = (CENTER_X - FOCAL_LENGTH, CENTER_Y)
        f2 = (CENTER_X + FOCAL_LENGTH, CENTER_Y)
        
        pygame.draw.circle(SCREEN, RED, f1, 5)
        pygame.draw.circle(SCREEN, RED, f2, 5)

        font = pygame.font.Font(None, 36)
        f1_label = font.render("F1", True, WHITE)
        f2_label = font.render("F2", True, WHITE)

        SCREEN.blit(f1_label, (f1[0] - 20, f1[1] + 10))
        SCREEN.blit(f2_label, (f2[0] + 10, f2[1] + 10))

        if lens.converging:
            if obj.x < f1[0]:
                ray_start = (obj.x, CENTER_Y - obj.height)
                ray_focus_end = f2
                ray_parallel_end = (CENTER_X, CENTER_Y - obj.height)

                draw_arrow(SCREEN, BLUE, ray_start, ray_parallel_end)
                draw_arrow(SCREEN, BLUE, ray_parallel_end, ray_focus_end)
                draw_arrow(SCREEN, BLUE, ray_start, (CENTER_X, CENTER_Y))

                ray_guide_center_start = (obj.x, CENTER_Y - obj.height)
                if CENTER_X - ray_guide_center_start[0] == 0:
                    slope_center = ( CENTER_Y - ray_guide_center_start[1]) / ( CENTER_X - ray_guide_center_start[0] + 0.1 )
                else:
                    slope_center = ( CENTER_Y - ray_guide_center_start[1]) / ( CENTER_X - ray_guide_center_start[0])
                max_center_x = WIDTH - 20
                max_center_y = ray_guide_center_start[1] + slope_center * (max_center_x - ray_guide_center_start[0])
                ray_center_end = (max_center_x, max_center_y)
                draw_arrow(SCREEN, BLUE, ray_guide_center_start, ray_center_end)

                ray_focus_start = (obj.x, CENTER_Y - obj.height)
                if f1[0] - ray_focus_start[0] == 0:
                    slope = (f1[1] - ray_focus_start[1]) / (f1[0] - ray_focus_start[0] + 0.1)
                else:
                    slope = (f1[1] - ray_focus_start[1]) / (f1[0] - ray_focus_start[0])
                lens_intersect_y = int(ray_focus_start[1] + slope * (CENTER_X - ray_focus_start[0]))
                ray_parallel_end = (CENTER_X, lens_intersect_y)
                draw_arrow(SCREEN, BLUE, ray_focus_start, f1)
                draw_arrow(SCREEN, BLUE, f1, ray_parallel_end)  # Esta es la que empieza en f1 y se va hasta la lente
                draw_arrow(SCREEN, BLUE, ray_parallel_end, (WIDTH - 20,lens_intersect_y))  # Esta es la que empieza en la lente y se va a la derecha

                ray_parallel_end_new = (CENTER_X, CENTER_Y - obj.height)
                slope_f2 = (f2[1] - ray_parallel_end_new[1]) / (f2[0] - ray_parallel_end_new[0])  # Pendiente entre F2 y el borde derecho
                max_x = WIDTH - 20
                max_y = ray_parallel_end_new[1] + slope_f2 * (max_x - ray_parallel_end_new[0])
                ray_f2_end = (max_x, max_y)
                draw_arrow(SCREEN, BLUE, f2, ray_f2_end)  # Dibuja flecha desde F2 hacia la derecha hasta ray_f2_end

                intersection = calculate_intersection(f2, ray_f2_end, ray_parallel_end, (WIDTH - 20, lens_intersect_y))
                if intersection:
                    draw_arrow(SCREEN, GREEN, (intersection[0], CENTER_Y), intersection)
            else:
                ray_start = (obj.x, CENTER_Y - obj.height)
                draw_arrow(SCREEN, BLUE, ray_start, (CENTER_X, CENTER_Y))
                ray_start = (obj.x, CENTER_Y - obj.height)
                if CENTER_X - ray_start[0] == 0:
                    slope_center = ( CENTER_Y - ray_start[1]) / ( CENTER_X - ray_start[0] + 0.1 )
                else:
                    slope_center = ( CENTER_Y - ray_start[1]) / ( CENTER_X - ray_start[0])
                max_center_x = WIDTH - 400
                max_center_y = ray_start[1] + slope_center * (max_center_x - ray_start[0])
                ray_center_end = (max_center_x, max_center_y)
                draw_arrow(SCREEN, BLUE, ray_start, ray_center_end)

                ray_center_out_end = ray_start[1] + slope_center * (WIDTH - 1230 - ray_start[0])

                ray_parallel_end = (CENTER_X, CENTER_Y - obj.height)
                draw_arrow(SCREEN, BLUE, ray_start, ray_parallel_end)
                draw_arrow(SCREEN, BLUE, ray_parallel_end, f2)
                f2_focal_slope = (f2[1] - ray_parallel_end[1]) / (f2[0] - ray_parallel_end[0])
                ray_f2_focal_out_end = ray_parallel_end[1] + f2_focal_slope * (WIDTH - 1230 - ray_parallel_end[0])

                intersection = calculate_intersection((WIDTH - 1230, ray_f2_focal_out_end), ray_parallel_end, (WIDTH - 1230, ray_center_out_end), ray_start)


                if intersection:
                    draw_arrow(SCREEN, GREEN, (intersection[0], CENTER_Y), intersection)
                    draw_dotted_arrow(SCREEN, BLUE, intersection, ray_start, dash_length=10, gap_length=5)
                    draw_dotted_arrow(SCREEN, BLUE, intersection, ray_parallel_end, dash_length=10, gap_length=5)
                    draw_arrow(SCREEN, BLUE, ray_start, (CENTER_X, intersection[1]))
                    draw_arrow(SCREEN, BLUE, (CENTER_X, intersection[1]), (WIDTH - 400, intersection[1]))
                    draw_dotted_arrow(SCREEN, BLUE, intersection, (CENTER_X, intersection[1]), dash_length=10, gap_length=5)


        else:
            ray_parallel_start = (obj.x, CENTER_Y - obj.height)
            ray_parallel_end = (CENTER_X, CENTER_Y - obj.height)
            draw_arrow(SCREEN, BLUE, ray_parallel_start, ray_parallel_end)
            ray_parallel_aux_start = f1
            
            parallel_slope = (ray_parallel_end[1] - f1[1]) / (ray_parallel_end[0] - f1[0])
            ray_parallel_out_end = ray_parallel_end[1] + parallel_slope * (WIDTH - 500 - ray_parallel_end[0])

            draw_arrow(SCREEN, BLUE, ray_parallel_end, (WIDTH - 500, ray_parallel_out_end))

            ray_center_start = (obj.x, CENTER_Y - obj.height)
            ray_center_end = (CENTER_X, CENTER_Y)
            draw_arrow(SCREEN, BLUE, ray_center_start, ray_center_end)

            ray_f2_start = (obj.x, CENTER_Y - obj.height)
            if CENTER_X - ray_center_start[0] == 0:
                ray_center_slope = (CENTER_Y - ray_center_start[1]) / (CENTER_X - ray_center_start[0] + 0.1)
            else:
                ray_center_slope = (CENTER_Y - ray_center_start[1]) / (CENTER_X - ray_center_start[0])
            ray_center_out_end = ray_center_start[1] + ray_center_slope * (WIDTH - 300 - ray_center_start[0])
            draw_arrow(SCREEN, BLUE, (CENTER_X, CENTER_Y), (WIDTH - 300, ray_center_out_end))

            intersection = calculate_intersection(ray_parallel_aux_start, ray_parallel_end, ray_center_start, ray_center_end)
            if intersection:
                draw_arrow(SCREEN, GREEN, (intersection[0], CENTER_Y), intersection)
                draw_dotted_arrow(SCREEN, BLUE, intersection, ray_parallel_end, dash_length=10, gap_length=5)
                draw_dotted_arrow(SCREEN, BLUE, intersection, (CENTER_X, intersection[1]), dash_length=10, gap_length=5)
                draw_arrow(SCREEN, BLUE, ray_f2_start, (CENTER_X, intersection[1]))
                draw_arrow(SCREEN, BLUE, (CENTER_X, intersection[1]), (WIDTH - 400, intersection[1]))

    obj = ObjectArrow()
    lens = Lens(converging=True)
    font = pygame.font.Font(None, 36)
    running = True
    while running:
        SCREEN.fill(BLACK)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220,80), text_input='Menú principal', font=get_font(20),
                                  base_color='#FFFFFF', hovering_color='Brown')
        CONVERGENT_BUTTON = Button(image=None, pos=(100, 80), text_input='Lente convergente', font=get_font(20),
                                  base_color='#FFFFFF', hovering_color='Brown')
        DIVERGENTE_BUTTON = Button(image=None, pos=(240, 80), text_input='Lente divergente', font=get_font(20),
                                  base_color='#FFFFFF', hovering_color='Brown')
        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)
        CONVERGENT_BUTTON.changeColor(MENU_MOUSE_POS)
        CONVERGENT_BUTTON.update(SCREEN)
        DIVERGENTE_BUTTON.changeColor(MENU_MOUSE_POS)
        DIVERGENTE_BUTTON.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if obj.x - 20 < event.pos[0] < obj.x + 20 and CENTER_Y - obj.height - 20 < event.pos[1] < CENTER_Y:
                    obj.dragging = True
                if CONVERGENT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lens_simulation()
                if DIVERGENTE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lens.converging = False
            elif event.type == pygame.MOUSEBUTTONUP:
                obj.dragging = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lens.converging = not lens.converging

        if obj.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            obj.update(mouse_x, mouse_y)

        lens.draw()
        obj.draw()
        draw_principal_rays(lens, obj, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def magnetic_field_simulation():
    pygame.display.set_caption('Simulación de Campo Magnético')

    # WIDTH, HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    BACKGROUND_COLOR = (255, 255, 255)
    BUTTON_COLOR = (200, 200, 200)
    BUTTON_HOVER_COLOR = (150, 150, 150)
    BUTTON_TEXT_COLOR = (0, 0, 0)
    BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50

    MAGNET_WIDTH = 30  # Tamaño del imán
    MAGNET_HEIGHT = 90
    MONOPOLE_RADIUS = 15  # Tamaño del monopolo
    LINE_SPACING = 20  # Espacio entre las líneas de campo
    ARROW_LENGTH = 12  # Tamaño de las flechas
    ARROW_HEAD_SIZE = 6

    button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw_button(screen, text):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def draw_arrow(screen, color, start, end, arrow_head_size):
        pygame.draw.line(screen, color, start, end, 2)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_head = [
            (end[0] - arrow_head_size * math.cos(angle - math.pi / 6), end[1] - arrow_head_size * math.sin(angle - math.pi / 6)),
            (end[0] - arrow_head_size * math.cos(angle + math.pi / 6), end[1] - arrow_head_size * math.sin(angle + math.pi / 6)),
            end
        ]
        pygame.draw.polygon(screen, color, arrow_head)

    def magnetic_field(px, py, magnets):
        Bx = 0
        By = 0
        for (x, y, mx, my) in magnets:
            if mx is not None and my is not None:  # Es un dipolo (imán)
                dx_n = px - x
                dy_n = py - y + MAGNET_HEIGHT // 4
                dx_s = px - x
                dy_s = py - y - MAGNET_HEIGHT // 4
                r_squared_n = dx_n**2 + dy_n**2
                r_squared_s = dx_s**2 + dy_s**2
                if r_squared_n > 0 and r_squared_s > 0:
                    # Campo saliendo desde el polo norte (rojo)
                    Bn = 1 / r_squared_n
                    Bx += Bn * dx_n / math.sqrt(r_squared_n)
                    By += Bn * dy_n / math.sqrt(r_squared_n)
                    # Campo entrando hacia el polo sur (azul)
                    Bs = -1 / r_squared_s
                    Bx += Bs * dx_s / math.sqrt(r_squared_s)
                    By += Bs * dy_s / math.sqrt(r_squared_s)
            else:  # Es un monopolo
                dx = px - x
                dy = py - y
                r_squared = dx**2 + dy**2
                if r_squared > 0:
                    B = 1 / r_squared
                    Bx += mx * B * dx / math.sqrt(r_squared)
                    By += my * B * dy / math.sqrt(r_squared)
        return Bx, By

    magnets = [
        (WIDTH // 2, HEIGHT // 2, 1, -1),  # Dipolo magnético inicial
    ]

    selected_magnet_index = None

    while True:
        SCREEN.fill(BACKGROUND_COLOR)

        MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1200,90), text_input='Menú principal', font=get_font(25),
                                  base_color='Brown', hovering_color='Black')
        BACK_MENU_BUTTON.changeColor(MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MOUSE_POS):
                    main_menu()
                mouse_x, mouse_y = event.pos
                if button_rect.collidepoint(mouse_x, mouse_y):
                    magnets.append((mouse_x, mouse_y, 1, -1))  # Nuevo dipolo en la posición del clic
                else:
                    for i, magnet in enumerate(magnets):
                        x, y, _, _ = magnet
                        if (x - MAGNET_WIDTH // 2 <= mouse_x <= x + MAGNET_WIDTH // 2 and
                            y - MAGNET_HEIGHT // 2 <= mouse_y <= y + MAGNET_HEIGHT // 2):
                            selected_magnet_index = i
                            break
            if event.type == pygame.MOUSEBUTTONUP:
                selected_magnet_index = None
            if event.type == pygame.MOUSEMOTION and selected_magnet_index is not None:
                mouse_x, mouse_y = event.pos
                x, y, mx, my = magnets[selected_magnet_index]
                magnets[selected_magnet_index] = (mouse_x, mouse_y, mx, my)

        for (x, y, mx, my) in magnets:
            if mx is not None and my is not None:
                pygame.draw.rect(SCREEN, (255, 0, 0), (x - MAGNET_WIDTH // 2, y - MAGNET_HEIGHT // 2, MAGNET_WIDTH, MAGNET_HEIGHT // 2))  # Polo norte arriba (rojo)
                pygame.draw.rect(SCREEN, (0, 0, 255), (x - MAGNET_WIDTH // 2, y, MAGNET_WIDTH, MAGNET_HEIGHT // 2))  # Polo sur abajo (azul)
            else:
                color = (255, 0, 0) if mx > 0 else (0, 0, 255)
                pygame.draw.circle(SCREEN, color, (x, y), MONOPOLE_RADIUS)

        for y in range(0, HEIGHT, LINE_SPACING):
            for x in range(0, WIDTH, LINE_SPACING):
                Bx, By = magnetic_field(x, y, magnets)
                magnitude = math.sqrt(Bx**2 + By**2)
                if magnitude > 0:
                    Bx /= magnitude
                    By /= magnitude
                    end_x = x + Bx * ARROW_LENGTH
                    end_y = y + By * ARROW_LENGTH
                    draw_arrow(SCREEN, (0, 0, 0), (x, y), (end_x, end_y), ARROW_HEAD_SIZE)

        draw_button(SCREEN, "Agregar imán")

        pygame.display.update()


def interference():
    WAVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(WAVE_EVENT, 2000)
    pygame.display.set_caption('Ondas: Simulación')

    waves1 = []
    waves2 = []

    while True:
        SCREEN.fill('Black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220, 80), text_input='Menú principal', font=get_font(20),
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
            if event.type == WAVE_EVENT:
                waves1.append((320, 360, 0))
                waves2.append((960, 360, 0))

        for i, wave in enumerate(waves1):
            x, y, radius = wave
            if radius < WIDTH:
                waves1[i] = (x, y, radius + 1)

        for i, wave in enumerate(waves2):
            x, y, radius = wave
            if radius < WIDTH:
                waves2[i] = (x, y, radius + 1)

        for x in range(0, WIDTH, 5):
            for y in range(0, HEIGHT, 5):
                amplitude1 = sum([math.sin(math.sqrt((x - wx) ** 2 + (y - wy) ** 2) - r) for wx, wy, r in waves1 if r < WIDTH])
                amplitude2 = sum([math.sin(math.sqrt((x - wx) ** 2 + (y - wy) ** 2) - r) for wx, wy, r in waves2 if r < WIDTH])
                total_amplitude = amplitude1 + amplitude2
                color_value = int((total_amplitude + 2) * 63.75)
                color_value = max(0, min(255, color_value))
                pygame.draw.circle(SCREEN, (color_value, color_value, 255 - color_value), (x, y), 2)

        clock.tick(FPS)
        pygame.display.update()


def transversal_wave(amplitude, period):
    pygame.display.set_caption('Onda Transversal: Simulación')

    frequency = 1 / period
    speed = 0.5
    phase = 0

    while True:
        SCREEN.fill('Black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220, 80), text_input='Menú principal', font=get_font(20),
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

        for x in range(0, WIDTH, 1):
            y = 360 + int(amplitude * math.sin(frequency * (x + phase)))
            pygame.draw.circle(SCREEN, (255, 0, 255), (x, y), 2)

        phase += speed
        clock.tick(FPS)
        pygame.display.update()


def transversal_period_wave(amplitude):
    pygame.display.set_caption('Escoge el periodo')

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('Black')
        TEXT = get_font(45).render('Escoge el periodo de la onda', True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640, 140))
        SCREEN.blit(TEXT, TEXT_RECT)


        PERIOD5 = Button(image=None, pos=(400, 360), text_input='5', font=get_font(25), base_color='White', hovering_color='Green')
        PERIOD10 = Button(image=None, pos=(600, 360), text_input='10', font=get_font(25), base_color='White', hovering_color='Green')
        PERIOD40 = Button(image=None, pos=(800, 360), text_input='40', font=get_font(25), base_color='White', hovering_color='Green')
        PERIOD80 = Button(image=None, pos=(400, 560), text_input='80', font=get_font(25), base_color='White', hovering_color='Green')
        PERIOD100 = Button(image=None, pos=(600, 560), text_input='100', font=get_font(25), base_color='White', hovering_color='Green')
        PERIOD200 = Button(image=None, pos=(800, 560), text_input='200', font=get_font(25), base_color='White', hovering_color='Green')

        PERIOD5.changeColor(MOUSE_POS)
        PERIOD5.update(SCREEN)
        PERIOD10.changeColor(MOUSE_POS)
        PERIOD10.update(SCREEN)
        PERIOD40.changeColor(MOUSE_POS)
        PERIOD40.update(SCREEN)
        PERIOD80.changeColor(MOUSE_POS)
        PERIOD80.update(SCREEN)
        PERIOD100.changeColor(MOUSE_POS)
        PERIOD100.update(SCREEN)
        PERIOD200.changeColor(MOUSE_POS)
        PERIOD200.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PERIOD5.checkForInput(MOUSE_POS):
                    transversal_wave(amplitude, 5)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PERIOD10.checkForInput(MOUSE_POS):
                    transversal_wave(amplitude, 10)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PERIOD40.checkForInput(MOUSE_POS):
                    transversal_wave(amplitude, 40)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PERIOD80.checkForInput(MOUSE_POS):
                    transversal_wave(amplitude, 80)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PERIOD100.checkForInput(MOUSE_POS):
                    transversal_wave(amplitude, 100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PERIOD200.checkForInput(MOUSE_POS):
                    transversal_wave(amplitude, 200)
        pygame.display.update()


def transversal_amplitud_wave():
    pygame.display.set_caption('Escoge la amplitud')

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('Black')
        TEXT = get_font(45).render('Escoge la amplitud de la onda', True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640, 140))
        SCREEN.blit(TEXT, TEXT_RECT)


        AMPLITUDE50 = Button(image=None, pos=(400, 360), text_input='50', font=get_font(25), base_color='White', hovering_color='Green')
        AMPLITUDE100 = Button(image=None, pos=(600, 360), text_input='100', font=get_font(25), base_color='White', hovering_color='Green')
        AMPLITUDE150 = Button(image=None, pos=(800, 360), text_input='150', font=get_font(25), base_color='White', hovering_color='Green')
        AMPLITUDE200 = Button(image=None, pos=(400, 560), text_input='200', font=get_font(25), base_color='White', hovering_color='Green')
        AMPLITUDE250 = Button(image=None, pos=(600, 560), text_input='500', font=get_font(25), base_color='White', hovering_color='Green')
        AMPLITUDE300 = Button(image=None, pos=(800, 560), text_input='600', font=get_font(25), base_color='White', hovering_color='Green')

        AMPLITUDE50.changeColor(MOUSE_POS)
        AMPLITUDE50.update(SCREEN)
        AMPLITUDE100.changeColor(MOUSE_POS)
        AMPLITUDE100.update(SCREEN)
        AMPLITUDE150.changeColor(MOUSE_POS)
        AMPLITUDE150.update(SCREEN)
        AMPLITUDE200.changeColor(MOUSE_POS)
        AMPLITUDE200.update(SCREEN)
        AMPLITUDE250.changeColor(MOUSE_POS)
        AMPLITUDE250.update(SCREEN)
        AMPLITUDE300.changeColor(MOUSE_POS)
        AMPLITUDE300.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AMPLITUDE50.checkForInput(MOUSE_POS):
                    transversal_period_wave(50)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AMPLITUDE100.checkForInput(MOUSE_POS):
                    transversal_period_wave(100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AMPLITUDE150.checkForInput(MOUSE_POS):
                    transversal_period_wave(150)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AMPLITUDE200.checkForInput(MOUSE_POS):
                    transversal_period_wave(200)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AMPLITUDE250.checkForInput(MOUSE_POS):
                    transversal_period_wave(250)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AMPLITUDE300.checkForInput(MOUSE_POS):
                    transversal_period_wave(300)
        pygame.display.update()


def spheric_wave(frequency):
    WAVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(WAVE_EVENT, frequency)
    pygame.display.set_caption('Ondas: Simulación')

    waves = []
    wave_stop = False

    while True:
        SCREEN.fill('Black')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220, 80), text_input='Menú principal', font=get_font(20),
                                  base_color='#d7fcd4', hovering_color='Green')
        STOP_BUTTON = Button(image=None, pos=(1220, 600), text_input='STOP', font=get_font(20),
                                  base_color='#d7fcd4', hovering_color='Green')

        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)
        STOP_BUTTON.changeColor(MENU_MOUSE_POS)
        STOP_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if STOP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    wave_stop = not wave_stop
            if event.type == WAVE_EVENT and not wave_stop:
                waves.append((640, 360, 0))

        for i, wave in enumerate(waves):
            x, y, radius = wave
            pygame.draw.circle(SCREEN, (0, 0, 255), (x, y), radius, 2)
            if not wave_stop and radius < 640:
                waves[i] = (x, y, radius + 1)
        
        clock.tick(60)
        pygame.display.update()

def spheric_frequency_wave():
    pygame.display.set_caption('Escoge el periodo')

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('Black')
        TEXT = get_font(45).render('Escoge el periodo de la onda', True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640, 140))
        SCREEN.blit(TEXT, TEXT_RECT)


        ZEROTWOFIVEFIVESECOND = Button(image=None, pos=(400, 360), text_input='0.125s', font=get_font(25), base_color='White', hovering_color='Green')
        ZEROTWOFIVESECOND = Button(image=None, pos=(600, 360), text_input='0.25s', font=get_font(25), base_color='White', hovering_color='Green')
        ZEROFIVESECOND = Button(image=None, pos=(800, 360), text_input='0.5s', font=get_font(25), base_color='White', hovering_color='Green')
        ONESECOND = Button(image=None, pos=(400, 560), text_input='1s', font=get_font(25), base_color='White', hovering_color='Green')
        TWOSECOND = Button(image=None, pos=(600, 560), text_input='2s', font=get_font(25), base_color='White', hovering_color='Green')
        THREESECOND = Button(image=None, pos=(800, 560), text_input='3s', font=get_font(25), base_color='White', hovering_color='Green')


        ZEROTWOFIVEFIVESECOND.changeColor(MOUSE_POS)
        ZEROTWOFIVEFIVESECOND.update(SCREEN)
        ZEROTWOFIVESECOND.changeColor(MOUSE_POS)
        ZEROTWOFIVESECOND.update(SCREEN)
        ZEROFIVESECOND.changeColor(MOUSE_POS)
        ZEROFIVESECOND.update(SCREEN)
        ONESECOND.changeColor(MOUSE_POS)
        ONESECOND.update(SCREEN)
        TWOSECOND.changeColor(MOUSE_POS)
        TWOSECOND.update(SCREEN)
        THREESECOND.changeColor(MOUSE_POS)
        THREESECOND.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ZEROTWOFIVEFIVESECOND.checkForInput(MOUSE_POS):
                    spheric_wave(125)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ZEROTWOFIVESECOND.checkForInput(MOUSE_POS):
                    spheric_wave(250)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ZEROFIVESECOND.checkForInput(MOUSE_POS):
                    spheric_wave(500)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ONESECOND.checkForInput(MOUSE_POS):
                    spheric_wave(1000)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TWOSECOND.checkForInput(MOUSE_POS):
                    spheric_wave(2000)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if THREESECOND.checkForInput(MOUSE_POS):
                    spheric_wave(3000)
        pygame.display.update()


def type_wave():
    pygame.display.set_caption('Tipos de onda')

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill('Black')
        TEXT = get_font(45).render('Escoge el tipo de onda', True, 'White')
        TEXT_RECT = TEXT.get_rect(center=(640, 240))
        SCREEN.blit(TEXT, TEXT_RECT)

        SPHERIC = Button(image=None, pos=(440, 460), text_input='Esféricas 2D', font=get_font(25), base_color='White', hovering_color='Red')
        TRANSVERSAL = Button(image=None, pos=(840, 460), text_input='Transveral', font=get_font(25), base_color='White', hovering_color='Red')

        SPHERIC.changeColor(MOUSE_POS)
        SPHERIC.update(SCREEN)
        TRANSVERSAL.changeColor(MOUSE_POS)
        TRANSVERSAL.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SPHERIC.checkForInput(MOUSE_POS):
                    spheric_frequency_wave()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TRANSVERSAL.checkForInput(MOUSE_POS):
                    transversal_amplitud_wave()
        pygame.display.update()


def equipotencial_surface():
    pygame.display.set_caption('Superficies equipotenciales: Simulación')

    CHARGE_RADIUS = 10
    LINE_SPACING = 25
    ARROW_LENGTH = 15
    ARROW_HEAD_SIZE = 5

    def is_charge_clicked(charge, mouse_x, mouse_y):
        x, y, _ = charge
        return (x - mouse_x) ** 2 + ( y - mouse_y ) ** 2 <= CHARGE_RADIUS ** 2
    
    def electric_field(px, py, charges):
        Ex = 0
        Ey = 0
        for ( x, y, q ) in charges:
            dx = px - x
            dy = py - y
            r_squared = dx**2 + dy**2
            if r_squared == 0:
                continue
            E = q / r_squared
            Ex += E * dx / math.sqrt(r_squared)
            Ey += E * dy / math.sqrt(r_squared)
        return Ex, Ey
    
    def draw_arrow(screen, color, start, end, arrow_head_size):
        pygame.draw.line(screen, color, start, end, 1)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_head = [
            (end[0] - arrow_head_size * math.cos(angle - math.pi / 6), end[1] - arrow_head_size * math.sin(angle - math.pi / 6)),
            (end[0] - arrow_head_size * math.cos(angle + math.pi / 6), end[1] - arrow_head_size * math.sin(angle + math.pi / 6)),
            end
        ]
        pygame.draw.polygon(screen, color, arrow_head)

    charges = [
        (WIDTH // 2 - 100, HEIGHT // 2, 1),
        (WIDTH // 2 + 100, HEIGHT // 2, -1),
    ]
    selected_charge_index = None
    
    while True:
        SCREEN.fill('White')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=None, pos=(1220,80), text_input='Menú principal', font=get_font(20),
                                  base_color='#000000', hovering_color='Brown')
        ADD_POSITIVE_BUTTON = Button(image=None, pos=(1220,140), text_input='Añadir positiva', font=get_font(20),
                                  base_color='Red', hovering_color='Green')
        ADD_NEGATIVE_BUTTON = Button(image=None, pos=(1220,200), text_input='Añadir negativa', font=get_font(20),
                                  base_color='Blue', hovering_color='Green')

        BACK_MENU_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_MENU_BUTTON.update(SCREEN)
        ADD_POSITIVE_BUTTON.changeColor(MENU_MOUSE_POS)
        ADD_POSITIVE_BUTTON.update(SCREEN)
        ADD_NEGATIVE_BUTTON.changeColor(MENU_MOUSE_POS)
        ADD_NEGATIVE_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if ADD_POSITIVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    charges.append((WIDTH // 2, HEIGHT // 2, 1))
                if ADD_NEGATIVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    charges.append((WIDTH // 2, HEIGHT // 2, -1))
                mouse_x, mouse_y = event.pos
                for i, charge in enumerate(charges):
                    if is_charge_clicked(charge, mouse_x, mouse_y):
                        selected_charge_index = i
                        break
            if event.type == pygame.MOUSEBUTTONUP:
                selected_charge_index = None
            if event.type == pygame.MOUSEMOTION and selected_charge_index is not None:
                mouse_x, mouse_y = event.pos
                x, y, q = charges[selected_charge_index]
                charges[selected_charge_index] = (mouse_x, mouse_y, q)
        for (x, y, q) in charges:
            color = (255, 0, 0) if q > 0 else (0, 0, 255)
            pygame.draw.circle(SCREEN, color, (x, y), CHARGE_RADIUS)
        
        for y in range(0, HEIGHT, LINE_SPACING):
            for x in range(0, WIDTH, LINE_SPACING):
                Ex, Ey = electric_field(x, y, charges)
                magnitude = math.sqrt(Ex**2 + Ey**2)
                if magnitude > 0:
                    Ex /= magnitude
                    Ey /= magnitude
                    end_x = x + Ex * ARROW_LENGTH
                    end_y = y + Ey * ARROW_LENGTH
                    draw_arrow(SCREEN, (0, 0, 0), (x, y), (end_x, end_y), ARROW_HEAD_SIZE)
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
    pendulum_length = length * 100
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

        initial_length_text = 'Longitud del péndulo(m): %s' % ( pendulum_length / 100 )
        text_surface = get_font(20).render(initial_length_text, True, 'White')
        SCREEN.blit(text_surface, (640, 120))

        position_x_text = 'Posición x: %s' % ( round(x - 200, 2) )
        text_surface = get_font(20).render(position_x_text, True, 'White')
        SCREEN.blit(text_surface, (640, 160))

        position_y_text = 'Posición y: %s' % ( round((y - 39) / 100, 2) )
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
    pendulum_initial_angle_input = pygame_gui.elements.UITextEntryLine(
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
            # if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#pendulum_initial_angle':
            #     pendulum_angle_value = float(event.text)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    main_menu()
                if NEXT.checkForInput(MOUSE_POS):
                    try:
                        pendulum_initial_angle_value = float(pendulum_initial_angle_input.get_text())
                        shm(pendulum_length, pendulum_initial_angle_value)
                    except ValueError:
                        print('Por favor, ingrese un número válido')

            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(SCREEN)
        pygame.display.update()


def pendulum_length():
    pygame.display.set_caption('Movimiento armónico simple: condiciones iniciales - Longitud')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    pendulum_length_input = pygame_gui.elements.UITextEntryLine(
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
            # if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#pendulum_length':
            #     pendulum_length_value = float(event.text)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    main_menu()
                if NEXT.checkForInput(MOUSE_POS):
                    try:
                        initial_length_value = float(pendulum_length_input.get_text())
                        pendulum_initial_angle(initial_length_value)
                    except ValueError:
                        print('Por favor, ingrese un valor válido.')

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
        ### Trajectory ###
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
    initial_angle_input = pygame_gui.elements.UITextEntryLine(
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
            # if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#initial_angle':
            #     initial_angle_value = float(event.text) or None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    initial_velocity()
                if NEXT.checkForInput(MOUSE_POS):
                    try:
                        initial_angle_value = float(initial_angle_input.get_text())
                        parabolic_movement(initial_velocity,initial_angle_value)
                    except ValueError:
                        print('Por favor, ingrese un número válido')
            manager.process_events(event)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(SCREEN)
        pygame.display.update()


def initial_velocity():
    pygame.display.set_caption('Movimiento parabólico: condiciones iniciales - velocidad')
    manager = pygame_gui.UIManager((WIDTH,HEIGHT))
    velocity_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((485, 300), (300, 40)),
        start_value=30,
        value_range=(30, 100),
        manager=manager
    )

    while True:
        MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill('black')

        TEXT = get_font(45).render('Velocidad inicial(m/s)', True, 'white')
        TEXT_RECT = TEXT.get_rect(center=(640,240))
        SCREEN.blit(TEXT, TEXT_RECT)

        ### HEre ###
        velocity_value = int(velocity_slider.get_current_value())
        velocity_text = get_font(30).render(f'Valor: {velocity_value}', True, 'white')
        SCREEN.blit(velocity_text, (600, 350))
        ### ###

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkForInput(MOUSE_POS):
                    main_menu()
                if NEXT.checkForInput(MOUSE_POS):
                    initial_angle(velocity_value)

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
                            pos=(1000, 400), text_input='LENTES', font=get_font(35),
                            base_color='#d7fcd4', hovering_color='White'
                        )

        DIFFRACTION_BUTTON = Button(image=pygame.image.load('assets/static/images/options.png'),
                            pos=(1000, 550), text_input='CAMPO MAGNÉTICO', font=get_font(35),
                            base_color='#d7fcd4', hovering_color='White'
                        )



        MILEVA_BUTTON = Button(image=None, pos=(1200,680), text_input='MilevaDot', font=get_font(20), base_color='#b68f40', hovering_color='Green')

        for button in [PARABOLIC_BUTTON,SHM_BUTTON,EQUIPOTENTIALS_BUTTON,WAVES_BUTTON,INTERFERENCE_BUTTON,MILEVA_BUTTON,DIFFRACTION_BUTTON]:
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
                    equipotencial_surface()
                if WAVES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    type_wave()
                if INTERFERENCE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lens_simulation()
                if DIFFRACTION_BUTTON.checkForInput(MENU_MOUSE_POS):
                    magnetic_field_simulation()
        pygame.display.update()


main_menu()
