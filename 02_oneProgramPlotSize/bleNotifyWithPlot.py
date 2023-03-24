import sys
import time 
import asyncio

import numpy as np
import pandas as pd
import tkinter as tk  
import matplotlib.pyplot as plt

from bleak import BleakClient
import struct

import csv

#참고자료
#https://www.youtube.com/watch?v=cx3vvBfLu04
#https://danielmuellerkomorowska.com/2022/02/14/measuring-and-visualizing-gpu-power-usage-in-real-time-with-asyncio-and-matplotlib/

#BLE 설정
address = "E9:3A:52:EB:D0:1C"
S_uuid = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
C_uuid = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

#PLOT 관련 
PLOT_SIZE = 6
ADC_SAMPLE_SIZE = 30

SAMPLING_FS = 1000
TIME_LENGTH = 10

#initalize plot 
N = SAMPLING_FS* TIME_LENGTH 
data_x = np.arange(0, N, 1)
data_y = np.ones((PLOT_SIZE,N)) 

plt.ion()
plt.rcParams.update({'font.size': 18})
figure =  plt.figure(figsize=(10,12))


#equal size with plot_size
subplots = []
lines = []
titles = ["value1","value2","value3","value4","value5","value6"]
minMaxs = [[0,10],[0,10],[0,100],[0,100],[0,500],[0,500]]
for i in range(PLOT_SIZE):
    ax = figure.add_subplot(6,1,i+1)
    l, = ax.plot(data_x, data_y[i],'b-', linewidth=3)
    subplots.append(ax)
    lines.append(l)
    plt.title(titles[i])

async def plot():
    while True:
        for i in range(PLOT_SIZE):
            lines[i].set_data(data_x,data_y[i])
            subplots[i].set_ylim(minMaxs[i])
            subplots[i].set_xlim(0,N)
        figure.canvas.flush_events()
        await asyncio.sleep(0.2)

#initalize file save
FILE_PATH = "./ppg.csv"

def bleDataParsing(data:bytearray):
    #int 
    # parsingData.append(data[i+1] * 255 +  data[i])

    #float
    #https://stackoverflow.com/questions/5415/convert-bytes-to-floating-point-numbers
    parsingData = [struct.unpack('f',data[i*4:(i+1)*4])[0] for i in range(30)]
    return parsingData


PLOT_FLAG = 0
def bleDataSet(parsingData):
    global PLOT_FLAG
    buff = []
    for i in range(len(parsingData)):
        #print(i%PLOT_SIZE, PLOT_FLAG)
        buff.append(parsingData[i])
        data_y[i%PLOT_SIZE][PLOT_FLAG] = parsingData[i]
        if(i%PLOT_SIZE==5):
            with open(FILE_PATH ,'a', newline='',encoding='utf8') as f:
                reader = csv.reader(f)
                wr = csv.writer(f)
                wr.writerow(buff)
                #print(buff)
            buff =[]
            PLOT_FLAG+=1
            if(PLOT_FLAG ==N):
                PLOT_FLAG = 0
    
def callback(sender:int , data:bytearray):
    #read
    parsingData = bleDataParsing(data)
    #print(parsingData)
    bleDataSet(parsingData)
    
async def ble(address):
    print("start")
    client = BleakClient(address)
    try:
        #connect
        print("connect start")
        await client.connect() 
        print("connect to " + client.address)

        # notify
        await client.start_notify(C_uuid,callback)
        
        while(True):
            data = await client.read_gatt_char(C_uuid)

    except Exception as e:
        print(e)
        pass

    finally:
        await client.disconnect()



async def main():
    t1 = loop.create_task(ble(address))
    t2 = loop.create_task(plot())
    await t2, t1
     
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())





