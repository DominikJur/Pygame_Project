import pygame
from pygame import mixer


class Player(pygame.sprite.Sprite):
    def __init__(self, scale: int, user_x: int, user_y: int):
        super(Player, self).__init__()
        self.scale = scale
        self.user_x = user_x
        self.user_y = user_y
        self.image_0: pygame.Surface = pygame.image.load(
            "graphics/sprite_0.png"
        ).convert_alpha()
        self.image_0 = pygame.transform.rotozoom(self.image_0, 0, scale)
        self.image_0 = pygame.transform.flip(self.image_0, True, False)
        self.image_1: pygame.Surface = pygame.image.load(
            "graphics/sprite_1.png"
        ).convert_alpha()
        self.image_1 = pygame.transform.rotozoom(self.image_1, 0, scale)
        self.image_1 = pygame.transform.flip(self.image_1, True, False)
        self.image_dead: pygame.Surface = pygame.image.load(
            "graphics/sprite_2.png"
        ).convert_alpha()
        self.image_dead = pygame.transform.rotozoom(self.image_dead, 0, scale)
        self.image_dead = pygame.transform.flip(self.image_dead, True, False)
        self.collision_sound = mixer.Sound("aduio\wall_collision.mp3")
        self.death_sound = mixer.Sound("aduio\game_over.mp3")
        self.jump_sound = mixer.Sound("aduio\jump.mp3")
        self.images = [self.image_0, self.image_1, self.image_dead]
        self.image = self.image_0
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = (user_x - self.rect.width) // 2
        self.rect.y = (user_y - self.rect.height) // 2
        self.dead: bool = False
        self.index: int = 0
        self.gravity: int = 1 * scale
        self.velocity: int = 4 * scale
        self.cooldown_count: int = 0

    def hide(self) -> None:
        self.rect.x = -1000 * self.scale
        self.rect.y = -1000 * self.scale

    def defult_pos(self) -> None:
        self.rect.x = (self.user_x - self.rect.width) // 2
        self.rect.y = (self.user_y - self.rect.height) // 2
        if self.velocity < 0:
            self.flip()
        self.velocity = 4 * self.scale
        self.gravity = 0

    def start_screen_animation(self) -> None:
        self.index += 0.05
        x, y = self.rect.x, self.rect.y
        self.image = self.images[(int(self.index) % 2)]
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect.x, self.rect.y = x, y

    def update(self) -> None:

        if not self.dead:
            self.rect.x += self.velocity
            self.gravity += 1
            self.rect.y += self.gravity
            if self.cooldown_count < 10:
                self.image = self.image_1
            else:
                self.image = self.image_0
            self.cooldown_count += 1

    def check_wall_collision(self) -> int:
        if self.rect.left <= 0:
            self.rect.left = 0
            return 1
        elif self.rect.right >= self.user_x:
            self.rect.right = self.user_x
            return -1
        return 0

    def after_collision(self) -> None:
        self.collision_sound.play()
        self.flip()
        self.velocity *= -1

    def jump(self) -> None:
        if not self.dead:
            self.jump_sound.play()
            self.cooldown_count = 0
            x, y = self.rect.x, self.rect.y
            self.gravity = -10
            self.image = self.image_1
            self.rect = pygame.Surface.get_rect(self.image)
            self.rect.x, self.rect.y = x, y

    def flip(self) -> None:
        x, y = self.rect.x, self.rect.y
        index = self.images.index(self.image)
        self.image_0, self.image_1, self.image_dead = (
            pygame.transform.flip(image, True, False) for image in self.images
        )
        self.images = [self.image_0, self.image_1, self.image_dead]
        self.image = self.images[index]
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect.x, self.rect.y = x, y

    def death(self) -> None:
        self.dead = True
        self.death_sound.play()
        self.image = self.image_dead
