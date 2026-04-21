import pygame
import random
import sys
from collections import deque

# ----------------------
# CONFIG
# ----------------------
WIDTH, HEIGHT = 900, 650
FPS = 60

MODE_MENU = "menu"
MODE_ROBOT = "robot"

ROBOT_SIZE = 40
PANEL_H = 90
GRAPH_H = 120
GRAPH_Y = HEIGHT - GRAPH_H - 20

# ----------------------
# INIT
# ----------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Biocomputing Lab Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
title_font = pygame.font.SysFont("arial", 36, bold=True)
banner_font = pygame.font.SysFont("arial", 28, bold=True)

# ----------------------
# UTIL
# ----------------------
def draw_text(text, x, y, color=(230, 230, 230), f=font):
    img = f.render(text, True, color)
    screen.blit(img, (x, y))

def draw_banner(text, color):
    surf = banner_font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bg = rect.inflate(30, 16)
    pygame.draw.rect(screen, (20, 20, 20), bg, border_radius=8)
    pygame.draw.rect(screen, color, bg, 2, border_radius=8)
    screen.blit(surf, rect)

# ----------------------
# SIGNAL GRAPH
# ----------------------
class SignalGraph:
    def __init__(self, max_points=100):
        self.data = deque(maxlen=max_points)

    def add(self, value):
        self.data.append(value)

    def draw(self, x, y, w, h, scale=10):
        pygame.draw.rect(screen, (50, 50, 50), (x, y, w, h), border_radius=8)
        # zero line
        pygame.draw.line(screen, (80, 80, 80), (x, y + h // 2), (x + w, y + h // 2), 1)
        if len(self.data) < 2:
            return

        step = w / len(self.data)
        points = []
        for i, val in enumerate(self.data):
            px = x + i * step
            py = y + h / 2 - val * scale
            py = max(y + 2, min(y + h - 2, py))  # clamp within box
            points.append((px, py))

        pygame.draw.lines(screen, (100, 200, 255), False, points, 2)

# ----------------------
# ROBOT SIM
# ----------------------
PLAY_TOP = PANEL_H
PLAY_BOTTOM = GRAPH_Y
PLAY_MID_Y = (PLAY_TOP + PLAY_BOTTOM) // 2

class RobotSim:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = PLAY_MID_Y
        self.mode = 1
        self.uv_on = True
        self.target_x = random.randint(60, WIDTH - 60)
        self.target_y = random.randint(PLAY_TOP + 20, PLAY_BOTTOM - 20)
        self.graph = SignalGraph()
        self.current_signal = 0
        self.goal_reached = False
        self.goal_timer = 0
        self.robot_img = pygame.image.load("goomba.png").convert_alpha()
        self.robot_img = pygame.transform.scale(self.robot_img, (ROBOT_SIZE, ROBOT_SIZE))
        self.target_img = pygame.image.load("mario.png").convert_alpha()
        self.target_img = pygame.transform.scale(self.target_img, (ROBOT_SIZE, ROBOT_SIZE))

    def _new_target(self):
        self.target_x = random.randint(60, WIDTH - 60)
        self.target_y = random.randint(PLAY_TOP + 20, PLAY_BOTTOM - 20)

    def generate_signal(self):
        return int(round(random.gauss(0, 2)))  # mean=0, stddev=2

    def update(self, keys):
        signal_x = self.generate_signal()
        signal_y = self.generate_signal()

        if self.mode == 2 and self.uv_on:
            signal = random.choice([0, 1, 2])
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:  signal_x -= signal
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: signal_x += signal
            if keys[pygame.K_UP] or keys[pygame.K_w]:    signal_y -= signal
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:  signal_y += signal

        if self.mode == 3:
            signal_x = 0
            signal_y = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:  signal_x = -4
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: signal_x = 4
            if keys[pygame.K_UP] or keys[pygame.K_w]:    signal_y = -4
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:  signal_y = 4

        self.current_signal = signal_x
        self.graph.add(signal_x)

        self.x = max(0, min(WIDTH - ROBOT_SIZE, self.x + signal_x))
        self.y = max(PLAY_TOP, min(PLAY_BOTTOM - ROBOT_SIZE, self.y + signal_y))

        robot_cx = self.x + ROBOT_SIZE // 2
        robot_cy = self.y + ROBOT_SIZE // 2
        if abs(robot_cx - self.target_x) < 18 and abs(robot_cy - self.target_y) < 18:
            self.goal_reached = True
            self.goal_timer = FPS * 2  # show banner for 2 seconds
            self._new_target()

        if self.goal_timer > 0:
            self.goal_timer -= 1
        else:
            self.goal_reached = False

    def draw(self):
        # UI Panel
        pygame.draw.rect(screen, (30, 30, 35), (0, 0, WIDTH, PANEL_H))

        # Title
        draw_text("Robot Simulation", 20, 10, (240, 240, 240), f=title_font)

        # Mode + signal (top row)
        mode_names = {1: "Natural", 2: "UV Assist", 3: "Manual Override"}
        draw_text(f"Mode: {mode_names[self.mode]}", 20, 60)
        draw_text(f"Signal: {self.current_signal}", 300, 60)

        # Divider line
        pygame.draw.line(screen, (70, 70, 70), (20, 90), (WIDTH - 20, 90), 1)

        # Controls section
        controls = [
            "1 = Natural (autonomous)",
            "2 = UV Assist (influence movement)",
            "3 = Override (direct control)",
            "ESC = Back to menu"
        ]

        y_offset = 95
        for line in controls:
            draw_text(line, 20, y_offset, (180, 180, 180))
            y_offset += 22

        # Context hint (right side)
        hint = ""
        if self.mode == 2:
            hint = "Use arrow keys / WASD to influence signal"
        elif self.mode == 3:
            hint = "Arrow keys / WASD = direct movement"

        draw_text(hint, 450, 110, (120, 200, 255))

        # Target
        # pygame.draw.circle(screen, (220, 80, 80), (self.target_x, self.target_y), 12)
        screen.blit(self.target_img, (self.target_x, self.target_y))
        pygame.draw.rect(screen, (200, 200, 200), (self.target_x, self.target_y, ROBOT_SIZE, ROBOT_SIZE), 2, border_radius=6)

        # Robot
        screen.blit(self.robot_img, (self.x, self.y))
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, ROBOT_SIZE, ROBOT_SIZE), 2, border_radius=6)

        # Graph — scale 4 for override (±4), 8 for UV (±5 bias), 10 for natural (±2)
        scale = {1: 10, 2: 6, 3: 8}.get(self.mode, 10)
        self.graph.draw(20, GRAPH_Y, WIDTH - 40, GRAPH_H, scale=scale)

        if self.goal_reached:
            draw_banner("Target reached! Move to the next mode.", (100, 220, 120))

# ----------------------
# APP
# ----------------------
class App:
    def __init__(self):
        self.mode = MODE_MENU
        self.robot = RobotSim()

    def run(self):
        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if self.mode == MODE_MENU:
                        if event.key == pygame.K_1: self.mode = MODE_ROBOT

                    elif self.mode == MODE_ROBOT:
                        if event.key == pygame.K_ESCAPE:
                            self.mode = MODE_MENU
                        if event.key == pygame.K_1:
                            self.robot.mode = 1
                        if event.key == pygame.K_2:
                            self.robot.mode = 2
                            self.robot.uv_on = True   # auto-enable UV on entry
                        if event.key == pygame.K_3:
                            self.robot.mode = 3
                        if event.key == pygame.K_u:
                            self.robot.uv_on = not self.robot.uv_on

            screen.fill((25, 25, 30))

            if self.mode == MODE_MENU:
                draw_text("Biocomputing Lab Simulator", 220, 180, f=title_font)
                draw_text("1 — Robot Sim: Navigate a biohybrid robot using fungal electrical signals", 160, 270)
                draw_text("Press 1 to begin", 340, 390, (140, 140, 140))

            elif self.mode == MODE_ROBOT:
                self.robot.update(keys)
                self.robot.draw()

            pygame.display.flip()
            clock.tick(FPS)

# ----------------------
# RUN
# ----------------------
if __name__ == "__main__":
    App().run()
