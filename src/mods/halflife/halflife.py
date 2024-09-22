import hlunity as unity

# Debugging
unity.Logger.set_logger( unity.LogLevel.debug );
unity.Logger.set_logger( unity.LogLevel.info );
unity.Logger.set_logger( unity.LogLevel.error );
unity.Logger.set_logger( unity.LogLevel.warning );

mod_folder = "{}\\valve".format( unity.HALFLIFE() );

maps = unity.mod.maps.copy( mod_folder );

def PostMapUpgrade( index : int, entity : unity.Entity, map : str ):

    if map == 'c2a2a':
        if entity.classname == 'worldspawn':
            entity.MaxRange = 8192

    elif map == 'c4a2':
        # Fixes Nihilanth's dialogue not playing at the start of <c>c4a2</c> (Gonarch's Lair).
        if entity.target == 'c4a2_startaudio':
            entity.triggerstate = 1;

    elif map == 'c2a5':
        # Removes the <c>globalname</c> keyvalue from the <c>func_breakable</c> crates next to the dam in <c>c2a5</c>.
        # The globalname is left over from copy pasting the entity from the crates in the tunnel earlier in the map
        # and causes these crates to disappear.
        if entity.classname == 'func_breakable' and entity.targetname == 'artillery_deploy3_expl' and entity.globalname == 'c2a4g_crate4':
            entity.globalname = None;

    elif map == 'c3a2':
        # Increases the reload delay after killing the scientist in <c>c3a2</c>
        # to allow the entire game over message to display.
        if entity.targetname == 'c3a2_restart':
            entity.loadtime = 10;

    elif map == 'c4a3':
        # Fixes the flare sprites shown during Nihilanth's death script using the wrong render mode.
        if entity.classname == 'env_sprite' and entity.model == 'sprites/XFlare3.spr':
            entity.rendermode = 5;
            entity.renderamt = 255;

    elif map == 'c2a5':
        # Fixes the barrels in <c>c2a5</c> not flying as high as they're supposed to on modern systems due to high framerates.

        if entity.classname == 'multi_manager': # Remove the second push trigger to avoid re-enabling it.
            if entity.targetname in [ 'can_expl2_mm', 'can_expl4_mm', 'can_expl5_mm' ]:
                entity.pop( entity.targetname.replace( '_mm', '_push' ), '' );
        elif entity.classname == 'func_pushable':
            if entity.targetname in [ 'can_expl2_shoot', 'can_expl4_shoot', 'can_expl5_shoot' ]:
                # Nudge this pushable up by a unit.
                # This prevents the pushable getting stuck in the ground.
                # If the player uses a radius damage attack directed at the middle of the road
                # (dead ahead exiting the tunnel)
                # the specific entity setup used here won't allow the pushable to fly up otherwise
                # because the engine thinks the pushable is somewhere else/outside the world.
                # Specifically, when breakables are destroyed they clear the groundentity variable for entities
                # (see CBreakable::Die)
                # This particular entity setup happens to cause the variable to be cleared at just the right time
                # for the pushable to touch the push trigger.
                # This doesn't happen if a RadiusDamage attack is used due to slight timing changes.
                # Only can_expl2_shoot has shown this behavior but just to be safe all of them are modified.
                origin: unity.Vector = unity.Vector( str( entity.origin ) );
                origin.z += 1;
                entity.origin = origin;

        elif entity.classname == 'trigger_push':
            if entity.targetname in [ 'can_expl2_push', 'can_expl4_push', 'can_expl5_push' ]:
                spawnflags = int( entity.spawnflags ) if entity.spawnflags else 0;
                spawnflags |= ( 1 << 0 );
                entity.spawnflags = spawnflags;

    elif map == 'c3a2b':
        # Prevents players from soft-locking the game by turning both valves at the same time in c3a2b (Lambda Core reactor water flow).

        if entity.target in [ 'ms1', 'ms2' ]:
            entity.master = 'valve_ms';
        elif entity.targetname in [ 'mm3', 'mm4' ]:
            entity.valve_ms_relay = 0.0; # Disable valves on start
        # Enable when the water stops moving
        elif entity.targetname in [ 'core1', 'core2' ]:
            entity.message = "valve_ms_relay";
        # Lock the valves while the water is moving
        elif entity.classname == 'worldspawn':
            multisource = unity.Entity();
            multisource.classname = 'multisource';
            multisource.targetname = 'valve_ms';
            unity.add_entity( multisource );
            relay = unity.Entity();
            relay.classname = 'trigger_relay';
            relay.targetname = 'valve_ms_relay';
            relay.target = 'valve_ms';
            unity.add_entity( relay );
            # Set initial multisource state to enabled
            auto = unity.Entity();
            auto.classname = 'trigger_auto';
            auto.spawnflags = 1; # Remove on fire
            auto.target = 'valve_ms_relay';
            unity.add_entity( auto );

    return entity


for mapname, path in maps.items():
    map = unity.MapUpgrader( path );
    map.upgrade();
