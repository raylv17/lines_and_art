
# Rafay Nawaid Alvi: 13.04.2024

""" 
Program inspired by the DES (Discrete Event Simulation) approach (in contract to continuous simulations that uses time_stepping)

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


Changes to make:
# Make smaller functions for single (or few) lines that animates each collision
def animate_line() ::: single lines reflections, given starting position (x,y), slope (vi,vf), number of collisions (range)
def animate_lines() :::
# Separate plot the functions, make the above functions return data for generated plots, but not plt.show() them.
create_plot() ::: 
create_video() ::: 
"""

"""
Overhaul notes:
# create particle
p = Particle(px,py,vx,vy)

# or create a list of particles:
vel = create_vel_directions(1,b)
pos = [ [pos_x,pos_y] ] * len(vel) 
particles = [Particle(pos[i], vel[i]) for i in range(len(pos))]

# generate updated particles movements
generate_reflections(p) 
generate_hopping(p)

# plotting and saving
plot_particle_movement(p)

# video
generate_video()
"""

from DES import *

# default values: ( for plot_fractal() and create_video() )
px = 0 # starting posiiton in x
py = 0 # starting position in y
vf = 10 # total range of gradients to take
vi = vf-1 # starting frame to generate from

# e.g.
# vf = 3, vi = 1 ::: [ [1,1], [1,2], [1,3], [2,1], [2,3], [3,1], [3,2] ]
# all the gradients that will be drawn from starting position (px,py)

# plot_folder_name
pname = f"Animate_rng{vf-vi}_vf{vf}_p{px}-{py}"

# plot fractals with reflection
plot_fractal(pos_x=px, pos_y=py, vel_i=vi, vel_f=vf, show_color=True, 
             show_plots=False, show_final_plot=False, pause_length=1,
             save_fig=True,
             line_width=0.1, dots_per_in=300, show_grid=False, 
             folder_name = pname)
# create_video(folder_name=pname, video_name=pname, max_range=[vi,vf], frame_rate=1)

# plot path animation