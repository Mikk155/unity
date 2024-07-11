import subprocess
from tools.path import unity

def merge( modelname='' ):
    subprocess.Popen(
        f'{unity}\mods\\tools\modelguy.exe merge "{unity}/mods/port/{modelname}"', shell=True )
