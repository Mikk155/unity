### Upgrading maps

Create a python script located in ``unity/mods/yourmod.py``

### Add the name of the mod
```python
mod = 'bshift'
```
- Generally it's the mod's folder's name


### Confirm the client has the mod installed.
```python
from tools.check_install import check_install
check_install( mod=mod, link='https://store.steampowered.com/app/130/HalfLife_Blue_Shift/' )
```
- Provide the mod's folder and a link to download the mod


### Track required assets
```python
from tools.resources import load_resources
assets = load_resources( mod='blueshift' )
```
Variable ``mod`` is the name of your .res file.

It is also located in the same folder as the python script

The res file is a simple text telling the script from-to-where copy the resources.
```python
"sound/vox/s.wav" "sound/deliver/vox/s.wav"
"sound/sentences.txt" "sound/deliver/sentences.txt"
"sound/materials.txt" "sound/deliver/materials.txt"
"titles.txt" "cfg/deliver/titles.txt"
```

### Copy the assets
```python
from tools.copy_assets import copy_assets
copy_assets( mod=mod, assets=assets )
```
This will copy the listed assets to a temporal folder in ``unity/mods/port/``

# Convert titles if needed
```python
from tools.titles_to_json import titles_to_json
titles_to_json( path='cfg/blueshift/titles.txt' )
```
This will convert titles.txt to our json-format titles

# Download necesary files
```python
from tools.download import download
download( [ 'https://github.com/Mikk155/unity-mods/archive/refs/heads/Blue-Shift.zip' ] )
```
This will download and install the files from your provided urls.

This is a list of mirrors, not all the urls will be downloaded but it will try to download another if one fails and so.

It's important to have a structure in the zip file wich would drop the files as if we we're within ``unity/`` folder.

# Upgrade maps
```python
from tools.map_upgrader import map_upgrader
map_upgrader()
```

This will export entity data and apply necesary changes, see upgrades.py

# upgrades.py
This script contains functions that will modify the entity data from the maps before importing them back to the BSP file.

All functions that doesn't estarts with ``"map_"`` will be applied to all maps.

if your function starts with ``"map_"`` we'll check for the next part of the name to match the current map that is being modified.
```python
def map_c1a0( entity:dict, entdata=[] ):
```

All functions are sorted by name. do well use of them if you need to apply a change before anything else.

# Adding additional entities
You can add additional entities by having a .json file located in ``port/maps/mapname.json``, Consider repacking it in your zip.

The formatting is just an array of dictionary. each dictionary is a entity.
```json
[
    {
        "message": "Hello world!",
        "targetname": "game_playerjoin",
        "classname": "env_message"
    },
    {
        "targetname": "game_playerspawn",
        "classname": "weapon_9mmhandgun"
    }
]
```
