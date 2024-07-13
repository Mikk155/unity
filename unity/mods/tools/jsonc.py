# ===============================================================================
# Json but the origina json does crash with commentary.
# So we load the file and skip them manually before encoding to json
# ===============================================================================

import json

def load_json( path='' ):

    js = {}
    jsdata = ''

    with open( path, 'r' ) as file:

        lines = file.readlines()

        for t, line in enumerate( lines ):

            line = line.strip()

            if line and line != '' and not line.startswith( '//' ):
                jsdata = f'{jsdata}\n{line}'

        js = json.loads( jsdata )

        file.close()

    return js
