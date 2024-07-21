# ===============================================================================
# Upgrade map's entity data
# ===============================================================================

import os
import json
import inspect
import tools.upgrades as upgrades
from tools.Entity import Entity

AdditionalEntities = []
# This may be slow but i did it this way so "upgrades" can be easly implemented
def upgrade_map( entdata=[], mapname='' ):

    TempEntData = entdata.copy()

    for i, entblock in enumerate( TempEntData ):

        for name, obj in inspect.getmembers( upgrades ):

            if name.startswith('__') and name.endswith('__'):
                continue

            if inspect.isfunction(obj):

                if name.startswith( 'map_' ) and name != f'map_{mapname}' or name.startswith( 'serie_' ) and not mapname.startswith( name[ 6 : ] ):
                    continue

                entity = Entity( entblock )
                entity = obj( entity )
                entblock = entity.ToDict()

        entdata[i] = ( json.dumps( entblock ) if len( entblock ) > 0 else {} )

    if False:
        if os.path.exists( f'{port}/maps/{mapname}.json'):
            with open( f'{port}/maps/{mapname}.json', 'r' ) as addent:
                additionalentities = json.load( addent )
                for newent in additionalentities:
                    entdata.append( json.dumps( newent ) )

    for ae in upgrades.AdditionalEntities:
        entdata.append( json.dumps( ae ) )

    return entdata

from tools.path import port, tools
from tools.bsp_read import bsp_read

def map_upgrader():

    for file in os.listdir( f'{port}/maps/'):
        if file.endswith( ".bsp" ):
            map = file[ : len(file) - 4 ]
            bsp = f'{map}.bsp'
            ent = f'{map}.json'

            lines = bsp_read( f'{port}/maps/{bsp}' )

            if lines == None:
                continue

            entity = {}
            entdata = []
            oldline = ''

            for line in lines:

                if line == '{':
                    continue

                line = line.strip()

                if not line.endswith( '"' ):
                    oldline = line
                elif oldline != '' and not line.startswith( '"' ):
                    line = f'{oldline}{line}'

                if line.find( '\\' ) != -1:
                    line = line.replace( '\\', '\\\\' )

                line = line.strip( '"' )

                if not line or line == '':
                    continue

                if line.startswith( '}' ): # startswith due to [NULL]
                    entdata.append( json.loads( json.dumps( entity ) ) )
                    entity.clear()
                else:
                    keyvalues = line.split( '" "' )
                    if len( keyvalues ) == 2:
                        entity[ keyvalues[0] ] = keyvalues[1]

            print(f'[map_upgrader] Upgrading {map}')

            entdata = upgrade_map( entdata=entdata, mapname=map )

            with open( f'{port}/maps/{ent}', 'w', encoding='ascii' ) as jsonfile:

                jsonfile.write( '[\n' )
                FirstBlockOf = True
                FirstKeyOf = True

                for entblock in entdata:

                    if len(entblock) <= 0 or not isinstance( entblock, str ):
                        continue

                    if FirstBlockOf:
                        FirstBlockOf = False
                    else:
                        jsonfile.write( ',\n' )

                    FirstKeyOf = True

                    jsonfile.write( '\t{\n' )

                    for key, value in json.loads( entblock ).items():

                        if FirstKeyOf:
                            FirstKeyOf = False
                        else:
                            jsonfile.write( ',\n' )

                        jsonfile.write( f'\t\t"{key}": "{value}"' )

                    jsonfile.write( '\n\t}' )

                jsonfile.write( '\n]\n' )
                jsonfile.close()

            newdata = ''

            for entblock in entdata:
                newdata += '{\n'
                if not isinstance( entblock, dict ):
                    entblock = json.loads( entblock )
                for key, value in entblock.items():
                    newdata += f'"{key}" "{value}"\n'
                newdata += '}\n'

            #bsp_read( f'{port}/maps/{bsp}', writedata=newdata )

        #os.remove( f'{port}/maps/{ent}' )
