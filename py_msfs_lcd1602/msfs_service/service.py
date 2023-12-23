from time import sleep
from simconnect import SimConnect, PERIOD_VISUAL_FRAME

# open a connection to the SDK
# or use as a context via `with SimConnect() as sc: ... `
sc = SimConnect(dll_path="D:/Games/SteamLibrary/steamapps/common/MicrosoftFlightSimulator/SimConnect.dll")

# one-off blocking fetch of a single simulator variable,
# which will wait up to 1s (default) to receive the value
altitude = sc.get_simdatum("Indicated Altitude")
print("Got indicated altitude", altitude)

# subscribing to one or more variables is much more efficient,
# with the SDK sending updated values up to once per simulator frame.
# the variables are tracked in `datadef.simdata`
# which is a dictionary that tracks the last modified time
# of each variable.  changes can also trigger an optional callback function
datadef = sc.subscribe_simdata(
    [
        "Indicated Altitude"
    ],
    # request an update every ten rendered frames
    period=PERIOD_VISUAL_FRAME,
    interval=10,
)
print("Inferred variable units", datadef.get_units())

# track the most recent data update
latest = datadef.simdata.latest()
print(latest)

# explicity close the SDK connection
sc.Close()