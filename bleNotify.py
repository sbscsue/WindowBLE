import sys
import time 
import asyncio


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from bleak import BleakClient
from npy_append_array import NpyAppendArray



address = "CC:54:16:E2:03:33"
S_uuid = "00001523-1212-efde-1523-785feabcd123"
C_uuid = "00001524-1212-efde-1523-785feabcd123"

#save init
folder = "./data/"
name = time.strftime('%Y%m%d_%H%M')
path = folder + name 

path1 = path + "_1" + ".npy"
path2 = path + "_2" + ".npy"

np_path1 = NpyAppendArray(path1)
np_path2 = NpyAppendArray(path2)




def callback(sender:int , data:bytearray):
    #read
    re_data = list(bytes(data))

    #show int terminal 
    #print("========================")
    bleTerminalPlot(re_data)
    #save 
    bleSave(path,re_data)

def bleTerminalPlot(data):
    cnt = 0
    for i in data:
        cnt+=1
        print(i,end=" ")
        if(cnt%10==0):
            print("\n")



def bleSave(path,data):
    first = data[0::2]
    data1 = np.array(first)
    np_path1.append(data1)

    second = data[1::2]
    data2 = np.array(second)
    np_path2.append(data2)


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






asyncio.run(ble(address))
