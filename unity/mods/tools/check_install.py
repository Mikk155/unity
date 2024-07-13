# ===============================================================================
# Find the mod folder to check it is installed.
# Exit imediatelly and print the given download link if not found.
# ===============================================================================

import os
from tools.path import halflife

def check_install( mod='', link='' ):

    if not os.path.exists( f'{halflife}/{mod}/' ):

        print( f'Couldn\'t find "{halflife}\{mod}\\"\ndid you installed the mod?\n{link}' )

        exit(1)

    else:

        print(f'Mod \'{mod}\' installation detected. Starting conversion...')
