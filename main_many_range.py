
# Rafay Nawaid Alvi: 13.04.2024

""" 
Program inspired by the DES (Discrete Event Simulation) approach (in contract to continuous simulations that uses time_stepping)

# Move with Reflection: 
A line with a given starting position (px,py) and slope is drawn in a finite world. Collision on the walls will result in the change of slope of the line.
examples:
1) [+m,+vy] -> wall(x=10) => [-m,+vy]
A line with a positive gradient (+m) moving in the +vy direction -> hits the wall defined by x=10 => results in a line with a negative gradient(-m) and direction (-vy)

2) [+m,+vy] -> wall(y=10) => [-m,-vy]
A line with a positive gradient (+m) moving in the +vy direction -> hits the wall defined by y=10 => results in a line with a negative gradient(-m) and direction (-vy)

3) [+m,-vy] -> wall(x=0) => [-m,-vy]
A line with a positive gradient (+m) moving in the +vy direction -> hits the wall defined by  x=0 => results in a line with a positive gradient(-m) and direction (-vy)

4) [+m,-vy] -> wall(y=0) => [-m,+vy]
A line with a positive gradient (+m) moving in the +vy direction -> hits the wall defined by  x=0 => results in a line with a positive gradient(-m) and direction (-vy)

Function Explanation:

def plot_fractal() ::: lines and their reflections are plotted from a given starting position (px,py) and a range of slopes [vi,vf]

"""

"""
Changes to make: [DONE]
# Make smaller functions for single (or few) lines that animates each collision
def animate_line() ::: single lines reflections, given starting position (x,y), slope (vi,vf), number of collisions (range)
def animate_lines() :::
# Separate plot the functions, make the above functions return data for generated plots, but not plt.show() them.
create_plot() ::: 
create_video() ::: 
"""

"""
Overhaul notes: [DONE]
# create particle
p = Particle(px,py,vx,vy)

# or create a list of particles:
vel = create_vel_directions(1,b)
pos = [ [pos_x,pos_y] ] * len(vel) 
particles = [Particle(pos[i], vel[i]) for i in range(len(pos))]

# generate updated particles movements
generate_reflections(p) 

# plotting and saving
plot_particle_movement(p)

# video
generate_video()
"""

"""
Hopping!
all_move_with_hopping(p,hopping_step)
"""

from DES import *

# default values: ( for plot_fractal() and create_video() )
px = 0 # starting posiiton in x
py = 0 # starting position in y
slope_range = 21 # total range of gradients to take 
dirname = f"Plots_rng{slope_range}_p{px}-{py}"

# Default program for many particles
vel = create_vel_directions_sorted_triangular(slope_range) 
# vel = create_vel_directions_sorted_ascending(1,slope_range)
pos = [ [px, py] ] * len(vel)
particles = [Particle(pos[i], vel[i]) for i in range(len(pos))]

all_move_with_reflection(particles,500, precision=1)
print(f"num of particles : {len(particles)}")
show_max_wall_collisions(particles)

# for many directions plot 
gen_plot(particles, show_grid=True, show_color=True, 
         colors=["r","g","k"], line_width=0.1,
         show_single_collision=True,
         show_wall_collision=True, show_final_plot=True, pause_time=0.001,
         save_wall_collision=False, save_final_plot=False, dots_per_in=200, 
         folder_name=dirname)

# create_video(dirname,video_name=f"Video_{dirname}",save_reverse_frames=False,frame_rate=12, 
#              max_range=[1, len(particles)])
