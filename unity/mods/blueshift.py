# ===============================================================================
# Blue Shift installation script
# ===============================================================================

import os, struct

mod = 'bshift'

from tools.path             import port
from tools.check_install    import check_install
from tools.resources        import load_resources
from tools.copy_assets      import copy_assets
from tools.titles_to_json   import titles_to_json
from tools.map_upgrader     import map_upgrader
from tools.Entity           import Entity

#check_install( mod=mod, link='https://store.steampowered.com/app/130/HalfLife_Blue_Shift/' )

assets = load_resources( mod='blueshift' )

#copy_assets( mod=mod, assets=assets )

#titles_to_json( path='cfg/blueshift/titles.txt' )

def BShiftMapConvert():
    for file in os.listdir( f'{port}/maps/'):
        if file.startswith( "ba_" ) and file.endswith( ".bsp" ):
            try:
                with open( f'{port}/maps/{file}', "rb+") as file:
                    start = file.tell()
                    if start == -1:
                        print(f"Error getting start position in \"{file}\"")
                        return
                    header = read_header(file)
                    header.lumps[0], header.lumps[1] = header.lumps[1], header.lumps[0]
                    file.seek(start, os.SEEK_SET)
                    print(f"Converting map \"{file}\"")
                    write_header(file, header)
            except IOError:
                print(f"Error opening file \"{file}\"")

HEADER_LUMPS = 15

class Lump:
    def __init__(self, fileofs, filelen):
        self.fileofs = fileofs
        self.filelen = filelen

class DHeader:
    def __init__(self):
        self.version = 0
        self.lumps = [Lump(0, 0) for _ in range(HEADER_LUMPS)]

def read_header(file):
    header = DHeader()
    data = file.read(4 + 8 * HEADER_LUMPS)
    header.version = struct.unpack('i', data[:4])[0]
    for i in range(HEADER_LUMPS):
        fileofs, filelen = struct.unpack('ii', data[4 + i * 8:4 + (i + 1) * 8])
        header.lumps[i] = Lump(fileofs, filelen)
    return header

def write_header(file, header):
    data = struct.pack('i', header.version)
    for lump in header.lumps:
        data += struct.pack('ii', lump.fileofs, lump.filelen)
    file.write(data)

#BShiftMapConvert()

def ba_tram1( index:int, entity:Entity, map:str ):
    if map == 'ba_tram1':
        if entity.targetname == 'sitter':
            entity.body = None
        elif entity.classname == 'item_suit':
            entity.remove()
    return entity

def ba_tram2( index:int, entity:Entity, map:str ):
    if map == 'ba_tram2':
        if entity.targetname == 'joey_normal' or entity.classname == 'joey_reflect':
            entity.skin = 1
    return entity

def ba_yard1( index:int, entity:Entity, map:str ):
    if map == 'ba_yard1' and entity.classname == 'monster_scientist_dead' and entity.body == '3':
        entity.body = 0
    return entity

def ba_outro( index:int, entity:Entity, map:str ):
    if map == 'ba_outro':
        if entity.classname == 'trigger_auto' and entity.target == 'start_outro':
            entity.spawnflags = 1
        elif entity.targetname == 'drag_grunt1':
            entity.body = 4
        elif entity.targetname == 'drag_grunt2':
            entity.body = 1
    return entity

def ba_power2( index:int, entity:Entity, map:str ):
    if map == 'ba_power2' and entity.classname == 'worldspawn':
        entity.chaptertitle = None
    return entity

def ba_security2( index:int, entity:Entity, map:str ):
    if map == 'ba_security2'and entity.targetname == 'gina_push':
        entity.model = 'models/blueshift/holo_cart.mdl'
    return entity

def ba_canal1( index:int, entity:Entity, map:str ):
    if map == 'ba_canal1'and entity.classname == 'monstermaker':
        if entity.targetname == 'tele5_spawner' or entity.targetname == 'tele4_spawner':
            entity.netname = None
    return entity

def globalfixes( index:int, entity:Entity, map:str ):
    if entity.classname == 'monster_rosenberg':
        entity.model = None
        SF_ROSENBERG_NO_USE = 256
        spawnflags = int( entity.spawnflags ) if entity.spawnflags else 0
        entity.allow_follow = 0 if spawnflags & SF_ROSENBERG_NO_USE else 1
        spawnflags &= ~SF_ROSENBERG_NO_USE
        entity.spawnflags = spawnflags
        entity.body = None
    elif entity.classname == 'monster_generic' and entity.body == '3' and entity.model == 'models/scientist.mdl':
        entity.model = 'models/rosenberg.mdl'
        entity.body = None
    elif entity.classname == 'monster_scientist' and entity.body == '3':
        entity.classname == 'monster_rosenberg'
        entity.model = None
        entity.body = None
    elif entity.classname == 'worldspawn':
        if map == 'ba_tram1':
            entity.mapcfg = 'blueshift/ba_tram1'
        else:
            entity.mapcfg = 'blueshift/default_config'
    return entity

map_upgrader()

from tools.download import download
#download( [ 'https://github.com/Mikk155/unity-mods/archive/refs/heads/Blue-Shift.zip' ] )
