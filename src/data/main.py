from os import path, listdir, makedirs
from hlunity import jsonc

abs = '{}\\'.format( path.abspath( "" ) )

Language = ''
sentences = {}
entitydata = {}
FGD = None
Hammer = None

def get_lang( label ):
    if label:
        if label in sentences:
            return sentences.get( label, {} ).get( Language, sentences.get( label, {} ).get( 'english', '' ) )
        elif not label.endswith( '::description' ):
            print( "No label {} in {}".format( Language, label ) )
    return ''

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
            sfbits = data.get( "choices", {} )

            for bits, bdata in sfbits.items():

                FGD.write( f'\t\t{bits} : "{get_lang( bdata.get( "title", "" ) )}" : 0 : "{get_lang( bdata.get( "description", "" ) )}"\n')

            FGD.write( f'\t]\n' )

        else:

            global Hammer
            if Hammer and False:
                variables = {
                    "sky": "string",
                    "float": "string",
                    "scale": "string",
                    "vector": "string",
                    "target_name_or_class": "target_destination",
                    "target_generic": "target_destination"
                    }
                if variable in variables:
                    variable = variables[ variable ]

            FGD.write( f'\t{key}({variable}) : "{get_lang( data.get( "title", "" ) )}" : ' )

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

                FGD.write( f' : "{get_lang( data.get( "description", "" ) )}"\n')

            else:

                FGD.write( f'"{value}" : "{get_lang( data.get( "description", "" ) )}" =\n\t[\n' )

                choices = data.get( "choices", {} )

                for choice, bchoice in choices.items():
                    FGD.write( f'\t\t"{choice}" : "{get_lang( bchoice.get( "title", "" ) )}" : "{get_lang( bchoice.get( "description", "" ) )}"\n')

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
        FGD.write( f' : "{get_lang( entdata.get( "title", "" ) )}" : "{get_lang( entdata.get( "description", "" ) )}"\n[\n' )

    if "data" in entdata:
        write_keyvalues( entdata.get( "data", {} ), name )

    FGD.write( ']\n\n' )

    if entdata.get( 'point', False ):

        entdata.pop( 'point', '' )
        entdata.pop( 'data', '' )
        entdata[ 'Class' ] = 'Point'
        AddHulls = entdata.get( 'base', [] ).copy()

        if not 'hulls' in AddHulls:
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

            if not f'EntClass{key}' in base:

                for b in [ 'Angles', 'Targetx', 'Target', 'Master', 'Global', 'Mandatory' ]:
                    if b in base:
                        base.insert( base.index( b ) + 1, f'EntClass{key}' )
                        break

                if not f'EntClass{key}' in base:

                    base.insert( 0, f'EntClass{key}')

                value[ 'base' ] = base

        # So not to include them on each entity manually. since all entities supports these
        Mandatory = value.get( 'base', [] )
        if not 'Appearflags' in Mandatory:
            Mandatory.append( 'Appearflags' )
        if not 'Mandatory' in Mandatory:
            Mandatory.insert( 0, 'Mandatory' )

        value[ 'base' ] = Mandatory

    write_class( entdata=value, name=key )

def build():

    global entitydata

    for file in listdir( '{}base'.format( abs ) ):
        try:
            entitydata[ file[ : len(file) - len('.json') ] ] = jsonc( '{}base\\{}'.format( abs, file ) )
        except Exception as e:
            print( "Failed to open {}: {}".format( file, e ) );
    for file in listdir( '{}entities'.format( abs ) ):
        try:
            entitydata[ file[ : len(file) - len('.json') ] ] = jsonc( '{}entities\\{}'.format( abs, file ) )
        except Exception as e:
            print( "Failed to open {}: {}".format( file, e ) );

    entities = []
    classess = []

    for ClassName, ClassData in entitydata.items():
        if ClassData.get( 'Class', '' ) in [ 'Point', 'Solid' ]:
            entities.append( ClassName )
        else:
            classess.append( ClassName )

    entities.sort()

    global sentences
    sentences = jsonc( '{}..\\..\\docs\\src\\sentences.json'.format( abs ) )

    Languages = sentences.get( "languages", [ 'english' ] )

    programs = [ 'Hammer', 'JACK' ]

    for program in programs:

        global Hammer
        Hammer = ( program == 'Hammer' )

        for lang in Languages:

            global Language
            Language = lang

            if not path.exists( '{}\\..\\..\\unity\\tools\\fgd\\{}\\'.format( abs, program ) ):
                makedirs( '{}\\..\\..\\unity\\tools\\fgd\\{}\\'.format( abs, program ) )

            global FGD
            FGD = open( '{}..\\..\\unity\\tools\\fgd\\{}\\halflife-unity-{}.fgd'.format( abs, program, Language ), 'w' )


            FGD.write( '''
//============ Copyright 1996-2005, Valve Corporation, All rights reserved. ============//
//                                                                                      //
// Purpose: Half-Life: Unity game definition file (.fgd)                                //
//                                                                                      //
// This file has been generated by a python script                                      //
// https://github.com/Mikk155/unity/blob/master/src/data/main.py                        //
//                                                                                      //
// DO NOT MODIFY THIS FILE, SEE https://github.com/Mikk155/unity/tree/master/src/data   //
//                                                                                      //
//======================================================================================//

''' )

            for key in classess:
                write_data( key, entitydata.get( key, {} ).copy() )

            for key in entities:
                write_data( key, entitydata.get( key, {} ).copy() )

build()