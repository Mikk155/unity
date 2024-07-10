import shutil, os
from tools.path import port, halflife

def copy_assets( mod='', assets={} ):
    for In, Out in assets.items():
        if Out.find( '/' ) != -1:
            path = f'{port}\{Out}'
            path = path[ : path.rfind( f'/' ) ]
            if not os.path.exists( path ):
                os.makedirs( path )
        shutil.copy( f'{halflife}\{mod}\{In}', f'{port}\{Out}' )
        print(f'Copying asset {In} > {Out}')
