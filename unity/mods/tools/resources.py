# ===============================================================================
# Load resources list
# ===============================================================================

from tools.path import mods

def load_resources( mod='' ):

    assets = {}

    print(f'[load_resources]  Loading {mod}.res' )

    with open( f'{mods}/{mod}.res', 'r' ) as res:

        lines = res.readlines()

        for line in lines:

            line = line.strip()
            line = line.strip( '"' )

            if not line or line.startswith( '//' ) or line == '':
                continue

            resources = line.split()

            if len(resources) < 2:
                print(f'[load_resources] Error in {mod}.res file!\n{line}' )
                exit(1)

            assets[ resources[0][ :-1 ] ] = resources[1][ 1 : ]

        res.close()

    if len(assets) == 0:
        print(f'[load_resources] Warning! no assets were found in {mod}.res' )
        exit(1)

    return assets
