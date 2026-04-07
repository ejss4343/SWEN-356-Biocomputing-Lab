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
MODE_MEMRISTOR = "memristor"

ROBOT_SIZE = 40
PANEL_H = 120
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

    def _new_target(self):
        self.target_x = random.randint(60, WIDTH - 60)
        self.target_y = random.randint(PLAY_TOP + 20, PLAY_BOTTOM - 20)

    def generate_signal(self):
        return random.choice([-2, -1, 0, 1, 2])

    def update(self, keys):
        signal_x = self.generate_signal()
        signal_y = self.generate_signal()

        if self.mode == 2 and self.uv_on:
            # bias toward target
            signal_x += random.choice([-3, 3])
            signal_y += random.choice([-3, 3])

        if self.mode == 3:
            signal_x = 0
            signal_y = 0
            if keys[pygame.K_LEFT]:  signal_x = -4
            if keys[pygame.K_RIGHT]: signal_x = 4
            if keys[pygame.K_UP]:    signal_y = -4
            if keys[pygame.K_DOWN]:  signal_y = 4

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
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, WIDTH, PANEL_H))
        draw_text("Robot Simulation", 20, 10, f=title_font)

        mode_names = {1: "Natural", 2: "UV", 3: "Override"}
        uv_status = f"  |  UV: {'ON' if self.uv_on else 'OFF'}" if self.mode == 2 else ""
        draw_text(f"Mode: {self.mode} — {mode_names[self.mode]}{uv_status}", 20, 55)
        draw_text(f"Signal: {self.current_signal}", 480, 55)

        hint3 = "  ←↑↓→=Move" if self.mode == 3 else ""
        draw_text(f"1=Natural  2=UV  3=Override  U=Toggle UV  ESC=Back{hint3}", 20, 88, (160, 160, 160))

        # Target
        pygame.draw.circle(screen, (220, 80, 80), (self.target_x, self.target_y), 12)

        # Robot
        pygame.draw.rect(screen, (80, 200, 120), (self.x, self.y, ROBOT_SIZE, ROBOT_SIZE), border_radius=6)

        # Graph — scale 4 for override (±4), 8 for UV (±5 bias), 10 for natural (±2)
        scale = {1: 10, 2: 6, 3: 8}.get(self.mode, 10)
        self.graph.draw(20, GRAPH_Y, WIDTH - 40, GRAPH_H, scale=scale)

        if self.goal_reached:
            draw_banner("Target reached! Move to the next mode.", (100, 220, 120))

# ----------------------
# MEMRISTOR SIM
# ----------------------
MEM_PANEL_H = 170

class MemristorSim:
    def __init__(self):
        self.memory = 0
        self.voltage = 0.0
        self.frequency = 1.0
        self.mushrooms = 1
        self.accuracy = 0.9
        self.graph = SignalGraph()
        self.goal_reached = False
        self.goal_timer = 0

    def update(self, keys):
        if keys[pygame.K_UP]:    self.voltage = min(10.0, self.voltage + 0.05)
        if keys[pygame.K_DOWN]:  self.voltage = max(-10.0, self.voltage - 0.05)
        if keys[pygame.K_RIGHT]: self.frequency = min(20.0, self.frequency + 0.05)
        if keys[pygame.K_LEFT]:  self.frequency = max(0.1, self.frequency - 0.05)

        self.memory = self.memory * 0.98 + self.voltage

        # Accuracy: peaks ~0.9 at low freq, degrades nonlinearly; mushrooms add diminishing recovery
        base = 0.9 - (self.frequency ** 1.8) * 0.015
        boost = 0.1 * (1 - 1 / self.mushrooms)
        self.accuracy = max(0.0, min(0.95, base + boost))

        scaled = max(-5, min(5, self.memory * 0.01))
        self.graph.add(scaled)

        if self.frequency >= 5 and self.accuracy > 0.8:
            if not self.goal_reached:
                self.goal_reached = True
                self.goal_timer = FPS * 3
        if self.goal_timer > 0:
            self.goal_timer -= 1
        else:
            self.goal_reached = False

    def draw(self):
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, WIDTH, MEM_PANEL_H))

        draw_text("Memristor Simulation", 20, 10, f=title_font)
        draw_text(f"Memory: {round(self.memory, 2)}", 20, 60)
        draw_text(f"Voltage: {round(self.voltage, 2)}", 220, 60)
        draw_text(f"Frequency: {round(self.frequency, 2)}", 420, 60)
        draw_text(f"Mushrooms: {self.mushrooms}", 640, 60)

        acc_color = (100, 220, 120) if self.accuracy > 0.8 else (220, 100, 100)
        draw_text(f"Accuracy: {round(self.accuracy, 2)}", 20, 100, acc_color)

        status = "GOOD" if self.accuracy > 0.8 else "UNSTABLE"
        draw_text(f"Status: {status}", 220, 100, acc_color)

        goal_color = (100, 220, 120) if (self.frequency >= 5 and self.accuracy > 0.8) else (180, 180, 180)
        draw_text("Goal: freq >= 5 AND accuracy > 0.8", 420, 100, goal_color)

        draw_text("↑↓=Voltage  ←→=Frequency  M=Add Mushroom  ESC=Back", 20, 138, (160, 160, 160))

        self.graph.draw(20, GRAPH_Y, WIDTH - 40, GRAPH_H, scale=8)

        if self.goal_reached:
            draw_banner("Goal reached! Answer the worksheet questions.", (100, 220, 120))

# ----------------------
# APP
# ----------------------
class App:
    def __init__(self):
        self.mode = MODE_MENU
        self.robot = RobotSim()
        self.memristor = MemristorSim()

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
                        if event.key == pygame.K_2: self.mode = MODE_MEMRISTOR

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

                    elif self.mode == MODE_MEMRISTOR:
                        if event.key == pygame.K_ESCAPE:
                            self.mode = MODE_MENU
                        if event.key == pygame.K_m:
                            self.memristor.mushrooms += 1

            screen.fill((25, 25, 30))

            if self.mode == MODE_MENU:
                draw_text("Biocomputing Lab Simulator", 220, 180, f=title_font)
                draw_text("1 — Robot Sim: Navigate a biohybrid robot using fungal electrical signals", 160, 270)
                draw_text("2 — Memristor Sim: Balance signal speed vs. accuracy using mushroom RAM", 160, 315)
                draw_text("Press 1 or 2 to begin", 340, 390, (140, 140, 140))

            elif self.mode == MODE_ROBOT:
                self.robot.update(keys)
                self.robot.draw()

            elif self.mode == MODE_MEMRISTOR:
                self.memristor.update(keys)
                self.memristor.draw()

            pygame.display.flip()
            clock.tick(FPS)

# ----------------------
# RUN
# ----------------------
if __name__ == "__main__":
    App().run()
