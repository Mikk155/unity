# ===============================================================================
# Utility library used for porting mods
# ===============================================================================

import io
import re
import os
import sys
import json
import struct
import shutil
import inspect
import zipfile
import requests

import __main__ as main

def __WARN__(m):
    print(f'WARNING! {m}')

def __ERROR__(m):
    print(f'ERROR! {m}')
    sys.exit(0)

__abs__ = os.path.abspath( '' ).replace( '\\', '/' )

if __abs__.rfind( 'unity' ) == -1:
    __ERROR__( 'This script must be executed within /unity/ folder!' )

__dir__ = __abs__[ : __abs__.rfind( 'unity' ) + 5 ]
__dir__ = f'{__dir__}/'

def directory():
    '''
    Returns the directory of unity mod.

    ``C:/Program Files (x86)/Steam/steamapps/common/Half-Life/unity/``

    This only works if the main script has been executed within any folder in unity folder three
    '''
    return __dir__

def check_install( mod_name : str, download_link : str ):
    '''
        Check if the mod is installed.

        If not, exit imediatelly and print the download link
    '''
    if not os.path.exists( f'{__dir__}../{mod_name}/' ):
        print( f'Couldn\'t find "{__dir__.replace( "unity", mod_name )}"\ndid you installed the mod?\n{download_link}' )
        exit(1)
    else:
        print(f'Mod \'{mod_name}\' installation detected. Starting conversion...')

def resources( mod_name : str, res_name : str = None ):
    '''
    Loads a .res file containing the assets required for the mod and copies them in a temporal folder

    Example:

    ``"maps/c1a0.bsp" "maps/hl_c01_a1.bsp"``
    '''
    if not res_name:
        res_name = mod_name

    assets = {}

    if not res_name.endswith( '.res' ):
        res_name = f'{res_name}.res'

    print(f'Loading {res_name}' )

    if not os.path.exists( f'{__abs__}/{res_name}' ):
       __ERROR__( f'Couldn\'t load {__abs__}/{res_name}' )

    with open( f'{__abs__}/{res_name}', 'r' ) as res:

        lines = res.readlines()

        for i, line in enumerate( lines ):

            oldline = line

            line = line[:line.rfind('"')].strip().strip( '"' )

            if not line or line.startswith( '//' ) or line == '':
                continue

            resources = line.split()

            if len(resources) < 2 or len(resources[0]) <= 1 or len(resources[1]) <= 1:
                __ERROR__( f'Error in {res_name} file at line {i}\n{oldline}' )

            assets[ resources[0][ :-1 ] ] = resources[1][ 1 : ]

        res.close()

    if len(assets) == 0:
        __ERROR__(f'No assets were found in {res_name}' )

    print(f'Copying asset...')

    for In, Out in assets.items():

        if Out.find( '/' ) != -1:

            path = f'{__dir__}mods/port/{Out}'
            path = path[ : path.rfind( f'/' ) ]
            if not os.path.exists( path ):
                os.makedirs( path )

        space = 100 - len(In) - len(Out)
        spaces=''
        for i in range(space):
            spaces = f'{spaces} '

        print(f'{In}{spaces}{Out}')
        shutil.copy( f'{__dir__}../{mod_name}/{In}', f'{__dir__}mods/port/{Out}' )

    return assets

def writefile( path:str, content:str ):
    '''
    Write a file, alternative for not repacking a small amount of files
    '''

    if path.find( '/' ) != -1:
        folder = f'{__dir__}mods/port/{path}'
        folder = folder[ : folder.rfind( f'/' ) ]

        if not os.path.exists( folder ):
            os.makedirs( folder )

    print( f'Writting {path}' )

    writefile = open( f'{__dir__}mods/port/{path}', 'w' )
    writefile.write( content )
    writefile.close()

class Vector:
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, str):
            values = x.split( ',' ) if x.find( ',' ) != -1 else x.split()
            if len(values) < 3:
                values += ['0'] * (3 - len(values))
            self.x, self.y, self.z = [self._parse_value(v) for v in values[:3]]
        else:
            self.x = self._parse_value(x) if isinstance( x, ( float, int ) ) else 0
            self.y = self._parse_value(y) if isinstance( y, ( float, int ) ) else 0
            self.z = self._parse_value(z) if isinstance( z, ( float, int ) ) else 0

    def _parse_value(self, value):
        value = float(value)
        if value.is_integer() or value == int(value):
            return int(value)
        return value

    def __str__(self):
        _y = str(self.y).split('.')[0] if str(self.y).endswith( '.0' ) else self.y
        _z = str(self.z).split('.')[0] if str(self.z).endswith( '.0' ) else self.z
        _x = str(self.x).split('.')[0] if str(self.x).endswith( '.0' ) else self.x
        return f'{_x} {_y} {_z}'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector( {self.x}, {self.y}, {self.z} )"

class Entity:
    def __init__( self, KeyValueData=None ):
        self.KeyValueData = KeyValueData if isinstance( KeyValueData, dict ) else KeyValueData.ToDict() if isinstance( KeyValueData, Entity ) else {}

    def ToDict( self ):
        """
            Converts this Entity class to a dict.
        """
        return self.KeyValueData

    def get( self, value:str ):
        self.KeyValueData.get( value )

    def copy(self):
        return Entity( self.KeyValueData.copy() )

    def set( self, value:str ):
        self.KeyValueData[ value ] = value

    def pop( self, value:str ):
        self.KeyValueData.pop( value, '' )

    def __getattr__( self, key ):
        return str( self.KeyValueData.get( key, "" ) ) if key in self.KeyValueData else None

    def __setattr__( self, key, value ):
        if key == 'KeyValueData':
            super().__setattr__( key, value )
        elif value == None:
            self.KeyValueData.pop( key, '' )
        else:
            self.KeyValueData[ key ] = str( value )

    def remove( self ):
        """
        Removes this entity from the entity data
        """
        self.KeyValueData.clear()


def jsonc( path : str ):
    '''
        Loads a file, strip commentary and then returns as json
    '''
    jsdata = ''
    js : dict
    if os.path.exists( f'{__dir__}{path}' ):
        with open( f'{__dir__}{path}', 'r' ) as file:
            lines = file.readlines()
            for t, line in enumerate( lines ):
                line = line.strip()
                if line and line != '' and not line.startswith( '//' ):
                    jsdata = f'{jsdata}\n{line}'
            js = json.loads( jsdata )
            return js
    return None

def ripent( bsp_path, ent_data = None ):
    '''
    Exports the map entity data in a json file as an array of dictionaries
    If ent_data is not None then the data will be imported instead
    '''
    with open( bsp_path, 'rb+' ) as bsp_file:

        bsp_file.read(4) # BSP version.
        entities_lump_start_pos = bsp_file.tell()
        read_start = int.from_bytes( bsp_file.read(4), byteorder='little' )
        read_len = int.from_bytes( bsp_file.read(4), byteorder='little' )
        bsp_file.seek( read_start )

        if ent_data != None:

            newdata = ''

            for entblock in entdata:
                if len(entblock) <= 0:
                    continue
                newdata += '{\n'
                if not isinstance( entblock, dict ):
                    entblock = json.loads( entblock )
                for key, value in entblock.items():
                    newdata += f'"{key}" "{value}"\n'
                newdata += '}\n'

            writedata_bytes = newdata.encode('ascii')
            new_len = len(writedata_bytes)

            if new_len <= read_len:
                bsp_file.write(writedata_bytes)
                if new_len < read_len:
                    bsp_file.write(b'\x00' * (read_len - new_len))
            else:
                bsp_file.seek(0, os.SEEK_END)
                new_start = bsp_file.tell()
                bsp_file.write(writedata_bytes)

                bsp_file.seek(entities_lump_start_pos)
                bsp_file.write(new_start.to_bytes(4, byteorder='little'))
                bsp_file.write(new_len.to_bytes(4, byteorder='little'))
        else:

            map_entities:str
            entities_lump = bsp_file.read( read_len )

            try:
                map_entities = entities_lump.decode('ascii', errors='strict').splitlines()
            except UnicodeDecodeError:
                __WARN__( f'Possible broken entity data in a map, Check and patch "{bsp_path}"' )
                map_entities = entities_lump.decode('utf-8', errors='ignore').splitlines()

            entblock = {}
            entdata = []
            oldline = ''

            for line in map_entities:

                if line == '{':
                    continue

                line = line.strip()

                if not line.endswith( '"' ):
                    oldline = line
                elif oldline != '' and not line.startswith( '"' ):
                    line = f'{oldline}{line}'

                if line.find( '\\' ) != -1:
                    line = line.replace( '\\', '\\\\' )

                line = line.strip( '"' )

                if not line or line == '':
                    continue

                if line.startswith( '}' ): # startswith due to [NULL]
                    entdata.append( json.loads( json.dumps( entblock ) ) )
                    entblock.clear()
                else:
                    keyvalues = line.split( '" "' )
                    if len( keyvalues ) == 2:
                        entblock[ keyvalues[0] ] = keyvalues[1]
            return entdata
    return None

__upgrades_new_entities__ = []

def add_entity( entity:Entity ):
    '''
        Adds a new entity to the current map
    '''
    global __upgrades_new_entities__
    __upgrades_new_entities__.append( entity if isinstance( entity, dict ) else entity.ToDict() )

def __upg_angle_to_angles__( index:int, entity:Entity, map:str ):
    if entity.angle != None:
        NewAngles = Vector()
        Angle = float( entity.angle )
        if Angle >= 0:
            NewAngles = Vector( entity.angles )
            NewAngles.y = Angle
        else:
            if int(Angle) == -1: # floor?
                Angle = -90
            else:
                Angle = 90
            NewAngles.y = Angle
        entity.angles = NewAngles
        entity.angle = None
    return entity

__upg_ItemMapping__ = {
    "weapon_glock": "weapon_9mmhandgun",
    "ammo_glockclip": "ammo_9mmclip",
    "weapon_mp5": "weapon_9mmar",
    "ammo_mp5clip": "ammo_9mmar",
    "ammo_mp5grenades": "ammo_argrenades",
    "weapon_python": "weapon_357",
    "weapon_shockroach": "weapon_shockrifle",
    "weapon_9mmAR": "weapon_9mmar",
    "ammo_9mmAR": "ammo_9mmar",
    "ammo_ARgrenades": "ammo_argrenades",
    "monster_ShockTrooper_dead": "monster_shocktrooper_dead",
}

def __upg_remap_classnames__( index:int, entity:Entity, map:str ):
    global __upg_ItemMapping__
    if entity.classname in __upg_ItemMapping__:
        entity.classname = __upg_ItemMapping__.get( entity.classname )
    elif entity.classname == 'game_player_equip':
        for old, new in __upg_ItemMapping__.items():
            if old in entity.ToDict():
                entity.set( new, entity.get( old ) )
                entity.pop( old )
    return entity

def __upg_worldspawn_format_wad__( index:int, entity:Entity, map:str ):
    if entity.classname == 'worldspawn':
        if entity.wad != None:
            wad = entity.wad
            dwads = ''
            wads = wad.split( ';' )
            for w in wads:
                if not w or w == '':
                    continue
                if w.rfind( '\\' ) != -1:
                    w = w[ w.rfind( '\\' ) + 1 : ]
                if w.rfind( '/' ) != -1:
                    w = w[ w.rfind( '/' ) + 1 : ]
                dwads = f'{dwads}{w};'
            entity.wad = dwads
    return entity

def __upg_chargers_dmdelay__( index:int, entity:Entity, map:str ):
    if entity.classname in [ 'func_healthcharger', 'func_recharge' ]:
        entity.dmdelay = None
    return entity

def __upg_remap_world_items__( index:int, entity:Entity, map:str ):
    if entity.classname == 'world_items':
        if entity.type != None and entity.type.isnumeric():
            value = int( entity.type )
            entity.type = None
            if value == 42:
                entity.classname = 'item_antidote'
            elif value == 43:
                entity.classname = 'item_security'
            elif value == 44:
                entity.classname = 'item_battery'
            elif value == 45:
                entity.classname = 'item_suit'
        if entity.classname == 'world_items':
            warn( f"Unknown value \"{entity.value}\" on world_items")
            entity.remove()
    return entity

def __upg_update_human_hulls__( index:int, entity:Entity, map:str ):
    if entity.classname in [ 'monster_generic', 'monster_generic' ] and entity.model in [ 'models/player.mdl', 'models/holo.mdl' ]:
        entity.custom_hull_min = Vector( -16, -16, -36 )
        entity.custom_hull_max = Vector( 16, 16, 36 )
    return entity

def __upg_ambient_generic_pitch__( index:int, entity:Entity, map:str ):
    if entity.classname == 'ambient_generic' and entity.message == 'buttons/bell1.wav' and entity.pitch == '80':
        entity.message = 'buttons/bell1_alt.wav'
        entity.pitch = 100
    return entity

def __upg_barney_dead_body__( index:int, entity:Entity, map:str ):
    if entity.classname == 'monster_barney_dead' and entity.body != None:
        body = int( entity.body )
        if body == 0:
            body = 1
        elif body == 2:
            body = 0
        else:
            body = 2
        entity.body = None
        entity.bodystate = body
    return entity

def __upg_breakable_spawnobject__( index:int, entity:Entity, map:str ):
    if entity.classname == 'func_breakable' or entity.classname == 'func_pushable':
        if entity.spawnobject != None and entity.spawnobject.isnumeric():
            i = int( entity.spawnobject )
            classnames = [ "item_battery", "item_healthkit",
                "weapon_9mmhandgun", "ammo_9mmclip", "weapon_9mmar",
                    "ammo_9mmar", "ammo_argrenades", "weapon_shotgun",
                        "ammo_buckshot", "weapon_crossbow", "ammo_crossbow",
                            "weapon_357", "ammo_357", "weapon_rpg", "ammo_rpgclip",
                                "ammo_gaussclip", "weapon_handgrenade", "weapon_tripmine",
                                    "weapon_satchel", "weapon_snark", "weapon_hornetgun", "weapon_penguin"
            ]
            if i > 0 and i <= len(classnames):
                entity.spawnobject = classnames[i]
            else:
                entity.spawnobject = None
                if i != 0:
                    warn( f"Unknown spawnobject \"{i}\" in {entity.classname}" )
    return entity

__upg_eventhandler__ = Entity( { "classname": "trigger_eventhandler", "m_Caller": "!activator" } )

__upg_game_playerdie__ = False
def __upg_event_playerdie__( index:int, entity:Entity, map:str ):
    global __upg_game_playerdie__
    if not __upg_game_playerdie__ and entity.targetname == 'game_playerdie':
        __upg_eventhandler__.target = entity.targetname
        __upg_eventhandler__.event_type = 1
        add_entity( __upg_eventhandler__ )
        __upg_game_playerdie__ = True
    return entity

__upg_game_playerleave__ = False
def __upg_event_playerleave__( index:int, entity:Entity, map:str ):
    global __upg_game_playerleave__
    if not __upg_game_playerleave__ and entity.targetname == 'game_playerleave':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 2
        add_entity( __upg_eventhandler__ )
        __upg_game_playerleave__ = True
    return entity

__upg_game_playerkill__ = False
def __upg_event_playerkill__( index:int, entity:Entity, map:str ):
    global __upg_game_playerkill__
    if not __upg_game_playerkill__ and entity.targetname == 'game_playerkill':
        __upg_eventhandler__target = 'game_playerkill_check'
        __upg_eventhandler__event_type = 3
        add_entity( __upg_eventhandler__ )
        Newent = {
            "classname": "trigger_entity_condition",
            "targetname": "game_playerkill_check",
            "pass_target": "game_playerkill",
            "condition": "0"
        }
        add_entity( Newent )
        __upg_game_playerkill__ = True
    return entity

__upg_game_playeractivate__ = False
def __upg_event_playeractivate__( index:int, entity:Entity, map:str ):
    global __upg_game_playeractivate__
    if not __upg_game_playeractivate__ and entity.targetname == 'game_playeractivate':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 4
        add_entity( __upg_eventhandler__ )
        __upg_game_playeractivate__ = True
    return entity

__upg_game_playerjoin__ = False
def __upg_event_playerjoin__( index:int, entity:Entity, map:str ):
    global __upg_game_playerjoin__
    if not __upg_game_playerjoin__ and entity.targetname == 'game_playerjoin':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 5
        Newent = __upg_eventhandler__.copy()
        Newent[ "appearflag_multiplayer" ] = "1" # Only in multiplayer
        add_entity( Newent )
        __upg_game_playerjoin__ = True
    return entity

__upg_game_playerspawn__ = False
def __upg_event_playerspawn__( index:int, entity:Entity, map:str ):
    global __upg_game_playerspawn__
    if not __upg_game_playerspawn__ and entity.targetname == 'game_playerspawn':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 6
        add_entity( __upg_eventhandler__ )
        __upg_game_playerspawn__ = True
    return entity

__upg_DefaultSound__ = "common/null.wav"
__upg_DefaultSentence__ = ""
__upg_DefaultButtonSound__ = ""
__upg_DefaultMomentaryButtonSound__ = "buttons/button9.wav"
__upg_DefaultTrackTrainSound__ = ""

__upg_DoorMoveSounds__ = [
    __upg_DefaultSound__,
    "doors/doormove1.wav",
    "doors/doormove2.wav",
    "doors/doormove3.wav",
    "doors/doormove4.wav",
    "doors/doormove5.wav",
    "doors/doormove6.wav",
    "doors/doormove7.wav",
    "doors/doormove8.wav",
    "doors/doormove9.wav",
    "doors/doormove10.wav"
]

__upg_DoorStopSounds__ = [
    __upg_DefaultSound__,
    "doors/doorstop1.wav",
    "doors/doorstop2.wav",
    "doors/doorstop3.wav",
    "doors/doorstop4.wav",
    "doors/doorstop5.wav",
    "doors/doorstop6.wav",
    "doors/doorstop7.wav",
    "doors/doorstop8.wav"
]

__upg_ButtonSounds__ = [
    __upg_DefaultSound__,
    "buttons/button1.wav",
    "buttons/button2.wav",
    "buttons/button3.wav",
    "buttons/button4.wav",
    "buttons/button5.wav",
    "buttons/button6.wav",
    "buttons/button7.wav",
    "buttons/button8.wav",
    "buttons/button9.wav",
    "buttons/button10.wav",
    "buttons/button11.wav",
    "buttons/latchlocked1.wav",
    "buttons/latchunlocked1.wav",
    "buttons/lightswitch2.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/lever1.wav",
    "buttons/lever2.wav",
    "buttons/lever3.wav",
    "buttons/lever4.wav",
    "buttons/lever5.wav"
]

__upg_ButtonLockedSentences__ = [
    "",
    "NA",
    "ND",
    "NF",
    "NFIRE",
    "NCHEM",
    "NRAD",
    "NCON",
    "NH",
    "NG"
]

__upg_ButtonUnlockedSentences__ = [
    "",
    "EA",
    "ED",
    "EF",
    "EFIRE",
    "ECHEM",
    "ERAD",
    "ECON",
    "EH"
]

class __upg_FixSoundsData__:
    def __init__( self, KeyName:str, DefaultValue:str = None, Names:list[str] = None, Optional:str = None ):
        self.KeyName = KeyName
        self.DefaultValue = DefaultValue
        self.Names = Names
        self.Optional = Optional

__upg_DoorData__ = [
    __upg_FixSoundsData__( "movesnd", __upg_DefaultSound__, __upg_DoorMoveSounds__ ),
    __upg_FixSoundsData__( "stopsnd", __upg_DefaultSound__, __upg_DoorStopSounds__ ),
    __upg_FixSoundsData__( "locked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "unlocked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "locked_sentence", __upg_DefaultSentence__, __upg_ButtonLockedSentences__ ),
    __upg_FixSoundsData__( "unlocked_sentence", __upg_DefaultSentence__, __upg_ButtonUnlockedSentences__ )
]

__upg_ButtonData__ = [
    __upg_FixSoundsData__( "sounds", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "locked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "unlocked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "locked_sentence", __upg_DefaultSentence__, __upg_ButtonLockedSentences__ ),
    __upg_FixSoundsData__( "unlocked_sentence", __upg_DefaultSentence__, __upg_ButtonUnlockedSentences__ )
]

__upg_Momentary_DoorMoveSounds__ = [
    __upg_DefaultSound__,
    "doors/doormove1.wav",
    "doors/doormove2.wav",
    "doors/doormove3.wav",
    "doors/doormove4.wav",
    "doors/doormove5.wav",
    "doors/doormove6.wav",
    "doors/doormove7.wav",
    "doors/doormove8.wav"
]

__upg_RotatingMoveSounds__ = [
    __upg_DefaultSound__,
    "fans/fan1.wav",
    "fans/fan2.wav",
    "fans/fan3.wav",
    "fans/fan4.wav",
    "fans/fan5.wav"
]

__upg_PlatMoveSounds__ = [
    __upg_DefaultSound__,
    "plats/bigmove1.wav",
    "plats/bigmove2.wav",
    "plats/elevmove1.wav",
    "plats/elevmove2.wav",
    "plats/elevmove3.wav",
    "plats/freightmove1.wav",
    "plats/freightmove2.wav",
    "plats/heavymove1.wav",
    "plats/rackmove1.wav",
    "plats/railmove1.wav",
    "plats/squeekmove1.wav",
    "plats/talkmove1.wav",
    "plats/talkmove2.wav"
]

__upg_PlatStopSounds__ = [
    __upg_DefaultSound__,
    "plats/bigstop1.wav",
    "plats/bigstop2.wav",
    "plats/freightstop1.wav",
    "plats/heavystop2.wav",
    "plats/rackstop1.wav",
    "plats/railstop1.wav",
    "plats/squeekstop1.wav",
    "plats/talkstop1.wav"
]

__upg_PlatData__ = [
    __upg_FixSoundsData__( "movesnd", __upg_DefaultButtonSound__, __upg_PlatMoveSounds__ ),
    __upg_FixSoundsData__( "stopsnd", __upg_DefaultButtonSound__, __upg_PlatStopSounds__ )
]

__upg_TrackTrainMoveSounds__ = [
    "",
    "plats/ttrain1.wav",
    "plats/ttrain2.wav",
    "plats/ttrain3.wav",
    "plats/ttrain4.wav",
    "plats/ttrain6.wav",
    "plats/ttrain7.wav"
]

__upg_FixSoundsEntityData__ = {

    "func_door": __upg_DoorData__,
    "func_water": __upg_DoorData__,
    "func_door_rotating": __upg_DoorData__,
    "momentary_door": __upg_FixSoundsData__( "movesnd", __upg_DefaultSound__, __upg_Momentary_DoorMoveSounds__ ),
    "func_rotating": __upg_FixSoundsData__( "sounds", __upg_DefaultSound__, __upg_RotatingMoveSounds__, "message" ),
    "func_button": __upg_ButtonData__,
    "func_rot_button": __upg_ButtonData__,
    "momentary_rot_button": __upg_FixSoundsData__( "sounds", __upg_DefaultMomentaryButtonSound__, __upg_ButtonSounds__ ),
    "func_train": __upg_PlatData__,
    "func_plat": __upg_PlatData__,
    "func_platrot": __upg_PlatData__,
    "func_trackchange": __upg_PlatData__,
    "func_trackautochange": __upg_PlatData__,
    "env_spritetrain": __upg_PlatData__,
    "func_tracktrain": __upg_FixSoundsData__( "sounds", __upg_DefaultTrackTrainSound__, __upg_TrackTrainMoveSounds__ )
}

def __upg_TryFixSoundsEnt__( entity:dict, Data:__upg_FixSoundsData__ ):
    name = Data.Optional
    if name is None:
        name = Data.DefaultValue
        if Data.KeyName in entity and entity.get( Data.KeyName ).isnumeric():
            index = int( entity.get( Data.KeyName ) )
            if index >= 0 and index < len( Data.Names ):
                name = Data.Names[ index ]
    entity[ Data.KeyName ] = None
    if len( name ) > 0:
        entity[ Data.KeyName ] = name
    return Entity( entity )

def __upg_fix_sounds_indexes__( index:int, entity:Entity, map:str ):
    if entity.classname in __upg_FixSoundsEntityData__:
        DataFix = __upg_FixSoundsEntityData__.get( entity.classname )
        if isinstance( DataFix, __upg_FixSoundsData__ ):
            entity = __upg_TryFixSoundsEnt__( entity.ToDict(), DataFix )
        else:
            for D in DataFix:
                entity = __upg_TryFixSoundsEnt__( entity.ToDict(), D )
    return entity

def __upg_rendercolor_invalid__( index:int, entity:Entity, map:str ):
    if entity.rendercolor != None:
        entity.rendercolor = str( Vector( entity.rendercolor ) )
    return entity

def __upg_multi_manager_maxkeys__( index:int, entity:Entity, map:str ):
    if entity.classname == 'multi_manager':
        KeySize = 15
        NewEnt = {}
        pEnt = entity.ToDict().copy()
        ignorelist = { "targetname", "classname", "origin", "wait", "spawnflags" }
        for p in ignorelist:
            if p in entity.ToDict():
                NewEnt[ p ] = entity.get( p )
                KeySize+=1
        for p, v in pEnt.items():
            NewEnt[ p ] = v
            if len( NewEnt ) >= KeySize:
                break
        if len( entity.ToDict() ) > len( NewEnt ):
            for k, v in NewEnt.items():
                if not k in ignorelist:
                    pEnt.pop( k, '' )
            pEnt[ "targetname" ] = entity.targetname + f'_{index}'
            add_entity( __upg_multi_manager_maxkeys__( index, Entity( pEnt ), map ).ToDict() )
            NewEnt[ pEnt.get( "targetname" ) ] = 0
            __WARN__( f"multi_manager exceds max values of 16, Creating a copy for chaining events.")
        entity = Entity( NewEnt )
    return entity

def upgrade_maps():
    '''
    Upgrade all maps located in ``unity/mods/port/maps/``

    You can hook your own upgrades in ``__main__``

    ``from unity_tools import Vector, Entity``
    ``def PreMapUpgrade( index : int, entity : Entity, map : str ):``
    ``def PostMapUpgrade( index : int, entity : Entity, map : str ):``
    '''

    for file in os.listdir( f'{__dir__}mods/port/maps/'):
        if file.endswith( ".bsp" ):
            map = file[ : len(file) - 4 ]
            bsp = f'{map}.bsp'

            entdata = ripent( f'{__dir__}mods/port/maps/{bsp}' )
 
            if entdata == None:
                continue

            print( f'Upgrading map {bsp}' )

            TempEntData = entdata.copy()

            for i, entblock in enumerate( TempEntData ):

                for name, obj in inspect.getmembers( main ):
                    if inspect.isfunction(obj) and name == 'PreMapUpgrade':
                        entblock =  obj( i, Entity( entblock ), map )

                # Converts the obsolete "angle" keyvalue to "angles"
                entblock = __upg_angle_to_angles__( i, Entity( entblock ), map )

                # Renames weapon and item classnames to their primary name.
                entblock = __upg_remap_classnames__( i, Entity( entblock ), map )

                # Delete wad paths to prevent issues
                entblock = __upg_worldspawn_format_wad__( i, Entity( entblock ), map )

                # Removes the "dmdelay" keyvalue from charger entities. The original game ignores these.
                entblock = __upg_chargers_dmdelay__( i, Entity( entblock ), map )

                # Converts <c>world_items</c> entities to their equivalent entity.
                entblock = __upg_remap_world_items__( i, Entity( entblock ), map )

                # Sets a custom hull size for <c>monster_generic</c> entities that use a model
                # that was originally hard-coded to use one.
                entblock = __upg_update_human_hulls__( i, Entity( entblock ), map )

                # Find all buttons/bell1.wav sounds that have a pitch set to 80.
                # Change those to use an alternative sound and set their pitch to 100.
                entblock = __upg_ambient_generic_pitch__( i, Entity( entblock ), map )

                # Converts <c>monster_barney_dead</c> entities with custom body value
                # to use the new <c>bodystate</c> keyvalue.
                entblock = __upg_barney_dead_body__( i, Entity( entblock ), map )

                # Converts <c>func_breakable</c>'s spawn object keyvalue from an index to a classname.
                entblock = __upg_breakable_spawnobject__( i, Entity( entblock ), map )

                # Convert special targetnames to our new entity trigger_eventhandler
                entblock = __upg_event_playerdie__( i, Entity( entblock ), map )
                entblock = __upg_event_playerleave__( i, Entity( entblock ), map )
                entblock = __upg_event_playerkill__( i, Entity( entblock ), map )
                entblock = __upg_event_playeractivate__( i, Entity( entblock ), map )
                entblock = __upg_event_playerjoin__( i, Entity( entblock ), map )
                entblock = __upg_event_playerspawn__( i, Entity( entblock ), map )

                # Converts all entities that use sounds or sentences by index
                # to use sound filenames or sentence names instead.
                entblock = __upg_fix_sounds_indexes__( i, Entity( entblock ), map )

                # Fixes the use of invalid render color formats in some maps.
                entblock = __upg_rendercolor_invalid__( i, Entity( entblock ), map )

                # Prunes excess keyvalues specified for <c>multi_manager</c> entities.
                # In practice this only affects a handful of entities used in retinal scanner scripts.
                entblock = __upg_multi_manager_maxkeys__( i, Entity( entblock ), map )

                for name, obj in inspect.getmembers( main ):
                    if inspect.isfunction(obj) and name == 'PostMapUpgrade':
                        entblock =  obj( i, Entity( entblock ), map )

                if isinstance( entblock, Entity ):
                    entblock = entblock.ToDict()

                entdata[i] = ( json.dumps( entblock ) if len( entblock ) > 0 else {} )

            global __upgrades_new_entities__

            for ae in __upgrades_new_entities__:
                entdata.append( json.dumps( ae ) )

            __upgrades_new_entities__ = []

def download( urls : list[str] ):
    '''
    Download third party assets if needed
    '''

    links = []

    if isinstance( urls, str ):
        links.append( urls )
    else:
        links = urls

    for url in links:
        print( f'[download] Downloading third-party assets\n{url}' )

        response = requests.get( url )

        if response.status_code == 200:

            zip_file = zipfile.ZipFile( io.BytesIO( response.content ) )

            zip_file.extractall( "test" )

            for member in zip_file.namelist():

                filename = os.path.basename( member )

                if not filename:
                    continue

                source = zip_file.open( member )
                target = open( os.path.join( f'{__dir__}/mods/port/', filename ), "wb" )

                with source, target:
                    target.write( source.read() )
            break # Break as soon as one url doesn't fail
        else:
            print( f"WARNING! Error: {response.status_code} Failed downloading assets" )

class PakFile:
    def __init__(self, filename):
        self.filename = filename
        self.files = {}
        self._read_pak_file()

    def _read_pak_file(self):
        with open(self.filename, 'rb') as f:
            header = f.read(12)
            if header[:4] != b'PACK':
                raise ValueError('Not a valid PAK file')

            (dir_offset, dir_length) = struct.unpack('ii', header[4:])
            f.seek(dir_offset)
            dir_data = f.read(dir_length)

            num_files = dir_length // 64
            for i in range(num_files):
                entry = dir_data[i*64:(i+1)*64]
                name = entry[:56].rstrip(b'\x00').decode('latin-1')
                (offset, length) = struct.unpack('ii', entry[56:])
                clean_name = self._clean_filename(name)
                self.files[clean_name] = (offset, length)

    def _clean_filename(self, name):
        name = re.sub(r'[^\x20-\x7E]', '_', name)
        name = re.sub(r'[<>:"\\|?*]', '_', name)
        name = re.sub(r'_+', '_', name)
        name = name.strip('_')
        name = name[:name.find('_',name.find('.'))]
        print(f'name {name}')
        return name

    def _extract(self, extract_to):
        with open(self.filename, 'rb') as f:
            for name, (offset, length) in self.files.items():
                f.seek(offset)
                data = f.read(length)

                extract_path = os.path.join(extract_to, name)
                os.makedirs(os.path.dirname(extract_path), exist_ok=True)

                if os.path.exists(extract_path):
                    #print(f"[pak.py] {name} exists. skipping...")
                    continue

                with open(extract_path, 'wb') as out_file:
                    out_file.write(data)

                print(f"Extracted {name} to {extract_path}")

def extract_pak( paks=[], mod='' ):
    '''
    Extracts files from .pak files
    '''
    for p in paks:
        if not p.endswith('.pak'):
            p = f'{p}.pak'
        pak = PakFile( f'{__dir__}../{mod}/{p}' )
        pak._extract( f'{__dir__}../{mod}/' )
