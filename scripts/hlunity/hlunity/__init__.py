"""
The MIT License (MIT)

Copyright (c) 2024 Mikk

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

__Logger__ = {
    "#init_nro1":
    {
        "english": "{} Download any of the following links to start the installation",
    },
    "#init_nro2":
    {
        "english": "{} Un-zip all the content",
    },
    "#init_nro3":
    {
        "english": "{} Write in here the full path to the folder containing the mod\'s assets",
    },
    "#init_nro4":
    {
        "english": "{} Press enter and wait for conversion",
    },
    "#init_Exception":
    {
        "english": "Incorrect absolute path to mod folder",
    },
    "#init_CleaningUp":
    {
        "english": "Cleaning up temporal folder {}",
    },
    "#Ripent_possibly_broken":
    {
        "english": "Possible broken entity data in a map, Check and patch \"{}\"",
    },
    "#printf_NotDictOrList":
    {
        "english": "'arguments' is not a 'list' or 'dict'",
    },
    "#Vector_out_of_index":
    {
        "english": "Vector is out of index. no matching {} Supported index are 0 (x), 1 (y), (2) z",
    },
    "#STEAM_Unsupported":
    {
        "english": "Unsupported Operative System {}",
    },
    "#HALFLIFE_Path":
    {
        "english": "Can not find Steam installation\nPlease define {} in the main script.",
    },
    "#pak_Skipping":
    {
        "english": "[pak] File {} already exists. Skipping",
    },
    "#pak_Extracted":
    {
        "english": "[pak] Extract file {}",
    },
    "#pak_NotValidPak":
    {
        "english": "[pak] File {} is not a valid pak",
    },
    "#download_Downloading":
    {
        "english": "Downloading third-party assets\n{}",
        "spanish": "Descargando contenido de terceros\n{}",
    },
    "#download_Failed":
    {
        "english": "Failed downloading {}",
    },
    "#upgrades_unknown_keyvalue":
    {
        "english": "[map upgrades] Unknown keyvalue {} on {}",
    },
    "#upgrades_multi_manager_exceds":
    {
        "english": "[map upgrades] multi_manager exceds max values of 16, Creating a copy for chaining events.",
    },
    "#upgrades_upgrading_map":
    {
        "english": "[map upgrades] Upgrading map {}",
    },
    "#FileNotExists":
    {
        "english": "{} Doesn't exists",
    },
}

def __get_language__():
    import locale
    syslang = locale.getlocale()
    lang = syslang[0]
    if lang.find( '_' ) != -1:
        lang = lang[ 0 : lang.find( '_' ) ]
    return str( lang.lower() )

language = __get_language__()
'''
Returns the OS's language, example ``english``, ``spanish``
'''

def printf( string: str | dict, arguments: dict | list[str] = [], cut_not_matched : bool = False, not_matched_trim : bool = False, dont_print : bool = False ) -> str:
    '''
    Formats the given string replacing all the closed brackets with the corresponding indexes of arguments

    ``string`` if is **dict** we'll get the language of the OS
    ``{ 'english': 'english string', 'spanish': 'spanish string' }``
    Returns 'english' if the label doesn't exists

    ``cut_not_matched`` = True, remove not matched brackets

    ``not_matched_trim`` = True, when ``cut_not_matched`` = True, trims leading white space for continuity

    ``dont_print`` = **True** don't print message, only return

    Returns the formatted string, if needed
    '''

    if isinstance( string, dict ):
        string = string.get( language, string[ 'english' ] )

    if isinstance( arguments, list ):

        for __arg__ in arguments:
            string = string.replace( "{}", str( __arg__ ), 1 )

        if cut_not_matched:
            __replace__ = '{} ' if not_matched_trim else '{}'
            string.replace( __replace__, '' )

    elif isinstance( arguments, dict ):

        for __oarg__, __narg__ in arguments.items():
            string = string.replace( "{"+__oarg__+"}", str( __narg__ ) )
            #if cut_not_matched: -TODO find open-bracket and check until closes for removing
    else:

        __except__ = printf( __Logger__[ '#printf_NotDictOrList' ], dont_print=True )
        raise Exception( __except__)

    if not dont_print:
        print( string )

    return string

__LOGGER_LEVEL__ = 0

class LOGGER_LEVEL:
    USER = 0
    '''
    Default Logger, This library doesn't use them
    '''
    IMPORTANT = 1
    '''
    Important Logger, These are displayed when something relevant is happening
    '''
    ALL = 2
    '''
    All Logger, These are displayed when anything happens
    '''

def set_logger( logger_level: LOGGER_LEVEL ):
    '''
    Set logger level, see ``LOGGER_LEVEL``
    '''
    global __LOGGER_LEVEL__
    __LOGGER_LEVEL__ = logger_level
    if __LOGGER_LEVEL__ > LOGGER_LEVEL.ALL:
        __LOGGER_LEVEL__ = LOGGER_LEVEL.ALL
    elif __LOGGER_LEVEL__ < LOGGER_LEVEL.USER:
        __LOGGER_LEVEL__ = LOGGER_LEVEL.USER

def logger( message: str, arguments: dict | list[str] = [], logger_level: int = LOGGER_LEVEL.USER ):
    '''
    Prints message replacing {} with ``arguments``

    use ``set_logger( logger_level: LOGGER_LEVEL )`` to enable specific levels
    '''
    global __LOGGER_LEVEL__
    if __LOGGER_LEVEL__ >= logger_level:
        printf( message, arguments, True, True )

def makedirs_file( file_path : str ):

    index = file_path.rfind( '\\' )
    find = '\\'
    if file_path.rfind( '/' ) > index:
        index = file_path.rfind( '/' )
        find = '/'
    if index != -1:
        __makedirs__ = file_path[ : file_path.rfind( find ) ]

        from os import path, makedirs

        if not path.exists( __makedirs__ ):
            makedirs( __makedirs__ )

def jsonc( obj : list[str] | str ) -> dict | list:
    '''
    Loads a text file and skips single-line commentary before loading a json object
    '''

    __js_split__ = ''
    __lines__: list[str]

    if isinstance( obj, list ):
        __lines__ = obj
    else:
        __lines__ = open( obj, 'r' ).readlines()

    for __line__ in __lines__:

        __line__ = __line__.strip()

        if __line__ and __line__ != '' and not __line__.startswith( '//' ):
            __js_split__ = f'{__js_split__}\n{__line__}'

    from json import loads
    return loads( __js_split__ )

class Vector:
    '''
    Vector ( y, x, z )
    '''
    def __init__( self, x:int|str=0, y=0, z=0 ):
        '''
        Initialise a Vector.

        if ``x`` is a str it will split spaces or comas to make the Vector

        if no arguments provided it will be 0, 0, 0
        '''

        if isinstance( x, str ):

            from re import sub

            x = sub( r'[^0-9. ]', '', x )

            __values__ = x.split( ',' ) if x.find( ',' ) != -1 else x.split()

            if len( __values__ ) < 3:
                __values__ += [ '0' ] * ( 3 - len( __values__ ) )

            self.x, self.y, self.z = [ self.__parse_value__(v) for v in __values__[:3] ]

        else:
            self.x = self.__parse_value__(x) if isinstance( x, ( float, int ) ) else 0
            self.y = self.__parse_value__(y) if isinstance( y, ( float, int ) ) else 0
            self.z = self.__parse_value__(z) if isinstance( z, ( float, int ) ) else 0

    def __parse_value__( self, __value__ ):

        __value__ = float( __value__ )

        if __value__.is_integer() or __value__ == int( __value__ ):

            return int( __value__ )
        
        return __value__

    def __to_string__( self, __value__ ):
        return str( __value__ ).split('.')[0] if str( __value__ ).endswith( '.0' ) else str( __value__ )

    def to_string( self, quoted : bool = False ):
        '''
        Converts the vector to string
        
        ``quoted`` = True, returns separating each number by a quote
        '''

        _y = self.__to_string__( self.y )
        _x = self.__to_string__( self.x )
        _z = self.__to_string__( self.z )

        if quoted:
            return f'{_x}, {_y}, {_z}'
        return f'{_x} {_y} {_z}'

    def __str__( self ):
        return self.to_string()

    def __add__(self, other):

        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        if isinstance( scalar, Vector ):
            return Vector(self.x * scalar.x, self.y * scalar.y, self.z * scalar.z)
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __eq__( self, other ):
        if isinstance( other, Vector):
            return ( self.x == other.x and self.z == other.z and self.y == other.y )
        return False

    def __ne__( self, other ):
        return not self.__eq__(other)

    def __getitem__( self, ang ):

        if ang == 0:
            return self.x

        elif ang == 1:
            return self.y

        elif ang == 2:
            return self.z

        else:
            __except__ = printf( __Logger__[ '#Vector_out_of_index' ], [ ang ], dont_print=True )
            raise Exception( __except__ )

    def __setitem__(self, ang, new):

        if ang == 0:
            self.x = self.__parse_value__( new )

        elif ang == 1:
            self.y = self.__parse_value__( new )

        elif ang == 2:
            self.z = self.__parse_value__( new )

        else:
            __except__ = printf( __Logger__[ '#Vector_out_of_index' ], [ ang ], dont_print=True )
            raise Exception( __except__ )

    def __repr__(self):
        return f"Vector( {self.x}, {self.y}, {self.z} )"

#========================================================
# Steam Path
#========================================================

def STEAM() -> str:

    '''
    Get steam's installation path
    '''

    from platform import system
    __OS__ = system()

    from os import path

    if __OS__ == "Windows":
        __paths__ = [
            path.expandvars( r"%ProgramFiles(x86)%\Steam" ),
            path.expandvars( r"%ProgramFiles%\Steam" )
        ]

        for __path__ in __paths__:
            if path.exists( __path__ ):
                return __path__

        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
                return winreg.QueryValueEx(key, "SteamPath")[0]
        except (ImportError, FileNotFoundError, OSError, PermissionError):
            return None

    elif __OS__ == "Linux":
        __paths__ = [
            "/usr/bin/steam",
            "/usr/local/bin/steam"
        ]    

        for __path__ in __paths__:
            if path.exists( __path__ ):
                return path.dirname( path.abspath( __path__ ) )
        return None

    else:
        __except__ = printf( __Logger__[ '#STEAM_Unsupported' ], [ __OS__ ], dont_print=True )
        raise NotImplementedError( __except__ )

def HALFLIFE() -> str:
    '''
    Get "Half-Life" folder within a steam installation
    '''

    __STEAM__ = STEAM()

    from os import path

    if __STEAM__:
        __HALFLIFE__ = f'{__STEAM__}\steamapps\common\Half-Life'
        if path.exists( __HALFLIFE__ ):
            return __HALFLIFE__

    try:
        from __main__ import halflife
        return halflife
    except Exception:
        __except__ = printf( __Logger__[ '#HALFLIFE_Path' ], [ 'halflife="C:/Path/To/Half-Life' ], dont_print=True )
        raise FileNotFoundError( __except__ )

#========================================================
# pak
#========================================================

class pak:
    '''
    Extracts pak's assets from the given mod folder
    '''
    def __init__( self, path_to_mod ):

        import struct
        from os import path, makedirs, walk
        from re import sub

        paks = []

        for root, dirs, files in walk( path_to_mod ):
            for file in files:
                if wildcard( file, '*pak*.pak' ):
                    paks.append( file )

        paks = sorted( paks, key=lambda x: int( x[ 3 : -4 ] ), reverse=True )

        for __paks__ in paks:
            __pak__ = open( f'{path_to_mod}\\{__paks__}', 'rb')

            if not __pak__:
                continue

            header = __pak__.read( 12 )

            if header[ : 4 ] != b'PACK':
                logger( '#pak_NotValidPak', [ __paks__ ] )
                continue

            ( dir_offset, dir_length ) = struct.unpack( 'ii', header[ 4 : ] )
            __pak__.seek( dir_offset )
            dir_data = __pak__.read( dir_length )

            num_files = dir_length // 64

            __files__ = {}

            for i in range( num_files ):
                entry = dir_data[ i * 64 : ( i + 1 ) * 64 ]
                name = entry[ : 56 ].split( b'\x00', 1 )[0].decode( 'latin-1' )
                name = sub( r'[^a-zA-Z0-9_\-./!]', '', name ) # May be missing something X[
                ( offset, length ) = struct.unpack( 'ii', entry[ 56 : ] )
                __files__[ name ] = ( offset, length )

            for name, ( offset, length ) in __files__.items():
                __pak__.seek( offset )
                data = __pak__.read( length )

                extract_path = path.join( path_to_mod, name )
                makedirs( path.dirname( extract_path ), exist_ok=True )

                if path.exists( extract_path ):
                    logger( __Logger__[ '#pak_Skipping' ], [ name ], LOGGER_LEVEL.ALL )
                    continue

                with open( extract_path, 'wb') as out_file:
                    logger( __Logger__[ '#pak_Extracted' ], [ name ], LOGGER_LEVEL.ALL )
                    out_file.write( data )

#========================================================
# Blue-Shift BSP Conversion
#========================================================

class __DHeader__:
    def __init__(self):
        self.version = 0
        self.lumps = [ [ 0, 0 ] for _ in range( 15 )]

def convert_blueshift_bsp( bsp_path : str, bsp_output : str ):
    '''
    Converts a Blue-Shift BSP to a generic goldsource BSP
    '''

    import struct
    from shutil import copy

    if bsp_path != bsp_output:
        copy( bsp_path, bsp_output )

    __LUMP_HEADER__ = 15
    __VERSION__ = 0
    __LUMPS__ = 1

    with open( bsp_output, 'rb+' ) as file:

        start = file.tell()

        if start == -1:
            raise Exception( f"Error getting start position in \"{file}\"" )

        header = [ 0, [ [ 0, 0 ] for _ in range( __LUMP_HEADER__ ) ] ]

        data = file.read( 4 + 8 * __LUMP_HEADER__ )
        header[__VERSION__] = struct.unpack('i', data[:4] )[0]

        for i in range( __LUMP_HEADER__ ):
            fileofs, filelen = struct.unpack( 'ii', data[ 4 + i * 8:4 + ( i + 1 ) * 8 ] )
            header[__LUMPS__][i] = [ fileofs, filelen ]
        
        if header[__LUMPS__][1][0] == 124:
            file.close() # Already converted, don't swap
            return

        header[__LUMPS__][0], header[__LUMPS__][1] = header[__LUMPS__][1], header[__LUMPS__][0]

        from os import SEEK_SET
        file.seek(start, SEEK_SET)

        data = struct.pack( 'i', header[__VERSION__] )
        for lump in header[__LUMPS__]:
            data += struct.pack('ii', lump[0], lump[1])

        file.write(data)

#========================================================
# starting, ending and midde wildcarding
#========================================================

def wildcard( compare : str, comparator : str, wildcard : str = '*' ) -> bool:
    '''
    Compare ``compare`` with ``comparator`` and see if they fully match or partial match by starting, ending or middle ``wildcard``
    '''
    if compare == comparator:
        return True

    elif wildcard not in comparator:
        return False

    __parts__ = comparator.split( wildcard )

    for __i__, __p__ in enumerate( __parts__ ):
        if __p__ == '':
            __parts__.pop( __i__ )

    __index__ : int = 0
    __matched__ : bool = True if len( __parts__ ) > 0 else False

    for __p__ in __parts__:
        if compare.find( __p__, __index__ ) < __index__:
            __matched__ = False
            break
        else:
            __index__ = compare.find( __p__, __index__ )

    return __matched__

#========================================================
# Entity, entity blocks from entity lumps
#========================================================

class Entity:
    '''
    Entity is basically a dict representing a entity block from a entity lump in a BSP

    Access any key-value with a dot, returns None if not set, set None to remove
    '''
    def __init__( self, KeyValueData=None ):
        self.KeyValueData = KeyValueData if isinstance( KeyValueData, dict ) else KeyValueData.ToDict() if isinstance( KeyValueData, Entity ) else {}

    def ToDict( self ):
        """
            Converts this Entity class to a dict.
        """
        return self.KeyValueData

    def get( self, value:str ):
        self.KeyValueData.get( value )

    def copy(self):
        return Entity( self.KeyValueData.copy() )

    def set( self, value:str ):
        self.KeyValueData[ value ] = value

    def pop( self, value:str ):
        self.KeyValueData.pop( value, '' )

    def __getattr__( self, key ):
        return str( self.KeyValueData.get( key, "" ) ) if key in self.KeyValueData else None

    def __setattr__( self, key, value ):
        if key == 'KeyValueData':
            super().__setattr__( key, value )
        elif value == None:
            self.KeyValueData.pop( key, '' )
        else:
            self.KeyValueData[ key ] = str( value )

    def remove( self ):
        """
        Removes this entity from the entity data
        """
        self.KeyValueData.clear()

    def __repr__(self):
        return str( self.KeyValueData )

#========================================================
# Ripent, BSP entity lump
#========================================================

__RIPENT_NONE__ = 0
__RIPENT_DATA__ = 1
__RIPENT_JSON__ = 2
__RIPENT_BSP__ = 3
__RIPENT_MAP__ = 4

class Ripent:
    '''
    Ripent, access to BSP's entity lumps
    '''
    def __init__( self, input : str | list[Entity] ):
        '''
        ``input`` Full path to a BSP, MAP or JSON file, it could also be a list[Entity] wich is the representation of the JSON format
        '''

        if isinstance( input, list ):
            self.format = __RIPENT_NONE__
        elif input.endswith( '.bsp' ):
            self.format = __RIPENT_BSP__
        elif input.endswith( '.map' ):
            self.format = __RIPENT_MAP__
        elif input.endswith( '.json' ):
            self.format = __RIPENT_JSON__
        else:
            self.format = __RIPENT_NONE__

        if isinstance( input, str ):
            self.path = input

    def __manipulate_lump__( self, ent_data : list[Entity] | list[dict] = None ) -> list[Entity]:

        from json import loads, dumps

        with open( self.path, 'rb+' ) as bsp_file:

            bsp_file.read(4) # BSP version.
            entities_lump_start_pos = bsp_file.tell()
            read_start = int.from_bytes( bsp_file.read(4), byteorder='little' )
            read_len = int.from_bytes( bsp_file.read(4), byteorder='little' )
            bsp_file.seek( read_start )

            if ent_data != None:

                newdata = ''

                for entblock in ent_data:

                    if isinstance( entblock, Entity ):
                        entblock = entblock.ToDict()
                    elif not isinstance( entblock, dict ):
                        entblock = loads( entblock )

                    if len(entblock) <= 0:
                        continue

                    newdata += '{\n'
                    for key, value in entblock.items():
                        newdata += f'"{key}" "{value}"\n'
                    newdata += '}\n'

                writedata_bytes = newdata.encode('ascii')
                new_len = len(writedata_bytes)

                if new_len <= read_len:
                    bsp_file.write(writedata_bytes)
                    if new_len < read_len:
                        bsp_file.write(b'\x00' * (read_len - new_len))
                else:
                    from os import SEEK_END
                    bsp_file.seek(0, SEEK_END)
                    new_start = bsp_file.tell()
                    bsp_file.write(writedata_bytes)

                    bsp_file.seek(entities_lump_start_pos)
                    bsp_file.write(new_start.to_bytes(4, byteorder='little'))
                    bsp_file.write(new_len.to_bytes(4, byteorder='little'))
            else:

                map_entities:str
                entities_lump = bsp_file.read( read_len )

                try:
                    map_entities = entities_lump.decode('ascii', errors='strict').splitlines()
                except UnicodeDecodeError:
                    map_entities = entities_lump.decode('utf-8', errors='ignore').splitlines()
                    logger( __Logger__[ '#Ripent_possibly_broken' ], [ self.path ] )

                entblock = {}
                entdata = []
                oldline = ''

                for line in map_entities:

                    if line == '{':
                        continue

                    line = line.strip()

                    if not line.endswith( '"' ):
                        oldline = line
                    elif oldline != '' and not line.startswith( '"' ):
                        line = f'{oldline}{line}'

                    __LastIndex__ = 0
                    while line.find( '\\', __LastIndex__ ) != -1:
                        __LastIndex__ = line.find( '\\', __LastIndex__ )
                        if line[ __LastIndex__ -1 : __LastIndex__ ] != '\\' and line[ __LastIndex__ + 1 : __LastIndex__ + 2 ] != '\\':
                            line = line[ : __LastIndex__ + 1 ] + line[ __LastIndex__ : ]
                        __LastIndex__ += 2

                    line = line.strip( '"' )

                    if not line or line == '':
                        continue

                    if line.startswith( '}' ): # startswith due to [NULL]
                        try:
                            lump = dumps( entblock )
                            block = loads( lump )
                            entity = Entity( block )
                            entdata.append( entity )
                            entblock.clear()
                        except Exception:
                            entblock.clear()
                    else:
                        keyvalues = line.split( '" "' )
                        if len( keyvalues ) == 2:
                            entblock[ keyvalues[0] ] = keyvalues[1]
                return entdata
        return None

    def __write_json__( self, entdata ):

        __fformat__ = '.bsp' if self.format == __RIPENT_BSP__ else '.map' if self.format == __RIPENT_MAP__ else None

        if __fformat__:

            with open( self.path.replace( __fformat__, '.json' ), 'w' ) as jsonfile:

                jsonfile.write( '[\n' )
                FirstBlockOf = True
                FirstKeyOf = True

                for entblock in entdata:

                    if isinstance( entblock, dict ):
                        entblock = Entity( entblock )

                    if FirstBlockOf:
                        FirstBlockOf = False
                    else:
                        jsonfile.write( ',\n' )

                    FirstKeyOf = True

                    jsonfile.write( '\t{\n' )

                    for key, value in entblock.ToDict().items():

                        if FirstKeyOf:
                            FirstKeyOf = False
                        else:
                            jsonfile.write( ',\n' )

                        jsonfile.write( f'\t\t"{key}": "{value}"' )

                    jsonfile.write( '\n\t}' )

                jsonfile.write( '\n]\n' )
                jsonfile.close()

    # Dafuk why can not i name it "import" >:[
    def import_( self, entity_data : list[Entity] = None, delete_json : bool = False ):
        '''
        Import the entity data if this Ripent instance is a BSP or MAP file

        ``entity_data`` if **None** we'll look for a valid JSON file within the BSP/MAP Path

        ``delete_json`` if **True** delete the json file used, if any.
        '''

        from json import load

        if not entity_data:

            __fformat__ = '.bsp' if self.format == __RIPENT_BSP__ else '.map' if self.format == __RIPENT_MAP__ else None

            if __fformat__:

                jsonpath = self.path.replace( __fformat__, '.json' )

                from os import path, remove

                if path.exists( jsonpath ):

                    with open( jsonpath, 'r' ) as jsonfile:
                        entity_data = load( jsonfile )
                        self.__manipulate_lump__( entity_data )
                        jsonfile.close()

                    if delete_json:
                        remove( jsonpath )

                else:
                    logger( __Logger__[ '#FileNotExists' ], [ jsonpath ], LOGGER_LEVEL.ALL )

        else:
            self.import_( self.__manipulate_lump__( entity_data ), False )

    def export( self, create_json : bool = False ) -> list[Entity] | None:
        '''
        Export the entity data if this Ripent instance is a BSP or MAP file else returns **None**

        ``create_json`` if **True** a json file will be generated at the BSP/MAP destination
        '''

        if self.format != __RIPENT_MAP__ and self.format != __RIPENT_BSP__:
            return None

        entdata = self.__manipulate_lump__()

        if create_json:
            self.__write_json__( entdata )

        return entdata

    def __repr__(self):
        return '{' + f'\'format\': \'{self.format}\', \'path\': \'{self.path}\'' + '}'

def init( urls : str | list[str] ) -> list[str]:
    '''
    Initialise mod installation telling the user to download one of the ``urls``

    Returns the absolute path to where the assets are
    '''
    logger( __Logger__[ '#init_nro1' ], [ '\n1 -' ] )

    if isinstance( urls, str ):
        print( urls )
    else:
        for url in urls:
            print( url )

    logger( __Logger__[ '#init_nro2' ], [ '\n2 -' ] )
    logger( __Logger__[ '#init_nro3' ], [ '\n3 -' ] )
    logger( __Logger__[ '#init_nro4' ], [ '\n4 -' ] )

    __asset__ = input()

    from os import path, makedirs
    from shutil import rmtree

    if __asset__ and path.exists( __asset__ ):

        __common_folders__ = (
            'sound',
            'sprites',
            'cl_dlls',
            'dlls',
            'events',
            'gfx',
            'maps',
            'media',
            'models',
            'resource',
        )
        if path.exists( any( f'{__asset__}\\{ __common_folders__ }\\' ) ):

            __temp_folder__ = f'{path.abspath( "" )}\\unity'
            if path.exists( __temp_folder__ ):
                logger( __Logger__[ "#init_CleaningUp" ], [ __temp_folder__ ], LOGGER_LEVEL.ALL )
                try:
                    rmtree( __temp_folder__ )
                except Exception as e:
                    logger( e, LOGGER_LEVEL.IMPORTANT )

            makedirs( __temp_folder__, exist_ok=True )

            return __asset__

    __except__ = printf( __Logger__[ '#init_Exception' ], dont_print=True )
    raise Exception( __except__ )

def copy_assets( mod_path : str, resources_path : str ) -> list[str]:
    '''
    Copy all assets listed in ``resources_path`` from ``mod_path`` to a temporal folder named ``unity`` where the script is located

    Returns a list[str] containing all the assets names and sub folders
    '''

    resources = jsonc( resources_path )

    assets = []

    from os import path
    from shutil import copy

    for resource in resources:

        __absp__ = f'{path.abspath( "" )}\\unity\\'

        makedirs_file( __absp__ + resource[1] )
        copy( f'{mod_path}\\{resource[0]}', __absp__ + resource[1] )
        assets.append( resource[1] )

    return assets

def download( urls : list[str] ):
    '''
    Download third party assets if needed
    '''

    from os import path
    from io import BytesIO
    from requests import get

    links = []

    if isinstance( urls, str ):
        links.append( urls )
    else:
        links = urls

    for url in links:
        logger( __Logger__[ '#download_Downloading' ], [ url ], LOGGER_LEVEL.IMPORTANT )

        response = get( url )

        if response.status_code == 200:

            from zipfile import ZipFile

            zip_file = ZipFile( BytesIO( response.content ) )

            zip_file.extractall( path.abspath( "" ) + '\\unity' )

            for member in zip_file.namelist():

                filename = path.basename( member )

                if not filename:
                    continue

                to_target = path.abspath( "" ) + '\\unity\\' + member[ member.find( '/' ) : ]

                makedirs_file( to_target )

                source = zip_file.open( member )
                target = open( to_target, "wb" )

                with source, target:
                    target.write( source.read() )
            break # Break as soon as one url doesn't fail
        else:
            logger( __Logger__[ '#download_Failed' ], [ response.status_code ], LOGGER_LEVEL.IMPORTANT )

#========================================================
# map upgrades
#========================================================

__upgrades_new_entities__ = []

def add_entity( entity:Entity ):
    '''
        Adds a new entity to the current map
    '''
    global __upgrades_new_entities__
    __upgrades_new_entities__.append( entity if isinstance( entity, dict ) else entity.ToDict() )

def __upg_angle_to_angles__( index:int, entity:Entity, map:str ):
    if entity.angle != None:
        NewAngles = Vector()
        Angle = float( entity.angle )
        if Angle >= 0:
            NewAngles = Vector( entity.angles )
            NewAngles.y = Angle
        else:
            if int(Angle) == -1: # floor?
                Angle = -90
            else:
                Angle = 90
            NewAngles.y = Angle
        entity.angles = NewAngles
        entity.angle = None
    return entity

__upg_ItemMapping__ = {
    "weapon_glock": "weapon_9mmhandgun",
    "ammo_glockclip": "ammo_9mmclip",
    "weapon_mp5": "weapon_9mmar",
    "ammo_mp5clip": "ammo_9mmar",
    "ammo_mp5grenades": "ammo_argrenades",
    "weapon_python": "weapon_357",
    "weapon_shockroach": "weapon_shockrifle",
    "weapon_9mmAR": "weapon_9mmar",
    "ammo_9mmAR": "ammo_9mmar",
    "ammo_ARgrenades": "ammo_argrenades",
    "monster_ShockTrooper_dead": "monster_shocktrooper_dead",
}

def __upg_remap_classnames__( index:int, entity:Entity, map:str ):
    global __upg_ItemMapping__
    if entity.classname in __upg_ItemMapping__:
        entity.classname = __upg_ItemMapping__.get( entity.classname )
    elif entity.classname == 'game_player_equip':
        for old, new in __upg_ItemMapping__.items():
            if old in entity.ToDict():
                entity.set( new, entity.get( old ) )
                entity.pop( old )
    return entity

def __upg_worldspawn_format_wad__( index:int, entity:Entity, map:str ):
    if entity.classname == 'worldspawn':
        if entity.wad != None:
            wad = entity.wad
            dwads = ''
            wads = wad.split( ';' )
            for w in wads:
                if not w or w == '':
                    continue
                if w.rfind( '\\' ) != -1:
                    w = w[ w.rfind( '\\' ) + 1 : ]
                if w.rfind( '/' ) != -1:
                    w = w[ w.rfind( '/' ) + 1 : ]
                dwads = f'{dwads}{w};'
            entity.wad = dwads
    return entity

def __upg_chargers_dmdelay__( index:int, entity:Entity, map:str ):
    if entity.classname in [ 'func_healthcharger', 'func_recharge' ]:
        entity.dmdelay = None
    return entity

def __upg_remap_world_items__( index:int, entity:Entity, map:str ):
    if entity.classname == 'world_items':
        if entity.type != None and entity.type.isnumeric():
            value = int( entity.type )
            entity.type = None
            if value == 42:
                entity.classname = 'item_antidote'
            elif value == 43:
                entity.classname = 'item_security'
            elif value == 44:
                entity.classname = 'item_battery'
            elif value == 45:
                entity.classname = 'item_suit'
        if entity.classname == 'world_items':
            logger( __Logger__[ '#upgrades_unknown_keyvalue' ], [ f'"type" "{entity.value}"', 'world_items' ], LOGGER_LEVEL.IMPORTANT )
            entity.remove()
    return entity

def __upg_update_human_hulls__( index:int, entity:Entity, map:str ):
    if entity.classname in [ 'monster_generic', 'monster_generic' ] and entity.model in [ 'models/player.mdl', 'models/holo.mdl' ]:
        entity.custom_hull_min = Vector( -16, -16, -36 )
        entity.custom_hull_max = Vector( 16, 16, 36 )
    return entity

def __upg_ambient_generic_pitch__( index:int, entity:Entity, map:str ):
    if entity.classname == 'ambient_generic' and entity.message == 'buttons/bell1.wav' and entity.pitch == '80':
        entity.message = 'buttons/bell1_alt.wav'
        entity.pitch = 100
    return entity

def __upg_barney_dead_body__( index:int, entity:Entity, map:str ):
    if entity.classname == 'monster_barney_dead' and entity.body != None:
        body = int( entity.body )
        if body == 0:
            body = 1
        elif body == 2:
            body = 0
        else:
            body = 2
        entity.body = None
        entity.bodystate = body
    return entity

def __upg_breakable_spawnobject__( index:int, entity:Entity, map:str ):
    if entity.classname == 'func_breakable' or entity.classname == 'func_pushable':
        if entity.spawnobject != None and entity.spawnobject.isnumeric():
            i = int( entity.spawnobject )
            classnames = [ "item_battery", "item_healthkit",
                "weapon_9mmhandgun", "ammo_9mmclip", "weapon_9mmar",
                    "ammo_9mmar", "ammo_argrenades", "weapon_shotgun",
                        "ammo_buckshot", "weapon_crossbow", "ammo_crossbow",
                            "weapon_357", "ammo_357", "weapon_rpg", "ammo_rpgclip",
                                "ammo_gaussclip", "weapon_handgrenade", "weapon_tripmine",
                                    "weapon_satchel", "weapon_snark", "weapon_hornetgun", "weapon_penguin"
            ]
            if i > 0 and i <= len(classnames):
                entity.spawnobject = classnames[i]
            else:
                entity.spawnobject = None
                if i != 0:
                    logger( __Logger__[ '#upgrades_unknown_keyvalue' ], [ f'"spawnobject" "{i}"', entity.classname ], LOGGER_LEVEL.IMPORTANT )
    return entity

__upg_eventhandler__ = Entity( { "classname": "trigger_eventhandler", "m_Caller": "!activator" } )

__upg_game_playerdie__ = False
def __upg_event_playerdie__( index:int, entity:Entity, map:str ):
    global __upg_game_playerdie__
    if not __upg_game_playerdie__ and entity.targetname == 'game_playerdie':
        __upg_eventhandler__.target = entity.targetname
        __upg_eventhandler__.event_type = 1
        add_entity( __upg_eventhandler__ )
        __upg_game_playerdie__ = True
    return entity

__upg_game_playerleave__ = False
def __upg_event_playerleave__( index:int, entity:Entity, map:str ):
    global __upg_game_playerleave__
    if not __upg_game_playerleave__ and entity.targetname == 'game_playerleave':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 2
        add_entity( __upg_eventhandler__ )
        __upg_game_playerleave__ = True
    return entity

__upg_game_playerkill__ = False
def __upg_event_playerkill__( index:int, entity:Entity, map:str ):
    global __upg_game_playerkill__
    if not __upg_game_playerkill__ and entity.targetname == 'game_playerkill':
        __upg_eventhandler__target = 'game_playerkill_check'
        __upg_eventhandler__event_type = 3
        add_entity( __upg_eventhandler__ )
        Newent = {
            "classname": "trigger_entity_condition",
            "targetname": "game_playerkill_check",
            "pass_target": "game_playerkill",
            "condition": "0"
        }
        add_entity( Newent )
        __upg_game_playerkill__ = True
    return entity

__upg_game_playeractivate__ = False
def __upg_event_playeractivate__( index:int, entity:Entity, map:str ):
    global __upg_game_playeractivate__
    if not __upg_game_playeractivate__ and entity.targetname == 'game_playeractivate':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 4
        add_entity( __upg_eventhandler__ )
        __upg_game_playeractivate__ = True
    return entity

__upg_game_playerjoin__ = False
def __upg_event_playerjoin__( index:int, entity:Entity, map:str ):
    global __upg_game_playerjoin__
    if not __upg_game_playerjoin__ and entity.targetname == 'game_playerjoin':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 5
        Newent = __upg_eventhandler__.copy()
        Newent[ "appearflag_multiplayer" ] = "1" # Only in multiplayer
        add_entity( Newent )
        __upg_game_playerjoin__ = True
    return entity

__upg_game_playerspawn__ = False
def __upg_event_playerspawn__( index:int, entity:Entity, map:str ):
    global __upg_game_playerspawn__
    if not __upg_game_playerspawn__ and entity.targetname == 'game_playerspawn':
        __upg_eventhandler__target = entity.targetname
        __upg_eventhandler__event_type = 6
        add_entity( __upg_eventhandler__ )
        __upg_game_playerspawn__ = True
    return entity

__upg_DefaultSound__ = "common/null.wav"
__upg_DefaultSentence__ = ""
__upg_DefaultButtonSound__ = ""
__upg_DefaultMomentaryButtonSound__ = "buttons/button9.wav"
__upg_DefaultTrackTrainSound__ = ""

__upg_DoorMoveSounds__ = [
    __upg_DefaultSound__,
    "doors/doormove1.wav",
    "doors/doormove2.wav",
    "doors/doormove3.wav",
    "doors/doormove4.wav",
    "doors/doormove5.wav",
    "doors/doormove6.wav",
    "doors/doormove7.wav",
    "doors/doormove8.wav",
    "doors/doormove9.wav",
    "doors/doormove10.wav"
]

__upg_DoorStopSounds__ = [
    __upg_DefaultSound__,
    "doors/doorstop1.wav",
    "doors/doorstop2.wav",
    "doors/doorstop3.wav",
    "doors/doorstop4.wav",
    "doors/doorstop5.wav",
    "doors/doorstop6.wav",
    "doors/doorstop7.wav",
    "doors/doorstop8.wav"
]

__upg_ButtonSounds__ = [
    __upg_DefaultSound__,
    "buttons/button1.wav",
    "buttons/button2.wav",
    "buttons/button3.wav",
    "buttons/button4.wav",
    "buttons/button5.wav",
    "buttons/button6.wav",
    "buttons/button7.wav",
    "buttons/button8.wav",
    "buttons/button9.wav",
    "buttons/button10.wav",
    "buttons/button11.wav",
    "buttons/latchlocked1.wav",
    "buttons/latchunlocked1.wav",
    "buttons/lightswitch2.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/button9.wav",
    "buttons/lever1.wav",
    "buttons/lever2.wav",
    "buttons/lever3.wav",
    "buttons/lever4.wav",
    "buttons/lever5.wav"
]

__upg_ButtonLockedSentences__ = [
    "",
    "NA",
    "ND",
    "NF",
    "NFIRE",
    "NCHEM",
    "NRAD",
    "NCON",
    "NH",
    "NG"
]

__upg_ButtonUnlockedSentences__ = [
    "",
    "EA",
    "ED",
    "EF",
    "EFIRE",
    "ECHEM",
    "ERAD",
    "ECON",
    "EH"
]

class __upg_FixSoundsData__:
    def __init__( self, KeyName:str, DefaultValue:str = None, Names:list[str] = None, Optional:str = None ):
        self.KeyName = KeyName
        self.DefaultValue = DefaultValue
        self.Names = Names
        self.Optional = Optional

__upg_DoorData__ = [
    __upg_FixSoundsData__( "movesnd", __upg_DefaultSound__, __upg_DoorMoveSounds__ ),
    __upg_FixSoundsData__( "stopsnd", __upg_DefaultSound__, __upg_DoorStopSounds__ ),
    __upg_FixSoundsData__( "locked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "unlocked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "locked_sentence", __upg_DefaultSentence__, __upg_ButtonLockedSentences__ ),
    __upg_FixSoundsData__( "unlocked_sentence", __upg_DefaultSentence__, __upg_ButtonUnlockedSentences__ )
]

__upg_ButtonData__ = [
    __upg_FixSoundsData__( "sounds", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "locked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "unlocked_sound", __upg_DefaultButtonSound__, __upg_ButtonSounds__ ),
    __upg_FixSoundsData__( "locked_sentence", __upg_DefaultSentence__, __upg_ButtonLockedSentences__ ),
    __upg_FixSoundsData__( "unlocked_sentence", __upg_DefaultSentence__, __upg_ButtonUnlockedSentences__ )
]

__upg_Momentary_DoorMoveSounds__ = [
    __upg_DefaultSound__,
    "doors/doormove1.wav",
    "doors/doormove2.wav",
    "doors/doormove3.wav",
    "doors/doormove4.wav",
    "doors/doormove5.wav",
    "doors/doormove6.wav",
    "doors/doormove7.wav",
    "doors/doormove8.wav"
]

__upg_RotatingMoveSounds__ = [
    __upg_DefaultSound__,
    "fans/fan1.wav",
    "fans/fan2.wav",
    "fans/fan3.wav",
    "fans/fan4.wav",
    "fans/fan5.wav"
]

__upg_PlatMoveSounds__ = [
    __upg_DefaultSound__,
    "plats/bigmove1.wav",
    "plats/bigmove2.wav",
    "plats/elevmove1.wav",
    "plats/elevmove2.wav",
    "plats/elevmove3.wav",
    "plats/freightmove1.wav",
    "plats/freightmove2.wav",
    "plats/heavymove1.wav",
    "plats/rackmove1.wav",
    "plats/railmove1.wav",
    "plats/squeekmove1.wav",
    "plats/talkmove1.wav",
    "plats/talkmove2.wav"
]

__upg_PlatStopSounds__ = [
    __upg_DefaultSound__,
    "plats/bigstop1.wav",
    "plats/bigstop2.wav",
    "plats/freightstop1.wav",
    "plats/heavystop2.wav",
    "plats/rackstop1.wav",
    "plats/railstop1.wav",
    "plats/squeekstop1.wav",
    "plats/talkstop1.wav"
]

__upg_PlatData__ = [
    __upg_FixSoundsData__( "movesnd", __upg_DefaultButtonSound__, __upg_PlatMoveSounds__ ),
    __upg_FixSoundsData__( "stopsnd", __upg_DefaultButtonSound__, __upg_PlatStopSounds__ )
]

__upg_TrackTrainMoveSounds__ = [
    "",
    "plats/ttrain1.wav",
    "plats/ttrain2.wav",
    "plats/ttrain3.wav",
    "plats/ttrain4.wav",
    "plats/ttrain6.wav",
    "plats/ttrain7.wav"
]

__upg_FixSoundsEntityData__ = {

    "func_door": __upg_DoorData__,
    "func_water": __upg_DoorData__,
    "func_door_rotating": __upg_DoorData__,
    "momentary_door": __upg_FixSoundsData__( "movesnd", __upg_DefaultSound__, __upg_Momentary_DoorMoveSounds__ ),
    "func_rotating": __upg_FixSoundsData__( "sounds", __upg_DefaultSound__, __upg_RotatingMoveSounds__, "message" ),
    "func_button": __upg_ButtonData__,
    "func_rot_button": __upg_ButtonData__,
    "momentary_rot_button": __upg_FixSoundsData__( "sounds", __upg_DefaultMomentaryButtonSound__, __upg_ButtonSounds__ ),
    "func_train": __upg_PlatData__,
    "func_plat": __upg_PlatData__,
    "func_platrot": __upg_PlatData__,
    "func_trackchange": __upg_PlatData__,
    "func_trackautochange": __upg_PlatData__,
    "env_spritetrain": __upg_PlatData__,
    "func_tracktrain": __upg_FixSoundsData__( "sounds", __upg_DefaultTrackTrainSound__, __upg_TrackTrainMoveSounds__ )
}

def __upg_TryFixSoundsEnt__( entity:dict, Data:__upg_FixSoundsData__ ):
    name = Data.Optional
    if name is None:
        name = Data.DefaultValue
        if Data.KeyName in entity and entity.get( Data.KeyName ).isnumeric():
            index = int( entity.get( Data.KeyName ) )
            if index >= 0 and index < len( Data.Names ):
                name = Data.Names[ index ]
    entity[ Data.KeyName ] = None
    if len( name ) > 0:
        entity[ Data.KeyName ] = name
    return Entity( entity )

def __upg_fix_sounds_indexes__( index:int, entity:Entity, map:str ):
    if entity.classname in __upg_FixSoundsEntityData__:
        DataFix = __upg_FixSoundsEntityData__.get( entity.classname )
        if isinstance( DataFix, __upg_FixSoundsData__ ):
            entity = __upg_TryFixSoundsEnt__( entity.ToDict(), DataFix )
        else:
            for D in DataFix:
                entity = __upg_TryFixSoundsEnt__( entity.ToDict(), D )
    return entity

def __upg_rendercolor_invalid__( index:int, entity:Entity, map:str ):
    if entity.rendercolor != None:
        entity.rendercolor = Vector( entity.rendercolor ).to_string()
    return entity

def __upg_multi_manager_maxkeys__( index:int, entity:Entity, map:str ):
    if entity.classname == 'multi_manager':
        KeySize = 16
        NewEnt = {}
        pEnt = entity.ToDict().copy()
        ignorelist = { "targetname", "classname", "origin", "wait", "spawnflags" }
        for p in ignorelist:
            if p in entity.ToDict():
                NewEnt[ p ] = entity.get( p )
                KeySize+=1
        for p, v in pEnt.items():
            NewEnt[ p ] = v
            if len( NewEnt ) >= KeySize:
                break
        if len( entity.ToDict() ) > len( NewEnt ):
            for k, v in NewEnt.items():
                if not k in ignorelist:
                    pEnt.pop( k, '' )
            pEnt[ "targetname" ] = entity.targetname + f'_{index}'
            add_entity( __upg_multi_manager_maxkeys__( index, Entity( pEnt ), map ).ToDict() )
            NewEnt[ pEnt.get( "targetname" ) ] = 0
            logger( __Logger__[ '#upgrades_multi_manager_exceds' ], logger_level=LOGGER_LEVEL.ALL )
        for k in ignorelist:
            if k in entity.ToDict():
                NewEnt[ k ] = entity.ToDict().get( k, '' )
        entity = Entity( NewEnt )
    return entity

def upgrade_maps():
    '''
    Apply map upgrades

    You can hook your own upgrades in ``__main__``

    ``def PreMapUpgrade( index : int, entity : Entity, map : str ):``

    ``def PostMapUpgrade( index : int, entity : Entity, map : str ):``

    These upgrades has been ported from C#

    https://github.com/twhl-community/HalfLife.UnifiedSdk-CSharp/tree/master/src/HalfLife.UnifiedSdk.MapUpgrader.Upgrades
    '''

    from json import dumps
    from os import listdir, path
    import __main__ as main

    for file in listdir( f'{path.abspath( "" )}\\unity\\maps\\'):
        if file.endswith( ".bsp" ):
            map = file[ : len(file) - 4 ]
            bsp = f'{map}.bsp'

            BSPEnt = Ripent( f'{path.abspath( "" )}\\unity\\maps\\{bsp}' )
            entdata = BSPEnt.export()
 
            if entdata == None:
                continue

            logger( __Logger__[ '#upgrades_upgrading_map' ], [ bsp ], LOGGER_LEVEL.ALL )

            TempEntData = entdata.copy()

            for i, entblock in enumerate( TempEntData ):

                try:
                    entblock =  main.PreMapUpgrade( i, Entity( entblock ), map )
                except:
                    pass

                # Converts the obsolete "angle" keyvalue to "angles"
                entblock = __upg_angle_to_angles__( i, Entity( entblock ), map )

                # Renames weapon and item classnames to their primary name.
                entblock = __upg_remap_classnames__( i, Entity( entblock ), map )

                # Delete wad paths to prevent issues
                entblock = __upg_worldspawn_format_wad__( i, Entity( entblock ), map )

                # Removes the "dmdelay" keyvalue from charger entities. The original game ignores these.
                entblock = __upg_chargers_dmdelay__( i, Entity( entblock ), map )

                # Converts <c>world_items</c> entities to their equivalent entity.
                entblock = __upg_remap_world_items__( i, Entity( entblock ), map )

                # Sets a custom hull size for <c>monster_generic</c> entities that use a model
                # that was originally hard-coded to use one.
                entblock = __upg_update_human_hulls__( i, Entity( entblock ), map )

                # Find all buttons/bell1.wav sounds that have a pitch set to 80.
                # Change those to use an alternative sound and set their pitch to 100.
                entblock = __upg_ambient_generic_pitch__( i, Entity( entblock ), map )

                # Converts <c>monster_barney_dead</c> entities with custom body value
                # to use the new <c>bodystate</c> keyvalue.
                entblock = __upg_barney_dead_body__( i, Entity( entblock ), map )

                # Converts <c>func_breakable</c>'s spawn object keyvalue from an index to a classname.
                entblock = __upg_breakable_spawnobject__( i, Entity( entblock ), map )

                # Convert special targetnames to our new entity trigger_eventhandler
                entblock = __upg_event_playerdie__( i, Entity( entblock ), map )
                entblock = __upg_event_playerleave__( i, Entity( entblock ), map )
                entblock = __upg_event_playerkill__( i, Entity( entblock ), map )
                entblock = __upg_event_playeractivate__( i, Entity( entblock ), map )
                entblock = __upg_event_playerjoin__( i, Entity( entblock ), map )
                entblock = __upg_event_playerspawn__( i, Entity( entblock ), map )

                # Converts all entities that use sounds or sentences by index
                # to use sound filenames or sentence names instead.
                entblock = __upg_fix_sounds_indexes__( i, Entity( entblock ), map )

                # Fixes the use of invalid render color formats in some maps.
                entblock = __upg_rendercolor_invalid__( i, Entity( entblock ), map )

                # Prunes excess keyvalues specified for <c>multi_manager</c> entities.
                # In practice this only affects a handful of entities used in retinal scanner scripts.
                entblock = __upg_multi_manager_maxkeys__( i, Entity( entblock ), map )

                try:
                    entblock =  main.PostMapUpgrade( i, Entity( entblock ), map )
                except:
                    pass

                if isinstance( entblock, Entity ):
                    entblock = entblock.ToDict()

                entdata[i] = ( dumps( entblock ) if len( entblock ) > 0 else {} )

            global __upgrades_new_entities__

            for ae in __upgrades_new_entities__:
                entdata.append( dumps( ae ) )

            __upgrades_new_entities__ = []

            BSPEnt.import_( entdata, False )
