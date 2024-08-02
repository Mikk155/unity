# ===============================================================================
# Upgrade map's entity data
# ===============================================================================

import os
import json
import inspect
import tools.upgrades as upgrades
import __main__ as main
from tools.Entity import Entity

new_entities = []

def add_entity( entity:Entity ):
    global new_entities
    new_entities.append( entity if isinstance( entity, dict ) else entity.ToDict() )

def HookMembers( index:int, entblock:Entity, entdata:list[dict], map:str, obj, name:str ):
    if not inspect.isfunction(obj):
        return entblock.ToDict()
    for name in [ 'index', 'entity', 'map' ]:
        if not name in inspect.signature(obj).parameters:
            return entblock.ToDict()
    return obj( index, entblock, map ).ToDict()

def upgrade_map( entdata=[], mapname='' ):

    TempEntData = entdata.copy()

    for i, entblock in enumerate( TempEntData ):

        for name, obj in inspect.getmembers( upgrades ):
            entblock = HookMembers( i, Entity( entblock ), entdata, mapname, obj, name )
        for name, obj in inspect.getmembers( main ):
            entblock = HookMembers( i, Entity( entblock ), entdata, mapname, obj, name )

        entdata[i] = ( json.dumps( entblock ) if len( entblock ) > 0 else {} )

    for ae in upgrades.AdditionalEntities:
        entdata.append( json.dumps( ae ) )
    global new_entities
    for ae in new_entities:
        entdata.append( json.dumps( ae ) )

    new_entities = []
    upgrades.AdditionalEntities = []

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
                if len(entblock) <= 0:
                    continue
                newdata += '{\n'
                if not isinstance( entblock, dict ):
                    entblock = json.loads( entblock )
                for key, value in entblock.items():
                    newdata += f'"{key}" "{value}"\n'
                newdata += '}\n'

            bsp_read( f'{port}/maps/{bsp}', writedata=newdata )
            os.remove( f'{port}/maps/{ent}' )
