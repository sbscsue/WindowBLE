# -*- coding: utf-8 -*-
import time 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from npy_append_array import NpyAppendArray

#window
sr = 500
t = 20
window = sr * t

#file path
folder = "./WindowBLE/data/"
name = "ppg"
path1 = folder + name + ".npy"

#plot variable
plot_D = np.zeros(window) 
global npy_flag
npy_flag = 0
global plot_flag
plot_flag = 0


#window size넘어가는 npy파일 처음 열어버리면 오류뜹니다 !! 로직이 그래요 
#blenotify하고 바로 키시길! 
def animate(i):
    global npy_flag
    global plot_flag

    data =np.load(path1)
    
    y = data[npy_flag:]
    n = len(y)
    print(n)
    if (plot_flag+n)>window:
        plot_D[plot_flag:] = y[0:window-plot_flag]
        plot_D[0:n-(window-plot_flag)] = y[window-plot_flag:]
        plot_flag = n-(window-plot_flag)
    else:
        plot_D[plot_flag:plot_flag+n] = y
        plot_flag = plot_flag+n
    npy_flag = npy_flag + n
    print("plot_flag:{} npy_flag:{}".format(plot_flag,npy_flag))


    plt.subplot(1,1,1).cla()

    ax1 = plt.subplot(1,1,1)
    ax1.set_ylim([5000,10000])
    ax1.plot(plot_D, label='PPG',color = 'orange')

    
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(),animate, interval = 1000)
 
plt.tight_layout()
plt.show()
