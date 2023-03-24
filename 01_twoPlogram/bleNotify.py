import sys
import time 
import asyncio


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from bleak import BleakClient
from npy_append_array import NpyAppendArray



address = "CA:14:9F:6E:8B:21"
S_uuid = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
C_uuid = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

#save init
folder = "./WindowBLE/data/"
name = "ppg"

path1 = folder + name + ".npy"

np_path1 = NpyAppendArray(path1)
print(path1)



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



def callback(sender:int , data:bytearray):
    #read
    type(data)

    print("======================================================")
    parsingData = []
    for i in range(0,len(data),2):
        parsingData.append(data[i+1] * 255 +  data[i])
    bleTerminalPlot(parsingData)
    bleSave(path1,parsingData)    
    



    

async def ble(address):
    print("start")
    client = BleakClient(address)
    try:
        #connect
        print("connect start")
        await client.connect() 
        print("connect to " + client.address)

        #start = time.time()

        # notify
        await client.start_notify(C_uuid,callback)
        
        while(True):
            data = await client.read_gatt_char(C_uuid)

    except Exception as e:
        print(e)
        pass

    finally:
        #end = time.time()
        #print(end-start)
        await client.disconnect()






asyncio.run(ble(address))


