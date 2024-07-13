import os

abs = os.path.abspath( '' )
halflife = abs[ : abs.find( '\\unity\mods' ) ]
unity = abs[ : abs.find( '\\mods' ) ]
port = f'{abs}\\port'
tools = f'{abs}\\tools'
mods = abs
