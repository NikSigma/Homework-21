import pygame
import json, os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Збір предметів та інвентар")
player_img = pygame.image.load("player.jpg").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))
pickaxe_img = pygame.image.load("Pickaxe.webp").convert_alpha()
pickaxe_img = pygame.transform.scale(pickaxe_img, (30, 30))
wood_img = pygame.image.load("Wood.webp").convert_alpha()
wood_img = pygame.transform.scale(wood_img, (30, 30))
chest_img = pygame.image.load("Chest.jpg").convert_alpha()
chest_img = pygame.transform.scale(chest_img, (50, 50))
stone_img = pygame.image.load("Stone.jpg").convert_alpha()
stone_img = pygame.transform.scale(stone_img, (30, 30))


portal_img = pygame.Surface((60, 60))
portal_img.fill((100, 0, 200))
portal = None
portal_active = False

player = pygame.Rect(100, 100, 50, 50)
chest = pygame.Rect(400, 300, 50, 50)
pickaxe = pygame.Rect(200, 150, 30, 30)
woods = [pygame.Rect(300, 400, 30, 30), pygame.Rect(500, 200, 30, 30)]
stones = [pygame.Rect(600, 400, 30, 30)]

inventory = {"Pickaxe": 0, "Wood": 0, "Stone": 0, "Sword": 0}

chest_opened = False
has_pickaxe = False
show_inventory = False
active_item = None
clock = pygame.time.Clock()

def blink_item(rect, image):
    for i in range(3):
        screen.blit(image, (rect.x, rect.y))
        pygame.display.flip()
        pygame.time.delay(100)
        screen.fill((255, 255, 255))
        pygame.display.flip()
        pygame.time.delay(100)

def save_game():
    data = {"inventory": inventory, "player": [player.x, player.y]}
    with open("save.json", "w") as f:
        json.dump(data, f)
    print("Гру збережено!")

def load_game():
    global inventory, player
    if os.path.exists("save.json"):
        with open("save.json", "r") as f:
            data = json.load(f)
            inventory.update(data["inventory"])
            player.x, player.y = data["player"]
        print("Гру завантажено!")

running = True
game_won = False 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_UP]:
        player.y -= 5
    if keys[pygame.K_DOWN]:
        player.y += 5
        
    if pickaxe and player.colliderect(pickaxe):
        if keys[pygame.K_e]:
            has_pickaxe = True
            inventory["Pickaxe"] = 1
            pickaxe = None

    
    if has_pickaxe:
        for wood in woods:
            if player.colliderect(wood) and keys[pygame.K_SPACE]:
                blink_item(wood, wood_img)
                inventory["Wood"] += 1

    
    if has_pickaxe:
        for stone in stones:
            if player.colliderect(stone) and keys[pygame.K_SPACE]:
                blink_item(stone, stone_img)
                inventory["Stone"] += 1

    
    if keys[pygame.K_c]:
        inventory["Sword"] += 1
        print("⚔️ Ви створили меч!")

    
    if keys[pygame.K_i]:
        show_inventory = not show_inventory
        pygame.time.wait(200)

    
    if keys[pygame.K_1]:
        active_item = "Pickaxe"
    if keys[pygame.K_2]:
        active_item = "Wood"
    if keys[pygame.K_3]:
        active_item = "Stone"
    if keys[pygame.K_4]:
        active_item = "Sword"

    
    if player.colliderect(chest) and inventory["Wood"] >= 20 and inventory["Stone"] >= 10:
        print("Ви зібрали всі ресурси!")
        game_won = True
        portal_active = True
        if portal is None:
            portal = pygame.Rect(370, 520, 60, 60)  

    
    if portal_active and portal and player.colliderect(portal):
        print("Ви перейшли на наступний рівень!")
        running = False  

    
    if keys[pygame.K_F5]:
        save_game()
        pygame.time.wait(300)
    if keys[pygame.K_F9]:
        load_game()
        pygame.time.wait(300)

    screen.fill((255, 255, 255))

    screen.blit(chest_img, (chest.x, chest.y))
    if pickaxe:
        screen.blit(pickaxe_img, (pickaxe.x, pickaxe.y))
    for wood in woods:
        screen.blit(wood_img, (wood.x, wood.y))
    for stone in stones:
        screen.blit(stone_img, (stone.x, stone.y))
    screen.blit(player_img, (player.x, player.y))

    
    if portal_active and portal:
        screen.blit(portal_img, (portal.x, portal.y))

    font = pygame.font.Font(None, 36)
    text = font.render(f"Wood: {inventory['Wood']}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pickaxe_text = font.render(f"Pickaxe: {'Yes' if has_pickaxe else 'No'}", True, (0, 0, 0))
    screen.blit(pickaxe_text, (10, 50))

    stone_text = font.render(f"Stone: {inventory['Stone']}", True, (0, 0, 0))
    screen.blit(stone_text, (10, 90))
    sword_text = font.render(f"Sword: {inventory['Sword']}", True, (0, 0, 0))
    screen.blit(sword_text, (10, 130))

    
    if show_inventory:
        pygame.draw.rect(screen, (220, 220, 220), (200, 100, 400, 400))
        y = 150
        for item, count in inventory.items():
            item_text = font.render(f"{item}: {count}", True, (0, 0, 0))
            screen.blit(item_text, (250, y))
            y += 40
        active_text = font.render(f"Активний: {active_item}", True, (0, 0, 200))
        screen.blit(active_text, (250, 480))

    if game_won:
        win_text = font.render("Рівень завершено! Зайдіть у портал ↓", True, (0, 150, 0))
        screen.blit(win_text, (200, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
