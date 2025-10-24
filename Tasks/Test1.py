import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Збір предметів та інвентар")

player = pygame.Rect(100, 100, 50, 50)
chest = pygame.Rect(400, 300, 50, 50)
chest_opened = False
items_collected = 0
items = [pygame.Rect(200, 150, 30, 30), pygame.Rect(600, 400, 30, 30)]
inventory = []

clock = pygame.time.Clock()

running = True
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

    if keys[pygame.K_SPACE]:
        if player.colliderect(chest) and not chest_opened:
            chest_opened = True

    for item in items[:]:
        if player.colliderect(item):
            items.remove(item)
            items_collected += 1
            inventory.append("Item")

    if keys[pygame.K_u]:
        if inventory:
            used_item = inventory.pop(0)
            print(f"Used: {used_item}")

    if keys[pygame.K_d]:
        if inventory:
            dropped_item = inventory.pop()
            print(f"Dropped: {dropped_item}")

    screen.fill((255, 255, 255))

    if chest_opened:
        pygame.draw.rect(screen, (0, 255, 0), chest)
        chest_opened = False
    else:
        pygame.draw.rect(screen, (139, 69, 19), chest)

    for item in items:
        pygame.draw.rect(screen, (255, 215, 0), item)

    pygame.draw.rect(screen, (0, 128, 255), player)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Items Collected: {items_collected}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    inventory_text = font.render(f"Inventory: {', '.join(inventory)}", True, (0, 0, 0))
    screen.blit(inventory_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
