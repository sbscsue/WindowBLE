import sys
import time 
import asyncio
import argparse


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from bleak import BleakClient
from npy_append_array import NpyAppendArray

parser = argparse.ArgumentParser(description='RECEIVE BLE DATA SAVE')
parser.add_argument('--MAC')
parser.add_argument('--C_UUID')
parser.add_argument('--mode')



args = parser.parse_args()
print(args)

address = args.MAC
C_uuid = args.C_UUID
mode = int(args.mode)
#save init
name = time.strftime('%Y%m%d_%H%M')

path =  name 

path1 = path + "_1" + ".npy"
path2 = path + "_2" + ".npy"

print(path1)
print(path2)

np_path1 = NpyAppendArray(path1)
np_path2 = NpyAppendArray(path2)

path0 = path + "_0" + ".npy"
np_path0 = NpyAppendArray(path0)



def callback(sender:int , data:bytearray):
    #read
    re_data = list(bytes(data))

    #show int terminal 
    #print("========================")
    bleTerminalPlot(re_data)
    #save 
    if(mode==1):
        bleSave1(path,re_data)
    if(mode==2):
        bleSave2(path,re_data)


   

async def ble(address):
    client = BleakClient(address)
    
    try:
        #connect
        await client.connect() 
        print("connect to " + client.address)

        

        start = time.time()

        # notify
        await client.start_notify(C_uuid,callback)
        
        while(True):
            data = await client.read_gatt_char(C_uuid)

           


    except Exception as e:
        print(e)
        pass

    finally:
        end = time.time()
        print(end-start)
        await client.disconnect()


def bleTerminalPlot(data):
    cnt = 0
    for i in data:
        cnt+=1
        print(i,end=" ")
        if(cnt%10==0):
            print("\n")


def bleSave1(path,data):
    np_path0.append(np.array(data))


def bleSave2(path,data):
    first = data[0::2]
    data1 = np.array(first)
    np_path1.append(data1)

    second = data[1::2]
    data2 = np.array(second)
    np_path2.append(data2)





asyncio.run(ble(address))



