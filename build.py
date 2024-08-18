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
