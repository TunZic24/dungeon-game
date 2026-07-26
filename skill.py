"""Skill System"""
import math
from constants import *

class Skill:
    """Base skill class"""
    def __init__(self, name, skill_type, cooldown, mana_cost, description=""):
        self.name = name
        self.skill_type = skill_type  # "slash", "rapid_fire", "fireball", etc
        self.cooldown = cooldown
        self.mana_cost = mana_cost
        self.description = description
        self.cooldown_timer = 0
        self.level = 1

    def update(self, dt):
        """Update cooldown"""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

    def can_use(self):
        """Check if skill can be used"""
        return self.cooldown_timer <= 0

    def use(self):
        """Use skill"""
        self.cooldown_timer = self.cooldown

    def execute(self, player_pos, target_pos, player):
        """
        Execute skill
        Returns effects/projectiles
        """
        return {}


class SlashSkill(Skill):
    """Sword skill - AOE slash attack"""
    def __init__(self):
        super().__init__("Slash", "slash", 1.5, 0, 
                        "Swing sword in an arc, hitting all enemies nearby")

    def execute(self, player_pos, target_pos, player):
        """Create slash effect"""
        return {
            'type': 'melee_aoe',
            'x': player_pos[0],
            'y': player_pos[1],
            'radius': 100,
            'damage': player.weapon.damage * 1.5,
            'duration': 0.3
        }


class RapidFireSkill(Skill):
    """Gun skill - shoot multiple projectiles"""
    def __init__(self):
        super().__init__("Rapid Fire", "rapid_fire", 2.0, 0,
                        "Shoot 5 projectiles in rapid succession")

    def execute(self, player_pos, target_pos, player):
        """Create multiple projectiles"""
        projectiles = []
        
        dx = target_pos[0] - player_pos[0]
        dy = target_pos[1] - player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist == 0:
            dx, dy = 1, 0
        else:
            dx /= dist
            dy /= dist

        # Spread angle
        angles = [-0.3, -0.15, 0, 0.15, 0.3]
        
        for angle_offset in angles:
            # Rotate direction vector
            angle = math.atan2(dy, dx) + angle_offset
            px = math.cos(angle) * PROJECTILE_SPEED
            py = math.sin(angle) * PROJECTILE_SPEED
            
            projectile = {
                'x': player_pos[0],
                'y': player_pos[1],
                'vx': px,
                'vy': py,
                'damage': player.weapon.damage * 0.8,
                'type': 'gun',
                'color': CYAN,
                'size': PROJECTILE_SIZE
            }
            projectiles.append(projectile)
        
        return {
            'type': 'projectiles',
            'projectiles': projectiles
        }


class FireballSkill(Skill):
    """Magic skill - large fireball explosion"""
    def __init__(self):
        super().__init__("Fireball", "fireball", 2.5, 0,
                        "Launch a massive fireball that explodes on impact")

    def execute(self, player_pos, target_pos, player):
        """Create fireball projectile"""
        dx = target_pos[0] - player_pos[0]
        dy = target_pos[1] - player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist == 0:
            dx, dy = 1, 0
        else:
            dx /= dist
            dy /= dist

        projectile = {
            'x': player_pos[0],
            'y': player_pos[1],
            'vx': dx * PROJECTILE_SPEED * 0.6,
            'vy': dy * PROJECTILE_SPEED * 0.6,
            'damage': player.weapon.damage * 2.0,
            'type': 'magic',
            'color': ORANGE,
            'size': PROJECTILE_SIZE + 5,
            'aoe_radius': 120
        }
        
        return {
            'type': 'projectile',
            'projectile': projectile
        }


# Available skills
SKILLS = {
    'slash': SlashSkill(),
    'rapid_fire': RapidFireSkill(),
    'fireball': FireballSkill(),
}


def get_skill(skill_key):
    """Get skill instance"""
    if skill_key in SKILLS:
        skill = SKILLS[skill_key]
        if isinstance(skill, SlashSkill):
            return SlashSkill()
        elif isinstance(skill, RapidFireSkill):
            return RapidFireSkill()
        elif isinstance(skill, FireballSkill):
            return FireballSkill()
    return None
