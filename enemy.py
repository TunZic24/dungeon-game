"""Enemy Classes"""
import pygame
import math
import random
from constants import *

class Enemy:
    """Base enemy class"""
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.width = ENEMY_SIZE
        self.height = ENEMY_SIZE
        self.enemy_type = enemy_type
        
        # Stats
        self.max_hp = ENEMY_MAX_HP
        self.hp = self.max_hp
        self.speed = ENEMY_SPEED
        self.damage = 5
        self.color = RED
        
        # AI
        self.state = "patrol"  # patrol, chase, attack, die
        self.patrol_points = []
        self.current_patrol = 0
        self.chase_distance = 200
        self.attack_distance = 60
        self.attack_cooldown = 0
        self.attack_range = 1.0
        
        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 1
        
        # Loot
        self.loot_table = []

    def update(self, dt, player):
        """Update enemy"""
        # Update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # AI Logic
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        distance = self._distance_to(player.x, player.y)
        
        # State machine
        if self.state == "die":
            return
        
        if distance < self.chase_distance:
            self.state = "chase"
        elif distance > self.chase_distance + 100:
            self.state = "patrol"
        
        # Execute state
        if self.state == "patrol":
            self._patrol(dt)
        elif self.state == "chase":
            self._chase(player, dt)
            
            if distance < self.attack_distance and self.attack_cooldown <= 0:
                self.state = "attack"
                self.attack_cooldown = self.attack_range
                return  # Attack will be handled by game
        
        # Move
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Clamp to screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def draw(self, surface):
        """Draw enemy"""
        # Draw body
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw HP bar
        bar_width = 30
        bar_height = 3
        hp_ratio = max(0, self.hp / self.max_hp)
        
        pygame.draw.rect(surface, RED, (self.x - bar_width/2 + self.width/2, 
                                       self.y - 10, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.x - bar_width/2 + self.width/2, 
                                         self.y - 10, bar_width * hp_ratio, bar_height))

    def get_rect(self):
        """Get enemy rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage):
        """Take damage"""
        self.hp -= damage
        if self.hp <= 0:
            self.state = "die"
            return True
        return False

    def _distance_to(self, x, y):
        """Calculate distance to position"""
        dx = x - self.x
        dy = y - self.y
        return math.sqrt(dx*dx + dy*dy)

    def _patrol(self, dt):
        """Patrol behavior"""
        self.vel_x = 0
        self.vel_y = 0
        
        # Simple left-right patrol
        if self.x < SCREEN_WIDTH / 4:
            self.direction = 1
        elif self.x > 3 * SCREEN_WIDTH / 4:
            self.direction = -1
        
        self.vel_x = self.direction * self.speed

    def _chase(self, player, dt):
        """Chase player"""
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist == 0:
            self.vel_x = 0
            self.vel_y = 0
        else:
            self.vel_x = (dx / dist) * self.speed
            self.vel_y = (dy / dist) * self.speed

    def can_attack(self):
        """Check if can attack"""
        return self.attack_cooldown <= 0 and self.state == "attack"

    def is_dead(self):
        """Check if dead"""
        return self.state == "die"

    def get_loot(self):
        """Get loot when dead"""
        if random.random() < 0.3 and self.loot_table:
            return random.choice(self.loot_table)
        return None


class BasicEnemy(Enemy):
    """Basic melee enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, "basic")
        self.max_hp = 20
        self.hp = self.max_hp
        self.speed = 2
        self.damage = 5
        self.color = RED
        self.attack_range = 1.0
        self.loot_table = ['iron_sword', 'leather_hat']


class FastEnemy(Enemy):
    """Fast enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, "fast")
        self.max_hp = 15
        self.hp = self.max_hp
        self.speed = 3.5
        self.damage = 4
        self.color = ORANGE
        self.attack_range = 0.8
        self.chase_distance = 250
        self.loot_table = ['pistol', 'leather_boots']


class StrongEnemy(Enemy):
    """Strong enemy"""
    def __init__(self, x, y):
        super().__init__(x, y, "strong")
        self.max_hp = 35
        self.hp = self.max_hp
        self.speed = 1.5
        self.damage = 8
        self.color = PURPLE
        self.attack_range = 1.5
        self.attack_distance = 80
        self.loot_table = ['steel_sword', 'steel_armor']


def spawn_enemy(x, y, enemy_type="basic"):
    """Spawn enemy by type"""
    if enemy_type == "fast":
        return FastEnemy(x, y)
    elif enemy_type == "strong":
        return StrongEnemy(x, y)
    else:
        return BasicEnemy(x, y)
