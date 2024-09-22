import hlunity as unity

# Debugging
unity.Logger.set_logger( unity.LogLevel.debug );
unity.Logger.set_logger( unity.LogLevel.info );
unity.Logger.set_logger( unity.LogLevel.error );
unity.Logger.set_logger( unity.LogLevel.warning );

mod_folder = "{}\\bshift".format( unity.HALFLIFE() );

maps = unity.mod.maps.copy( mod_folder );

def PostMapUpgrade( index : int, entity : unity.Entity, map : str ):

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
        entity.classname = 'monster_rosenberg'
        entity.model = None
        entity.body = None

    if map == 'ba_tram1':
        if entity.targetname == 'sitter':
            entity.body = None
        elif entity.classname == 'item_suit':
            entity.clear()

    elif map == 'ba_tram2':
        if entity.targetname == 'joey_normal' or entity.classname == 'joey_reflect':
            entity.skin = 1

    elif map == 'ba_yard1':
        if entity.classname == 'monster_scientist_dead' and entity.body == '3':
            entity.body = 0

    elif map == 'ba_outro':
        if entity.classname == 'trigger_auto' and entity.target == 'start_outro':
            entity.spawnflags = 1
        elif entity.targetname == 'drag_grunt1':
            entity.body = 4
        elif entity.targetname == 'drag_grunt2':
            entity.body = 1

    elif map == 'ba_power2':
        if entity.classname == 'worldspawn':
            entity.chaptertitle = None

    elif map == 'ba_security2':
        if entity.targetname == 'gina_push':
            entity.model = 'models/blueshift/holo_cart.mdl'

    elif map == 'ba_canal1':
        if entity.classname == 'monstermaker' and entity.targetname == 'tele5_spawner' or entity.targetname == 'tele4_spawner':
            entity.netname = None

    return entity

for mapname, path in maps.items():
    map = unity.MapUpgrader( path );
    map.upgrade();
