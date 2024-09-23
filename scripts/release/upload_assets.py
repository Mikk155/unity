import zipfile
from os import walk
import os.path as ospath
from github import Github
from shutil import copytree
from vars import env, path

print( "Copying game assets..." );

copytree( '{}/{}/'.format( path.main(), env( "MOD_NAME" ) ), '{}/{}/{}/'.format( path.main(), env( "GAME_NAME"), env( "MOD_NAME" ) ) );

with zipfile.ZipFile( "Game-Assets.zip", 'w', zipfile.ZIP_DEFLATED ) as z:

    for root, dirs, files in walk( '{}/{}'.format( path.main(), env( "GAME_NAME" ) ) ):

        for file in files:

            print( f'{root}\\{file}' );

            p = ospath.join( root, file );

            z.write( p, ospath.relpath( p, env( "MOD_NAME" ) ) );

    z.close();

g = Github( env( "TOKEN" ) );

repom = g.get_repo( '{}/{}'.format( env( "USER" ), env( "REPOSITORY" ) ) );

releases = repom.get_releases();

release = None;

for r in releases:

    if r.tag_name == env( "VERSION" ):

        release = r;

        file_path = '{}/Game-Assets.zip'.format( path.main() );

        release.upload_asset( file_path, label="Game-Assets.zip" );

        print( 'Uploaded "Game-Assets.zip" to "{}"'.format( env( "VERSION" ) ) );

        break;
