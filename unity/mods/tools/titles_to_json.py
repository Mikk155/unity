# ===============================================================================
# convert titles.txt to our json-formatted titles
# ===============================================================================

import os

from tools.path import port, unity
from tools.jsonc import load_json

def titles_to_json( path='' ):

    filetext = f'{port}/{path}'

    print(f'[titles_to_json] Converting {path} to JSON' )

    with open( f'{filetext}', 'r' ) as txt, open( filetext.replace( ".txt", ".json" ), 'w' ) as jsfile:

        ogtitles = load_json( path=f'{unity}/cfg/titles.json' )

        jsfile.write( '{\n' )
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

                Message = Message.replace( '"', '\\"')

                # Compare with the original titles
                if Title in ogtitles and Message == ogtitles.get( Title, {} ).get( "english", "" ).replace( '\n', '\\n' ):
                    Message = ''
                    Title = ''
                    continue

                if not FirstLineOf:
                    jsfile.write( ',\n' )
                else:
                    FirstLineOf = False

                jsfile.write(f'\t"{Title}":\n')
                jsfile.write('\t{\n')
                FirstSegOf = True

                for p, a in Params.items():

                    if not FirstSegOf:
                        jsfile.write( ',\n' )
                    else:
                        FirstSegOf = False

                    s = str(a).replace("'", "")
                    jsfile.write(f'\t\t"{p}": {s}')

                if not FirstSegOf:
                    jsfile.write(f',\n')

                jsfile.write(f'\t\t"english": "{Message}"\n')
                jsfile.write('\t}')
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

        jsfile.write( '\n}\n' )

        txt.close()
        jsfile.close()

        os.remove( f'{filetext}' )
