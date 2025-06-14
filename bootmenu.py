import pygame
import sys
import subprocess
import os
import time

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()
pygame.display.set_caption("Boot Menu")

FONT = pygame.font.SysFont("Arial", 36)
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 100
BUTTON_COLOR = (50, 150, 255)
HOVER_COLOR = (70, 180, 255)
SELECTED_BORDER = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (10, 10, 10)

TIMEOUT_SECONDS = 10
start_time = time.time()

# --- Button Class ---
class Button:
    def __init__(self, icon_path, center, action):
        self.action = action
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.smoothscale(self.icon, (BUTTON_WIDTH - 20, BUTTON_HEIGHT - 20))
        self.rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.rect.center = center

    def draw(self, mouse_pos, is_selected=False):
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=20)
        if is_selected:
            pygame.draw.rect(screen, SELECTED_BORDER, self.rect, 4, border_radius=20)
        icon_rect = self.icon.get_rect(center=self.rect.center)
        screen.blit(self.icon, icon_rect)

    def click(self):
        self.action()

# --- Actions ---
def boot_raspbian():
    pygame.quit()
    subprocess.call(['startlxde'])

def boot_retro():
    pygame.quit()
    subprocess.call(['emulationstation'])

def boot_cli():
    pygame.quit()
    # No GUI, returns to CLI

# --- Button Placement ---
gap = 100
center_y = screen_rect.centery
center_x = screen_rect.centerx

buttons = [
    Button("raspbian_icon.png", (center_x - BUTTON_WIDTH - gap//2, center_y), boot_raspbian),
    Button("retropie_icon.png", (center_x + BUTTON_WIDTH + gap//2, center_y), boot_retro),
]

selected_index = 0

# --- Main Loop ---
running = True
while running:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()
    elapsed = time.time() - start_time

    # --- Draw Buttons ---
    for idx, button in enumerate(buttons):
        button.draw(mouse_pos, is_selected=(idx == selected_index))

    # --- Timer ---
    if elapsed < TIMEOUT_SECONDS:
        remaining = TIMEOUT_SECONDS - elapsed
        timer_text = FONT.render(f"CLI fallback in {int(remaining)}s", True, (180, 180, 180))
        screen.blit(timer_text, (screen_rect.centerx - timer_text.get_width() // 2, screen_rect.bottom - 60))
    else:
        boot_cli()

    pygame.display.flip()

    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            start_time = time.time()  # Reset timeout on any key press
            if event.key == pygame.K_LEFT:
                selected_index = (selected_index - 1) % len(buttons)
            elif event.key == pygame.K_RIGHT:
                selected_index = (selected_index + 1) % len(buttons)
            elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                buttons[selected_index].click()
            elif event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
sys.exit()
