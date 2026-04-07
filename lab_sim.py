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

# ----------------------
# INIT
# ----------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Biocomputing Lab Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
title_font = pygame.font.SysFont("arial", 36, bold=True)

# ----------------------
# UTIL
# ----------------------
def draw_text(text, x, y, color=(230,230,230), f=font):
    img = f.render(text, True, color)
    screen.blit(img, (x, y))

# ----------------------
# SIGNAL GRAPH
# ----------------------
class SignalGraph:
    def __init__(self, max_points=100):
        self.data = deque(maxlen=max_points)

    def add(self, value):
        self.data.append(value)

    def draw(self, x, y, w, h):
        pygame.draw.rect(screen, (50,50,50), (x, y, w, h), border_radius=8)
        if len(self.data) < 2:
            return

        step = w / len(self.data)
        points = []
        for i, val in enumerate(self.data):
            px = x + i * step
            py = y + h/2 - val * 10
            points.append((px, py))

        pygame.draw.lines(screen, (100,200,255), False, points, 2)

# ----------------------
# ROBOT SIM
# ----------------------
class RobotSim:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.mode = 1
        self.uv_on = False
        self.target_x = random.randint(50, WIDTH - 50)
        self.graph = SignalGraph()
        self.current_signal = 0

    def generate_signal(self):
        return random.choice([-2,-1,0,1,2])

    def update(self, keys):
        signal = self.generate_signal()

        if self.mode == 2 and self.uv_on:
            signal += random.choice([-5, 5])

        if self.mode == 3:
            if keys[pygame.K_LEFT]:
                signal = -3
            elif keys[pygame.K_RIGHT]:
                signal = 3

        self.current_signal = signal
        self.graph.add(signal)

        self.x += signal
        self.x = max(0, min(WIDTH, self.x))

        if abs(self.x - self.target_x) < 10:
            self.target_x = random.randint(50, WIDTH - 50)

    def draw(self):
        # Robot
        pygame.draw.rect(screen, (80,200,120), (self.x, self.y, 40, 40), border_radius=6)

        # Target
        pygame.draw.circle(screen, (220,80,80), (self.target_x, self.y+20), 10)

        # UI Panel
        pygame.draw.rect(screen, (40,40,40), (0,0,WIDTH,120))

        draw_text("Robot Simulation", 20, 10, f=title_font)
        draw_text(f"Mode: {self.mode}", 20, 55)
        draw_text(f"Signal: {self.current_signal}", 200, 55)

        draw_text("1=Natural  2=UV  3=Override  U=Toggle UV  ESC=Back", 20, 85, (180,180,180))

        # Graph
        self.graph.draw(20, HEIGHT-160, WIDTH-40, 120)

# ----------------------
# MEMRISTOR SIM
# ----------------------
class MemristorSim:
    def __init__(self):
        self.memory = 0
        self.voltage = 0
        self.frequency = 1
        self.mushrooms = 1
        self.accuracy = 1.0
        self.graph = SignalGraph()

    def update(self, keys):
        if keys[pygame.K_UP]: self.voltage += 0.05
        if keys[pygame.K_DOWN]: self.voltage -= 0.05
        if keys[pygame.K_RIGHT]: self.frequency += 0.05
        if keys[pygame.K_LEFT]: self.frequency = max(0.1, self.frequency - 0.05)
        if keys[pygame.K_m]: self.mushrooms += 1

        self.memory *= 0.98  # slight decay
        self.memory += self.voltage

        # base penalty (nonlinear)
        penalty = (self.frequency ** 1.5) * 0.03

        # diminishing returns on mushrooms
        boost = 0.15 * (1 - (1 / (self.mushrooms)))

        self.accuracy = max(0.0, 1.0 - penalty + boost)
        self.accuracy = min(1.0, self.accuracy)

        scaled = max(-5, min(5, self.memory * 0.01)) # keep graph on screen
        self.graph.add(scaled)

    def draw(self):
        pygame.draw.rect(screen, (40,40,40), (0,0,WIDTH,160))

        draw_text("Memristor Simulation", 20, 10, f=title_font)
        draw_text(f"Memory: {round(self.memory,2)}", 20, 60)
        draw_text(f"Voltage: {round(self.voltage,2)}", 200, 60)
        draw_text(f"Frequency: {round(self.frequency,2)}", 380, 60)
        draw_text(f"Mushrooms: {self.mushrooms}", 560, 60)
        draw_text(f"Accuracy: {round(self.accuracy,2)}", 740, 60)

        status = "GOOD" if self.accuracy > 0.8 else "UNSTABLE"
        color = (100,220,120) if self.accuracy > 0.8 else (220,100,100)
        draw_text(f"Status: {status}", 20, 100, color)

        target_freq = 5
        draw_text(f"Goal: freq >= {target_freq} AND accuracy > 0.8", 20, 150)

        draw_text("UP/DOWN=Voltage  LEFT/RIGHT=Freq  M=Add Mushroom  ESC=Back", 20, 130, (180,180,180))

        self.graph.draw(20, HEIGHT-160, WIDTH-40, 120)

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
                        if event.key == pygame.K_ESCAPE: self.mode = MODE_MENU
                        if event.key == pygame.K_1: self.robot.mode = 1
                        if event.key == pygame.K_2: self.robot.mode = 2
                        if event.key == pygame.K_3: self.robot.mode = 3
                        if event.key == pygame.K_u: self.robot.uv_on = not self.robot.uv_on

                    elif self.mode == MODE_MEMRISTOR:
                        if event.key == pygame.K_ESCAPE: self.mode = MODE_MENU

            screen.fill((25,25,30))

            if self.mode == MODE_MENU:
                draw_text("Biocomputing Lab", 300, 220, f=title_font)
                draw_text("1 - Robot Simulation", 330, 300)
                draw_text("2 - Memristor Simulation", 330, 340)

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
