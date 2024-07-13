# ===============================================================================
# convert skill.cfg to our json-formatting skills
# ===============================================================================

import os

from tools.path import port, unity
from tools.jsonc import load_json

def skill_to_json( path='' ):

    filetext = f'{port}/{path}'

    print(f'[skill_to_json] Converting {path} to JSON' )

    with open( f'{filetext}', 'r' ) as txt, open( filetext.replace( ".cfg", ".json" ), 'w' ) as jsonfile:

        ogskills = load_json( path=f'{unity}/cfg/skill.json' )

        jsonfile.write( '{\n' )
        FirstLineOf = True
        lines = txt.readlines()

        for line in lines:
            line = line.strip()

            if not line or line == '' or line.startswith( '//' ):
                continue

            sk = line.split()
            sk[0] = sk[0].strip()
            if len(sk) <= 2:
                sk.append( '0' )
            sk[1] = sk[1].strip()
            sk[1] = sk[1].strip( '"' )

            if sk[0].startswith( 'sk_' ):
                sk[0] = sk[0][ 3 : ]

            # Compare with the original skills
            if sk[0] in ogskills or sk[0][ len(sk[0]) - 1 : ] in [ '1', '2', '3' ] and sk[0][ : len(sk[0]) - 1  ] in ogskills:
                continue

            if not FirstLineOf:
                jsonfile.write( ',\n' )
            else:
                FirstLineOf = False

            jsonfile.write(f'\t"{sk[0]}": {sk[1]}')

        jsonfile.write( '\n}\n' )

        txt.close()
        jsonfile.close()

        os.remove( f'{filetext}' )
