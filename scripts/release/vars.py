def env( env: str ) -> str:

    ''' Get enviroment variable'''

    from os import getenv

    var: str = str( getenv( env ) ) if getenv( env ) else '';

    return var

class path:
    
    @staticmethod
    def main() -> str:

        '''Absolute path to this repository's main folder'''

        return path.abs().replace( "scripts\\release", '' );

    @staticmethod
    def abs() -> str:

        '''Absolute path to where this script is'''

        import os

        return os.path.abspath( __file__ ).replace( '\\{}.py'.format( __name__ ), '' );
