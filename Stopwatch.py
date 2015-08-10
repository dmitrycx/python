# template for "Stopwatch: The Game"
import simplegui

# define global variables
time_in_tenths = 0
attemts = 0
successful_attemts = 0

#define some consts here
tenths_of_sec_in_sec = 10
sec_in_min = 60


def format(t):
    """
    helper function that converts time
    in tenths of seconds into formatted string A:BC.D
    """
    sec_fractional = t % tenths_of_sec_in_sec # D - fractional part of a second.
    sec_integer = t / tenths_of_sec_in_sec # store our seconds without tenths here
    
    sec = sec_integer % sec_in_min # BC
    
    # no str.format() on codesculptor for some reason, so need to do it by hands
    # add 0 if seconds is one digit number
    str_sec = str(sec)
    if(len(str_sec) < 2):
        str_sec = "0" + str_sec
    
    min_integer = sec_integer / sec_in_min # A - get our minutes here
    
    # return string in A:BC.D format
    return str(min_integer) + ":" + str_sec + "." + str(sec_fractional)


def update_attemts():
    global attemts, successful_attemts
    if (timer.is_running()):
        attemts += 1
    
        if (time_in_tenths % tenths_of_sec_in_sec == 0):
            successful_attemts += 1
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    update_attemts()
    timer.stop()
    

def reset():
    global time_in_tenths, attemts, successful_attemts
    time_in_tenths = 0
    attemts = 0
    successful_attemts = 0
    
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time_in_tenths
    time_in_tenths += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time_in_tenths), [120,100], 35, "White")
    str_attemt = str(successful_attemts) + "/" + str(attemts)
    canvas.draw_text(str_attemt, [260, 20], 25, "green")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# register event handlers
frame.add_button("start", start, 200)
frame.add_button("stop", stop, 200)
frame.add_button("reset", reset, 200)

frame.set_draw_handler(draw_handler)

timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()

