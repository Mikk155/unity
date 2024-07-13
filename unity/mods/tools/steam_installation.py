# ===============================================================================
# Find steam installation so the scripts uses x32 or x64 bits tools.
# ===============================================================================

import winreg

def _STEAM_INSTALLATION(rk):

    PATH_STEAM = None

    hkey = None

    try:

        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rk)

    except:

        print("HKey: \"HKEY_LOCAL_MACHINE\\{}\" failed.".format(rk))

        return

    try:

        PATH_STEAM = winreg.QueryValueEx(hkey, "InstallPath")[0]

    except:

        PATH_STEAM = None

    return PATH_STEAM

STEAM_IS64 = _STEAM_INSTALLATION( "SOFTWARE\\Wow6432Node\\Valve\Steam" )
