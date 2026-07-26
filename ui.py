"""UI System"""
import pygame
from constants import *

class UI:
    """UI renderer"""
    def __init__(self):
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)

    def draw_hud(self, surface, player):
        """Draw heads-up display"""
        # Health
        stats = player.get_stats()
        health_text = self.font_small.render(
            f"HP: {int(stats['hp'])}/{int(stats['max_hp'])}", True, WHITE
        )
        surface.blit(health_text, (10, 10))
        
        # Level
        level_text = self.font_small.render(f"Level: {stats['level']}", True, WHITE)
        surface.blit(level_text, (10, 35))
        
        # Equipment
        eq_text = []
        if player.equipment['hat']:
            eq_text.append(player.equipment['hat'].name)
        if player.equipment['armor']:
            eq_text.append(player.equipment['armor'].name)
        if player.equipment['shoes']:
            eq_text.append(player.equipment['shoes'].name)
        if player.equipment['pants']:
            eq_text.append(player.equipment['pants'].name)
        
        eq_display = ", ".join(eq_text) if eq_text else "No equipment"
        eq_render = self.font_small.render(f"Equipment: {eq_display[:40]}", True, YELLOW)
        surface.blit(eq_render, (10, 60))
        
        # Weapon
        weapon_text = self.font_small.render(f"Weapon: {player.weapon.name}", True, CYAN)
        surface.blit(weapon_text, (10, 85))
        
        # Skill
        if player.skill:
            skill_status = "Ready"
            if player.skill.cooldown_timer > 0:
                skill_status = f"Cooldown: {player.skill.cooldown_timer:.1f}s"
            skill_text = self.font_small.render(
                f"Skill: {player.skill.name} - {skill_status}", True, PURPLE
            )
            surface.blit(skill_text, (10, 110))

    def draw_inventory(self, surface, player):
        """Draw inventory screen"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(DARK_GRAY)
        surface.blit(overlay, (0, 0))
        
        # Title
        title = self.font_large.render("INVENTORY (Press E to close)", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        surface.blit(title, title_rect)
        
        # Equipment section
        y_pos = 100
        equipment_title = self.font_medium.render("EQUIPMENT", True, YELLOW)
        surface.blit(equipment_title, (50, y_pos))
        y_pos += 40
        
        for eq_type in ['hat', 'armor', 'shoes', 'pants']:
            eq = player.equipment[eq_type]
            if eq:
                eq_text = f"{eq_type.upper()}: {eq.name}"
                eq_stats = f"  HP+{eq.hp_bonus} DEF+{eq.defense_bonus} SPD+{eq.speed_bonus:.1f}"
                eq_render = self.font_small.render(eq_text, True, GREEN)
                stats_render = self.font_small.render(eq_stats, True, LIGHT_GRAY)
                surface.blit(eq_render, (70, y_pos))
                surface.blit(stats_render, (90, y_pos + 25))
                y_pos += 55
            else:
                eq_render = self.font_small.render(f"{eq_type.upper()}: Empty", True, GRAY)
                surface.blit(eq_render, (70, y_pos))
                y_pos += 30
        
        # Weapon section
        y_pos += 20
        weapon_title = self.font_medium.render("WEAPON", True, CYAN)
        surface.blit(weapon_title, (50, y_pos))
        y_pos += 40
        
        weapon_text = f"Current: {player.weapon.name}"
        weapon_render = self.font_small.render(weapon_text, True, CYAN)
        surface.blit(weapon_render, (70, y_pos))
        y_pos += 30
        
        weapon_stats = f"Damage: {player.weapon.damage:.1f}, Speed: {player.weapon.attack_speed:.1f}"
        stats_render = self.font_small.render(weapon_stats, True, LIGHT_GRAY)
        surface.blit(stats_render, (70, y_pos))

    def draw_puzzle(self, surface, puzzle):
        """Draw puzzle screen"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(DARK_GRAY)
        surface.blit(overlay, (0, 0))
        
        # Puzzle title
        title = self.font_large.render("PUZZLE", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        surface.blit(title, title_rect)
        
        # Puzzle description
        desc = self.font_medium.render(puzzle.get_ui_text(), True, WHITE)
        desc_rect = desc.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(desc, desc_rect)
        
        # Input field (for math puzzle)
        if hasattr(puzzle, 'user_answer'):
            input_text = "Answer: " + str(puzzle.user_answer or "")
            input_render = self.font_medium.render(input_text, True, CYAN)
            input_rect = input_render.get_rect(center=(SCREEN_WIDTH // 2, 250))
            surface.blit(input_render, input_rect)
            
            hint = self.font_small.render("Type your answer and press ENTER", True, LIGHT_GRAY)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 300))
            surface.blit(hint, hint_rect)

    def draw_pause(self, surface):
        """Draw pause screen"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(pause_text, pause_rect)
        
        # Resume text
        resume_text = self.font_medium.render("Press P to resume", True, YELLOW)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        surface.blit(resume_text, resume_rect)

    def draw_game_over(self, surface):
        """Draw game over screen"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Game over text
        over_text = self.font_large.render("GAME OVER", True, RED)
        over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(over_text, over_rect)
        
        # Restart text
        restart_text = self.font_medium.render("Press R to restart or ESC to quit", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        surface.blit(restart_text, restart_rect)

    def draw_win(self, surface):
        """Draw win screen"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Win text
        win_text = self.font_large.render("YOU WIN!", True, GREEN)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(win_text, win_rect)
        
        # Restart text
        restart_text = self.font_medium.render("Press R to restart or ESC to quit", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        surface.blit(restart_text, restart_rect)

    def draw_damage_text(self, surface, x, y, damage, color=RED):
        """Draw floating damage text"""
        damage_text = self.font_small.render(f"-{int(damage)}", True, color)
        surface.blit(damage_text, (x, y))
