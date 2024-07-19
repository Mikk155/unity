from tools.Entity import Entity
from tools.Vector import Vector

def a1_angle_to_angles( entity:Entity, entdata=[] ):
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

def a1_classname_mapping( entity:Entity, entdata=[] ):
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

def b1_worldspawn( entity:Entity, entdata=[] ):
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

def b1_chargers_dmdelay( entity:Entity, entdata=[] ):
    if entity.classname and entity.classname in [ 'func_healthcharger', 'func_recharge' ]:
        entity.dmdelay = None
    return entity

def b1_world_items( entity:Entity, entdata=[] ):
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

def b1_prop_human_hulls( entity:Entity, entdata=[] ):
    if entity.classname in [ 'monster_generic', 'monster_generic' ] and entity.model in [ 'models/player.mdl', 'models/holo.mdl' ]:
        entity.custom_hull_min = '-16 -16 -36'
        entity.custom_hull_max = '16 16 36'
    return entity

def b1_ambient_generic_pitchbell( entity:Entity, entdata=[] ):
    if entity.classname == 'ambient_generic' and entity.message == 'buttons/bell1.wav' and entity.pitch == '80':
        entity.message = 'buttons/bell1_alt.wav'
        entity.pitch = 100
    return entity

def b1_monster_barney_dead( entity:Entity, entdata=[] ):
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

# Feel free to rename any function's name, they're automatically catched anyways.

# ===============================================================================
# Blue Shift Map-specific upgrades
# ===============================================================================

def serie_ba_( entity:Entity, entdata=[] ):
    if entity.classname == 'monster_rosenberg':
        entity.model = None
        SF_ROSENBERG_NO_USE = 256
        spawnflags = int( entity.spawnflags ) if entity.spawnflags else 0
        entity.allow_follow = 0 if spawnflags & SF_ROSENBERG_NO_USE else 1
        spawnflags &= ~SF_ROSENBERG_NO_USE
        entity.spawnflags = spawnflags
    elif entity.classname == 'monster_generic' and entity.body == '3' and entity.model == 'models/scientist.mdl':
        entity.model = 'models/rosenberg.mdl'
    elif entity.classname == 'monster_scientist' and entity.body == '3':
        entity.classname == 'monster_rosenberg'
        entity.model = None
    entity.body = None
    return entity

def map_ba_canal1( entity:Entity, entdata=[] ):
    if entity.classname == 'monstermaker':
        if entity.targetname == 'tele5_spawner' or entity.targetname == 'tele4_spawner':
            entity.netname = None
    return entity

def map_ba_outro( entity:Entity, entdata=[] ):
    if entity.classname == 'trigger_auto' and entity.target == 'start_outro':
        entity.spawnflags = 1
    elif entity.targetname == 'drag_grunt1':
        entity.body = 4
    elif entity.targetname == 'drag_grunt2':
        entity.body = 1
    return entity

def map_ba_power2( entity:Entity, entdata=[] ):
    if entity.classname == 'worldspawn':
        entity.chaptertitle = None
    return entity

def map_ba_security2( entity:Entity, entdata=[] ):
    if entity.targetname == 'gina_push':
        entity.model = 'models/blueshift/holo_cart.mdl'
    return entity

def map_ba_tram1( entity:Entity, entdata=[] ):
    if entity.targetname == 'sitter':
        entity.body = None
    elif entity.classname == 'item_suit':
        entity.remove()
    return entity

def map_ba_tram2( entity:Entity, entdata=[] ):
    if entity.targetname == 'joey_normal' or entity.classname == 'joey_reflect':
        entity.skin = 1
    return entity

def map_ba_yard1( entity:Entity, entdata=[] ):
    if entity.classname == 'monster_scientist_dead' and entity.body == '3':
        entity.body = 0
    return entity

# ===============================================================================
# Half Life Map-specific upgrades
# ===============================================================================

def map_c2a2a( entity:Entity, entdata=[] ):
    if entity.classname == 'worldspawn':
        entity.MaxRange = 8192
    return entity
