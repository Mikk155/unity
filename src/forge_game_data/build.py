import json, os

abs = os.path.abspath( '' )

sentences={}

def description( name ):
    return sentences.get( name, {} ).get( 'english', '' )

def write_keyvalues( entitydata, classname ):
    for key, data in entitydata.items():

        variable = data.get( "variable", "" )
        value = data.get( "value", "" )

        FGD.write( f'\t{key}({variable}) : "{description( f"{classname}::{key}" )}" : ' )

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

            FGD.write( f' : "{description( f"{classname}::{key}::description" )}"\n')
        else:
            FGD.write( f'"{description( f"{classname}::{key}::description" )}" : "{value}" =\n\t[\n' )
            choices = data.get( "choices", [] )

            for choice in choices:
                FGD.write( f'\t\t"{choice}" : "{description( f"{classname}::{key}::{choice}" )}" : "{description( f"{classname}::{key}::{choice}::description" )}"\n')
            FGD.write( f'\t]\n' )



def write_class( entdata={}, FGD=None, name='', html=None ):

    Class = entdata.get( "Class", '' )

    FGD.write( f'@{Class}Class = {name}' )

    if Class == 'Base':
        FGD.write( '\n[\n' )
    else:
        html.write( f'<th><button class="menu-firstsub" onclick="SFX(\'sfx_open\');fetchent(\'{name}\')" onmouseenter="SFX(\'sfx_view\')">{name}</th>' )
        FGD.write( f' : "{description( f"{name}::classname" )}" : "{description(f"{name}::classname::description")}"\n[\n' )

    if "data" in entdata:
        write_keyvalues( entdata.get( "data", {} ), name )

    FGD.write( ']\n\n' )


with open( f'{abs}/../../docs/entities.html', 'w' ) as html, open( f'{abs}/../../game/half-life-unity.fgd', 'w' ) as FGD, open( f'{abs}/entitydata.json', 'r' ) as Json, open( f'{abs}/../../docs/src/sentences.json', 'r' ) as sentence:
    JsonData = json.load( Json )
    sentences = json.load( sentence )

    for key, value in JsonData.items():

        write_class( FGD=FGD, entdata=JsonData.get( key, {} ), name=key, html=html )

    FGD.close()
    Json.close()
    html.close()
    sentence.close()

exit(0)
