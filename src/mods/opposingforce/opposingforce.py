import hlunity as unity

# Debugging
unity.Logger.set_logger( unity.LogLevel.debug );
unity.Logger.set_logger( unity.LogLevel.info );
unity.Logger.set_logger( unity.LogLevel.error );
unity.Logger.set_logger( unity.LogLevel.warning );

import os
import shutil

maps = {}

for root, dirs, files in os.walk( '{}\\gearbox\\maps'.format( unity.HALFLIFE() ) ):
    for file in files:
        if file.endswith( '.bsp' ):
            src = '{}\\gearbox\\maps\\{}'.format( unity.HALFLIFE(), file );
            dest = '{}\\unity_addon\\maps\\{}'.format( unity.HALFLIFE(), file );
            maps[file] = dest;
            shutil.copy2( src, dest );


def PostMapUpgrade( index : int, entity : unity.Entity, map : str ):

    if map == 'of6a1':

        # Sets the <c>assassin4_spawn</c> <c>monstermaker</c> in <c>of6a1</c> to spawn a Black Ops assassin immediately
        # to make the switch from prisoner less obvious.'''
        if entity.classname == 'monstermaker' and entity.targetname == 'assassin4_spawn':
            entity.delay = 0;

    elif map == 'of0a0':

        # Disables item dropping for a couple NPCs in the Opposing Force intro map so players can't get weapons from them if they die.
        if entity.targetname in [ 'ichabod', 'booth' ]:
            entity.allow_item_dropping = 0;

    elif map == 'of1a1':

        # Updates the stretcher grunt's body value to make the grunt's weapon invisible.
        if entity.targetname == 'stretcher_grunt':
            entity.body = 17;

    elif map == 'of1a4b':

        # Changes the loader entity's skin in <c>of1a4b</c> to use the correct crate texture.
        if entity.classname == 'monster_op4loader':
            entity.skin = 1;

    return entity

for mapname, path in maps.items():
    map = unity.MapUpgrader( path );
    map.Upgrades.OpposingForce = True;
    map.upgrade();
