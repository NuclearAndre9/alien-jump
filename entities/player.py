import pygame.locals
import pygame as pg
import colors as cs
from global_variables import *

WIDTH, HEIGHT = (TILE_SIZE / 2, TILE_SIZE / 2)
DZ_WIDTH, DZ_HEIGHT = (WIDTH + TILE_SIZE, HEIGHT + TILE_SIZE)
LENGTH_SHIFT = 2
HORIZONTAL, VERTICAL = 0, 1

MAX_SPEED = {
    "horizontal": 5,
    "jumping": 15,
    "falling": 10
}

DETECTION_SIZES = [
    (MAX_SPEED["horizontal"], HEIGHT - LENGTH_SHIFT),
    (MAX_SPEED["horizontal"], HEIGHT - LENGTH_SHIFT),
    (WIDTH - LENGTH_SHIFT, MAX_SPEED["jumping"]),
    (WIDTH - LENGTH_SHIFT, MAX_SPEED["falling"]),
]

collisions = sides.copy()
collision_distance = sides_float.copy()

detected_collisions = sides.copy()
detected_distance = sides_float.copy()

fall_enable = True


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_alive = True
        self.image = pg.image.load("sprites/standing.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (WIDTH, HEIGHT))
        # self.image = pg.Surface([WIDTH, HEIGHT])
        # self.image.fill(cs.BLACK)
        # self.image_shift = ()

        self.rect = pg.rect.Rect(((SCREENWIDTH - WIDTH) / 2, (SCREENHEIGTH - HEIGHT) / 2), self.image.get_size())

        self.detection_zones = []
        self.dt_zones_images = []

        self.create_detection_zones()

        self.is_jumping = False
        self.start_jump = False
        self.is_falling = False
        self.is_colliding = False
        self.terminal_velocity = 200
        self.position = [0, 0]
        self.velocity = [MAX_SPEED["horizontal"], 0]

    def update_movement(self):
        self.position[HORIZONTAL] = self.velocity[HORIZONTAL]
        self.rect.move_ip(self.position[HORIZONTAL], self.position[VERTICAL])
        for zone in self.detection_zones:
            zone.rect.move_ip(self.position[HORIZONTAL], self.position[VERTICAL])
        self.velocity[HORIZONTAL] = 0

    def update(self):
        if visible_collisions:
            for tile in level:
                tile.image.fill(cs.GREEN)

        pressed_keys = pg.key.get_pressed()
        self.detect_tiles()
        self.move(pressed_keys)
        self.update_movement()
        self.colliding()

    # movement
    def move(self, keys: pg.key.ScancodeWrapper):
        global fall_enable
        self.position = [0, 0]

        # Horizontal movement
        if keys[pygame.locals.K_a] and self.rect.left >= LEFT_SIDE and not collisions["left"]:
            self.move_horizontal("left")
        if keys[pygame.locals.K_d] and self.rect.right <= RIGHT_SIDE and not collisions["right"]:
            self.move_horizontal("right")

        # vertical movement
        self.check_if_falling()

        if self.is_falling and fall_enable:
            self.fall()
        else:
            self.control_jump(keys[pygame.locals.K_SPACE])

        # if keys[pygame.locals.K_w]:
        #     self.position[VERTICAL] = -5

        # if keys[pygame.locals.K_s]:
        #     self.position[VERTICAL] = 5

        if keys[pygame.locals.K_q]:
            fall_enable = not fall_enable
        # self.movement_debug()

    def move_horizontal(self, direction):
        if direction == "left":
            self.velocity[HORIZONTAL] = -MAX_SPEED["horizontal"]
            self.correct_movement(LEFT, HORIZONTAL)
        else:
            self.velocity[HORIZONTAL] = +MAX_SPEED["horizontal"]
            self.correct_movement(RIGHT, HORIZONTAL)

    def correct_movement(self, collision_side, orientation):
        distance = detected_distance[collision_side]
        velocity = self.velocity[orientation]
        # if collision_side == LEFT and detected_collisions[collision_side]:
        #     print(f"\n{collision_side} = {self.velocity[orientation]}")
        #     print(f"distance: {distance} velocity: {velocity}")

        if not detected_collisions[collision_side]:
            self.position[orientation] = self.velocity[orientation]
            return

        if collision_side == BOTTOM and distance < velocity:
            self.velocity[orientation] = detected_distance[collision_side] + 1

        if collision_side == TOP and distance < abs(velocity):
            self.velocity[orientation] = -detected_distance[collision_side] - 1

        if collision_side == LEFT and distance < abs(velocity):
            self.velocity[orientation] = -detected_distance[collision_side] - 1

        if collision_side == RIGHT and distance < abs(velocity):
            self.velocity[orientation] = detected_distance[collision_side] + 1

        self.position[orientation] = self.velocity[orientation]

    def movement_debug(self):
        print(f"falling: {self.is_falling}")
        print(f"jumping: {self.is_jumping}")
        print(f"start jump: {self.start_jump}")
        print(f"colliding: {self.is_colliding}")
        print()
        pass

    def control_jump(self, space_pressed):
        if self.is_jumping:
            self.jump()
        else:
            if space_pressed:
                self.is_jumping = True
                self.start_jump = True

    def jump(self):
        if self.start_jump:
            self.velocity[VERTICAL] = -MAX_SPEED["jumping"]
            self.start_jump = False
        else:
            self.velocity[VERTICAL] += GRAVITY

        self.position[VERTICAL] = self.velocity[VERTICAL]

        self.correct_movement(TOP, VERTICAL)

        if self.velocity[VERTICAL] >= 0:
            self.velocity[VERTICAL] = 0
            self.is_jumping = False

    def fall(self):
        # self.velocity[VERTICAL] = GRAVITY
        self.velocity[VERTICAL] += GRAVITY
        if self.velocity[VERTICAL] >= MAX_SPEED["falling"]:
            self.velocity[VERTICAL] = MAX_SPEED["falling"]

        self.correct_movement(BOTTOM, VERTICAL)
        # print(f"distance: {detected_distance} velocity: {self.velocity[VERTICAL]}")

    def check_if_falling(self):
        if not collisions["bottom"] and not self.is_jumping:
            self.is_falling = True
            return
        self.is_falling = False

    # collision
    def create_detection_zones(self):
        for dimensions in DETECTION_SIZES:
            zone = pg.sprite.Sprite()
            zone.image = pg.Surface(dimensions)
            zone.image.fill(cs.BLACK)
            zone.image.set_alpha(120)
            zone.rect = zone.image.get_rect()
            zone.rect.center = self.rect.center
            self.detection_zones.append(zone)

        self.detection_zones[0].rect.right = self.rect.left
        self.detection_zones[1].rect.left = self.rect.right
        self.detection_zones[2].rect.bottom = self.rect.top
        self.detection_zones[3].rect.top = self.rect.bottom

    def detect_tiles(self):
        # poner todas las colisiones en false
        detected_collisions.update((side, False) for side in detected_collisions)

        self.detect_tile(0, "left")
        self.detect_tile(1, "right")
        self.detect_tile(2, "top")
        self.detect_tile(3, "bottom")

    def detect_tile(self, side_number, side_name):
        detected_tiles = pg.sprite.spritecollide(self.detection_zones[side_number], level, False)
        if not detected_tiles:
            return

        for tile in detected_tiles:
            tile_pos, player_pos, tile_detected = self.get_side_position(tile, side_name)
            if tile_detected:
                if visible_collisions:
                    tile.image.fill(cs.BLUE)
                detected_distance[side_name] = abs(tile_pos - player_pos)
                detected_collisions[side_name] = True
                # print(f"{side_name}: {detected_collisions[side_name]}: {detected_distance[side_name]}")

    def get_side_position(self, tile, side):
        if side == LEFT:
            return tile.rect.right, self.rect.left, tile.rect.right >= self.detection_zones[0].rect.left
        if side == RIGHT:
            return tile.rect.left, self.rect.right, tile.rect.left <= self.detection_zones[1].rect.right
        if side == TOP:
            return tile.rect.bottom, self.rect.top, tile.rect.bottom >= self.detection_zones[2].rect.top
        if side == BOTTOM:
            return tile.rect.top, self.rect.bottom, tile.rect.top <= self.detection_zones[3].rect.bottom

    def colliding(self):
        # LAS COORDENADAS VAN DE ARRIBA HACIA ABAJO
        # poner todas las colisiones en false
        collisions.update((side, False) for side in collisions)

        collision_tiles = pg.sprite.spritecollide(self, level, False)
        if not collision_tiles:
            return

        for tile in collision_tiles:
            if visible_collisions:
                tile.image.fill(cs.RED)
            collision_distance["left"] = abs(tile.rect.right - self.rect.left)
            collision_distance["right"] = abs(tile.rect.left - self.rect.right)
            collision_distance["top"] = abs(tile.rect.bottom - self.rect.top)
            collision_distance["bottom"] = abs(tile.rect.top - self.rect.bottom)

            if collision_distance["left"] <= 1 and detected_collisions["left"]:
                collisions["left"] = True
            if collision_distance["right"] <= 1 and detected_collisions["right"]:
                collisions["right"] = True
            if collision_distance["top"] <= 1 and detected_collisions["top"]:
                collisions["top"] = True
            if collision_distance["bottom"] <= 1 and detected_collisions["bottom"]:
                collisions["bottom"] = True

        # not used

    def create_inflated_rect(self):
        self.rect = self.image.get_rect()
        self.rect.center = ((SCREENWIDTH - WIDTH) / 2, (SCREENHEIGTH - HEIGHT) / 2)
        image_size = self.rect.size
        self.rect.inflate_ip((2, 2))
        rect_size = self.rect.size
        self.image_shift = ((rect_size[0] - image_size[0]) / 2, (rect_size[1] - image_size[1]) / 2)
        # print(f"shift = {self.image_shift}")

    def kill(self):
        self.is_alive = False

    # rendering
    def draw(self, surface: pg.Surface):
        if visible_collisions:
            for zone in self.detection_zones:
                surface.blit(zone.image, zone.rect)

        # surface.blit(self.rect_image, self.rect)
        # position = (self.rect.topleft[0]+self.image_shift[0],self.rect.topleft[1]+self.image_shift[1])
        surface.blit(self.image, self.rect)
