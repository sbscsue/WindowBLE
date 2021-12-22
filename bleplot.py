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

window = sr*t

name = time.strftime('%Y%m%d_%H%M')
 
def animate(i):
    if mode == 1:
        data1 =np.load(name+"_0.npy")
        print("data one:{}".format(data1.size))

        flag = data1.size // window
        start  = flag*window

        print(flag)

        y1 = data1[start:]
        print("slice one:{}".format(y1.size))
    
        plt.subplot(1,1,1).cla()

        ax1 = plt.subplot(1,1,1)


        ax1.plot(y1, label='ECG 1',color = 'orange')


        #ax1.set_xlim(len(y1))
        ax1.set_ylim([0,255])

        
        plt.tight_layout()

    if mode == 2:
        data1 =np.load(name+"_1.npy")
        data2 =np.load(name+"_2.npy")
        print("data one:{} two:{}".format(data1.size, data2.size))

        flag = data1.size // window
        start  = flag*window

        print(flag)

        y1 = data1[start:]
        y2 = data2[start:]
        print("slice one:{} two:{}".format(y1.size, y2.size))
    
        plt.subplot(2,1,1).cla()
        plt.subplot(2,1,2).cla()

        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)

        ax1.plot(y1, label='ECG 1',color = 'orange')
        ax2.plot(y2, label='ECG 2',color = 'blue')

        #ax1.set_xlim(len(y1))
        ax1.set_ylim([0,255])
        #ax2.set_xlim(len(y2))
        ax2.set_ylim([0,255])
        
        plt.tight_layout()
 
ani = FuncAnimation(plt.gcf(),animate, interval = 1000)
 
plt.tight_layout()
plt.show()
