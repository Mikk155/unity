# This script builds the FGD file with whatever entitydata.json has

from __main__ import abs
from hlunity import jsonc

Language = ''
#Languages = [ 'english', 'spanish' ]
Languages = [ 'english' ]
sentences = {}
entitydata = {}
FGD = None

def description( name, customdata = '', AdditionalData = '' ):

    if customdata == '' and name.startswith( 'EntClass' ):
        name = name[ 8: ]

    fromt = f'{customdata}{AdditionalData}' if customdata != '' else name

    text = sentences.get( fromt, {} ).get( Language, '' ).replace( '\n', '\\n' )

    if text == '' and not fromt.endswith( '::description' ):
        print(f'Missing sentence at "{fromt}" in {Language}')

    return text

def write_keyvalues( entdata, classname ):

    for key, data in entdata.items():

        variable = data.get( "variable", "" )
        value = data.get( "value", "" )

        if key == 'spawnflags':
            FGD.write( f'\tspawnflags(flags) =\n\t[\n' )
            sfbits = data.get( "choices", [] )

            for bits in sfbits:

                titlevar = description( f'{classname}::{key}::{bits}', data.get( "title_choices", {} ).get( f"{bits}", "" ) )
                descrvar = description( f'{classname}::{key}::{bits}::description', data.get( "title_choices", {} ).get( f"{bits}", "" ), "::description" )

                FGD.write( f'\t\t{bits} : "{titlevar}" : 0 : "{descrvar}"\n')

            FGD.write( f'\t]\n' )

        else:

            titlevar = description( f'{classname}::{key}', data.get( "title", "" ) )

            FGD.write( f'\t{key}({variable}) : "{titlevar}" : ' )

            if variable != 'choices':

                number = ( variable in [ "integer", "float" ] )

                if not number:
                    FGD.write( '"' )

                if number:

                    if not value or value == '':

                        if variable == 'float':
                            FGD.write( '0.0' )

                        else:
                            FGD.write( '0' )
                    else:
                        FGD.write( f'{value}' )
                else:
                    FGD.write( f'{value}' )

                if not number:
                    FGD.write( '"' )

                descrvar = description( f'{classname}::{key}::description', data.get( "title", "" ), f'::description' )
                FGD.write( f' : "{descrvar}"\n')

            else:

                descrvar = description( f'{classname}::{key}::description', data.get( "title", "" ), f'::description' )

                FGD.write( f'"{value}" : "{descrvar}" =\n\t[\n' )

                choices = data.get( "choices", [] )

                for choice in choices:

                    titlevar = description( f'{classname}::{key}::{choice}', data.get( "title_choices", {} ).get( f"{choice}", "" ) )
                    descrvar = description( f'{classname}::{key}::{choice}::description', data.get( "title_choices", {} ).get( f"{choice}", "" ), f'::description' )

                    FGD.write( f'\t\t"{choice}" : "{titlevar}" : "{descrvar}"\n')

                FGD.write( f'\t]\n' )

def write_class( entdata={}, name='' ):

    Class = entdata.get( "Class", '' )

    FGD.write( f'@{Class}Class ' )

    for jkey, jvalue in entdata.items():

        if jkey == 'data':
            continue

        elif jkey == 'size':

            min = str(jvalue[0]).replace( ',', '' ).strip( '[' ).strip( ']' )
            FGD.write( f'size( {min}' )

            if len(jvalue) > 1:
                max = str(jvalue[1]).replace( ',', '' ).strip( '[' ).strip( ']' )
                FGD.write( f', {max}' )

            FGD.write( f' ) ' )

        elif jkey == 'base' and len(jvalue) > 0:

            baseclasses = str(jvalue).replace( '\'', '' ).strip( '[' ).strip( ']' )
            FGD.write( f'base( {baseclasses} ) ' )

        elif jkey == 'color':

            colors = str(jvalue).replace( ',', '' ).strip( '[' ).strip( ']' )
            FGD.write( f'color( {colors} ) ' )

        elif jkey == 'studio':

            if isinstance( jvalue, str ):
                FGD.write( f'studio( "{jvalue}" ) ' )

            else:
                FGD.write( f'studio() ' )

        elif jkey == 'sprite':

            if isinstance( jvalue, str ):
                FGD.write( f'sprite( "{jvalue}" ) ' )
            else:
                FGD.write( f'sprite() ' )

        elif jkey == 'flags':

            FGD.write( f'flags( {jvalue} ) ' )

        elif jkey == 'iconsprite':

            FGD.write( f'iconsprite( "{jvalue}" ) ' )

        elif jkey == 'offset':

            offset = str(jvalue).replace( ',', '' ).strip( '[' ).strip( ']' )
            FGD.write( f'offset( {offset} ) ' )

    FGD.write( f'= {name}' )

    if Class == 'Base':
        FGD.write( '\n[\n' )
    else:
        FGD.write( f' : "{description( f"{name}::classname" )}" : "{description(f"{name}::classname::description")}"\n[\n' )

    if "data" in entdata:
        write_keyvalues( entdata.get( "data", {} ), name )

    FGD.write( ']\n\n' )

    if entdata.get( 'point', False ):

        entdata.pop( 'point', '' )
        entdata.pop( 'data', '' )
        entdata[ 'Class' ] = 'Point'
        AddHulls = entdata.get( 'base', [] )

        for b in [ 'Angles', 'Targetx', 'Target', 'Master', 'Global', 'Mandatory' ]:

            if b in AddHulls:
                AddHulls.insert( AddHulls.index( b ) + 1, f'hulls' )
                break

        entdata[ 'base' ] = AddHulls

        write_class( entdata=entdata, name=name )

def write_data( key, value={} ):

    if value.get( 'Class', '' ) in [ 'Point', 'Solid' ] and key != 'worldspawn':

        if len( value.get( 'data', {} ) ) > 0:

            KeyValueDatas = value.get( 'data', {} )
            value.pop( 'data', '' )
            value[ 'own_data' ] = KeyValueDatas

            write_class( entdata={ "Class": "Base", "data": KeyValueDatas }, name=f'EntClass{key}' )

            base = value.get( 'base', [] )

            for b in [ 'Angles', 'Targetx', 'Target', 'Master', 'Global', 'Mandatory' ]:
                if b in base:
                    base.insert( base.index( b ) + 1, f'EntClass{key}' )
                    break

            if not f'EntClass{key}' in base:

                base.insert( 0, f'EntClass{key}')

            value[ 'base' ] = base

        # So not to include them on each entity manually. since all entities supports these
        Mandatory = value.get( 'base', [] )
        Mandatory.append( 'Appearflags' )
        Mandatory.insert( 0, 'Mandatory' )

        value[ 'base' ] = Mandatory

    write_class( entdata=value, name=key )

def build():

    global entitydata
    entitydata = jsonc( f'{abs}/entitydata.json' )
    entitydata.pop( "EOF", '' )

    entities = []
    classess = []

    for ClassName, ClassData in entitydata.items():
        if ClassData.get( 'Class', '' ) in [ 'Point', 'Solid' ]:
            entities.append( ClassName )
        else:
            classess.append( ClassName )

    entities.sort()

    global sentences
    sentences = jsonc( f'{abs}/docs/src/sentences.json' )
    sentences.pop( "EOF", '' )

    for lang in Languages:

        global Language
        Language = lang

        global FGD
        FGD = open( f'{abs}/unity/half-life-unity-{Language}.fgd', 'w' )

        for key in classess:
            write_data( key, entitydata.get( key, {} ) )

        for key in entities:
            write_data( key, entitydata.get( key, {} ) )
