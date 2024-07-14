# ===============================================================================
# Upgrade map's entity data
# ===============================================================================

import os
import json
import inspect
import subprocess
import tools.upgrades as upgrades

# This may be slow but i did it this way so "upgrades" can be easly implemented
def upgrade_map( entdata=[], mapname='' ):

    for i, e in enumerate( entdata ):

        entblock = json.loads(e)

        for name, obj in inspect.getmembers( upgrades ):

            if name.startswith('__') and name.endswith('__'):
                continue

            if inspect.isfunction(obj):

                if name.startswith( 'map_' ) and name != f'map_{mapname}':
                    continue

                entblock = obj( entblock, entdata=entdata )

        if len( entblock ) > 0:
            entdata[i] = json.dumps( entblock )

    return entdata

from tools.path import port, tools

from tools.steam_installation import STEAM_IS64

def map_upgrader():

    MAPENTS = {}

    RIPENT = f'{tools}/' + 'Ripent.exe' if STEAM_IS64 else 'Ripent_x64'

    BSP_SOURCES = {}

    for file in os.listdir( f'{port}/maps/'):
        if file.endswith( ".bsp" ):
            map = file[ : len(file) - 4 ]
            bsp = f'{map}.bsp'
            ent = f'{map}.ent'

            BSP_SOURCES[ map ] = ent
            subprocess.call( [ RIPENT, "-export", f'{port}/maps/{ent}' ], stdout = open( os.devnull, "wb" ) )

            entdata = []

            with open( f'{port}/maps/{ent}', 'r', errors='ignore' ) as entfile:

                lines = entfile.readlines()

                entity = {}
                oldline = ''

                for line in lines:

                    if line == '{':
                        continue

                    line = line.strip()

                    if not line.endswith( '"' ): # ba_tram2.ent's "wad" was broken
                        oldline = line # This is some sort of stupid fix i've did
                    elif oldline != '' and not line.startswith( '"' ): # Hopefully momentarly.
                        line = f'{oldline}{line}'

                    line = line.strip( '"' )

                    if not line or line == '':
                        continue

                    if line.startswith( '}' ): # startswith due to [NULL]
                        entdata.append( json.dumps( entity ) )
                        entity.clear()
                    else:
                        keyvalues = line.split( '" "' )
                        if len( keyvalues ) == 2:
                            entity[ keyvalues[0] ] = keyvalues[1]

                entfile.close()

            MAPENTS[ map ] = entdata

    for m, data in MAPENTS.items():

        newdata = upgrade_map( entdata=data, mapname=m )

        print(f'[map_upgrader] Upgrading {m}')

        with open( f'{port}/maps/{m}.ent', 'w' ) as entfiles:

            for entblock in newdata:

                entfiles.write( '{\n' )

                for key, value in json.loads( entblock ).items():

                    entfiles.write( f'"{key}" "{value}"\n' )

                entfiles.write( '}\n' )

            entfiles.close()

        #subprocess.call( [ RIPENT, "-import", f'{port}/maps/{m}.ent' ], stdout = open( os.devnull, "wb" ) )

    if len( BSP_SOURCES ) == 0:
        return
