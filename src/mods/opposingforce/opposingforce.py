import hlunity as unity

# Debugging
unity.Logger.set_logger( unity.LogLevel.debug );
unity.Logger.set_logger( unity.LogLevel.info );
unity.Logger.set_logger( unity.LogLevel.error );
unity.Logger.set_logger( unity.LogLevel.warning );

mod_folder = "{}\\gearbox".format( unity.HALFLIFE() );

maps = unity.mod.maps.copy( mod_folder );

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

    # Fixes <c>monster_generic</c> entities that use <c>hgrunt_opfor.mdl</c> to use the correct body value.
    elif map == 'of2a2':

        if entity.targetname in [ 'fgrunt1', 'fgrunt2' ]:
            entity.body = 1;

    # Fixes the Pit Worm's Nest bridge possibly breaking if triggered too soon.
    elif map == 'of4a4':

        if entity.targetname == 'kill_pitworm_mm':
            entity.bridge_global_trigger = 30;
            entity.bridge_mm = 30;

    # Fixes the Bullsquids in <c>of5a2</c> having the wrong targetnames causing the eating scripts to fail.
    elif map == 'of5a2':

        if entity.targetname == 't27':
            entity.targetname = 'feeder_1';
        elif entity.targetname == 't6':
            entity.targetname = 'feeder_2';

    # Adds a missing <c>.wav</c> extension to the sound played when the Geneworm enters in <c>of6a5</c>.
    elif map == 'of6a5':

        if entity.targetname == 'genearrivesound':
            entity.message += '.wav';

    # Prevents the Osprey in <c>ofboot1</c> from switching to the <c>rotor</c> animation and falling through the ground after loading a save game.
    elif map == 'ofboot1':

        if entity.classname == 'scripted_sequence' and entity.m_iszEntity == 'osprey':
            # Naming the script prevents it from immediately completing and removing the script itself.
            entity.targetname = 'osprey_script';

    return entity

for mapname, path in maps.items():
    map = unity.MapUpgrader( path );
    map.Upgrades.OpposingForce = True;
    map.upgrade();
