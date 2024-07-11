import os
from tools.path import unity

def skill_to_json( path='' ):
    filetext = f'{unity}/mods/port/{path}'
    with open( f'{filetext}', 'r' ) as txt, open( filetext.replace( ".cfg", ".json" ), 'w' ) as json:
        print(f'[skill_to_json] Converting {path} to JSON' )
        json.write( '{\n' )
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
            if not FirstLineOf:
                json.write( ',\n' )
            else:
                FirstLineOf = False
            json.write(f'\t"{sk[0]}": {sk[1]}')
        json.write( '\n}' )
        txt.close()
        json.close()
        os.remove( f'{filetext}' )
