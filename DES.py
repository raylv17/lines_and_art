import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
import itertools
import os
from shutil import copy

count = 0
worldmin = [0,0]
worldmax = [10,10]
class Particle:
    def __init__(self, pos, vel=[1,1]):
        self.s_x = [pos[0]]
        self.s_y = [pos[1]]
        self.v_x = [vel[0]]
        self.v_y = [vel[1]]
        self.color = "b"
        self.worldmin = [worldmin[0],worldmin[1]]
        self.worldmax = [worldmax[0],worldmax[1]]
        pos = pos
        # print("particle created")

    def move_with_reflection(self):
        # check direction, set collision val.
        m = 0
        if self.v_x[-1] != 0:
            m = self.v_y[-1] / self.v_x[-1]
        if m > 0 and self.v_y[-1] >= 0:
            x_wall = self.worldmax[0] # L 
            y_wall = self.worldmax[1] # L 
        elif m < 0 and self.v_y[-1] >= 0:
            x_wall = self.worldmin[0] # 0
            y_wall = self.worldmax[1] # L
        elif m > 0 and self.v_y[-1] <= 0:
            x_wall = self.worldmin[0] # 0 
            y_wall = self.worldmin[1] # 0
        elif m < 0 and self.v_y[-1] <= 0:
            x_wall = self.worldmax[0] # L
            y_wall = self.worldmin[1] # 0
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

def create_vel_directions_sorted_ascending(a,b):
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

def create_vel_directions_sorted_triangular(range):
    new_vel = []
    i = 1
    while i < range:
        j = 1
        while j <= i:
            if not (list(Fraction(i,j).as_integer_ratio()) in new_vel):
                if i != j:
                    new_vel.append([j,i])
                    new_vel.append([i,j])
                else:
                    new_vel.append([i,j])
            # print(i,j)
            j = j + 1
        i = i + 1
    return new_vel   

def all_move_with_reflection(particles, num_of_collisions=1, precision=10):
    for p in particles:
        x_list = []
        y_list = []
        for _ in range(num_of_collisions):
            x_list.append(round(p.s_x[-1],precision))
            y_list.append(round(p.s_y[-1],precision))
            p.move_with_reflection()
            # 2 is equal to 2.002 (close numbers are assumed as equal)
            if (round(p.s_x[-1],precision),round(p.s_y[-1],precision)) in zip(x_list,y_list):
                # print(f"{p.s_y[-1]} :ro: {round(p.s_y[-1],3)} :co: {p.s_y[0]} ")
                # p.s_x.pop()
                # p.s_y.pop()
                break

def show_max_wall_collisions(particles,get=False):
    max_col = 0
    for p in particles:
        if max_col < len(p.s_x):
            max_col = len(p.s_x)
    print(f"max wall collisions: {max_col}")
    if get: return max_col
    

def set_color(particles, show_color=True, colors=["r","g","k"]):
    if show_color:
        for p in particles:
            if p.v_x[0] % 2 == 0:
                p.color = colors[0] # r
            else:
                if p.v_y[0] % 2 == 0:
                    p.color = colors[1] # g
                else:
                    p.color = colors[2] # k

def create_dir(folder_name):
    path = os.getcwd()
    folder_dir = os.path.join(path,folder_name)
    if not os.path.isdir(folder_dir):
        os.system(f"mkdir {folder_name}")

def gen_plot(particles, show_grid=True, show_color=True, 
             colors=["r","g","k"], line_width=0.1,
             show_single_collision=False, save_every_single_collision=False,
             show_wall_collision=False, save_wall_collision=False,
             pause_time=0.1, show_final_plot=True,
             save_final_plot=False, folder_name="untitled", dots_per_in=300):
    if show_color: set_color(particles, show_color, colors)
    fig, ax = plt.subplots()
    ax.set_xlim([worldmin[0], worldmax[0]])
    ax.set_ylim([worldmin[1], worldmax[1]])
    ax.set_aspect('equal') 
    if show_grid: ax.grid()
    if save_final_plot or save_wall_collision or save_every_single_collision:
        create_dir(folder_name)
    frame_num = 0
    count = 0
    for p in particles:
        count = count + 1
        if show_single_collision:
            col_count = 0
            for i in range(len(p.s_x)):
                col_count = col_count + 1
                ax.set_title(f"{p.v_x[0],p.v_y[0]} | {col_count} | #collisions: {len(p.s_x)}") 
                plt.plot(p.s_x[i:i+2],p.s_y[i:i+2], p.color, linewidth=line_width)
                plt.pause(pause_time)
                if save_every_single_collision:
                    frame_num = frame_num + 1
                    plt.savefig(os.path.join(folder_name,f"frame_{frame_num:04d}"),dpi=dots_per_in)
        else:
            ax.set_title(f"{p.v_x[0],p.v_y[0]} | {count} | #lines: {len(particles)}") 
            plt.plot(p.s_x, p.s_y, p.color, linewidth=line_width)
            if show_wall_collision: 
                plt.pause(pause_time)
            if save_wall_collision:
                frame_num = frame_num + 1
                plt.savefig(os.path.join(folder_name,f"frame_{frame_num:04d}"),dpi=dots_per_in)
    
    ax.set_title(fr"$p_0${p.s_x[0],p.s_y[0]} | #lines: {len(particles)}") 
    if save_final_plot:
        frame_num = frame_num + 1
        plt.savefig(os.path.join(folder_name,f"frame_{frame_num:04d}"),dpi=dots_per_in)
    
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

if __name__ == "__main__":
    # one particle movement
    particles = []
    particles.append(Particle(pos=[0,0], vel=[1,2]))
    particles.append(Particle(pos=[0,0], vel=[2,1]))
    particles.append(Particle(pos=[0,0], vel=[1,3]))
    all_move_with_reflection(particles, 100)
    gen_plot(particles, show_color=True)
    plt.show()
    