"""Player Class"""
import pygame
import math
from constants import *
from weapon import get_weapon
from skill import get_skill
from equipment import get_equipment

class Player:
    """Player class"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        
        # Stats
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.speed = PLAYER_SPEED
        self.base_defense = 0
        
        # Weapon and Skills
        self.weapon = get_weapon('iron_sword')
        self.skill = get_skill('slash')
        
        # Equipment
        self.equipment = {
            'hat': None,
            'armor': None,
            'shoes': None,
            'pants': None
        }
        
        # Inventory
        self.inventory = []
        self.inventory_open = False
        
        # Input
        self.vel_x = 0
        self.vel_y = 0
        
        # Combat
        self.attack_range = 100
        self.facing_angle = 0
        
        # Misc
        self.color = BLUE
        self.invincible_timer = 0
        self.level = 1
        self.experience = 0

    def update(self, dt, keys, mouse_pos):
        """Update player"""
        # Movement
        self.vel_x = 0
        self.vel_y = 0
        
        speed = self.speed + self._get_speed_bonus()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y = -speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y = speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = speed

        # Move
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Clamp to screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        # Facing angle
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.facing_angle = math.atan2(dy, dx)
        
        # Update weapon and skill
        self.weapon.update(dt)
        if self.skill:
            self.skill.update(dt)
        
        # Invincibility timer
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

    def draw(self, surface):
        """Draw player"""
        # Draw body
        color = self.color
        if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2:
            color = WHITE
        
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        
        # Draw direction indicator
        end_x = self.x + math.cos(self.facing_angle) * 25
        end_y = self.y + math.sin(self.facing_angle) * 25
        pygame.draw.line(surface, YELLOW, (self.x, self.y), (end_x, end_y), 2)
        
        # Draw HP bar
        bar_width = 40
        bar_height = 5
        hp_ratio = max(0, self.hp / self.max_hp)
        
        # Background
        pygame.draw.rect(surface, RED, (self.x - bar_width/2 + self.width/2, 
                                       self.y - 15, bar_width, bar_height))
        # HP
        pygame.draw.rect(surface, GREEN, (self.x - bar_width/2 + self.width/2, 
                                         self.y - 15, bar_width * hp_ratio, bar_height))

    def get_rect(self):
        """Get player rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage):
        """Take damage"""
        if self.invincible_timer <= 0:
            defense = self.base_defense + self._get_defense_bonus()
            actual_damage = max(1, damage - defense)
            self.hp -= actual_damage
            self.invincible_timer = 0.5
            return True
        return False

    def heal(self, amount):
        """Heal player"""
        self.hp = min(self.max_hp, self.hp + amount)

    def equip_equipment(self, equipment):
        """Equip equipment"""
        if equipment:
            self.equipment[equipment.eq_type] = equipment
            self._update_stats()

    def unequip_equipment(self, eq_type):
        """Unequip equipment"""
        if eq_type in self.equipment:
            self.equipment[eq_type] = None
            self._update_stats()

    def set_weapon(self, weapon):
        """Set weapon"""
        self.weapon = weapon
        # Update skill based on weapon
        if weapon.weapon_type == "sword":
            self.skill = get_skill('slash')
        elif weapon.weapon_type == "gun":
            self.skill = get_skill('rapid_fire')
        elif weapon.weapon_type == "magic":
            self.skill = get_skill('fireball')

    def add_to_inventory(self, item):
        """Add item to inventory"""
        self.inventory.append(item)

    def _get_speed_bonus(self):
        """Calculate total speed bonus from equipment"""
        bonus = 0
        for eq in self.equipment.values():
            if eq:
                bonus += eq.get_total_speed_bonus()
        return bonus

    def _get_defense_bonus(self):
        """Calculate total defense bonus from equipment"""
        bonus = 0
        for eq in self.equipment.values():
            if eq:
                bonus += eq.get_total_defense_bonus()
        return bonus

    def _get_hp_bonus(self):
        """Calculate total HP bonus from equipment"""
        bonus = 0
        for eq in self.equipment.values():
            if eq:
                bonus += eq.get_total_hp_bonus()
        return bonus

    def _update_stats(self):
        """Update player stats from equipment"""
        base_hp = PLAYER_MAX_HP
        hp_bonus = self._get_hp_bonus()
        self.max_hp = base_hp + hp_bonus
        
        # Restore some HP when equipping
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def is_alive(self):
        """Check if player is alive"""
        return self.hp > 0

    def get_stats(self):
        """Get player stats"""
        return {
            'hp': self.hp,
            'max_hp': self.max_hp,
            'defense': self.base_defense + self._get_defense_bonus(),
            'speed': self.speed + self._get_speed_bonus(),
            'level': self.level,
            'experience': self.experience
        }
