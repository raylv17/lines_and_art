
# Rafay Nawaid Alvi: 13.04.2024

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
px = 1   # starting posiiton in x
py = 0 # starting position in y
vx = 9 # x component of direction
vy = 8 # y component of direction
dirname = f"Plots_vx{vx}-vy{vy}_p{px}-{py}"

# Default program for single particle
particles = [Particle(pos = [px,py], vel= [vx, vy])]
all_move_with_reflection(particles,500)
show_max_wall_collisions(particles)

# for single_direction plots
gen_plot(particles, show_grid=True, show_color=True, line_width=1, pause_time=0.1,
         show_single_collision=True, save_every_single_collision=False,
                show_final_plot=True,             save_final_plot=False, 
         dots_per_in=200, 
         folder_name=dirname)

# create_video(dirname,video_name=f"Video_{dirname}",save_reverse_frames=False,frame_rate=5, 
#              max_range=[1, len(particles)])