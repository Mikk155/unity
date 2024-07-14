# ===============================================================================
# Upgrades hooking goes here.
# Call a function with a map name to execute it only for that map
# i.e "def map_c1a0( entity:dict, entdata=[] )" will be applied only to the map c1a0
# The functions are sorted by name, name them in order
# a: Required to be called first
# b: Doesn't conflict
# c: Required to be called last
# ===============================================================================

from tools.Vector import Vector

def a1_angle_to_angles( entity:dict, entdata=[] ):
    if 'angle' in entity:
        NewAngles = Vector()
        Angle = float( entity.get( 'angle', '' ) )
        if Angle >= 0:
            NewAngles = Vector( entity.get( 'angles', '' ) )
            NewAngles.y = Angle
        else:
            if int(Angle) == -1: # floor?
                Angle = -90
            else:
                Angle = 90
            NewAngles.y = Angle
        entity[ 'angles' ] = NewAngles.ToString()
        entity.pop( 'angle', '' )
    return entity

def a1_ClassNameMapping( entity:dict, entdata=[] ):
    classnames = {
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
    if entity.get( 'classname', '' ) in classnames:
        entity[ 'classname' ] = classnames.get( entity.get( 'classname', '' ), '' )
    elif entity.get( 'classname', '' ) == 'game_player_equip':
        for old, new in classnames.items():
            if old in entity:
                entity[ new ] = classnames.get( old, '' )
                entity.pop( old )
    return entity

def b1_worldspawn( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'worldspawn':
        #================================================
        # Wad fix
        #================================================
        wad = entity.get( 'wad', '' )
        if wad:
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
            entity[ 'wad' ] = dwads
        #================================================
        # 
        #================================================
    return entity

def b1_chargers_dmdelay( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) in [ 'func_healthcharger', 'func_recharge' ]:
        entity.pop( 'dmdelay', '' )
    return entity

def b1_world_items( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'world_items':
        value = int( entity.get( 'type', '0' ) )
        entity.pop( 'type', '' )
        if value == 42:
            entity[ 'classname' ] = 'item_antidote'
        elif value == 43:
            entity[ 'classname' ] = 'item_security'
        elif value == 44:
            entity[ 'classname' ] = 'item_battery'
        elif value == 45:
            entity[ 'classname' ] = 'item_suit'
        else:
            entity.clear()
    return entity


def b1_prop_human_hulls( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) in [ 'monster_generic', 'monster_generic' ] and entity.get( 'model', '' ) in [ 'models/player.mdl', 'models/holo.mdl' ]:
        entity[ 'custom_hull_min' ] = '-16 -16 -36'
        entity[ 'custom_hull_max' ] = '16 16 36'
    return entity

def b1_ambient_generic_pitchbell( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'ambient_generic' and entity.get( 'pitch', '' ) == 'buttons/bell1.wav' and entity.get( 'pitch', '' ) == '80':
        entity[ 'message' ] = 'buttons/bell1_alt.wav'
        entity[ 'pitch' ] = '100'
    return entity

def b1_monster_barney_dead( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'monster_barney_dead' and 'body' in entity:
        body = int(entity.get( 'body', '' ))
        if body == 0:
            body = 1
        elif body == 2:
            body = 0
        else:
            body = 2
        entity.pop( 'body', '' )
        entity[ 'bodystate' ] = str(body)
    return entity


# Feel free to rename any function's name, they're automatically catched anyways.

# ===============================================================================
# Map-specific upgrades
# ===============================================================================

def map_ba_canal1( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'monstermaker':
        if 'tele5_spawner' in entity or 'tele4_spawner' in entity:
            entity.pop( 'netname', '' )
    return entity

def map_ba_outro( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'trigger_auto' and entity.get( 'target', '' ) == 'start_outro':
        flags = int(entity.get( 'spawnflags', '0' ))
        flags |= 1
        entity[ 'spawnflags' ] = str(flags)
    elif entity.get( 'targetname', '' ) == 'drag_grunt1':
        entity[ 'body' ] = '4'
    elif entity.get( 'targetname', '' ) == 'drag_grunt2':
        entity[ 'body' ] = '1'
    return entity

def map_ba_power2( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'worldspawn':
        entity.pop( 'chaptertitle', '' )
    return entity

def map_c2a2a( entity:dict, entdata=[] ):
    if entity.get( 'classname', '' ) == 'worldspawn':
        entity[ 'MaxRange' ] = '8192'
    return entity
