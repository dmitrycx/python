# program template for Spaceship
import simplegui
import math
import random
import time

#consts
WIDTH = 800
HEIGHT = 600
INITIAL_SCORE = 0
INITIAL_LIVES = 3

# globals for user interface
score = INITIAL_SCORE
lives = INITIAL_LIVES
time = 0
started = False


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# IMAGES & SOUNDS 
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_info_thrust = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


def process_sprite_group(group, canvas):
    group_copy = group.copy()
    for item in group_copy:
        item.update()
        if item.is_alive():
            item.draw(canvas)
        else:            
            group.remove(item)

            
def group_collide(group, object):
    group_copy = group.copy() # avoid removing while iterating
    is_collided = False
    
    for item in group_copy:
        if item.collide(object):
            # add explosion insted of object that was collided
            explosion = Sprite(object.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            group.remove(item)
            is_collided = True

    return is_collided        


def group_group_collide(group1, group2):
    group1_copy = group1.copy()
    count_collided = 0
    
    for item in group1_copy:
        if group_collide(group2, item):
            group1.discard(item)
            count_collided += 1
            
    return count_collided
    

def clear_data(canvas):
    global rock_group
    while len(rock_group) > 0:
        rock_group.pop()

    soundtrack.pause()
    canvas.draw_image(splash_image, splash_info.get_center(), 
                    splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                    splash_info.get_size())        
        
        
def init_data():
    global score, lives
    soundtrack.rewind()
    soundtrack.play()
    score = INITIAL_SCORE
    lives = INITIAL_LIVES
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.alive = True
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            # with each update move center to the next image in tiled image
            #change only X coord, because Y remains the same
            initial_center_x = self.image_size[0] / 2
            self.image_center[0] = initial_center_x + ((self.image_size[0]) * self.age)
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH # use modular arithmetic for screen loops
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT  
        self.angle += self.angle_vel
        self.age += 1
        
        if self.age >= self.lifespan:
            self.alive = False
            self.age = 0
            
    def is_alive(self):
        return self.alive
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, object):
        return dist(self.pos, object.pos) <= (self.radius + object.radius)

    
# Ship class
class Ship:
    ANGLE_VEL_COEF = 0.05 # speed of changing direction
    THRUST_ACCELERATION_COEF = 0.1 # coef not to accelerate very fast
    FRICTION_COEF = 0.99 # need friction not to fly infinitely
    SHOOT_ACCELERATION_COEF = 6 # for missiles to go faster
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.is_thrust = False
        self.is_shooting = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH # use modular arithmetic for screen loops
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.forward_vector = angle_to_vector(self.angle)
        # if thrusting - moving to the direction of ship front
        if self.is_thrust:
            self.vel[0] += self.forward_vector[0] * self.THRUST_ACCELERATION_COEF
            self.vel[1] += self.forward_vector[1] * self.THRUST_ACCELERATION_COEF
        #add friction to stop ship in time and cap the speed            
        self.vel[0] *= self.FRICTION_COEF
        self.vel[1] *= self.FRICTION_COEF
        
    def thrust(self, is_thrust):
        self.is_thrust = is_thrust
        if self.is_thrust:
            self.image_center = ship_info_thrust.get_center()
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            self.image_center = ship_info.get_center()
 
    def shoot(self, is_shooting):
        self.is_shooting = is_shooting
        if started and is_shooting:
            missile_pos = [self.pos[0] + self.radius * self.forward_vector[0], self.pos[1] + self.radius * self.forward_vector[1]]
            missile = Sprite([missile_pos[0], missile_pos[1]], 
                            [self.vel[0] + self.forward_vector[0] * self.SHOOT_ACCELERATION_COEF, self.vel[1] + self.forward_vector[1] * self.SHOOT_ACCELERATION_COEF], 
                            self.angle, 
                            self.angle_vel, 
                            missile_image, 
                            missile_info, 
                            missile_sound)
        
            missile_group.add(missile)
    
    def turn_right(self):
        self.angle_vel += self.ANGLE_VEL_COEF
        
    def turn_left(self):
        self.angle_vel -= self.ANGLE_VEL_COEF

    def accelerate(self):
        self.thrust(True)
    
    def stop_accelerating(self):
        self.thrust(False)
    
    def start_shooting(self):
        self.shoot(True)

    def stop_shooting(self):
        self.shoot(False)

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius        

    def get_pos(self):
        return self.pos
    

def draw(canvas):
    global time, started, lives, score
    FONT_SIZE = 25
    FONT_COLOR = 'White'
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw score and lives
    canvas.draw_text('Lives', [20,20], FONT_SIZE, FONT_COLOR)
    canvas.draw_text(str(lives), [20,45], FONT_SIZE, FONT_COLOR)
    
    canvas.draw_text('Score', [720,20], FONT_SIZE, FONT_COLOR)
    canvas.draw_text(str(score), [720,45], FONT_SIZE, FONT_COLOR)
    
    # draw ship
    my_ship.draw(canvas)
    my_ship.update()
    
    # process all sprites
    process_sprite_group(missile_group, canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    score += group_group_collide(rock_group, missile_group)

    if not started:
        clear_data(canvas)
    
    if lives == 0:
        clear_data(canvas)
        started = False
        
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, WIDTH, HEIGHT, my_ship, score
    ROCK_MAX_AMOUNT = 12
    distance_coef = 1.5
    
    if started and len(rock_group) < ROCK_MAX_AMOUNT:
        ANGLE_CAP = 628 # approximately 2 * math.pi (whole circle)
        ANGLE_VEL_CAP = 3
        DIVIDER = 100.0 # random get only int number
        
        # improve difficulty
        difficulty_coef = score / 5
        
        vel_lower_band = -2 - difficulty_coef
        vel_higher_band = 2 + difficulty_coef
        
    
        random_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        
        # spawn a rock only if its not close to the ship
        if dist(my_ship.get_pos(), random_pos) > ((my_ship.get_radius() + asteroid_info.get_radius()) * distance_coef):
            random_vel = [random.randrange(vel_lower_band, vel_higher_band), random.randrange(vel_lower_band, vel_higher_band)]
            random_angle = random.randrange(ANGLE_CAP) / DIVIDER
            random_angle_vel = random.randrange(ANGLE_VEL_CAP) / DIVIDER
            rock = Sprite(random_pos, random_vel, random_angle, random_angle_vel, asteroid_image, asteroid_info)
            rock_group.add(rock)

    
def key_down(key):
    global my_ship
    for i in key_downs:
        if key == simplegui.KEY_MAP[i]:
            key_downs[i]()

            
def key_up(key):
    for i in key_ups:
        if key == simplegui.KEY_MAP[i]:
            key_ups[i]()

            
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        init_data()
        
        
# initialize
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

explosion_group = set()
missile_group = set()
rock_group = set()
rock_spawner()


# key enums
key_downs = {"up" : my_ship.accelerate,
             "left" : my_ship.turn_left,
             "right" : my_ship.turn_right,
             "space" : my_ship.start_shooting}


key_ups = {"up" : my_ship.stop_accelerating,
           "left" : my_ship.turn_right,
           "right" : my_ship.turn_left,
           "space" : my_ship.stop_shooting}


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
