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

EntListing=[]

def description( name, customdata = '', AdditionalData = '' ):
    if customdata == '' and name.startswith( 'EntClass' ):
        name = name[ 8: ]
    return sentences.get( f'{customdata}{AdditionalData}' if customdata != '' else name, {} ).get( 'english', '' ).replace( '\n', '\\n' )

def write_table( classname='', key='', values={}, file=None, choices=[] ):

    if len(choices) > 0:
        for c in choices:
            file.write( f'\t</tr>\n')
            file.write( f'\t\t<td pkvd="{classname}::{key}::{c}"></td>\n')
            file.write( f'\t\t<td>{key}</td>\n')
            file.write( f'\t\t<td>{values.get( "variable", "" )}</td>\n')
            file.write( f'\t\t<td>{c}</td>\n')
            file.write( f'\t\t<td style="text-align: left;" pkvd="{classname}::{key}::{c}::description"></td>\n')
            file.write( f'\t</tr>\n')
    else:
        file.write( f'\t</tr>\n')
        file.write( f'\t\t<td pkvd="{classname}::{key}"></td>\n')
        file.write( f'\t\t<td>{key}</td>\n')
        file.write( f'\t\t<td>{values.get( "variable", "" )}</td>\n')
        file.write( f'\t\t<td>{values.get( "value", "" )}</td>\n')
        file.write( f'\t\t<td style="text-align: left;" pkvd="{classname}::{key}::description"></td>\n')
        file.write( f'\t</tr>\n')

def write_entity( entd={}, classname='', JsonData={} ):
    with open( f'{abs}/docs/entityguide/entities/table/{classname}.html', 'w' ) as file:
        file.write( f'<h1>{classname}</h1>\n')
        file.write( f'<h2 pkvd="{classname}::classname"></h2>\n')
        file.write( f'<h3 pkvd="{classname}::classname::description"></h3>\n')
        file.write( f'<table border class="EntityKeyValueTable">\n')
        file.write( f'\t<th pkvd="Title"></th>\n')
        file.write( f'\t<th pkvd="key"></th>\n')
        file.write( f'\t<th pkvd="type"></th>\n')
        file.write( f'\t<th pkvd="value"></th>\n')
        file.write( f'\t<th pkvd="Description"></th>\n')

        if "base" in entd:
            for base in entd.get( "base", [] ):
                if base.startswith( 'EntClass' ):
                    for bk, bv in entd.get( 'own_data', {} ).items():
                        write_table( classname=classname, key=bk, values=bv, file=file, choices=bv.get( 'choices', [] ) )
                    continue
                baseclasses = JsonData.get( base, {} )
                if 'data' in baseclasses:
                    dataclass = baseclasses.get( 'data', {} )
                    for bk, bv in dataclass.items():
                        write_table( classname=base, key=bk, values=bv, file=file, choices=bv.get( 'choices', [] ) )

        if 'data' in entd:
            dataclass = entd.get( 'data', {} )
            for bk, bv in dataclass.items():
                write_table( classname=classname, key=bk, values=bv, file=file, choices=bv.get( 'choices', [] ) )

        file.write( f'</table>\n')
        file.write( f'<br><br>\n')
        if os.path.exists( f'{abs}/docs/entityguide/entities/{classname}.html' ):
            file.write( f'<div id="entityguide-extra"></div>\n')

def write_keyvalues( entitydata, classname ):
    for key, data in entitydata.items():

        variable = data.get( "variable", "" )
        value = data.get( "value", "" )

        if key == 'spawnflags':
            FGD.write( f'\tspawnflags(flags) =\n\t[\n' )
            sfbits = data.get( "choices", [] )

            for bits in sfbits:
                titlevar = description( f'{classname}::{key}::{bits}', data.get( "title", "" ) )
                descrvar = description( f'{classname}::{key}::{bits}::description', data.get( 'description', '' ) )
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

                descrvar = description( f'{classname}::{key}::description', data.get( "description", "" ) )
                FGD.write( f' : "{descrvar}"\n')
            else:
                descrvar = description( f'{classname}::{key}::description', data.get( "description", "" ) )
                FGD.write( f'"{value}" : "{descrvar}" =\n\t[\n' )
                choices = data.get( "choices", [] )

                for choice in choices:
                    titlevar = description( f'{classname}::{key}::{choice}', data.get( "title_choices", "" ), f'::{choice}' )
                    descrvar = description( f'{classname}::{key}::{choice}::description', data.get( "title_choices", "" ), f'::{choice}::description' )
                    FGD.write( f'\t\t"{choice}" : "{titlevar}" : "{descrvar}"\n')
                FGD.write( f'\t]\n' )



def write_class( entdata={}, FGD=None, name='', JsonData={} ):

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
        if not version:
            write_entity( classname=name, entd=entdata, JsonData=JsonData)
            EntListing.append( name )
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
        write_class( entdata=entdata, FGD=FGD, name=name, JsonData=JsonData )


class jsonc:
    def __init__( self, FileLines : list[ str ] ):
        self.jsdata = ''
        for t, line in enumerate( FileLines ):
            line = line.strip()
            if line and line != '' and not line.startswith( '//' ):
                self.jsdata = f'{self.jsdata}\n{line}'
        self.data = json.loads( self.jsdata )
        self.data.pop( 'EOF', '' )
    def load(self):
        return self.data

with open( f'{abs}/docs/entities.html', 'w' ) as html, open( f'{abs}/unity/half-life-unity.fgd', 'w' ) as FGD, open( f'{abs}/entitydata.json', 'r' ) as Json, open( f'{abs}/docs/src/sentences.json', 'r' ) as sentence:
    JsonData = jsonc( Json ).load()
    sentences = json.load( sentence )

    for key, value in JsonData.items():

        if value.get( 'Class', '' ) in [ 'Point', 'Solid' ] and key != 'worldspawn':
            if len( value.get( 'data', {} ) ) > 0:
                KeyValueDatas = value.get( 'data', {} )
                value.pop( 'data', '' )
                value[ 'own_data' ] = KeyValueDatas
                write_class( FGD=FGD, entdata={ "Class": "Base", "data": KeyValueDatas }, name=f'EntClass{key}', JsonData=JsonData )
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

        write_class( FGD=FGD, entdata=value, name=key, JsonData=JsonData )

    EntListing.sort()
    for entname in EntListing:
        html.write( f'<li><button class="menu-firstsub" onclick="SFX(\'sfx_open\');fetchent(\'{entname}\')" onmouseenter="SFX(\'sfx_view\')">{entname}</li>\n' )

    FGD.close()
    Json.close()
    html.close()
    sentence.close()

# Only release on virtual machine. if run on my local it's only for the website htmls or testing FGD
if not version:
    exit(0)

print( f'Preparing assets...' )

shutil.copytree( f'{abs}/{modname}/', f'{abs}/{gamename}/{modname}/' )

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
