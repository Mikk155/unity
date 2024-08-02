# ===============================================================================
# Write a file, alternative for not repacking a small amount of files
# ===============================================================================

import os
from tools.path import port

def writefile( path:str, content:str ):

    if path.find( '/' ) != -1:
        folder = f'{port}\{path}'
        folder = folder[ : folder.rfind( f'/' ) ]

        if not os.path.exists( folder ):
            os.makedirs( folder )

    print( f'Writting {path}' )
    writefile = open( f'{port}/{path}', 'w' )
    writefile.write( content )
    writefile.close()
