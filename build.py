import os, zipfile, shutil
from github import Github, GithubException

abs = os.path.abspath( '' )

assets = 'Game-Assets.zip'

token = os.getenv( "TOKEN" )

version = os.getenv( "VERSION" )

user = os.getenv( "USER" )

repository = os.getenv( "REPOSITORY" )

gamename = os.getenv( "GAME_NAME" )

modname = os.getenv( "MOD_NAME" )

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
