from tools.Entity import Entity
from tools.Vector import Vector

AdditionalEntities = []

def a1_angle_to_angles( index:int, entity:Entity, map:str ):
    if entity.angle:
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

def a1_classname_mapping( index:int, entity:Entity, map:str ):
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
    if entity.classname and entity.classname in classnames:
        entity.classname = classnames.get( entity.classname, '' )
    elif entity.classname == 'game_player_equip':
        for old, new in classnames.items():
            if old in entity.KeyValueData:
                entity.KeyValueData[ new ] = entity.KeyValueData.get( old, '' )
                entity.KeyValueData.pop( old, '' )
    return entity

def b1_worldspawn( index:int, entity:Entity, map:str ):
    if entity.classname == 'worldspawn':
        wad = entity.wad
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
            entity.wad = dwads
    return entity

def b1_chargers_dmdelay( index:int, entity:Entity, map:str ):
    if entity.classname and entity.classname in [ 'func_healthcharger', 'func_recharge' ]:
        entity.dmdelay = None
    return entity

def b1_world_items( index:int, entity:Entity, map:str ):
    if entity.classname == 'world_items':
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
        else:
            entity.remove()
    return entity

def b1_prop_human_hulls( index:int, entity:Entity, map:str ):
    if entity.classname in [ 'monster_generic', 'monster_generic' ] and entity.model in [ 'models/player.mdl', 'models/holo.mdl' ]:
        entity.custom_hull_min = '-16 -16 -36'
        entity.custom_hull_max = '16 16 36'
    return entity

def b1_ambient_generic_pitchbell( index:int, entity:Entity, map:str ):
    if entity.classname == 'ambient_generic' and entity.message == 'buttons/bell1.wav' and entity.pitch == '80':
        entity.message = 'buttons/bell1_alt.wav'
        entity.pitch = 100
    return entity

def b1_monster_barney_dead( index:int, entity:Entity, map:str ):
    if entity.classname == 'monster_barney_dead' and entity.body != None:
        body = int(entity.body )
        if body == 0:
            body = 1
        elif body == 2:
            body = 0
        else:
            body = 2
        entity.body = None
        entity.bodystate = body
    return entity

game_playerdie = False
def b1_game_playerdie( index:int, entity:Entity, map:str ):
    global game_playerdie
    if not game_playerdie and entity.targetname == 'game_playerdie':
        Newent = {
            "classname": "trigger_event",
            "event_type": "1",
            "target": "game_playerdie",
            "m_Caller": "!activator"
        }
        AdditionalEntities.append( Newent )
        game_playerdie = True
    return entity

game_playerleave = False
def b1_game_playerleave( index:int, entity:Entity, map:str ):
    global game_playerleave
    if not game_playerleave and entity.targetname == 'game_playerleave':
        Newent = {
            "classname": "trigger_event",
            "event_type": "2",
            "target": "game_playerleave",
            "m_Caller": "!activator"
        }
        AdditionalEntities.append( Newent )
        game_playerleave = True
    return entity

game_playerkill = False
def b1_game_playerkill( index:int, entity:Entity, map:str ):
    global game_playerkill
    if not game_playerkill and entity.targetname == 'game_playerkill':
        Newent = {
            "classname": "trigger_event",
            "event_type": "3",
            "target": "game_playerkill_check",
            "m_Caller": "!activator"
        }
        AdditionalEntities.append( Newent )
        Newent = {
            "classname": "trigger_entity_condition",
            "targetname": "game_playerkill_check",
            "pass_target": "game_playerkill",
            "condition": "0"
        }
        AdditionalEntities.append( Newent )
        game_playerkill = True
    return entity

game_playeractivate = False
def b1_game_playeractivate( index:int, entity:Entity, map:str ):
    global game_playeractivate
    if not game_playeractivate and entity.targetname == 'game_playeractivate':
        Newent = {
            "classname": "trigger_event",
            "event_type": "4",
            "target": "game_playeractivate",
            "m_Caller": "!activator"
        }
        AdditionalEntities.append( Newent )
        game_playeractivate = True
    return entity

game_playerjoin = False
def b1_game_playerjoin( index:int, entity:Entity, map:str ):
    global game_playerjoin
    if not game_playerjoin and entity.targetname == 'game_playerjoin':
        Newent = {
            "classname": "trigger_event",
            "event_type": "5",
            "target": "game_playerjoin",
            "m_Caller": "!activator",
            "appearflag_multiplayer": "1" # Only in multiplayer
        }
        AdditionalEntities.append( Newent )
        game_playerjoin = True
    return entity

game_playerspawn = False
def b1_game_playerspawn( index:int, entity:Entity, map:str ):
    global game_playerspawn
    if not game_playerspawn and entity.targetname == 'game_playerspawn':
        Newent = {
            "classname": "trigger_event",
            "event_type": "6",
            "target": "game_playerspawn",
            "m_Caller": "!activator"
        }
        AdditionalEntities.append( Newent )
        game_playerspawn = True
    return entity

def map_c2a2a( index:int, entity:Entity, map:str ):
    if entity.classname == 'worldspawn':
        entity.MaxRange = 8192
    return entity
