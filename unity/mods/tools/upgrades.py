# ===============================================================================
# Upgrades hooking goes here.
# Call a function with a map name to execute it only for that map
# i.e "def map_c1a0( entdata:dict )" will be applied only to the map c1a0
# ===============================================================================

def worldspawn( entdata:dict ):
    if entdata.get( 'classname', '' ) == 'worldspawn':
        #================================================
        # Wad fix
        #================================================
        wad = entdata.get( 'wad', '' )
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
            entdata[ 'wad' ] = dwads
        #================================================
        # 
        #================================================
    return entdata

def world_items( entdata:dict ):
    if entdata.get( 'classname', '' ) == 'world_items':
        value = int( entdata.get( 'type', '0' ) )
        entdata.pop( 'type', '' )
        if value == 42:
            entdata[ 'classname' ] = 'item_antidote'
        elif value == 43:
            entdata[ 'classname' ] = 'item_security'
        elif value == 44:
            entdata[ 'classname' ] = 'item_battery'
        elif value == 45:
            entdata[ 'classname' ] = 'item_suit'
        else:
            entdata.clear()
    return entdata


def chargers_dmdelay( entdata:dict ):
    if entdata.get( 'classname', '' ) in [ 'func_healthcharger', 'func_recharge' ]:
        entdata.pop( 'dmdelay', '' )
    return entdata

def prop_human_hulls( entdata:dict ):
    if entdata.get( 'classname', '' ) in [ 'monster_generic', 'monster_generic' ] and entdata.get( 'model', '' ) in [ 'models/player.mdl', 'models/holo.mdl' ]:
        entdata[ 'custom_hull_min' ] = '-16 -16 -36'
        entdata[ 'custom_hull_max' ] = '16 16 36'
    return entdata

def ambient_generic_pitchbell( entdata:dict ):
    if entdata.get( 'classname', '' ) == 'ambient_generic' and entdata.get( 'pitch', '' ) == 'buttons/bell1.wav' and entdata.get( 'pitch', '' ) == '80':
        entdata[ 'message' ] = 'buttons/bell1_alt.wav'
        entdata[ 'pitch' ] = '100'
    return entdata

def ClassNameMapping( entdata:dict ):
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
    if entdata.get( 'classname', '' ) in classnames:
        entdata[ 'classname' ] = classnames.get( entdata.get( 'classname', '' ), '' )
    elif entdata.get( 'classname', '' ) == 'game_player_equip':
        for old, new in classnames.items():
            if old in entdata:
                entdata[ new ] = classnames.get( old, '' )
                entdata.pop( old )
    return entdata

# Feel free to rename any function's name, they're automatically catched anyways.

# ===============================================================================
# Map-specific upgrades
# ===============================================================================

def map_c2a2a( entdata:dict ):
    if entdata.get( 'classname', '' ) == 'worldspawn':
        entdata[ 'MaxRange' ] = '8192'
    return entdata
