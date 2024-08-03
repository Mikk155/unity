# This script builds the html files in docs/entityguide/entities/ with whatever entitydata.json has

import os
from __main__ import abs
from scripts.jsonc import jsonc

def write_table( classname:str, key:str, values:dict, file=None, choices=None, get='value' ):

    if isinstance( choices, list ) and len(choices) > 0:
        for c in choices:
            write_table( classname, key, values, file=file, get=c )
        return

    altkey = key
    value = values.get( get, "" )
    variable = values.get( "variable", "" )

    if get != 'value':
        altkey += f'::{get}'
        value = get
        variable = 'bits' if key == 'spawnflags' else 'choices'

    file.write( f'\t</tr>\n')
    file.write( f'\t\t<td pkvd="{classname}::{key}"></td>\n')
    file.write( f'\t\t<td>{key}</td>\n')
    file.write( f'\t\t<td>{variable}</td>\n')
    file.write( f'\t\t<td>{value}</td>\n')
    file.write( f'\t\t<td style="text-align: left;" pkvd="{classname}::{key}::description"></td>\n')
    file.write( f'\t</tr>\n')

def read_data( data:dict, classname:str, file ):
    if len( data ) > 0:
        for key, values in data.items():
            write_table( classname, key, values, file=file, choices=values.get( 'choices', [] ) )

def read_base( data:list[str], classname:str, file, entitydata:dict ):
    data.append( 'Appearflags' )
    for base in data:
        read_data( entitydata.get( base, {} ).get( 'data', {} ), classname, file )

def build():

    entitydata = jsonc( open( f'{abs}/entitydata.json', 'r' ).readlines() ).load()

    entities = []

    for ClassName, ClassData in entitydata.items():

        if ClassData.get( 'Class', '' ) in [ 'Point', 'Solid' ]:

            entities.append( ClassName )

    entities.sort()

    entities_html = open( f'{abs}/docs/entities.html', 'w' )

    tabledir = f'{abs}/docs/entityguide/entities/table'

    if not os.path.exists( tabledir ):
        os.makedirs( tabledir )

    for classname in entities:

        entities_html.write( f'<li><button class="menu-firstsub" onclick="SFX(\'sfx_open\');fetchent(\'{classname}\')" onmouseenter="SFX(\'sfx_view\')">{classname}</li>\n' )

        with open( f'{tabledir}/{classname}.html', 'w' ) as entfile:

            entfile.write( f'<h1>{classname}</h1>\n')
            entfile.write( f'<h2 pkvd="{classname}::classname"></h2>\n')
            entfile.write( f'<h3 pkvd="{classname}::classname::description"></h3>\n')
            entfile.write( f'<table border class="EntityKeyValueTable">\n')
            entfile.write( f'\t<th pkvd="Title"></th>\n')
            entfile.write( f'\t<th pkvd="key"></th>\n')
            entfile.write( f'\t<th pkvd="type"></th>\n')
            entfile.write( f'\t<th pkvd="value"></th>\n')
            entfile.write( f'\t<th pkvd="Description"></th>\n')

            read_data( entitydata.get( 'Mandatory', {} ).get( 'data', {} ), classname, entfile )
            read_data( entitydata.get( classname, {} ).get( 'data', {} ), classname, entfile )
            read_base( entitydata.get( classname, {} ).get( 'base', [] ), classname, entfile, entitydata )

            entfile.write( f'</table>\n')
            entfile.write( f'<br><br>\n')

            if os.path.exists( f'{abs}/docs/entityguide/entities/{classname}.html' ):
                entfile.write( f'<div id="entityguide-extra"></div>\n')
