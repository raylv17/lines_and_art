from DES import *

vel_end = 30
vel_start = vel_end-1
pname = f"Animate_f{vel_end-vel_start}_v{vel_end}"

plot_fractal(pos_x=0, pos_y=0, vel_i=vel_start, vel_f=vel_end, show_color=True, 
             show_plots=False, pause_length=1, save_fig=True, save_reverse_frames=True, 
             line_width=0.01, dots_per_in=3000, show_grid=False, 
             folder_name = pname)
# create_video(folder_name=pname, video_name=pname, frame_rate=1)