# program template for Spaceship
import simplegui
import math
import random
import time

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

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
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH # use modular arithmetic for screen loops
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT  
        self.angle += self.angle_vel
    

    
# Ship class
class Ship:
    ANGLE_VEL_COEF = 0.03 # speed of changing direction
    THRUST_ACCELERATION_COEF = 0.1 # coef not to accelerate very fast
    FRICTION_COEF = 0.985 # need friction not to fly infinitely
    SHOOT_ACCELERATION_COEF = 5 # for missiles to go faster
    
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
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            self.image_center = ship_info.get_center()
 
    def shoot(self, is_shooting):
        global a_missile
        self.is_shooting = is_shooting
        if self.is_shooting:
            missile_pos = [self.pos[0] + self.radius * self.forward_vector[0], self.pos[1] + self.radius * self.forward_vector[1]]
            a_missile = Sprite([missile_pos[0], missile_pos[1]], 
                               [self.vel[0] + self.forward_vector[0] * self.SHOOT_ACCELERATION_COEF, self.vel[1] + self.forward_vector[1] * self.SHOOT_ACCELERATION_COEF], 
                               self.angle, 
                               self.angle_vel, 
                               missile_image, 
                               missile_info, 
                               missile_sound)
    
    def turn_right(self):
        self.angle_vel = self.ANGLE_VEL_COEF
        
    def turn_left(self):
        self.angle_vel = -self.ANGLE_VEL_COEF
        
    def stop_turning(self):
        self.angle_vel = 0
    
    def accelerate(self):
        self.thrust(True)
    
    def stop_accelerating(self):
        self.thrust(False)
    
    def start_shooting(self):
        self.shoot(True)

    def stop_shooting(self):
        self.shoot(False)
        

def draw(canvas):
    global time
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
    
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    if a_missile is not None:
        a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    if a_missile is not None:
        a_missile.update()
        
        
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, WIDTH, HEIGHT
    ANGLE_CAP = 628 # approximately 2 * math.pi (whole circle)
    ANGLE_VEL_CAP = 10
    DIVIDER = 100.0 # random get only int number
    MIN_VELOCITY = -2
    MAX_VELOCITY = 2
    VELOCITY_STEP = 1
    
    random_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    random_vel = [random.randrange(MIN_VELOCITY, MAX_VELOCITY, VELOCITY_STEP), random.randrange(MIN_VELOCITY, MAX_VELOCITY, VELOCITY_STEP)]
    random_angle = random.randrange(ANGLE_CAP) / DIVIDER
    random_angle_vel = random.randrange(ANGLE_VEL_CAP) / DIVIDER
    a_rock = Sprite(random_pos, random_vel, random_angle, random_angle_vel, asteroid_image, asteroid_info)

    
def key_down(key):
    global my_ship
    for i in key_downs:
        if key == simplegui.KEY_MAP[i]:
            key_downs[i]()

def key_up(key):
    for i in key_ups:
        if key == simplegui.KEY_MAP[i]:
            key_ups[i]()

            
# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_spawner()
a_missile = None


key_downs = {"up" : my_ship.accelerate,
             "left" : my_ship.turn_left,
             "right" : my_ship.turn_right,
             "space" : my_ship.start_shooting}

key_ups = {"up" : my_ship.stop_accelerating,
           "left" : my_ship.stop_turning,
           "right" : my_ship.stop_turning,
           "space" : my_ship.stop_shooting}


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
