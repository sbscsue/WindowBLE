import asyncio
from bleak import BleakClient

address = "CC:54:16:E2:03:33"
S_uuid = "00001523-1212-efde-1523-785feabcd123"
C_uuid = ""

async def main(address):
    client = BleakClient(address)
    try:
        await client.connect() 
        print("connect to " + client.address)
        s = await client.get_services()
      
        
    except Exception as e:
        print(e)
        pass
    finally:
        await client.disconnect()

asyncio.run(main(address))