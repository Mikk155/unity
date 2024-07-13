# ===============================================================================
# FCopy assets from the mod folder to unity/mods/port
# ===============================================================================

import shutil, os

from tools.path import port, halflife

def copy_assets( mod='', assets={} ):

    print(f'Copying asset...')

    for In, Out in assets.items():

        if Out.find( '/' ) != -1:
            path = f'{port}\{Out}'
            path = path[ : path.rfind( f'/' ) ]

            if not os.path.exists( path ):
                os.makedirs( path )

        print(f'{In}  >  {Out}')

        shutil.copy( f'{halflife}\{mod}\{In}', f'{port}\{Out}' )
