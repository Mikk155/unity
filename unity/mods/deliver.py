# Deliverance installation script

mod = 'deliver'

from tools.check_install import check_install
check_install( mod=mod, link='https://www.moddb.com/mods/deliverance/downloads/deliverance-v3' )

from tools.pak import extract_pak
extract_pak( paks=[ 'pak0' ], mod=mod )

assets = {
    "maps/deliver1.bsp": "maps/deliver1.bsp",
    "maps/deliver2.bsp": "maps/deliver2.bsp",
    "maps/deliver3a.bsp": "maps/deliver3a.bsp",
    "maps/deliver3b.bsp": "maps/deliver3b.bsp",
    "maps/deliver4.bsp": "maps/deliver4.bsp",
    "maps/deliver5.bsp": "maps/deliver5.bsp",
    "maps/deliver6.bsp": "maps/deliver6.bsp",
    "maps/deliver7.bsp": "maps/deliver7.bsp",

    "models/gordon.mdl": "models/deliver/gordon.mdl",

    "sound/ambience/huey.wav": "sound/deliver/ambience/huey.wav",
    "sound/ambience/jetflyby2.wav": "sound/deliver/ambience/jetflyby2.wav",
    "sound/ambience/motorstart.wav": "sound/deliver/ambience/motorstart.wav",
    "sound/ambience/projector.wav": "sound/deliver/ambience/projector.wav",
    "sound/ambience/semiidle.wav": "sound/deliver/ambience/semiidle.wav",
    "sound/ambience/snoring.wav": "sound/deliver/ambience/snoring.wav",
    "sound/ambience/thunder.wav": "sound/deliver/ambience/thunder.wav",
    "sound/ambience/toilet.wav": "sound/deliver/ambience/toilet.wav",
    "sound/ambience/bedsqueak.wav": "sound/deliver/ambience/bedsqueak.wav",
    "sound/ambience/cabdoor.wav": "sound/deliver/ambience/cabdoor.wav",
    "sound/ambience/carskid.wav": "sound/deliver/ambience/carskid.wav",
    "sound/ambience/earthquake.wav": "sound/deliver/ambience/earthquake.wav",
    "sound/barney/ba_freeman.wav": "sound/deliver/barney/ba_freeman.wav",
    "sound/barney/ba_getinhere.wav": "sound/deliver/barney/ba_getinhere.wav",
    "sound/barney/ba_whatthehell.wav": "sound/deliver/barney/ba_whatthehell.wav",
    "sound/barney/ba_glad.wav": "sound/deliver/barney/ba_glad.wav",
    "sound/barney/ba_anyidea.wav": "sound/deliver/barney/ba_anyidea.wav",
    "sound/debris/impact.wav": "sound/deliver/debris/impact.wav",
    "sound/debris/bustglass4.wav": "sound/deliver/debris/bustglass4.wav",
    "sound/debris/metalclang.wav": "sound/deliver/debris/metalclang.wav",
    "sound/debris/carexplo.wav": "sound/deliver/debris/carexplo.wav",
    "sound/doors/dooropen.wav": "sound/deliver/doors/dooropen.wav",
    "sound/friendly/fr_attack2.wav": "sound/deliver/friendly/fr_attack2.wav",
    "sound/friendly/fr_attack1.wav": "sound/deliver/friendly/fr_attack1.wav",
    "sound/friendly/fr_attack3.wav": "sound/deliver/friendly/fr_attack3.wav",
    "sound/gman/gman_impressed.wav": "sound/deliver/gman/gman_impressed.wav",
    "sound/hgrunt/back!.wav": "sound/deliver/hgrunt/back!.wav",
    "sound/hgrunt/fallback!.wav": "sound/deliver/hgrunt/fallback!.wav",
    "sound/hgrunt/mine!.wav": "sound/deliver/hgrunt/mine!.wav",
    "sound/hgrunt/pullingout.wav": "sound/deliver/hgrunt/pullingout.wav",
    "sound/scientist/almostthere.wav": "sound/deliver/scientist/almostthere.wav",
    "sound/scientist/getaway.wav": "sound/deliver/scientist/getaway.wav",
    "sound/scientist/getusout.wav": "sound/deliver/scientist/getusout.wav",
    "sound/scientist/gordon.wav": "sound/deliver/scientist/gordon.wav",
    "sound/scientist/noscanner.wav": "sound/deliver/scientist/noscanner.wav",
    "sound/scientist/opendoor.wav": "sound/deliver/scientist/opendoor.wav",
    "sound/scientist/sci_world.wav": "sound/deliver/scientist/sci_world.wav",
    "sound/vox/s.wav": "sound/deliver/vox/s.wav",

    "sound/sentences.txt": "sound/deliver/sentences.txt",
    "sound/materials.txt": "sound/deliver/materials.txt",

    "titles.txt": "cfg/deliver/titles.txt",
}

from tools.copy_assets import copy_assets
copy_assets( mod=mod, assets=assets )

from tools.titles_to_json import titles_to_json
titles_to_json( path='cfg/deliver/titles.txt' )

from tools.path import tools
import subprocess
#subprocess.Popen( f'python {tools}\\lazyripent.py', shell=True )
