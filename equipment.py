"""Equipment/Armor System"""
from constants import *

class Equipment:
    """Base equipment class"""
    def __init__(self, name, eq_type, hp_bonus=0, defense_bonus=0, speed_bonus=0, color=WHITE):
        self.name = name
        self.eq_type = eq_type  # "hat", "armor", "shoes", "pants"
        self.hp_bonus = hp_bonus
        self.defense_bonus = defense_bonus
        self.speed_bonus = speed_bonus
        self.color = color
        self.level = 1

    def get_total_hp_bonus(self):
        return self.hp_bonus * (1 + self.level * 0.1)

    def get_total_defense_bonus(self):
        return self.defense_bonus * (1 + self.level * 0.1)

    def get_total_speed_bonus(self):
        return self.speed_bonus * (1 + self.level * 0.1)


class Hat(Equipment):
    """Hat - increases HP"""
    def __init__(self, name="Leather Hat", hp_bonus=10):
        super().__init__(name, "hat", hp_bonus=hp_bonus, color=ORANGE)


class Armor(Equipment):
    """Armor - increases defense"""
    def __init__(self, name="Leather Armor", defense_bonus=5):
        super().__init__(name, "armor", defense_bonus=defense_bonus, color=GRAY)


class Shoes(Equipment):
    """Shoes - increases speed"""
    def __init__(self, name="Leather Boots", speed_bonus=1.0):
        super().__init__(name, "shoes", speed_bonus=speed_bonus, color=BROWN)


class Pants(Equipment):
    """Pants - balanced stats"""
    def __init__(self, name="Leather Pants", hp_bonus=5, defense_bonus=2, speed_bonus=0.5):
        super().__init__(name, "pants", hp_bonus=hp_bonus, defense_bonus=defense_bonus, 
                        speed_bonus=speed_bonus, color=LIGHT_GRAY)


# Colors for equipment
BROWN = (139, 69, 19)

# Available equipment
EQUIPMENT_DB = {
    'hat': {
        'leather_hat': Hat("Leather Hat", 10),
        'iron_hat': Hat("Iron Hat", 20),
        'golden_hat': Hat("Golden Hat", 35),
    },
    'armor': {
        'leather_armor': Armor("Leather Armor", 5),
        'steel_armor': Armor("Steel Armor", 10),
        'golden_armor': Armor("Golden Armor", 20),
    },
    'shoes': {
        'leather_boots': Shoes("Leather Boots", 1.0),
        'iron_boots': Shoes("Iron Boots", 2.0),
        'golden_boots': Shoes("Golden Boots", 3.5),
    },
    'pants': {
        'leather_pants': Pants("Leather Pants", 5, 2, 0.5),
        'steel_pants': Pants("Steel Pants", 10, 4, 1.0),
        'golden_pants': Pants("Golden Pants", 20, 8, 1.5),
    }
}


def get_equipment(eq_type, eq_key):
    """Get equipment instance"""
    if eq_type in EQUIPMENT_DB and eq_key in EQUIPMENT_DB[eq_type]:
        eq = EQUIPMENT_DB[eq_type][eq_key]
        # Create new instance
        if isinstance(eq, Hat):
            return Hat(eq.name, eq.hp_bonus)
        elif isinstance(eq, Armor):
            return Armor(eq.name, eq.defense_bonus)
        elif isinstance(eq, Shoes):
            return Shoes(eq.name, eq.speed_bonus)
        elif isinstance(eq, Pants):
            return Pants(eq.name, eq.hp_bonus, eq.defense_bonus, eq.speed_bonus)
    return None


def get_all_equipment():
    """Get all available equipment"""
    all_eq = []
    for eq_type in EQUIPMENT_DB:
        for eq_key in EQUIPMENT_DB[eq_type]:
            eq = EQUIPMENT_DB[eq_type][eq_key]
            all_eq.append(eq)
    return all_eq
