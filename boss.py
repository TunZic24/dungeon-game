"""Boss Class"""
import pygame
import math
import random
from constants import *

class Boss:
    """Boss class - complex AI and attack patterns"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BOSS_SIZE
        self.height = BOSS_SIZE
        self.color = PURPLE
        
        # Stats
        self.max_hp = BOSS_MAX_HP
        self.hp = self.max_hp
        self.speed = BOSS_SPEED
        self.damage = 15
        
        # AI
        self.state = "idle"  # idle, chase, attack1, attack2, attack3, die
        self.attack_cooldown = 0
        self.state_timer = 0
        self.attack_pattern = 0
        
        # Movement
        self.vel_x = 0
        self.vel_y = 0
        
        # Projectiles
        self.projectiles = []

    def update(self, dt, player):
        """Update boss"""
        if self.state == "die":
            return
        
        # Update timers
        self.state_timer += dt
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # Distance to player
        distance = self._distance_to(player.x, player.y)
        
        # State machine
        if self.state == "idle":
            self.state = "chase"
            self.state_timer = 0
        elif self.state == "chase":
            # Chase for 3 seconds then attack
            if self.state_timer > 3:
                self.state = f"attack{random.randint(1, 3)}"
                self.state_timer = 0
                self.attack_pattern = random.randint(1, 3)
            else:
                self._chase(player, dt)
        
        elif self.state == "attack1":
            # Fireball pattern
            self._fireball_pattern(player, dt)
            if self.state_timer > 3:
                self.state = "chase"
                self.state_timer = 0
        
        elif self.state == "attack2":
            # Bullet circle pattern
            self._bullet_circle_pattern(player, dt)
            if self.state_timer > 3:
                self.state = "chase"
                self.state_timer = 0
        
        elif self.state == "attack3":
            # Tracking projectiles pattern
            self._tracking_pattern(player, dt)
            if self.state_timer > 3:
                self.state = "chase"
                self.state_timer = 0
        
        # Move
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Clamp to screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        # Update projectiles
        for proj in self.projectiles[:]:
            proj['x'] += proj['vx']
            proj['y'] += proj['vy']
            
            # Remove if off screen
            if proj['x'] < -50 or proj['x'] > SCREEN_WIDTH + 50 or \
               proj['y'] < -50 or proj['y'] > SCREEN_HEIGHT + 50:
                self.projectiles.remove(proj)

    def draw(self, surface):
        """Draw boss"""
        # Draw body
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)
        
        # Draw HP bar
        bar_width = 100
        bar_height = 8
        hp_ratio = max(0, self.hp / self.max_hp)
        
        pygame.draw.rect(surface, RED, (self.x - bar_width/2 + self.width/2, 
                                       self.y - 25, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (self.x - bar_width/2 + self.width/2, 
                                         self.y - 25, bar_width * hp_ratio, bar_height))
        
        # Draw projectiles
        for proj in self.projectiles:
            pygame.draw.circle(surface, proj['color'], 
                             (int(proj['x']), int(proj['y'])), proj['size'])

    def get_rect(self):
        """Get boss rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage):
        """Take damage"""
        self.hp -= damage
        if self.hp <= 0:
            self.state = "die"
            return True
        return False

    def _distance_to(self, x, y):
        """Calculate distance"""
        dx = x - self.x
        dy = y - self.y
        return math.sqrt(dx*dx + dy*dy)

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

    def _fireball_pattern(self, player, dt):
        """Shoot fireballs at player"""
        self.vel_x = 0
        self.vel_y = 0
        
        if int(self.state_timer * 3) % 1 == 0 and self.state_timer * 3 < 3:
            # Shoot fireball at player
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 0:
                dx /= dist
                dy /= dist
                
                proj = {
                    'x': self.x + self.width/2,
                    'y': self.y + self.height/2,
                    'vx': dx * 3,
                    'vy': dy * 3,
                    'size': 10,
                    'color': ORANGE,
                    'damage': 10,
                    'aoe': 60
                }
                self.projectiles.append(proj)

    def _bullet_circle_pattern(self, player, dt):
        """Shoot bullets in circle pattern"""
        self.vel_x = 0
        self.vel_y = 0
        
        # Shoot bullets every 0.3 seconds
        if int(self.state_timer * 10) % 3 == 0 and self.state_timer > 0:
            num_bullets = 8
            for i in range(num_bullets):
                angle = (i / num_bullets) * 2 * math.pi + self.state_timer * 2
                
                proj = {
                    'x': self.x + self.width/2,
                    'y': self.y + self.height/2,
                    'vx': math.cos(angle) * 4,
                    'vy': math.sin(angle) * 4,
                    'size': 6,
                    'color': RED,
                    'damage': 8,
                    'aoe': 0
                }
                self.projectiles.append(proj)

    def _tracking_pattern(self, player, dt):
        """Shoot tracking projectiles"""
        self.vel_x = 0
        self.vel_y = 0
        
        if int(self.state_timer * 2) % 1 == 0 and self.state_timer < 2.5:
            # Shoot tracking projectile
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 0:
                dx /= dist
                dy /= dist
                
                proj = {
                    'x': self.x + self.width/2,
                    'y': self.y + self.height/2,
                    'vx': dx * 2.5,
                    'vy': dy * 2.5,
                    'size': 7,
                    'color': CYAN,
                    'damage': 10,
                    'aoe': 50,
                    'tracking': True,
                    'target_x': player.x,
                    'target_y': player.y
                }
                self.projectiles.append(proj)
                
                # Update tracking
                for p in self.projectiles:
                    if p.get('tracking'):
                        dx = player.x - p['x']
                        dy = player.y - p['y']
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist > 0:
                            p['vx'] = (dx / dist) * 2.5
                            p['vy'] = (dy / dist) * 2.5

    def is_dead(self):
        """Check if dead"""
        return self.state == "die"

    def get_projectiles(self):
        """Get all projectiles"""
        return self.projectiles
