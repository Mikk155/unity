# ===============================================================================
# Deliverance installation script
# ===============================================================================

mod = 'deliver'

from tools.check_install import check_install
check_install( mod=mod, link='https://www.moddb.com/mods/deliverance/downloads/deliverance-v3' )

from tools.pak import extract_pak
extract_pak( paks=[ 'pak0' ], mod=mod )

from tools.resources import load_resources

assets = load_resources( mod=mod )

from tools.copy_assets import copy_assets
copy_assets( mod=mod, assets=assets )

from tools.titles_to_json import titles_to_json
titles_to_json( path='cfg/deliver/titles.txt' )

from tools.map_upgrader import map_upgrader
map_upgrader()

from tools.download import download
# download( [ 'https://github.com/Mikk155/Discord-Rich-Presence-Dynamic/archive/refs/heads/main.zip' ] )
