import asyncio
import winsdk.windows.devices.geolocation as wdg

async def getCoords():
    locator                     = wdg.Geolocator()
    pos                         = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]

def getLoc():
    try:
        return asyncio.run(getCoords())
    except PermissionError:
        print("ERROR: You need to allow applications to access you location in Windows settings")
        return [0, 0]
