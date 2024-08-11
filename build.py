import os, shutil, zipfile, subprocess
from github import Github, GithubException

abs = os.path.abspath( '' )

assets = 'Game-Assets.zip'

TOKEN = os.getenv( "TOKEN" )

VERSION = os.getenv( "VERSION" )

USER = os.getenv( "USER" )

REPOSITORY = os.getenv( "REPOSITORY" )

GAME_NAME = os.getenv( "GAME_NAME" )

MOD_NAME = os.getenv( "MOD_NAME" )

from scripts.forgegamedata import build
print(f'Building FGD File...')
build()

# Only release on virtual machine. if run on my local it's only for the website htmls or testing FGD
if not TOKEN:

    import importlib

    importlib.import_module( f'scripts.entityguide' ).build()

    exit(0)

def mods_installer():

    for root, dirs, files in os.walk( f'{abs}/unity/mods/' ):

        if root[:len(root)-1].endswith( 'mods' ):

            for file in files:

                if file.endswith( '.py' ):

                    print(f'Building executable script for porting tool "{file}"')

                    process = subprocess.Popen( f'pyinstaller --onefile "{abs}/unity/mods/{file}"', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
                    process.wait()

                    shutil.copy( f'{abs}/dist/{file.replace( ".py", ".exe" )}', f'{abs}/unity/mods/' )

                    # Cleanup
                    os.remove( f'{abs}/{file.replace( ".py", ".spec" )}')
                    os.remove( f'{abs}/dist/{file.replace( ".py", ".exe" )}')

# mods_installer()

print( f'Copying game assets...' )

shutil.copytree( f'{abs}/{MOD_NAME}/', f'{abs}/{GAME_NAME}/{MOD_NAME}/' )

with zipfile.ZipFile( assets, 'w', zipfile.ZIP_DEFLATED ) as z:

    for root, dirs, files in os.walk( f'{GAME_NAME}' ):

        for file in files:

            print( f'{root}\\{file}' )

            p = os.path.join( root, file )

            z.write( p, os.path.relpath( p, f'{MOD_NAME}' ) )

    z.close()

try:

    g = Github( TOKEN )

    repo = g.get_repo( f'{USER}/{REPOSITORY}' )

    release = repo.create_git_release( VERSION, f"# {GAME_NAME}: {MOD_NAME} ({VERSION})", '', False, False )

    print( f'Generating release version {VERSION}' )

    release.upload_asset( f'{abs}/{assets}', label=assets )

    print( f'Assets uploaded at https://github.com/{USER}/{REPOSITORY}/releases/tag/{VERSION}' )

except GithubException as e:

    if e.status == 422:

        print( f'WARNING! version {VERSION} Already exists. Update the enviroment variable VERSION in the workflow.' )

    print(e)

    exit(1)
