import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
import itertools
import os
from shutil import copy

worldmin = [0,0]
worldmax = [10,10]
count = 0

class Particle:
    def __init__(self, pos, vel=[1,1]):
        self.s_x = [pos[0]]
        self.s_y = [pos[1]]
        self.v_x = [vel[0]]
        self.v_y = [vel[1]]
        pos = pos
        # print("particle created")

    def move_with_reflection(self):
        # check direction, set collision val.
        m = 0
        if self.v_x[-1] != 0:
            m = self.v_y[-1] / self.v_x[-1]
        if m > 0 and self.v_y[-1] >= 0:
            x_wall = worldmax[0] # L 
            y_wall = worldmax[1] # L 
        elif m < 0 and self.v_y[-1] >= 0:
            x_wall = worldmin[0] # 0
            y_wall = worldmax[1] # L
        elif m > 0 and self.v_y[-1] <= 0:
            x_wall = worldmin[0] # 0 
            y_wall = worldmin[1] # 0
        elif m < 0 and self.v_y[-1] <= 0:
            x_wall = worldmax[0] # L
            y_wall = worldmin[1] # 0
        else:
            raise Exception("no collision")
            return self.s_x[-1], self.s_y[-1]
        
            
        y_temp = (  m  *(x_wall - self.s_x[-1]) + self.s_y[-1])
        x_temp = ((1/m)*(y_wall - self.s_y[-1]) + self.s_x[-1])
        dist_xwall = ( (x_wall - self.s_x[-1])**2 + (y_temp - self.s_y[-1])**2 )**(1/2) # hits x = 0 or x = L
        dist_ywall = ( (x_temp - self.s_x[-1])**2 + (y_wall - self.s_y[-1])**2 )**(1/2) # hits y = 0 or y = L
        # x_temp = abs(x_temp)
        # y_temp = abs(y_temp)
        if (dist_xwall <= dist_ywall):
            self.s_x.append(x_wall)
            self.s_y.append(y_temp)
            self.v_x.append(-self.v_x[-1])
            self.v_y.append(self.v_y[-1])
        
        if (dist_ywall <= dist_xwall):
            self.s_x.append(x_temp)
            self.s_y.append(y_wall)
            self.v_x.append(self.v_x[-1])
            self.v_y.append(-self.v_y[-1])
        
        return self.s_x, self.s_y
    
    def current_position(self):
        return self.s_x[-1], self.s_y[-1]
    
    # def move_with_hopping(self,direction):
        # if direction == "+y": # up
        #     self.s_y = self.s_y + 1
        # elif direction == "-y": # down 
        #     self.s_y = self.s_y - 1 
        # elif direction == "+x": # left 
        #     self.s_x = self.s_x + 1
        # elif direction == "-x": # right
        #     self.s_x = self.s_x - 1
    
    def __repr__(self) -> str:
        global count
        count = count + 1
        return f"{count:3d} | position: {self.s_x[-1]:5.2f}, {self.s_y[-1]:5.2f} | velocity: {self.v_x[-1]:5.2f}, {self.v_y[-1]:5.2f}"


# pos = [[i,j] for i,j in zip(range(1,9),range(9,1,-1))]
# pos = [[0,0] for i in range(a,b) for j in range(a,b)]
# vel = [[i,j] for i in range(a,b) for j in range(a,b)]

def create_vel_directions(a,b):
    vel = [ [i,j] for i in range(a,b) for j in range(a,b)]
    # print(len(vel))
    for i in range(len(vel)):
        f = Fraction(vel[i][0], vel[i][1])
        vel[i] = [f.denominator, f.numerator]
        # print(vel[i][0], vel[i][1])
    vel.sort()
    # list(k for k,_ in itertools.groupby(k))
    vel = list(vel for vel,_ in itertools.groupby(vel))
    return vel

def create_particle_colors(vel, show_color = True):
    color = []
    if show_color == True:
        for v in vel:
            if v[0] % 2 == 0:
                color.append("r") # r
            else:
                if v[1] % 2 == 0:
                    color.append("g") # g
                else: 
                    color.append("k") # k
    else:
        for v in vel:
            color.append("k")

    return color

def create_dir(folder_name):
    path = os.getcwd()
    folder_dir = os.path.join(path,folder_name)
    if not os.path.isdir(folder_dir):
        os.system(f"mkdir {folder_name}")


def plot_fractal(pos_x=0, pos_y=0, vel_i=1, vel_f=10, show_color=True, 
                 show_plots=True, show_final_plot=True, pause_length=0.1, 
                 save_fig=False, line_width=0.1, dots_per_in= 300, show_grid=False,
                 folder_name="Animate_01"):
    create_dir(folder_name)
    fig, ax = plt.subplots()
    print(f"first_direction: (1,{vel_i})")
    print(f"final_direction: (1,{vel_f})")
    print(f"initital_position : ({pos_x},{pos_y})")

    ax.set_xlim([worldmin[0], worldmax[0]])
    ax.set_ylim([worldmin[1], worldmax[1]])
    ax.set_aspect('equal')
    if show_grid: ax.grid()
    frame_num = 0
    for b in range(vel_i, vel_f):
        vel = create_vel_directions(1,b)
        pos = [ [pos_x,pos_y] ] * len(vel) 
        colors = create_particle_colors(vel,show_color)
        particles = [Particle(pos[i], vel[i]) for i in range(len(pos))]
        for p in particles:
            for _ in range(200):
            # print(particle)
                try:
                    p.move_with_reflection()
                except Exception as e:
                    print(e)
                
                if (p.s_x[-1], p.s_y[-1]) in zip(p.s_x[:-1], p.s_y[:-1]):
                    break

        print(f"\nstep: {b}/{vel_f-1}, total lines: {len(vel)} ", end="")
        for p, color in zip(particles, colors):
            # print(f"{p.v_x[0],p.v_y[0]}", end=" ")
            for i in range(len(p.s_x) + 1):
                ax.plot(p.s_x[i:i+2], p.s_y[i:i+2], color, linewidth=line_width)
                ax.set_title(rf"$p_0${p.s_x[0], p.s_y[0]} | $v_0${p.v_x[0], p.v_y[0]} | #{len(vel)} | {b}")
        if show_plots:
            plt.pause(pause_length)

        # plot save:
        if save_fig:
            frame_num = frame_num + 1
            plt.savefig(os.path.join(folder_name,f"frame_{frame_num:04d}"),dpi=dots_per_in)
    
    print()
    folder_dir = os.path.join(os.getcwd(),folder_name)
    os.chdir(folder_dir)
    os.chdir("..")

    if show_final_plot: plt.show()

def create_video(folder_name, video_name, save_reverse_frames=True, max_range=[], frame_rate=1):
    folder_dir = os.path.join(os.getcwd(),folder_name)
    os.chdir(folder_dir)
    print(os.getcwd())
    frame_range = (max_range[-1] - max_range[0])*2
    last_frame = [i for i in os.walk(folder_dir)][-1][-1][-1]
    last_frame = int(last_frame.split(".")[0].split("_")[1])
    
    if last_frame < frame_range:
        if save_reverse_frames: 
            generate_frames_in_reverse(last_frame)
        else: 
            copy(f"frame_{last_frame:04d}.png",f"frame_{last_frame+1:04d}.png")

    if os.path.isdir(folder_dir):
        os.system(f"ffmpeg -r {frame_rate} -i frame_%04d.png -q:v 0 {video_name}.avi -y")
    else:
        print("folder does not exist")


def generate_frames_in_reverse(last_frame):
    i = last_frame + 1
    for b in range(last_frame,0,-1):
        # print(f"frame_{b:04d} to {i}")
        orig_forw = f"frame_{b:04d}.png"
        renm_back = f"frame_{i:04d}.png"
        copy(orig_forw, renm_back)
        i = i + 1