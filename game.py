"""Main Game Logic"""
import pygame
import random
import math
from constants import *
from player import Player
from enemy import spawn_enemy
from weapon import get_weapon
from equipment import get_equipment
from puzzle import DoorPuzzle, create_puzzle, MathPuzzle
from boss import Boss
from ui import UI
from skill import get_skill

class Game:
    """Main game class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 Dungeon Game - Action Puzzle Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_MENU
        
        # UI
        self.ui = UI()
        
        # Game objects
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.boss = None
        self.current_room = ROOM_1
        self.doors = []
        self.current_puzzle = None
        
        # Font
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        
        self.init_game()

    def init_game(self):
        """Initialize new game"""
        self.state = STATE_PLAYING
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.current_room = ROOM_1
        self.load_room(ROOM_1)

    def load_room(self, room_id):
        """Load a room"""
        self.enemies = []
        self.projectiles = []
        self.doors = []
        self.current_puzzle = None
        
        if room_id == ROOM_1:
            self.load_room_1()
        elif room_id == ROOM_2:
            self.load_room_2()
        elif room_id == ROOM_3:
            self.load_room_3()
        elif room_id == ROOM_BOSS:
            self.load_boss_room()

    def load_room_1(self):
        """Load room 1 - basic enemies"""
        self.current_room = ROOM_1
        self.player.x = 100
        self.player.y = SCREEN_HEIGHT // 2
        
        # Spawn enemies
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 150, 150, "basic"))
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 200, 400, "basic"))
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 100, 600, "fast"))
        
        # Create door to next room
        puzzle = MathPuzzle("room1_puzzle")
        self.doors.append(DoorPuzzle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 40, 100, puzzle))
        self.current_puzzle = puzzle

    def load_room_2(self):
        """Load room 2 - stronger enemies"""
        self.current_room = ROOM_2
        self.player.x = 100
        self.player.y = SCREEN_HEIGHT // 2
        
        # Spawn enemies
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 150, 150, "strong"))
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 200, 400, "fast"))
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 100, 600, "basic"))
        
        # Door
        puzzle = create_puzzle("sequence")
        self.doors.append(DoorPuzzle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 40, 100, puzzle))
        self.current_puzzle = puzzle

    def load_room_3(self):
        """Load room 3 - final room before boss"""
        self.current_room = ROOM_3
        self.player.x = 100
        self.player.y = SCREEN_HEIGHT // 2
        
        # Spawn enemies
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 150, 150, "strong"))
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 200, 400, "strong"))
        self.enemies.append(spawn_enemy(SCREEN_WIDTH - 100, 600, "fast"))
        
        # Door to boss
        puzzle = create_puzzle("memory")
        self.doors.append(DoorPuzzle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 40, 100, puzzle))
        self.current_puzzle = puzzle

    def load_boss_room(self):
        """Load boss room"""
        self.current_room = ROOM_BOSS
        self.player.x = 100
        self.player.y = SCREEN_HEIGHT // 2
        self.boss = Boss(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2)

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_e:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_INVENTORY
                    elif self.state == STATE_INVENTORY:
                        self.state = STATE_PLAYING
                elif event.key == pygame.K_p:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSE
                    elif self.state == STATE_PAUSE:
                        self.state = STATE_PLAYING
                elif event.key == pygame.K_r:
                    if self.state in [STATE_GAME_OVER, STATE_WIN]:
                        self.init_game()
                
                # Puzzle input
                elif self.state == STATE_PUZZLE and self.current_puzzle:
                    if isinstance(self.current_puzzle, MathPuzzle):
                        if event.key == pygame.K_RETURN:
                            if self.current_puzzle.check_answer(self.current_puzzle.user_answer):
                                self.state = STATE_PLAYING
                        elif event.key == pygame.K_BACKSPACE:
                            if self.current_puzzle.user_answer:
                                self.current_puzzle.user_answer = self.current_puzzle.user_answer[:-1]
                        elif event.unicode.isdigit() or event.unicode == '-':
                            if not self.current_puzzle.user_answer:
                                self.current_puzzle.user_answer = event.unicode
                            else:
                                self.current_puzzle.user_answer += event.unicode
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == STATE_PLAYING:
                    self.player_attack(pygame.mouse.get_pos())
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == STATE_PLAYING:
                    self.player_skill(pygame.mouse.get_pos())

    def player_attack(self, target_pos):
        """Player attack"""
        if self.player.weapon.can_attack():
            self.player.weapon.attack()
            
            # Get projectiles from weapon
            projectiles = self.player.weapon.get_projectiles(
                (self.player.x, self.player.y),
                target_pos
            )
            self.projectiles.extend(projectiles)

    def player_skill(self, target_pos):
        """Player uses skill"""
        if self.player.skill and self.player.skill.can_use():
            self.player.skill.use()
            effect = self.player.skill.execute(
                (self.player.x, self.player.y),
                target_pos,
                self.player
            )
            
            if effect.get('type') == 'melee_aoe':
                # AOE damage
                for enemy in self.enemies:
                    if not enemy.is_dead():
                        dx = enemy.x - effect['x']
                        dy = enemy.y - effect['y']
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist < effect['radius']:
                            enemy.take_damage(effect['damage'])
            elif effect.get('type') == 'projectiles':
                self.projectiles.extend(effect['projectiles'])
            elif effect.get('type') == 'projectile':
                self.projectiles.append(effect['projectile'])

    def update(self, dt):
        """Update game state"""
        if self.state == STATE_PLAYING:
            # Update player
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.player.update(dt, keys, mouse_pos)
            
            # Update enemies
            for enemy in self.enemies:
                if not enemy.is_dead():
                    enemy.update(dt, self.player)
            
            # Update boss
            if self.boss:
                self.boss.update(dt, self.player)
            
            # Update projectiles
            for proj in self.projectiles[:]:
                proj['x'] += proj['vx']
                proj['y'] += proj['vy']
                
                # Check off-screen
                if proj['x'] < -50 or proj['x'] > SCREEN_WIDTH + 50 or \
                   proj['y'] < -50 or proj['y'] > SCREEN_HEIGHT + 50:
                    self.projectiles.remove(proj)
            
            # Check collisions: projectiles vs enemies
            for proj in self.projectiles[:]:
                for enemy in self.enemies[:]:
                    if not enemy.is_dead():
                        dist = math.sqrt((proj['x'] - enemy.x)**2 + (proj['y'] - enemy.y)**2)
                        if dist < ENEMY_SIZE / 2 + proj.get('size', 5):
                            enemy.take_damage(proj['damage'])
                            if proj in self.projectiles:
                                self.projectiles.remove(proj)
                            break
            
            # Check collisions: projectiles vs boss
            if self.boss and not self.boss.is_dead():
                for proj in self.projectiles[:]:
                    dist = math.sqrt((proj['x'] - self.boss.x)**2 + (proj['y'] - self.boss.y)**2)
                    if dist < BOSS_SIZE / 2 + proj.get('size', 5):
                        self.boss.take_damage(proj['damage'])
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)
            
            # Check collisions: boss projectiles vs player
            if self.boss:
                for proj in self.boss.projectiles:
                    dist = math.sqrt((proj['x'] - self.player.x)**2 + (proj['y'] - self.player.y)**2)
                    if dist < PLAYER_SIZE / 2 + proj.get('size', 5):
                        self.player.take_damage(proj['damage'])
                        if proj in self.boss.projectiles:
                            self.boss.projectiles.remove(proj)
            
            # Check enemy attacks
            for enemy in self.enemies:
                if enemy.can_attack():
                    dist = math.sqrt((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)
                    if dist < 60:
                        self.player.take_damage(enemy.damage)
            
            # Check dead enemies - loot
            for enemy in self.enemies[:]:
                if enemy.is_dead():
                    loot = enemy.get_loot()
                    if loot:
                        # Get random loot
                        if loot.startswith('iron') or loot.startswith('steel'):
                            weapon = get_weapon(loot)
                            if weapon:
                                self.player.weapon = weapon
                        else:
                            # Equipment
                            for eq_type in ['hat', 'armor', 'shoes', 'pants']:
                                eq = get_equipment(eq_type, loot)
                                if eq:
                                    self.player.equip_equipment(eq)
                                    break
                    self.enemies.remove(enemy)
            
            # Check door collision for puzzle
            for door in self.doors:
                door.update(dt)
                if door.blocks_player(self.player.get_rect()):
                    if not door.is_open():
                        self.state = STATE_PUZZLE
                        if not self.current_puzzle:
                            self.current_puzzle = create_puzzle("math")
                        break
            
            # Check boss defeat
            if self.boss and self.boss.is_dead():
                self.state = STATE_WIN
            
            # Check room clear
            if len(self.enemies) == 0 and self.current_room < ROOM_BOSS:
                # Check if player reached door
                if self.player.x > SCREEN_WIDTH - 100:
                    self.current_room += 1
                    self.load_room(self.current_room)
            
            # Check player death
            if not self.player.is_alive():
                self.state = STATE_GAME_OVER

    def draw(self):
        """Draw game"""
        self.screen.fill(BLACK)
        
        if self.state == STATE_PLAYING:
            # Draw game world
            self.player.draw(self.screen)
            
            for enemy in self.enemies:
                if not enemy.is_dead():
                    enemy.draw(self.screen)
            
            for proj in self.projectiles:
                pygame.draw.circle(self.screen, proj.get('color', YELLOW),
                                  (int(proj['x']), int(proj['y'])),
                                  proj.get('size', 5))
            
            for door in self.doors:
                door.draw(self.screen)
            
            if self.boss:
                self.boss.draw(self.screen)
            
            # Draw HUD
            self.ui.draw_hud(self.screen, self.player)
            
            # Draw controls
            font = pygame.font.Font(None, 20)
            controls = [
                "Arrow/WASD: Move | Click: Attack | E: Inventory",
                "Space: Skill | P: Pause | ESC: Quit"
            ]
            for i, text in enumerate(controls):
                ctrl_text = font.render(text, True, GRAY)
                self.screen.blit(ctrl_text, (10, SCREEN_HEIGHT - 30 - i * 20))
        
        elif self.state == STATE_INVENTORY:
            self.ui.draw_inventory(self.screen, self.player)
        
        elif self.state == STATE_PUZZLE:
            self.ui.draw_puzzle(self.screen, self.current_puzzle)
        
        elif self.state == STATE_PAUSE:
            self.ui.draw_pause(self.screen)
        
        elif self.state == STATE_GAME_OVER:
            self.ui.draw_game_over(self.screen)
        
        elif self.state == STATE_WIN:
            self.ui.draw_win(self.screen)
        
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
