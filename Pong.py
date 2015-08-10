# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [0, 0]
ball_vel = [0, 0]

paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0


def spawn_ball(direction):
    """ 
        initialize ball_pos and ball_vel for new bal in middle of table
        if direction is RIGHT, the ball's velocity is upper right, else upper left
    """
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [HALF_WIDTH, HALF_HEIGHT]
    # make direction of the ball random
    vert_vel = random.randrange(-2, -1)
    hor_vel = random.randrange(1, 6)
    
    if direction == LEFT:
        hor_vel = - hor_vel
    
    ball_vel = [hor_vel, vert_vel]
    
def new_game():
    """
        reset all counters and start new game
    """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = HALF_HEIGHT
    paddle2_pos = HALF_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    
    # 50% chance of start the game with ball moving right or moving left
    if random.randrange(0, 2) > 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
        
def get_paddle1_coordinates():
    """
    update left paddle and get its coordinates
    """
    
    global paddle1_pos, paddle1_vel
    
    left_upper = [0, paddle1_pos - HALF_PAD_HEIGHT]
    right_upper = [PAD_WIDTH-1, paddle1_pos - HALF_PAD_HEIGHT]
    right_bottom = [PAD_WIDTH-1, paddle1_pos + HALF_PAD_HEIGHT]
    left_bottom = [0, paddle1_pos + HALF_PAD_HEIGHT]
    
    #hold paddle on the screen
    next_pos = paddle1_pos + paddle1_vel
    bottom_point = HALF_PAD_HEIGHT
    top_point = HEIGHT - HALF_PAD_HEIGHT
    
    if bottom_point <= next_pos <= top_point:
        paddle1_pos += paddle1_vel
    
    return [left_upper, right_upper, right_bottom, left_bottom]

def get_paddle2_coordinates():
    """
    update right paddle and get its coordinates
    """
    
    global paddle2_pos, paddle2_vel
    
    left_upper = [WIDTH - PAD_WIDTH + 1, paddle2_pos - HALF_PAD_HEIGHT]
    right_upper = [WIDTH, paddle2_pos - HALF_PAD_HEIGHT]
    right_bottom = [WIDTH, paddle2_pos + HALF_PAD_HEIGHT]
    left_bottom = [WIDTH - PAD_WIDTH + 1, paddle2_pos + HALF_PAD_HEIGHT]
    
    #hold paddle on the screen
    next_pos = paddle2_pos + paddle2_vel
    bottom_point = HALF_PAD_HEIGHT
    top_point = HEIGHT - HALF_PAD_HEIGHT
    
    if bottom_point <= next_pos <= top_point:
        paddle2_pos += paddle2_vel
        
    return [left_upper, right_upper, right_bottom, left_bottom]

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #hold ball inside vertical bounds
    top_point = HEIGHT - BALL_RADIUS
    bottom_point = BALL_RADIUS
    if (top_point < ball_pos[1] or ball_pos[1] < bottom_point):
        ball_vel[1] = - ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # draw paddles
    canvas.draw_polygon(get_paddle1_coordinates(), 1, 'White', 'White')
    canvas.draw_polygon(get_paddle2_coordinates(), 1, 'White', 'White')
    
    # determine whether paddle and ball collide
    left_point = PAD_WIDTH + BALL_RADIUS
    right_point = WIDTH - BALL_RADIUS - PAD_WIDTH 
    ball_collide_right_paddle = paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT
    ball_collide_left_paddle = paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT
    
    if (ball_pos[0] > right_point):
        if (ball_collide_right_paddle):
            ball_vel[0] = - ball_vel[0]*1.1
        else:
            spawn_ball(LEFT)
            score1 += 1
    elif (ball_pos[0] < left_point):
        if (ball_collide_left_paddle):
            ball_vel[0] = - ball_vel[0]*1.1
        else:
            spawn_ball(RIGHT)
            score2 += 1
    
    # draw scores
    canvas.draw_text(str(score1), [200,50], 35, 'white')
    canvas.draw_text(str(score2), [383,50], 35, 'white')
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5    
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0   
        
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button('Restart', new_game)
frame.add_label('',100)
frame.add_label('player1 controls:',200)
frame.add_label('w - move paddle up:',200)
frame.add_label('s - move paddle down:',200)
frame.add_label('',100)
frame.add_label('player2 controls:',200)
frame.add_label('up - move paddle up:',200)
frame.add_label('down - move paddle down:',200)

# start frame
new_game()
frame.start()
