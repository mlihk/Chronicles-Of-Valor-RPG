import random
import pygame
import sys
import time
import pygame.mixer
from weapons import item_library
from armours import armour_library


#color codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

CELL_SIZE = 50
GRID_SIZE = 10
WINDOW_SIZE = (800, 600)
INFO_BOARD_WIDTH = 200

current_map = ""

mob_image_path = "logo/boarpic.png"
player_info_button_rect = pygame.Rect(WINDOW_SIZE[0] - INFO_BOARD_WIDTH + 10, 200, INFO_BOARD_WIDTH - 20, 30)
cogwheel_rect = None
backpack_rect = None

class Player:
    def __init__(self, name, position):
        self.name = name
        self.health = 100
        self.strength = 10
        self.stamina = 10
        self.current_stamina = self.stamina
        self.intelligence = 10
        self.defense = 10
        self.position = position
        self.inventory = ["1", "2", "8"]
        self.equipped_weapon = None
        self.equipped_armour = None

    def player_attack(self):
        return self.strength

    def weapon_damage(self, amount):
        self.strength += amount

    def weapon_damage_taken_off(self, amount):
        self.strength -= amount

    def armour_defense(self, amount):
        self.defense += amount

    def armour_defense_taken_off(self, amount):
        self.defense -= amount

    def player_take_damage(self, damage):
        self.health -= damage

    def player_heal(self, amount):
        self.health += amount

    def player_add_item(self, item):
        self.inventory.append(item)

    def player_move(self, direction):
        if self.current_stamina >0:
            if direction == "up":
                self.position[0] -= 1
            elif direction == "down":
                self.position[0] += 1
            elif direction == "left":
                self.position[1] -= 1
            elif direction == "right":
                self.position[1] += 1

    def reduce_stamina(self, amount):
        if self.current_stamina > 0:
            if self.current_stamina - amount < 0:
                self.current_stamina = 0
            else:
                self.current_stamina -= amount

    def regenerate_stamina(self, amount):
        if self.current_stamina < self.stamina:
            if self.current_stamina + amount < self.stamina:
                self.current_stamina += amount
            else:
                self.current_stamina = self.stamina
    
    def player_show_inventory(self):
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print("-", item)
        else:
            print("Inventory is empty.")

    def equip_item(self, item_id):
        item = find_item_by_id(item_id, item_library)
        if item:
            if item.type == "weapon":
                if self.equipped_weapon == None:
                    self.equipped_weapon = item
                    self.weapon_damage(item.damage)
            elif item.type == "armour":
                if self.equipped_armour == None:
                    self.equipped_armour = item
                    self.armour_defense(item.defense)
        #else:
        #    print("Cannot equip item of type:", item.type)

    def unequip_item(self, item):
        if item:
            if item.type == "weapon":
                # Unequip the weapon
                self.equipped_weapon = None
                # Restore player's strength
                self.weapon_damage_taken_off(item.damage)
            elif item.type == "armour":
                # Unequip the armour
                self.equipped_armour = None
                # Restore player's defense
                self.armour_defense_taken_off(item.defense)

    def draw(self, screen):
        x, y = self.position
        body_color = GREEN

        # Draw head
        pygame.draw.circle(screen, body_color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2 - 15), 10)
        
        # Draw body
        pygame.draw.line(screen, body_color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2 + 20), 3)
        
        # Draw arms
        pygame.draw.line(screen, body_color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), (x * CELL_SIZE + CELL_SIZE // 2 - 10, y * CELL_SIZE + CELL_SIZE // 2 + 10), 3)
        pygame.draw.line(screen, body_color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), (x * CELL_SIZE + CELL_SIZE // 2 + 10, y * CELL_SIZE + CELL_SIZE // 2 + 10), 3)
        
        # Draw legs
        pygame.draw.line(screen, body_color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2 + 20), (x * CELL_SIZE + CELL_SIZE // 2 - 10, y * CELL_SIZE + CELL_SIZE // 2 + 40), 3)
        pygame.draw.line(screen, body_color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2 + 20), (x * CELL_SIZE + CELL_SIZE // 2 + 10, y * CELL_SIZE + CELL_SIZE // 2 + 40), 3)
        
def draw_player_info(screen, font, player):
    # Define dimensions for the player info bar
    info_board_width = 200
    info_board_height = 200  # Adjust this value as needed
    info_board_x = WINDOW_SIZE[0] - info_board_width
    info_board_y = (WINDOW_SIZE[1] - info_board_height) // 2  # Center vertically

    # Draw outer border rectangle
    info_bar_rect_outer = pygame.Rect(info_board_x, info_board_y, info_board_width, info_board_height)
    pygame.draw.rect(screen, (255, 215, 0), info_bar_rect_outer, 2)  # Gold color, thickness 2

    # Define dimensions for the inner background rectangle
    inner_padding = 2
    inner_width = info_board_width - 2 * inner_padding
    inner_height = info_board_height - 2 * inner_padding
    inner_x = info_board_x + inner_padding
    inner_y = info_board_y + inner_padding

    # Draw inner background rectangle
    info_bar_rect_inner = pygame.Rect(inner_x, inner_y, inner_width, inner_height)
    pygame.draw.rect(screen, BLACK, info_bar_rect_inner)

    # Display player information
    player_info_text = font.render("Player Info:", True, WHITE)
    screen.blit(player_info_text, (inner_x + 10, inner_y + 20))
    # Display player stats, inventory, etc.
    # Example:
    player_name_text = font.render(f"Name: {player.name}", True, WHITE)
    screen.blit(player_name_text, (inner_x + 10, inner_y + 50))
    player_health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(player_health_text, (inner_x + 10, inner_y + 80))
    player_strength_text = font.render(f"Strength: {player.strength}", True, WHITE)
    screen.blit(player_strength_text, (inner_x + 10, inner_y + 110))
    player_defense_text = font.render(f"Defense: {player.defense}", True, WHITE)
    screen.blit(player_defense_text, (inner_x + 10, inner_y + 140))
    player_stamina_text = font.render(f"Stamina: {player.current_stamina}/{player.stamina}", True, WHITE)
    screen.blit(player_stamina_text, (inner_x + 10, inner_y + 170))


    
def draw_tools_bar_info(screen, font, player):
    global cogwheel_rect
    cogwheel_img = pygame.image.load("logo/cogwheel.jpg")
    cogwheel_img = pygame.transform.scale(cogwheel_img, (30,30))
    cogwheel_rect = cogwheel_img.get_rect()
    cogwheel_rect.topright = (screen.get_width() - 10, 10)
    screen.blit(cogwheel_img, cogwheel_rect)
    
    global backpack_rect
    backpack_img = pygame.image.load("logo/backpack.jpg")
    backpack_img = pygame.transform.scale(backpack_img, (30,30))
    backpack_rect = backpack_img.get_rect()
    backpack_rect.topright = (cogwheel_rect.left - 10, 10)
    screen.blit(backpack_img, backpack_rect)
    

class Mob:
    def __init__(self, name, health, strength, defense, position, image_path, cell_size):
        self.name = name
        self.health = health
        self.strength = strength
        self.defense = defense
        self.position = position
        self.cell_size = cell_size
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, (cell_size, cell_size))

    def mob_attack(self):
        return random.randint(1, self.strength)

    def mob_defend(self):
        return random.randint(1, self.defense)

    def mob_take_damage(self, damage):
        self.health -= damage

    def draw(self, screen):
        x, y = self.position
        screen.blit(self.image, (x * CELL_SIZE, y * CELL_SIZE))


        
def find_item_by_id(item_id, item_library):
    for item in item_library:
        if item_id in item.id:
            return item
    return None
    
def draw_settings_popup(screen, font, player, mouse_pos):
    # Draw background
    popup_width = 400
    popup_height = 300
    popup_x = (WINDOW_SIZE[0] - popup_width) // 2
    popup_y = (WINDOW_SIZE[1] - popup_height) // 2
    pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height))
    
    title_text = font.render("Settings", True, BLACK)
    screen.blit(title_text, (popup_x + 20, popup_y + 20))
    
    volume_text = font.render("Volume:", True, BLACK)
    screen.blit(volume_text, (popup_x + 20, popup_y + 100))
    
    volume_bar_width = 200
    volume_bar_height = 20
    volume_bar_x = popup_x + 90
    volume_bar_y = popup_y + 100
    pygame.draw.rect(screen, BLACK, (volume_bar_x, volume_bar_y, volume_bar_width, volume_bar_height))
    

    # Calculate the position of the volume indicator based on the music volume
    music_volume = pygame.mixer.music.get_volume()
    volume_indicator_x = volume_bar_x + int(music_volume * volume_bar_width)
    volume_indicator_y = volume_bar_y + 10
    volume_indicator_width = 20
    volume_indicator_height = 30
    pygame.draw.rect(screen, RED, (volume_indicator_x - volume_indicator_width // 2, volume_indicator_y - volume_indicator_height // 2,
                                    volume_indicator_width, volume_indicator_height))

    
    if pygame.Rect(volume_indicator_x - volume_indicator_width // 2, volume_indicator_y - volume_indicator_height // 2,
                    volume_indicator_width, volume_indicator_height).collidepoint(mouse_pos):
        # If the mouse is pressed, update the music volume based on the mouse position
        if pygame.mouse.get_pressed()[0]:
            volume_indicator_x = min(max(volume_bar_x, mouse_pos[0]), volume_bar_x + volume_bar_width)
            pygame.mixer.music.set_volume((volume_indicator_x - volume_bar_x) / volume_bar_width)
            
    volume_percentage = int(music_volume * 100)
    volume_percentage_text = font.render(f"{volume_percentage}%", True, BLACK)
    volume_percentage_rect = volume_percentage_text.get_rect(topright=(popup_x + popup_width - 20, popup_y + 100))
    screen.blit(volume_percentage_text, volume_percentage_rect)

    pygame.display.update()

    
    


def draw_inventory_popup(screen, font, player, mouse_pos):
    # Draw background
    popup_width = 400
    popup_height = 300
    popup_x = (WINDOW_SIZE[0] - popup_width) // 2
    popup_y = (WINDOW_SIZE[1] - popup_height) // 2
    pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height))

    # Display inventory title
    title_text = font.render("Inventory", True, BLACK)
    screen.blit(title_text, (popup_x + 20, popup_y + 20))

    # Display equipped weapon
    equipped_weapon_text = font.render(f"Equipped Weapon: {player.equipped_weapon.name if player.equipped_weapon else 'None'}", True, BLACK)
    screen.blit(equipped_weapon_text, (popup_x + 20, popup_y + 60))

    # Display remove button for equipped weapon
    if player.equipped_weapon:
        remove_weapon_text = font.render("[x]", True, RED)
        remove_weapon_button = pygame.Rect(popup_x + equipped_weapon_text.get_width() + 30, popup_y + 60, remove_weapon_text.get_width() + 10, 30)
        pygame.draw.rect(screen, WHITE, remove_weapon_button)
        screen.blit(remove_weapon_text, (popup_x + equipped_weapon_text.get_width() + 35, popup_y + 60))
        # Check if the remove button is clicked
        if remove_weapon_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                player.unequip_item(player.equipped_weapon)

    # Display equipped armour
    equipped_armour_text = font.render(f"Equipped Armour: {player.equipped_armour.name if player.equipped_armour else 'None'}", True, BLACK)
    screen.blit(equipped_armour_text, (popup_x + 20, popup_y + 100))

    # Display remove button for equipped armour
    if player.equipped_armour:
        remove_armour_text = font.render("[x]", True, RED)
        remove_armour_button = pygame.Rect(popup_x + equipped_armour_text.get_width() + 30, popup_y + 100, remove_armour_text.get_width() + 10, 30)
        pygame.draw.rect(screen, WHITE, remove_armour_button)
        screen.blit(remove_armour_text, (popup_x + equipped_armour_text.get_width() + 35, popup_y + 100))
        # Check if the remove button is clicked
        if remove_armour_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                player.unequip_item(player.equipped_armour)

    # Display inventory items
    inventory_text = font.render("Inventory:", True, BLACK)
    screen.blit(inventory_text, (popup_x + 20, popup_y + 120))
    inventory_y = popup_y + 160
    for item_id in player.inventory:
        item = find_item_by_id(item_id, item_library)
        if item:
            item_name_text = font.render(item.name, True, BLACK)
            screen.blit(item_name_text, (popup_x + 40, inventory_y))

            # Add equip button
            equip_button_rect = pygame.Rect(popup_x + 200, inventory_y, 100, 30)
            pygame.draw.rect(screen, GREEN, equip_button_rect)
            equip_text = font.render("Equip", True, BLACK)
            screen.blit(equip_text, equip_button_rect.topleft)

            # Check if the mouse is over the equip button
            if equip_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, RED, equip_button_rect, 2)  # Highlight button on hover
                if pygame.mouse.get_pressed()[0]:
                    player.equip_item(item_id)

            inventory_y += 30

    pygame.display.update()




class Map:
    def __init__(self, size):
        self.size = size
        self.map = [["." for _ in range(size)] for _ in range(size)]

    def generate_map(self):
        # Logic to randomly generate map layout
        pass

    def place_entity(self, entity, position):
        self.map[position[0]][position[1]] = entity
        
    def place_items(self):
        # Logic to place weapons and armors on the map
        for item in items:
            self.map[item.position[0]][item.position[1]] = "I"

    def draw(self, screen, font):
        map_width = self.size * CELL_SIZE
        map_height = self.size * CELL_SIZE
        offset_x = (WINDOW_SIZE[0] - map_width - INFO_BOARD_WIDTH) // 2
        offset_y = (WINDOW_SIZE[1] - map_height) // 2

        # Draw grid lines
        for i in range(self.size + 1):
            pygame.draw.line(screen, WHITE, (offset_x + i * CELL_SIZE, offset_y),
                             (offset_x + i * CELL_SIZE, offset_y + map_height), 2)
            pygame.draw.line(screen, WHITE, (offset_x, offset_y + i * CELL_SIZE),
                             (offset_x + map_width, offset_y + i * CELL_SIZE), 2)

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
                if cell is None:
                    pygame.draw.rect(screen, WHITE, rect)
                elif isinstance(cell, Player):
                    cell.draw(screen)
                elif isinstance(cell, Mob):
                    cell.draw(screen)

        # Draw x-coordinate indicators
        for x in range(self.size):
            text = font.render(str(x), True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (offset_x + x * CELL_SIZE + CELL_SIZE // 2, offset_y - 20)
            screen.blit(text, text_rect)

        # Draw y-coordinate indicators
        for y in range(self.size):
            text = font.render(str(y), True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (offset_x - 20, offset_y + y * CELL_SIZE + CELL_SIZE // 2)
            screen.blit(text, text_rect)

            
class GameEngine:
    def __init__(self, player, map):
        self.player = player
        self.map = map

    def move_player(self, direction):
        current_position = self.player.position[:]
        
        # Logic to move player on the map
        if direction == "up":
            current_position[1] -= 1
        elif direction == "down":
            current_position[1] += 1
        elif direction == "left":
            current_position[0] -= 1
        elif direction == "right":
            current_position[0] += 1

        # Check if the new position is within the map boundaries
        if 1 <= current_position[0] < (self.map.size)+1 and 1 <= current_position[1] < (self.map.size)+1:
            # Update player position
            self.player.position = current_position


    def explore_current_location(self):
        # Logic to trigger events at current location (e.g., combat, item pickup)
        pass

    def combat(self, mob):
        # Logic for combat between player and mob
        pass

    def pickup_item(self, item):
        # Logic to add item to player's inventory
        pass

def display_warning_text(screen, text):
    font = pygame.font.SysFont(None, 36)
    warning_text = font.render(text, True, WHITE)
    screen.blit(warning_text, ((WINDOW_SIZE[0] - warning_text.get_width()) // 2, (WINDOW_SIZE[1] - warning_text.get_height()) // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds
    
def update_game_music():
    global current_map
    if current_map == "map1":
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/map1_bgm.mp3")
        pygame.mixer.music.play(-1)
    elif current_map == "map2":
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/map2_bgm.mp3")
        pygame.mixer.music.play(-1)
    
def update_map_background(screen):
    global current_map
    if current_map == "map1":
        background_image = pygame.image.load("logo/map1_bg.jpg")
        background_image = pygame.transform.scale(background_image, WINDOW_SIZE)
        screen.blit(background_image, (0, 0))
    
def main():
    player_name = input("Enter your name: ")
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Map")
    
    global cogwheel_rect
    global backpack_rect
    global current_map
    current_map = "map1"
    
    pygame.mixer.init()
    
    update_game_music()
    #update_map_background(screen)

    map = Map(GRID_SIZE)
    mob_cell_size = CELL_SIZE
    
    player = Player(player_name, [5, 5])
    mob1 = Mob("Wild Boar", int(10), int(10), int(10), [2, 3], mob_image_path, mob_cell_size)
    mob2 = Mob("Wild Bear", int(15), int(15), int(10), [7, 8], mob_image_path, mob_cell_size)
    
    map.place_entity(player, player.position)
    map.place_entity(mob1, mob1.position)
    map.place_entity(mob2, mob2.position)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    game_engine = GameEngine(player, map)

    start_time = time.time()

    show_inventory_popup = False
    show_settings_popup = False

    # Game loop
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if player.current_stamina > 0:
                    if event.key == pygame.K_UP:
                        game_engine.move_player("up")
                        player.reduce_stamina(1)
                    elif event.key == pygame.K_DOWN:
                        game_engine.move_player("down")
                        player.reduce_stamina(1)
                    elif event.key == pygame.K_LEFT:
                        game_engine.move_player("left")
                        player.reduce_stamina(1)
                    elif event.key == pygame.K_RIGHT:
                        game_engine.move_player("right")
                        player.reduce_stamina(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if cogwheel_rect.collidepoint(event.pos):
                        if show_settings_popup == True:
                            show_settings_popup = False
                        else:
                            show_settings_popup = True
                    elif backpack_rect.collidepoint(event.pos):
                        if show_inventory_popup == True:
                            show_inventory_popup = False
                        else:
                            show_inventory_popup = True



        if elapsed_time >= 3:
            player.regenerate_stamina(1)
            start_time = current_time

        screen.fill(BLACK)
        
        map.draw(screen, font)

        draw_player_info(screen, font, player)
        draw_tools_bar_info(screen, font, player)

        if show_inventory_popup:
            draw_inventory_popup(screen, font, player, pygame.mouse.get_pos())
        
        if show_settings_popup:
            draw_settings_popup(screen, font, player, pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
