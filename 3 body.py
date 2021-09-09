from vpython import *
from numba import jit
import numpy as np
import time
### Defining constants for ease of conversion
G = 6.67*10**(-11) # m^3/(kg*s^2)
AU = 1.496*10**11 # m

### Defining time intervals in seconds
HOUR = 3600 # s
DAY = 86400 # s
YEAR = 3.154*10**7 # s

on = True
running = True
time=0

scene.width = 1000
scene.height = 1000


### Planetary data importing
mercury_data = [0.39*AU, 48236, 3.3*10**23]
venus_data = [0.723*AU, 35008, 4.87*10**24]
earth_data = [AU, 29784, 5.98*10**24]
mars_data = [1.524*AU, 24134, 6.42*10**23]
jupiter_data = [5.203*AU, 13072, 1.90*10**27]
saturn_data = [9.539*AU, 9651, 5.69*10**26]
uranus_data = [19.18*AU, 6799, 8.68*10**25]
neptune_data = [30.06*AU, 5435, 1.02*10**26]

def angular_speed(mass, radius):
    # Defining a function to find the angular speed of something given mass 
    # and distance between objects.
    return np.sqrt(G*mass/r**3)

def find_speed(x,y,z):
    # Defining a function to find the speed of something given x,y and z 
    # velocities
    speed=float(( x**2 + y**2 + z**2)**0.5)
    return speed

def pause_play():
    # Defining a function to be used with a button in vpython to pause/play
    # the simulation as decided by the user.
    global running
    if running == True:
        running = False
    else: running = True


### Creating axis markers for reference
xaxis=cylinder(pos=vector(-2*AU,0,0), axis=vector(4*AU,0,0), radius=0.01*AU)
yaxis=cylinder(pos=vector(0,-2*AU,0), axis=vector(0,4*AU,0), radius=xaxis.radius)
zaxis=cylinder(pos=vector(0,0,-2*AU), axis=vector(0,0,4*AU), radius=xaxis.radius)
scene.background = color.black
[distant_light(direction=vector( 0.22,  0.44,  0.88), color=color.gray(0.8)),
 distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.gray(0.3))]
local_light(pos=vector(0,0,0), color=color.yellow)
scene.range=100*AU

scene.width = 1000
      
MASS= 1.988*10**(30) # kg, 1 solar mass
MASS_POS = np.array([0,0,0])

def force_grav(mass_1, pos_1, mass_2, pos_2):
    # Calculating a vector force on an object due to the graviational force of
    # another object
    distance = np.sqrt((pos_1.x-pos_2.x)**2 + (pos_1.y-pos_2.y)**2 + 
                       (pos_1.z-pos_2.z)**2)

    force = -G*mass_1*mass_2/(distance)**2
    force_vector = np.array([force*((pos_1.x-pos_2.x)/distance), 
                             force*((pos_1.y-pos_2.y)/distance), 
                             force*((pos_1.z-pos_2.z)/distance)])

    return force_vector

def off():
    # Function corresponding to the stop button, which allows the user to stop
    # the simulation.
    global on
    on = False

def pos_change(a, v, pos, ):
    # Function used to numerically calculate the change in position and velocity
    # due to the forces acting upon it.
    v.x = v.x + step*a[0]
    pos.x = pos.x + step * v.x
    v.y = v.y + step*a[1]
    pos.y = pos.y + step * v.y
    v.z = v.z + step*a[2]
    pos.z = pos.z + step * v.z     
    
    return v, pos

### Defining the speeds, positions and visual sizes of the stars
star_1 = sphere(pos=vector(80*AU,20*AU,5*AU), radius=2*AU, color=color.yellow)
star_1.velocity = vector(0,-13500,0)
star_2 = sphere(pos=vector(100*AU,32*AU,16*AU), radius=2*AU, color=color.yellow)
star_2.velocity = vector(0,27000,0)
star_3 = sphere(pos=vector(0,0,0), radius=2*AU, color=color.yellow)
star_3.velocity = vector(10000,10000,0)


### Defining the mass of each star
mass_1 = 72*MASS
mass_2 = 64*MASS
mass_3 = 20*MASS


graph(width=400, height=250)
xDots = gdots(color=color.green)
yDots = gdots(color=color.magenta)
zDots = gdots(color=color.red)

def focus1():
    scene.center=star_1.pos
def focus2():
    scene.center=star_2.pos
def focus3():
    scene.center=star_3.pos



button(text="Pause/Play", bind=pause_play)
button(text="Stop", bind=off)
scene.append_to_caption("\n\n")
button(text="Focus on Object 1", bind=focus1)
button(text="Focus on Object 2", bind=focus2)
button(text="Focus on Object 3", bind=focus3)

def adjust_mass_1():
    # Function associated with a slider to be used by the user to change the
    # value of star 1's mass mid or pre simulation.
    global mass_1
    mass_1 = 72*MASS + massSlider.value*10*MASS
    star_1.radius = star_2.radius*(massSlider.value)/45

massSlider = slider(left=10, min=0, max=90, step=1, value=45,
bind=adjust_mass_1)

time=0
    

### While loop used to run the simulation, and pause/play and stop as per user 
### input.
while on == True:
    while running == True:
        rate(500)
        step = DAY
    
        a_1 = (force_grav(mass_1, star_1.pos, mass_2, star_2.pos) + force_grav(
                mass_1, star_1.pos, mass_3, star_3.pos))/mass_1
        star_1.velocity, star_1.pos = pos_change(a_1, star_1.velocity, 
                                                 star_1.pos)
        a_2 = (force_grav(mass_2, star_2.pos, mass_1, star_1.pos) + force_grav(
                mass_2, star_2.pos, mass_3, star_3.pos))/mass_2
        star_2.velocity, star_2.pos = pos_change(a_2, star_2.velocity, 
                                                 star_2.pos)
        a_3 = (force_grav(mass_3, star_3.pos, mass_2, star_2.pos) + force_grav(
                mass_3, star_3.pos, mass_1, star_1.pos))/mass_3
        star_3.velocity, star_3.pos = pos_change(a_3, star_3.velocity, 
                                                 star_3.pos)
        speed_1 = find_speed(star_1.velocity.x, star_1.velocity.y, 
                             star_1.velocity.z)
        speed_2 = find_speed(star_2.velocity.x, star_2.velocity.y, 
                             star_2.velocity.z)
        speed_3 = find_speed(star_3.velocity.x, star_3.velocity.y, 
                             star_3.velocity.z)
        
        
        time+=1

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    