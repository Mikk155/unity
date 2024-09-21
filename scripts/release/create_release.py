from github import Github, GithubException
from vars import env

try:

    g = Github( env( "TOKEN" ) );

    repo = g.get_repo( '{}/{}'.format( env( "USER" ), env( "REPOSITORY" ) ) );

    release = repo.create_git_release( env( "VERSION" ), "# {}: {} ({})".format( env( "GAME_NAME" ), env( "MOD_NAME" ), env( "VERSION" ) ), '', draft=False, prerelease=False  );

    print( 'Generated release version {}'.format( env( "VERSION" ) ) );
    print( 'Starting compiling binaries...');

except GithubException as e:

    if e.status == 422:

        print( 'WARNING! version {} Already exists. Update the enviroment variable VERSION in the workflow.'.format( env( "VERSION" ) ) )

    print(e)

    exit(1)
