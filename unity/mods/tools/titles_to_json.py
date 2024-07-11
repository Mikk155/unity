import os
from tools.path import unity

def titles_to_json( path='' ):
    filetext = f'{unity}/mods/port/{path}'
    with open( f'{filetext}', 'r' ) as txt, open( filetext.replace( ".txt", ".json" ), 'w' ) as json:
        print(f'[titles_to_json] Converting {path} to JSON' )
        json.write( '{\n' )
        FirstLineOf = True
        lines = txt.readlines()
        Title = ''
        Message = ''
        Params = {}
        for line in lines:
            line = line.strip()
            if not line or line == '' or line.startswith( '//' ) or line.startswith( '{' ):
                continue
            if line.startswith( '}' ):
                if not FirstLineOf:
                    json.write( ',\n' )
                else:
                    FirstLineOf = False
                Message = Message.replace( '"', '\\"')
                json.write(f'\t"{Title}":\n')
                json.write('\t{\n')
                FirstSegOf = True
                for p, a in Params.items():
                    if not FirstSegOf:
                        json.write( ',\n' )
                    else:
                        FirstSegOf = False
                    s = str(a).replace("'", "")
                    json.write(f'\t\t"{p}": {s}')
                if not FirstSegOf:
                    json.write(f',\n')
                json.write(f'\t\t"english": "{Message}"\n')
                json.write('\t}')
                Message = ''
                Title = ''
            elif line.startswith( '$' ):
                line = line[ 1: ]
                parameters = line.split()
                if len(parameters) > 1:
                    if len(parameters) > 2:
                        pairs = parameters.copy()
                        pairs.pop(0)
                        Params[ parameters[0] ] = pairs
                    else:
                        try:
                            Params[ parameters[0] ] = float(parameters[1])
                        except Exception as e:
                            Params[ parameters[0] ] = 0
            elif not Title or Title == '':
                Title = line
            else:
                Message = f'{Message}{line}\\n'
        json.write( '\n}' )
        txt.close()
        json.close()
        os.remove( f'{filetext}' )
