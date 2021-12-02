import asyncio
import bleak
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        print(d.name)
    
        if d.name == "Nordic_Blinky":
            print("====================================")
            #client = bleak.BleakClient.connect(d.address)
            #print(client)
        

        

asyncio.run(main())