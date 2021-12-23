# -*- coding: utf-8 -*-
import time 
import argparse

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from npy_append_array import NpyAppendArray

parser = argparse.ArgumentParser(description='RECEIVE BLE DATA SAVE')
parser.add_argument('--sr')
parser.add_argument('--time')
parser.add_argument('--mode')

args = parser.parse_args()
sr = int(args.sr)
t = int(args.time)
mode = int(args.mode)

name = time.strftime('%Y%m%d_%H%M')


window = sr*t
plot_D = np.zeros(window) 
plot_D1 = np.zeros(window) 
plot_D2 = np.zeros(window) 
global npy_flag
npy_flag = 0
global plot_flag
plot_flag = 0

def animate(i):
    global npy_flag
    global plot_flag

    if mode == 1:
        data =np.load(name+"_0.npy")
    
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
        ax1.plot(plot_D, label='ECG 1',color = 'orange')


        #ax1.set_xlim(len(y1))
        ax1.set_ylim([0,255])

        
        plt.tight_layout()

    if mode == 2:
        data1 =np.load(name+"_1.npy")
        data2 =np.load(name+"_2.npy")
        print("data one:{} two:{}".format(data1.size, data2.size))

        print("1")

        y1 = data1[npy_flag:]
        n = len(y1)
        print(n)

        if (plot_flag+n)>window:
            plot_D1[plot_flag:] = y1[0:window-plot_flag]
            plot_D1[0:n-(window-plot_flag)] = y1[window-plot_flag:]
        else:
            plot_D1[plot_flag:plot_flag+n] = y1
        print("plot_flag:{} npy_flag:{}".format(plot_flag,npy_flag))

        
        print("2")
        y2 = data2[npy_flag:]
        n = len(y2)
        print(n)

        if (plot_flag+n)>window:
            plot_D2[plot_flag:] = y1[0:window-plot_flag]
            plot_D2[0:n-(window-plot_flag)] = y2[window-plot_flag:]
            plot_flag = n-(window-plot_flag)
        else:
            plot_D2[plot_flag:plot_flag+n] = y2
            plot_flag = plot_flag+n
        npy_flag = npy_flag + n
        print("plot_flag:{} npy_flag:{}".format(plot_flag,npy_flag))



        plt.subplot(2,1,1).cla()
        plt.subplot(2,1,2).cla()

        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)

        ax1.plot(plot_D1, label='ECG 1',color = 'orange')
        ax2.plot(plot_D2, label='ECG 2',color = 'blue')

        #ax1.set_xlim(len(y1))
        ax1.set_ylim([0,255])
        #ax2.set_xlim(len(y2))
        ax2.set_ylim([0,255])
        
        plt.tight_layout()

 
ani = FuncAnimation(plt.gcf(),animate, interval = 500)
 
plt.tight_layout()
plt.show()
