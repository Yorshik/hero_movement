import pygame


class Box(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        self.image = pygame.image.load('data/box.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = 'box'


class Grass(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        self.image = pygame.image.load('data/grass.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = 'grass'


class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('data/mar.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.name = 'mario'


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def move_sprites(*groups, x, y):
    for group in groups:
        for sp in group.sprites():
            sp.rect.y += y
            sp.rect.x += x


if __name__ == '__main__':
    screen = pygame.display.set_mode((500, 500))
    all_spites = pygame.sprite.Group()
    grasses = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    try:
        with open(f'data/levels/{input("Имя файла с уровнем: ")}') as level:
            data = level.read().split('\n')
            print(data)
    except FileNotFoundError:
        print('no such file')
        quit()
    for i, line in enumerate(data):
        for j, element in enumerate(line):
            if element == 'g':
                grass = Grass(all_spites, grasses, x=i * 50, y=j * 50)
            elif element == 'b':
                box = Box(all_spites, boxes, x=i * 50, y=j * 50)
    mario = Player(all_spites)
    print_fg = False
    fg = pygame.transform.scale(pygame.image.load('data/fon.jpg'), (500, 500))
    game = True
    clock = pygame.time.Clock()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print_fg = not print_fg
                elif event.key == pygame.K_LEFT:
                    for sprite in all_spites:
                        if (sprite.name == 'grass' and mario.rect.y == sprite.rect.y and
                                sprite.rect.x + 50 == mario.rect.x and not print_fg):
                            move_sprites(boxes, grasses, x=50, y=0)
                            break
                elif event.key == pygame.K_RIGHT:
                    for sprite in all_spites:
                        if (sprite.name == 'grass' and mario.rect.y == sprite.rect.y and
                                sprite.rect.x - 50 == mario.rect.x and not print_fg):
                            move_sprites(boxes, grasses, x=-50, y=0)
                            break
                elif event.key == pygame.K_UP:
                    for sprite in all_spites:
                        if (sprite.name == 'grass' and mario.rect.x == sprite.rect.x and
                                sprite.rect.y + 50 == mario.rect.y and not print_fg):
                            move_sprites(boxes, grasses, x=0, y=50)
                            break
                elif event.key == pygame.K_DOWN:
                    for sprite in all_spites:
                        if (sprite.name == 'grass' and mario.rect.x == sprite.rect.x and
                                sprite.rect.y - 50 == mario.rect.y and not print_fg):
                            move_sprites(boxes, grasses, x=0, y=-50)
                            break
        if mario.rect.x > 500:
            mario.rect.x = 450
        elif mario.rect.x < 0:
            mario.rect.x = 0
        elif mario.rect.y > 500:
            mario.rect.y = 450
        elif mario.rect.y < 0:
            mario.rect.y = 0
        screen.fill((0, 0, 0))
        if print_fg:
            screen.blit(fg, (0, 0))
        else:
            all_spites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
