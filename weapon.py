"""Weapon System"""
import math
from constants import *

class Weapon:
    """Base weapon class"""
    def __init__(self, name, weapon_type, damage, attack_speed, attack_range, color, skill_name=""):
        self.name = name
        self.weapon_type = weapon_type  # "sword", "gun", "magic"
        self.damage = damage
        self.attack_speed = attack_speed  # attacks per second
        self.attack_range = attack_range
        self.color = color
        self.skill_name = skill_name
        self.attack_cooldown = 0
        self.level = 1

    def update(self, dt):
        """Update cooldown"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    def can_attack(self):
        """Check if weapon can attack"""
        return self.attack_cooldown <= 0

    def attack(self):
        """Trigger attack cooldown"""
        self.attack_cooldown = 1.0 / self.attack_speed

    def get_projectiles(self, player_pos, target_pos):
        """
        Return list of projectiles to spawn
        Override in subclasses for different attack patterns
        """
        return []

    def get_melee_damage(self):
        """Get melee damage (for sword)"""
        return self.damage


class Sword(Weapon):
    """Melee sword weapon"""
    def __init__(self, name="Iron Sword", damage=15, attack_speed=1.5):
        super().__init__(name, "sword", damage, attack_speed, 60, YELLOW, "Slash")
        self.damage = damage

    def get_projectiles(self, player_pos, target_pos):
        """Sword creates melee hit effect"""
        return []

    def get_melee_damage(self):
        return self.damage * (1 + self.level * 0.1)


class Gun(Weapon):
    """Ranged gun weapon"""
    def __init__(self, name="Pistol", damage=10, attack_speed=2.5):
        super().__init__(name, "gun", damage, attack_speed, 600, BLUE, "Rapid Fire")
        self.damage = damage

    def get_projectiles(self, player_pos, target_pos):
        """Gun fires single projectile"""
        dx = target_pos[0] - player_pos[0]
        dy = target_pos[1] - player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist == 0:
            dx, dy = 1, 0
        else:
            dx /= dist
            dy /= dist

        damage = self.damage * (1 + self.level * 0.1)
        projectile = {
            'x': player_pos[0],
            'y': player_pos[1],
            'vx': dx * PROJECTILE_SPEED,
            'vy': dy * PROJECTILE_SPEED,
            'damage': damage,
            'type': 'gun',
            'color': BLUE,
            'size': PROJECTILE_SIZE
        }
        return [projectile]


class MagicStaff(Weapon):
    """Magic staff weapon with AOE"""
    def __init__(self, name="Fire Staff", damage=20, attack_speed=1.0):
        super().__init__(name, "magic", damage, attack_speed, 400, PURPLE, "Fireball")
        self.damage = damage

    def get_projectiles(self, player_pos, target_pos):
        """Magic fires projectile that explodes on impact"""
        dx = target_pos[0] - player_pos[0]
        dy = target_pos[1] - player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist == 0:
            dx, dy = 1, 0
        else:
            dx /= dist
            dy /= dist

        damage = self.damage * (1 + self.level * 0.1)
        projectile = {
            'x': player_pos[0],
            'y': player_pos[1],
            'vx': dx * PROJECTILE_SPEED * 0.7,
            'vy': dy * PROJECTILE_SPEED * 0.7,
            'damage': damage,
            'type': 'magic',
            'color': PURPLE,
            'size': PROJECTILE_SIZE + 3,
            'aoe_radius': 80
        }
        return [projectile]


# Available weapons
WEAPONS = {
    'iron_sword': Sword("Iron Sword", 15, 1.5),
    'steel_sword': Sword("Steel Sword", 20, 1.8),
    'golden_sword': Sword("Golden Sword", 30, 2.0),
    
    'pistol': Gun("Pistol", 10, 2.5),
    'rifle': Gun("Rifle", 15, 2.0),
    'machine_gun': Gun("Machine Gun", 8, 4.0),
    
    'fire_staff': MagicStaff("Fire Staff", 20, 1.0),
    'ice_staff': MagicStaff("Ice Staff", 18, 1.2),
    'lightning_staff': MagicStaff("Lightning Staff", 25, 0.8),
}


def get_weapon(weapon_key):
    """Get weapon instance"""
    if weapon_key in WEAPONS:
        weapon = WEAPONS[weapon_key]
        # Create new instance to avoid sharing state
        if isinstance(weapon, Sword):
            return Sword(weapon.name, weapon.damage, weapon.attack_speed)
        elif isinstance(weapon, Gun):
            return Gun(weapon.name, weapon.damage, weapon.attack_speed)
        elif isinstance(weapon, MagicStaff):
            return MagicStaff(weapon.name, weapon.damage, weapon.attack_speed)
    return get_weapon('iron_sword')
