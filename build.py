import os, zipfile, shutil, json
from github import Github, GithubException

abs = os.path.abspath( '' )

assets = 'Game-Assets.zip'

token = os.getenv( "TOKEN" )

version = os.getenv( "VERSION" )

user = os.getenv( "USER" )

repository = os.getenv( "REPOSITORY" )

gamename = os.getenv( "GAME_NAME" )

modname = os.getenv( "MOD_NAME" )

sentences={}

def description( name ):
    return sentences.get( name, {} ).get( 'english', '' )

def write_keyvalues( entitydata, classname ):
    for key, data in entitydata.items():

        variable = data.get( "variable", "" )
        value = data.get( "value", "" )

        if variable == 'flags':
            FGD.write( f'\tspawnflags(flags) =\n\t[\n' )
            sfbits = data.get( "choices", [] )

            for bits in sfbits:
                FGD.write( f'\t\t{bits} : "{description( f"{classname}::{key}::{bits}" )}" : 0 : "{description( f"{classname}::{key}::{bits}::description" )}"\n')
            FGD.write( f'\t]\n' )
        else:

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
        html.write( f'<li><button class="menu-firstsub" onclick="SFX(\'sfx_open\');fetchent(\'{name}\')" onmouseenter="SFX(\'sfx_view\')">{name}</li>\n' )
        FGD.write( f' : "{description( f"{name}::classname" )}" : "{description(f"{name}::classname::description")}"\n[\n' )

    if "data" in entdata:
        write_keyvalues( entdata.get( "data", {} ), name )

    FGD.write( ']\n\n' )

with open( f'{abs}/docs/entities.html', 'w' ) as html, open( f'{abs}/game/half-life-unity.fgd', 'w' ) as FGD, open( f'{abs}/entitydata.json', 'r' ) as Json, open( f'{abs}/docs/src/sentences.json', 'r' ) as sentence:
    JsonData = json.load( Json )
    sentences = json.load( sentence )

    for key, value in JsonData.items():

        write_class( FGD=FGD, entdata=JsonData.get( key, {} ), name=key, html=html )

    FGD.close()
    Json.close()
    html.close()
    sentence.close()

# Only release on virtual machine. if run on my local it's only for the website htmls or testing FGD
if not version:
    exit(0)

print( f'Preparing assets...' )

shutil.copytree( f'{abs}/game/', f'{abs}/{gamename}/{modname}/' )

with zipfile.ZipFile( assets, 'w', zipfile.ZIP_DEFLATED ) as z:

    for root, dirs, files in os.walk( f'{gamename}' ):

        for file in files:

            print( f'{root}\\{file}' )

            p = os.path.join( root, file )

            z.write( p, os.path.relpath( p, f'{modname}' ) )

    z.close()

try:
        
    g = Github( token )

    repo = g.get_repo( f'{user}/{repository}' )

    release = repo.create_git_release( version, f"# {gamename}: {modname} ({version})", '', False, False )

    print( f'Generating release version {version}' )

    release.upload_asset( f'{abs}/{assets}', label=assets )

    print( f'Assets uploaded at https://github.com/{user}/{repository}/releases/tag/{version}' )

except GithubException as e:

    if e.status == 422:

        print( f'WARNING! version {version} Already exists. Update the enviroment variable VERSION in the workflow.' )

    exit(1)
