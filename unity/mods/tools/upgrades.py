from tools.Entity import Entity
from tools.Vector import Vector

def warn(m):
    print( f'[upgrades] Warning! {m}' )

# ==========================================================================================
# array of dict, append to add a new entity
# ==========================================================================================
AdditionalEntities = []

# ==========================================================================================
# Converts the obsolete "angle" keyvalue to "angles"
# ==========================================================================================
def a1_angle_to_angles( index:int, entity:Entity, map:str ):
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

# ==========================================================================================
# Renames weapon and item classnames to their primary name.
# ==========================================================================================
ItemMapping = {
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

def a1_classname_mapping( index:int, entity:Entity, map:str ):
    if entity.classname in ItemMapping:
        entity.classname = ItemMapping.get( entity.classname )
    elif entity.classname == 'game_player_equip':
        for old, new in ItemMapping.items():
            if old in entity.ToDict():
                entity.set( new, entity.get( old ) )
                entity.pop( old )
    return entity

# ==========================================================================================
# Delete wad paths to prevent issues
# ==========================================================================================
def b1_worldspawn( index:int, entity:Entity, map:str ):
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

# ==========================================================================================
# Removes the "dmdelay" keyvalue from charger entities. The original game ignores these.
# ==========================================================================================
def b1_chargers_dmdelay( index:int, entity:Entity, map:str ):
    if entity.classname in [ 'func_healthcharger', 'func_recharge' ]:
        entity.dmdelay = None
    return entity

# ==========================================================================================
# Converts <c>world_items</c> entities to their equivalent entity.
# ==========================================================================================
def b1_world_items( index:int, entity:Entity, map:str ):
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

# ==========================================================================================
# Sets a custom hull size for <c>monster_generic</c> entities that use a model
# that was originally hard-coded to use one.
# ==========================================================================================
def b1_prop_human_hulls( index:int, entity:Entity, map:str ):
    if entity.classname in [ 'monster_generic', 'monster_generic' ] and entity.model in [ 'models/player.mdl', 'models/holo.mdl' ]:
        entity.custom_hull_min = '-16 -16 -36'
        entity.custom_hull_max = '16 16 36'
    return entity

# ==========================================================================================
# Find all buttons/bell1.wav sounds that have a pitch set to 80.
# Change those to use an alternative sound and set their pitch to 100.
# ==========================================================================================
def b1_ambient_generic_pitchbell( index:int, entity:Entity, map:str ):
    if entity.classname == 'ambient_generic' and entity.message == 'buttons/bell1.wav' and entity.pitch == '80':
        entity.message = 'buttons/bell1_alt.wav'
        entity.pitch = 100
    return entity

# ==========================================================================================
# Converts <c>monster_barney_dead</c> entities with custom body value
# to use the new <c>bodystate</c> keyvalue.
# ==========================================================================================
def b1_monster_barney_dead( index:int, entity:Entity, map:str ):
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


# ==========================================================================================
# Converts <c>func_breakable</c>'s spawn object keyvalue from an index to a classname.
# ==========================================================================================
def b1_func_breakable( index:int, entity:Entity, map:str ):
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

# ==========================================================================================
# Convert special targetnames to our new entity trigger_eventhandler
# ==========================================================================================
eventhandler = Entity( { "classname": "trigger_eventhandler", "m_Caller": "!activator" } )

game_playerdie = False
def b1_game_playerdie( index:int, entity:Entity, map:str ):
    global game_playerdie
    if not game_playerdie and entity.targetname == 'game_playerdie':
        eventhandler.target = entity.targetname
        eventhandler.event_type = 1
        AdditionalEntities.append( eventhandler.ToDict() )
        game_playerdie = True
    return entity

game_playerleave = False
def b1_game_playerleave( index:int, entity:Entity, map:str ):
    global game_playerleave
    if not game_playerleave and entity.targetname == 'game_playerleave':
        eventhandler.target = entity.targetname
        eventhandler.event_type = 2
        AdditionalEntities.append( eventhandler.ToDict() )
        game_playerleave = True
    return entity

game_playerkill = False
def b1_game_playerkill( index:int, entity:Entity, map:str ):
    global game_playerkill
    if not game_playerkill and entity.targetname == 'game_playerkill':
        eventhandler.target = 'game_playerkill_check'
        eventhandler.event_type = 3
        AdditionalEntities.append( eventhandler.ToDict() )
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
        eventhandler.target = entity.targetname
        eventhandler.event_type = 4
        AdditionalEntities.append( eventhandler.ToDict() )
        game_playeractivate = True
    return entity

game_playerjoin = False
def b1_game_playerjoin( index:int, entity:Entity, map:str ):
    global game_playerjoin
    if not game_playerjoin and entity.targetname == 'game_playerjoin':
        eventhandler.target = entity.targetname
        eventhandler.event_type = 5
        Newent = eventhandler.ToDict().copy()
        Newent[ "appearflag_multiplayer" ] = "1" # Only in multiplayer
        AdditionalEntities.append( Newent )
        game_playerjoin = True
    return entity

game_playerspawn = False
def b1_game_playerspawn( index:int, entity:Entity, map:str ):
    global game_playerspawn
    if not game_playerspawn and entity.targetname == 'game_playerspawn':
        eventhandler.target = entity.targetname
        eventhandler.event_type = 6
        AdditionalEntities.append( eventhandler.ToDict() )
        game_playerspawn = True
    return entity

# ==========================================================================================
# Converts all entities that use sounds or sentences by index
# to use sound filenames or sentence names instead.
# ==========================================================================================
DefaultSound = "common/null.wav"
DefaultSentence = ""
DefaultButtonSound = ""
DefaultMomentaryButtonSound = "buttons/button9.wav"
DefaultTrackTrainSound = ""

DoorMoveSounds = [
    DefaultSound,
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

DoorStopSounds = [
    DefaultSound,
    "doors/doorstop1.wav",
    "doors/doorstop2.wav",
    "doors/doorstop3.wav",
    "doors/doorstop4.wav",
    "doors/doorstop5.wav",
    "doors/doorstop6.wav",
    "doors/doorstop7.wav",
    "doors/doorstop8.wav"
]

ButtonSounds = [
    DefaultSound,
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

ButtonLockedSentences = [
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

ButtonUnlockedSentences = [
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

class FixSoundsData:
    def __init__( self, KeyName:str, DefaultValue:str = None, Names:list[str] = None, Optional:str = None ):
        self.KeyName = KeyName
        self.DefaultValue = DefaultValue
        self.Names = Names
        self.Optional = Optional

DoorData = [
    FixSoundsData( "movesnd", DefaultSound, DoorMoveSounds ),
    FixSoundsData( "stopsnd", DefaultSound, DoorStopSounds ),
    FixSoundsData( "locked_sound", DefaultButtonSound, ButtonSounds ),
    FixSoundsData( "unlocked_sound", DefaultButtonSound, ButtonSounds ),
    FixSoundsData( "locked_sentence", DefaultSentence, ButtonLockedSentences ),
    FixSoundsData( "unlocked_sentence", DefaultSentence, ButtonUnlockedSentences )
]

ButtonData = [
    FixSoundsData( "sounds", DefaultButtonSound, ButtonSounds ),
    FixSoundsData( "locked_sound", DefaultButtonSound, ButtonSounds ),
    FixSoundsData( "unlocked_sound", DefaultButtonSound, ButtonSounds ),
    FixSoundsData( "locked_sentence", DefaultSentence, ButtonLockedSentences ),
    FixSoundsData( "unlocked_sentence", DefaultSentence, ButtonUnlockedSentences )
]

MomentaryDoorMoveSounds = [
    DefaultSound,
    "doors/doormove1.wav",
    "doors/doormove2.wav",
    "doors/doormove3.wav",
    "doors/doormove4.wav",
    "doors/doormove5.wav",
    "doors/doormove6.wav",
    "doors/doormove7.wav",
    "doors/doormove8.wav"
]

RotatingMoveSounds = [
    DefaultSound,
    "fans/fan1.wav",
    "fans/fan2.wav",
    "fans/fan3.wav",
    "fans/fan4.wav",
    "fans/fan5.wav"
]

PlatMoveSounds = [
    DefaultSound,
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

PlatStopSounds = [
    DefaultSound,
    "plats/bigstop1.wav",
    "plats/bigstop2.wav",
    "plats/freightstop1.wav",
    "plats/heavystop2.wav",
    "plats/rackstop1.wav",
    "plats/railstop1.wav",
    "plats/squeekstop1.wav",
    "plats/talkstop1.wav"
]

PlatData = [
    FixSoundsData( "movesnd", DefaultButtonSound, PlatMoveSounds ),
    FixSoundsData( "stopsnd", DefaultButtonSound, PlatStopSounds )
]

TrackTrainMoveSounds = [
    "",
    "plats/ttrain1.wav",
    "plats/ttrain2.wav",
    "plats/ttrain3.wav",
    "plats/ttrain4.wav",
    "plats/ttrain6.wav",
    "plats/ttrain7.wav"
]

FixSoundsEntityData = {

    "func_door": DoorData,
    "func_water": DoorData,
    "func_door_rotating": DoorData,
    "momentary_door": FixSoundsData( "movesnd", DefaultSound, MomentaryDoorMoveSounds ),
    "func_rotating": FixSoundsData( "sounds", DefaultSound, RotatingMoveSounds, "message" ),
    "func_button": ButtonData,
    "func_rot_button": ButtonData,
    "momentary_rot_button": FixSoundsData( "sounds", DefaultMomentaryButtonSound, ButtonSounds ),
    "func_train": PlatData,
    "func_plat": PlatData,
    "func_platrot": PlatData,
    "func_trackchange": PlatData,
    "func_trackautochange": PlatData,
    "env_spritetrain": PlatData,
    "func_tracktrain": FixSoundsData( "sounds", DefaultTrackTrainSound, TrackTrainMoveSounds )
}

def TryFixSoundsEnt( entity:dict, Data:FixSoundsData ):
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

def b1_fix_sounds( index:int, entity:Entity, map:str ):
    if entity.classname in FixSoundsEntityData:
        DataFix = FixSoundsEntityData.get( entity.classname )
        if isinstance( DataFix, FixSoundsData ):
            entity = TryFixSoundsEnt( entity.ToDict(), DataFix )
        else:
            for D in DataFix:
                entity = TryFixSoundsEnt( entity.ToDict(), D )
    return entity

# Bruh that last fix was shit, i should have re-imagined it instead of porting it as-is from ConvertSoundIndicesToNamesUpgrade.cs

# ==========================================================================================
# Fixes the use of invalid render color formats in some maps.
# ==========================================================================================
def b1_rendercolor( index:int, entity:Entity, map:str ):
    if entity.rendercolor != None:
        entity.rendercolor = str( Vector( entity.rendercolor ) )
    return entity

# ==========================================================================================
# Prunes excess keyvalues specified for <c>multi_manager</c> entities.
# In practice this only affects a handful of entities used in retinal scanner scripts.
# ==========================================================================================
def b1_multimanager( index:int, entity:Entity, map:str ):
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
            AdditionalEntities.append( b1_multimanager( index, Entity( pEnt ), map ).ToDict() )
            NewEnt[ pEnt.get( "targetname" ) ] = 0
            warn( f"multi_manager exceds max values of 16, Creating a copy for chaining events.")
        entity = Entity( NewEnt )
    return entity

# Over complicated but well, we won't have to worry about broken entity triggering