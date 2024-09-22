"""
# Description

This library contains utility functions to make mod porting easy in Half-Life: Unity

Some functions may not be explicit for the mod so aim directly to the global class ``mod``

# Licence

The MIT License (MIT)

Copyright (c) 2024 Mikk155

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
    "#BSP_ENTITY_DATA_BROKEN":
    {
        "english": "Possible broken entity data in a map, Check and patch \"{}\"",
    },
    "#BSP_ENTITY_BLOCK_EXCEPTION":
    {
        "english": "Ignoring entblock before line {} possibly broken:\n{}",
    },
    "#BSP_ENTITY_SAVING":
    {
        "english": "Saving entity data in {}",
    },
    "#Entity_INIT_ERROR":
    {
        "english": "Entity instance initialised as empty",
    },
    "#printf_NotDictOrList":
    {
        "english": "'arguments' is not a 'list' or 'dict'",
    },
    "#Vector_out_of_index":
    {
        "english": "Vector is out of index. no matching index \"{}\" Supported indexes are 0 (x), 1 (y), (2) z",
    },
    "#STEAM_Unsupported":
    {
        "english": "Unsupported Operative System {}",
    },
    "#Something_went_wrong":
    {
        "english": "Something went wrong code: {}",
    },
    "#STEAM_Define":
    {
        "english": "Can not find Steam installation on your machine.\n1 - Open with any text editor the file \"{}\"\n2 - Go to the line {} and add your steam installation path to \"STEAM_INSTALLATION\"",
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
        "english": "Upgrading map {}",
    },
    "#FileNotExists":
    {
        "english": "{} Doesn't exists",
    },
    "#Installing":
    {
        "english": "Installing {}",
    },
}

#============================================================================================================
# language
#============================================================================================================

def language() -> str:

    '''
    Returns the Operative System's language, example ``english``, ``spanish``
    '''

    import locale;

    syslang = locale.getlocale();

    lang = syslang[ 0 ];

    if lang.find( '_' ) != -1: # type: ignore

        lang = lang[ 0 : lang.find( '_' ) ]; # type: ignore

    return str( lang.lower() ); # type: ignore

#============================================================================================================
# printf
#============================================================================================================

def printf( string: str | dict, arguments: dict | list[str] = [], cut_not_matched : bool = False, not_matched_trim : bool = False, dont_print : bool = False ) -> str:
    '''
    Formats the given string replacing all the closed brackets with the corresponding indexes of arguments

    ``string`` if is **dict** we'll get the language of the OS
    Returns 'english' if the label doesn't exists
    ``{ 'english': 'english string', 'spanish': 'spanish string' }``

    ``cut_not_matched`` = **True**, remove not matched brackets

    ``not_matched_trim`` = **True**, when ``cut_not_matched`` = **True**, trims leading white space for continuity

    ``dont_print`` = **True** don't print message, only return
    '''

    if isinstance( string, dict ):

        string = string.get( language, string.get( 'english', '' ) );

    if isinstance( arguments, list ):

        for __arg__ in arguments:

            string = string.replace( "{}", str( __arg__ ), 1 ); # type: ignore

        if cut_not_matched:

            __replace__ = '{} ' if not_matched_trim else '{}';

            string.replace( __replace__, '' ); # type: ignore

    elif isinstance( arguments, dict ):

        for __oarg__, __narg__ in arguments.items():

            string = string.replace( "{"+__oarg__+"}", str( __narg__ ) ); # type: ignore

            #if cut_not_matched: -TODO find open-bracket and check until closes for removing
    else:

        __except__ = printf( __Logger__[ '#printf_NotDictOrList' ], dont_print=True );

        raise Exception( __except__);

    if not dont_print:

        print( string );

    return string; # type: ignore

#============================================================================================================
# Logger System
#============================================================================================================

__LOGGER_LEVEL__ = 0

class LogLevel:
    '''Logger Level enums'''
    warning = ( 1 << 0 )
    '''Warning messages'''
    info = ( 1 << 1 )
    '''Informative messages'''
    debug = ( 1 << 2 )
    '''Debugging messages'''
    error = ( 1 << 3 )
    '''Error messages'''

class Logger:
    '''Logger instance'''

    @staticmethod
    def set_logger( logger_level: int, clear_level: bool = False ):
        '''
        Set a logger level

        ``clear_level`` if **True** instead of setting it will clear the ``LogLevel``
        '''
        global __LOGGER_LEVEL__;
        if not clear_level:
            if ( __LOGGER_LEVEL__ & logger_level ) == 0:
                __LOGGER_LEVEL__ |= logger_level;
        elif ( __LOGGER_LEVEL__ & logger_level ) != 0:
                __LOGGER_LEVEL__ &= ~logger_level;

    @staticmethod
    def __log__( log_type, message, arguments, logger_level ):
        global __LOGGER_LEVEL__;
        if ( __LOGGER_LEVEL__ & logger_level ) != 0:
            log_message = printf( message, arguments, True, True, True );
            print( '[{}] {}'.format( log_type, log_message ) );

    @staticmethod
    def debug( message: str | dict, arguments: dict | list[str] = [] ):
        '''Uses ``printf`` formatting'''
        Logger.__log__( 'Debug', message, arguments, LogLevel.debug );

    @staticmethod
    def info( message: str | dict, arguments: dict | list[str] = [] ):
        '''Uses ``printf`` formatting'''
        Logger.__log__( 'Info', message, arguments, LogLevel.info );

    @staticmethod
    def warning( message: str | dict, arguments: dict | list[str] = [] ):
        '''Uses ``printf`` formatting'''
        Logger.__log__( 'Warning', message, arguments, LogLevel.warning );

    @staticmethod
    def error( message: str | dict, arguments: dict | list[str] = [] ):
        '''Uses ``printf`` formatting'''
        Logger.__log__( 'Error', message, arguments, LogLevel.error );

#============================================================================================================
# makedirs
#============================================================================================================

def makedirs( file_path : str ):
    '''
    Creates the subfolders for the given destination file if it doesn't exists
    '''

    left_slash = file_path.rfind( '\\' );
    right_slash = file_path.rfind( '/' );

    # Get the last slash
    index = right_slash if right_slash > left_slash else left_slash;

    if index != -1:
        makedir = file_path[ : index ];

        from os import path;
        if not path.exists( makedir ):
            from os import makedirs as osmakedirs
            osmakedirs( makedir );

#============================================================================================================
# jsonc
#============================================================================================================

def jsonc( obj : list[str] | str ) -> dict | list:
    '''
    Loads a text file and skips single-line commentary before loading a json object

    ``obj`` could be a path to a .json file or either an already opened file
    '''

    __js_split__ = '';
    __lines__: list[str];

    if isinstance( obj, list ):
        __lines__ = obj;
    else:
        __lines__ = open( obj, 'r' ).readlines();

    for __line__ in __lines__:

        __line__ = __line__.strip();

        if __line__ and __line__ != '' and not __line__.startswith( '//' ):
            __js_split__ = f'{__js_split__}\n{__line__}';

    from json import loads;
    return loads( __js_split__ )

#============================================================================================================
# float to int/str conversion
#============================================================================================================
def slashfix_string( string : str ) -> str:
    '''Fix standalone backslashing on strings by adding a new one behind them if it's needed.'''
    __LastIndex__ = 0;
    while string.find( '\\', __LastIndex__ ) != -1:
        __LastIndex__ = string.find( '\\', __LastIndex__ );
        if string[ __LastIndex__ -1 : __LastIndex__ ] != '\\' and string[ __LastIndex__ + 1 : __LastIndex__ + 2 ] != '\\':
            string = string[ : __LastIndex__ + 1 ] + string[ __LastIndex__ : ];
        __LastIndex__ += 2;
    return string;

#============================================================================================================
# float to int/str conversion
#============================================================================================================

class FloatConversion:
    '''Enum for ``convert_float``'''
    none = 0
    digits_6 = 1
    digits_5 = 2
    digits_4 = 3
    digits_3 = 4
    digits_2 = 5
    digits_1 = 6
    integer = 7
    integer_round_up = 8
    integer_round_down = 9
    not_zero = 10
    '''Remove zeros from float's decimals'''

def __convert_float__( number, digits ):
    if len( number ) > digits:
        return number[ 0 : digits ];
    while len( number ) < digits:
        number += '0';
    return number;

def __conver_float_2__( number ):
    while number.find( '.' ) != -1 and ( number.endswith( '0' ) or number.endswith( '.' ) ):
        number = number[ : len( number ) - 1 ];
    return number;

def convert_float( number: float | str, float_conversion: int = FloatConversion.none ) -> str:
    '''Converts a float to int/str'''

    if isinstance( number, float ):
        number = str( number );

    if float_conversion == FloatConversion.none:
        return number; # type: ignore

    digits = number[ number.find( '.' ) + 1 : ] if number.find( '.' ) != -1 else '0'; # type: ignore

    number = number[ : number.find( '.' ) ] if number.find( '.' ) != -1 else number; # type: ignore

    if float_conversion == FloatConversion.digits_6:
        return '{}.{}'.format( number, __convert_float__( digits, 6 ) );
    elif float_conversion == FloatConversion.digits_5:
        return '{}.{}'.format( number, __convert_float__( digits, 5 ) );
    elif float_conversion == FloatConversion.digits_4:
        return '{}.{}'.format( number, __convert_float__( digits, 4 ) );
    elif float_conversion == FloatConversion.digits_3:
        return '{}.{}'.format( number, __convert_float__( digits, 3 ) );
    elif float_conversion == FloatConversion.digits_2:
        return '{}.{}'.format( number, __convert_float__( digits, 2 ) );
    elif float_conversion == FloatConversion.digits_1:
        return '{}.{}'.format( number, __convert_float__( digits, 1 ) );
    elif float_conversion == FloatConversion.integer:
        return number if int( digits[0] ) < 5 else str( int( number ) + 1 ); # type: ignore
    elif float_conversion == FloatConversion.integer_round_up:
        return number if int( digits[0] ) == 0 else str( int( number ) + 1 ); # type: ignore
    elif float_conversion == FloatConversion.integer_round_down:
        return number if int( digits[0] ) != 0 else str( int( number ) + 1 ); # type: ignore
    elif float_conversion == FloatConversion.not_zero:
        return __conver_float_2__( '{}.{}'.format( number, digits ) );

    return number; # type: ignore

#============================================================================================================
# Vector
#============================================================================================================

# TODO: Normalize, Length
class Vector:
    '''Vector class'''

    def __init__( self, x: int | str = 0, y = 0, z = 0 ):
        '''
        Initialise a Vector.

        if ``x`` is a str it will split spaces or comas to make the Vector

        if no arguments provided it will be 0, 0, 0
        '''

        if isinstance( x, str ):
            from re import sub;
            x = sub( r'[^0-9. -]', '', x );
            __values__ = x.split( ',' ) if x.find( ',' ) != -1 else x.split();
            if len( __values__ ) < 3:
                __values__ += [ '0' ] * ( 3 - len( __values__ ) );
            self.x, self.y, self.z = [ self.__parse_value__( v ) for v in __values__[ : 3 ] ];

        else:
            self.x = self.__parse_value__( x ) if isinstance( x, ( float, int ) ) else 0;
            self.y = self.__parse_value__( y ) if isinstance( y, ( float, int ) ) else 0;
            self.z = self.__parse_value__( z ) if isinstance( z, ( float, int ) ) else 0;

    def __parse_value__( self, __value__ ):
        __value__ = float( __value__ );
        if __value__.is_integer() or __value__ == int( __value__ ):
            return float( int( __value__ ) );
        return __value__;

    def to_string( self, apply_coma : bool = False, rounded : int = FloatConversion.not_zero ) -> str:
        '''
        Converts a ``Vector`` to a ``str``

        ``apply_coma`` if **True** apply a coma to the vectors

        ``rounded`` Explicitly set how to round the values
        '''
        coma = ',' if apply_coma else ''
        return '{}{} {}{} {}'.format( convert_float( str( self.x ), rounded ), coma, convert_float( str( self.y ), rounded ), coma, convert_float( str( self.z ), rounded ) )

    def to_list( self ) -> list[float]:
        '''Converts a ``Vector`` to a ``list[float]``'''
        return [ self.x, self.y, self.z ];

    def __getitem__( self, index: int ) -> float:

        if index == 0:
            return self.x;

        elif index == 1:
            return self.y;

        elif index == 2:
            return self.z;

        else:
            Logger.warning( __Logger__[ '#Vector_out_of_index' ], [ index ], ); # type: ignore
            return 0;

    def __setitem__( self, index, new_value ):

        if index == 0:
            self.x = self.__parse_value__( new_value );

        elif index == 1:
            self.y = self.__parse_value__( new_value );

        elif index == 2:
            self.z = self.__parse_value__( new_value );

        else:
            Logger.warning( __Logger__[ '#Vector_out_of_index' ], [ index ], );

    def __repr__( self ):
        return self.to_string()
        #return "Vector( {} )".format( self.to_string( True, FloatConversion.digits_6 ) ); # type: ignore

    def __add__( self, other ):
        return Vector( self.x + other.x, self.y + other.y, self.z + other.z );

    def __sub__( self, other ):
        return Vector( self.x - other.x, self.y - other.y, self.z - other.z );

    def __mul__( self, scalar ):
        return Vector( self.x * scalar.x, self.y * scalar.y, self.z * scalar.z ) if isinstance( scalar, Vector ) else Vector( self.x * scalar, self.y * scalar, self.z * scalar ); # type: ignore

    def __eq__( self, other ):
        return ( self.x == other.x and self.z == other.z and self.y == other.y ) if isinstance( other, Vector ) else False;

    def __ne__( self, other ):
        return not self.__eq__( other );

#============================================================================================================
# wildcard
#============================================================================================================

def wildcard( compare : str, comparator : str, wildcard : str = '*' ) -> bool:
    '''
    Compare ``compare`` with ``comparator`` and see if they fully match or partial match by starting, ending or middle ``wildcard``
    '''

    if compare == comparator:
        return True;

    elif wildcard not in comparator:
        return False;

    __parts__ = comparator.split( wildcard );

    for __i__, __p__ in enumerate( __parts__ ):
        if __p__ == '':
            __parts__.pop( __i__ );

    __index__ : int = 0;
    __matched__ : bool = True if len( __parts__ ) > 0 else False;

    for __p__ in __parts__:
        if compare.find( __p__, __index__ ) < __index__:
            __matched__ = False;
            break;
        else:
            __index__ = compare.find( __p__, __index__ );

    return __matched__;

#============================================================================================================
# Installation paths
#============================================================================================================

def STEAM() -> str:

    '''
    Get steam's installation path
    '''

    from platform import system;

    __OS__ = system();

    from os import path;

    if __OS__ == "Windows":

        __paths__ = [
            path.expandvars( r"%ProgramFiles(x86)%\Steam" ),
            path.expandvars( r"%ProgramFiles%\Steam" )
        ];

        for __path__ in __paths__:
            if path.exists( __path__ ):
                return __path__;

        try:
            import winreg;
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
                return winreg.QueryValueEx(key, "SteamPath")[0];
        except (ImportError, FileNotFoundError, OSError, PermissionError) as e:
            Logger.error( __Logger__[ "#Something_went_wrong" ], [ e ] ); # type: ignore

    elif __OS__ == "Linux":
        __paths__ = [
            "/usr/bin/steam",
            "/usr/local/bin/steam"
        ];

        for __path__ in __paths__:
            if path.exists( __path__ ):
                return path.dirname( path.abspath( __path__ ) );

    else:
        Logger.error( __Logger__[ "#STEAM_Unsupported" ], [ __OS__ ] );

    # Define your custom steam installation path in here
    # Should look like "C:\Program Files (x86)\Steam"
    STEAM_INSTALLATION = ''

    if STEAM_INSTALLATION == '' or not path.exists( STEAM_INSTALLATION ):
        from inspect import getsourcelines;
        l, ln = getsourcelines( lambda: STEAM_INSTALLATION );
        printf( __Logger__[ "#STEAM_Define" ], [ __file__, str( ln - 4 ) ] );
        input();
        raise ValueError( 'Undefined Steam installation' );
    else:
        return STEAM_INSTALLATION;

def HALFLIFE() -> str:

    '''
    Get "Half-Life" folder within a steam installation
    '''

    from os import path;

    __STEAM__ = STEAM();

    if __STEAM__:
        __HALFLIFE__ = f'{__STEAM__}\\steamapps\\common\\Half-Life';
        if path.exists( __HALFLIFE__ ):
            return __HALFLIFE__;

    # Define your custom steam installation path in here
    # Should look like "C:\Program Files (x86)\Steam\steamapps\common\Half-Life"
    HALFLIFE_INSTALLATION = ''

    if HALFLIFE_INSTALLATION == '' or not path.exists( HALFLIFE_INSTALLATION ):
        from inspect import getsourcelines;
        l, ln = getsourcelines( lambda: HALFLIFE_INSTALLATION );
        printf( __Logger__[ "#STEAM_Define" ], [ __file__, str( ln - 4 ) ] );
        input();
        raise ValueError( 'Undefined Steam installation' );
    else:
        return HALFLIFE_INSTALLATION;

#============================================================================================================
# BSP
#============================================================================================================

class Entity( dict ):
    '''
    Entity is basically a dict representing a entity block from a entity lump in a BSP

    Access any key-value with a dot, returns None if not set, set keys to None to remove the key-value pair

    Convert to str for getting the entblock as-is in the entity lump
    '''
    def __init__( self, data: dict = None ): # type: ignore
        if isinstance( data, dict ):
            super().__init__( data );
        elif isinstance( data, Entity ):
            super().__init__( data );
        else:
            try:
                from json import loads;
                super().__init__( loads( data ) );
            except:
                super().__init__( {} );
                Logger.warning( __Logger__[ "#Entity_INIT_ERROR" ] );

    def __getattr__( self, key ) -> str:
        return str( self[ key ] ) if key in self else None; # type: ignore

    def __setattr__( self, key, value ):
        if key == 'KeyValueData':
            super().__setattr__( key, value );
        elif value == None:
            self.pop( key, '' );
        else:
            self[ key ] = str( value );

    def __repr__( self ):
        entblock = '{\n';
        for key, value in self.items():
            entblock += f'"{key}" "{value}"\n'
        entblock += '}\n'
        return entblock;

    def __str__( self ):
        return self.__repr__();

def ent_to_json( entdata : list[Entity] | list[dict], json_path : str ):
    with open( json_path, 'w' ) as jsonfile:
        Logger.info( __Logger__[ "#BSP_ENTITY_SAVING" ], [ json_path ] );
        from json import dumps;
        jsonfile.writelines( dumps( entdata, indent=4 ) );
        jsonfile.close()

def ent_to_list( entity_data : list[str] ) -> list[Entity]:
    '''Converts the regular entity data (.ent) to a list of dict'''
    entblock = {};
    entdata = [];
    oldline = '';

    from json import loads, dumps;

    for i, line in enumerate( entity_data ):

        if line == '{':
            continue;

        line = line.strip();

        if not line.endswith( '"' ):
            oldline = line;
        elif oldline != '' and not line.startswith( '"' ):
            line = f'{oldline}{line}';

        # This fixes some problems due to "wad" containing full paths
        line = slashfix_string( line );

        line = line.strip( '"' );

        if not line or line == '':
            continue;

        if line.startswith( '}' ): # startswith due to [NULL]
            try:
                lump = dumps( entblock );
                block = loads( lump );
                entdata.append( Entity( block ) );
            except Exception:
                Logger.warning( __Logger__[ "#BSP_ENTITY_BLOCK_EXCEPTION" ], [ str( i ), str( entblock ) ] );
            entblock.clear();
        else:
            keyvalues = line.split( '" "' );
            if len( keyvalues ) == 2:
                entblock[ keyvalues[0] ] = keyvalues[1];

    return entdata;

class BSP_LUMPS:
    LUMP_ENTITIES     =  0
    LUMP_PLANES       =  1
    LUMP_TEXTURES     =  2
    LUMP_VERTICES     =  3
    LUMP_VISIBILITY   =  4
    LUMP_NODES        =  5
    LUMP_TEXINFO      =  6
    LUMP_FACES        =  7
    LUMP_LIGHTING     =  8
    LUMP_CLIPNODES    =  9
    LUMP_LEAVES       = 10
    LUMP_MARKSURFACES = 11
    LUMP_EDGES        = 12
    LUMP_SURFEDGES    = 13
    LUMP_MODELS       = 14
    HEADER_LUMPS      = 15

class BSP_LUMP:

    def __init__( self, offset: int, length: int ):

        self.nOffset = offset;

        self.nLength = length;

    def to_bytes( self ) -> bytes:
        '''
        Return the number of bytes for this lump
        '''

        offset_bytes = self.nOffset.to_bytes( 4, byteorder='little' );
        length_bytes = self.nLength.to_bytes( 4, byteorder='little' );

        return ( offset_bytes + length_bytes );

class BSP_HEADER:

    def __init__( self, version: int, lumps ):
        self.nVersion = version
        self.lump = lumps

    def to_bytes( self ) -> bytes:
        '''Return the header bytes for lumps'''

        header_bytes = self.nVersion.to_bytes( 4, byteorder='little' );

        for lump in self.lump:
            header_bytes += lump.to_bytes();

        return header_bytes;

    @classmethod
    def from_file( cls, file ):

        import struct

        version = struct.unpack( 'i', file.read( 4 ) )[0];

        lumps = []

        file.seek( 0 )

        file.read( 4 )
        
        for i in range( BSP_LUMPS.HEADER_LUMPS ):

            offset = int.from_bytes( file.read( 4 ), byteorder='little' );

            length = int.from_bytes( file.read( 4 ), byteorder='little' );

            lumps.append( BSP_LUMP( offset, length ) );
        
        return cls( version, lumps )

class BSP:

    def __init__(self, bsp_path: str):

        '''
        Don't know how to do this automatically so when importing data to a newer instance of a BSP
        Make sure to first call ``read_entities`` before importing fresh data so we keep track of the null byte in ``self.null``
        '''

        self.null = None

        self.__get_path_and_name__( bsp_path )

        bsp_file = open(self.abspath(), 'rb+')

        self.header = BSP_HEADER.from_file( bsp_file );

    def read_lump( self, lump : BSP_LUMPS ) -> bytes:
        '''
        Reads a lump and returns the bytes
        '''
        header: BSP_LUMP = self.header.lump[ lump ];

        with open( self.abspath(), 'rb+' ) as bsp_file:

            bsp_file.seek( header.nOffset );

            lump_read = bsp_file.read( header.nLength );

            return lump_read;

    def write_data( self, ent_data: list[Entity] | list[dict] = None ) -> list[Entity]: # type: ignore
        '''
        Writes the given entity data into it's lump
        '''
        for i, entblock in enumerate( ent_data.copy() ):

            if not isinstance( entblock, Entity ):

                ent_data[ i ] = Entity( entblock );

        self.entities = ent_data;

        self.import_data();

    def read_entities( self ) -> list[Entity]:
        '''
        Reads the entity lump and returns a json object in a list of dict
        '''

        entities_lump = self.read_lump( BSP_LUMPS.LUMP_ENTITIES ); # type: ignore

        try:

            map_entities = entities_lump.decode( 'ascii', errors='strict' ).splitlines();

        except UnicodeDecodeError:

            map_entities = entities_lump.decode( 'utf-8', errors='ignore' ).splitlines();

            Logger.warning( __Logger__[ '#BSP_ENTITY_DATA_BROKEN' ], [ self.path() + self.name() + 'json' ] );

        if map_entities[ len( map_entities ) - 1 ] != '}':

            self.null = map_entities[ len( map_entities ) - 1 ]

        self.entities = ent_to_list( map_entities );

        return self.entities;

    def __get_path_and_name__( self, bsp_path ):

        __formatted_path__ = bsp_path.replace('/', '\\')

        if not __formatted_path__.endswith('.bsp'):

            __formatted_path__ = '{}.bsp'.format(__formatted_path__)

        __subdirs__ = __formatted_path__.split( '\\' )

        __name__ = __subdirs__[len(__subdirs__) - 1]


        self.___name__ = __name__[:len(__name__) - 4]

        self.__path__ = __formatted_path__[:__formatted_path__.rfind('\\') + 1]

    def path( self ):
        '''
        Returns the path to where this BSP is located
        '''
        return self.__path__

    def name( self ):
        '''
        Returns the name of the BSP file without file extension
        '''
        return self.___name__

    def abspath( self ):
        '''
        Returns the absolute path to this BSP file, the path is formatted to use normal slash
        '''
        return '{}{}.bsp'.format(self.__path__, self.___name__).replace('\\', '/')

    def export_json( self, filename: str = None ): # type: ignore
        '''
        Writes a json object containing the entity data

        ``filename`` if not set, it will be located where the BSP is
        '''

        if not filename:

            filename = '{}{}.json'.format( self.path(), self.name() );

        elif not filename.endswith( '.json' ):

            filename = '{}.json'.format( filename );

        ent_to_json( self.read_entities(), filename );

    def write_lump( self, lump: BSP_LUMPS, write_bytes: bytes ):
        '''
        Write bytes to a specific lump and clamp the length to the new length
        '''

        header: BSP_LUMP = self.header.lump[ lump ];

        with open( self.abspath(), 'rb+' ) as bsp_file:

            bsp_file.seek( 0 );

            data = bsp_file.read();

            new_length = len( write_bytes );

            old_length = header.nLength;

            delta = new_length - old_length;

            new_data = (
                data[ : header.nOffset ] +
                write_bytes +
                data[ header.nOffset + old_length : ]
            );

            header.nLength = new_length;

            if delta != 0:
                for lump_header in self.header.lump:
                    if lump_header.nOffset > header.nOffset:
                        lump_header.nOffset += delta;

            bsp_file.seek( 0 );

            bsp_file.write( new_data );

        self.__update_global_header__();

    def __update_global_header__( self ):

        with open( self.abspath(), 'rb+' ) as bsp_file:

            bsp_file.seek( 0 );

            bsp_file.write( self.header.to_bytes() );


    def import_data( self ):

        newdata = '';

        for i, entblock in enumerate( self.entities ):

            if len( entblock ) <= 0:
                continue;

            newdata = '{}{}'.format( newdata, str( entblock ) );

        if self.null:

            newdata = newdata[ : newdata.rfind( '}' ) ] + self.null;

        writedata_bytes = newdata.encode( 'ascii' );

        self.write_lump( BSP_LUMPS.LUMP_ENTITIES, writedata_bytes ); # type: ignore
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
                Logger.error( __Logger__[ '#pak_NotValidPak' ], [ __paks__ ] )
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
                    Logger.warning( __Logger__[ '#pak_Skipping' ], [ name ] )
                    continue

                with open( extract_path, 'wb') as out_file:
                    Logger.info( __Logger__[ '#pak_Extracted' ], [ name ] )
                    out_file.write( data )

__upgrades_new_entities__: list[Entity] = []

def add_entity( entity:Entity ):
    '''
        Adds a new entity to the current MapUpgrader instance
    '''
    global __upgrades_new_entities__;
    __upgrades_new_entities__.append( entity if isinstance( entity, dict ) else entity )

class MapUpgrader:

    class Upgrades:
        OpposingForce = False;
        '''Change to **True** For applying Opposing-Force mods upgrades'''
        Cooperative = False;
        '''Change to **True** For applying Co-Operative mods upgrades'''
        SvenCoop = False;
        '''Change to **True** For applying Sven Co-op mods upgrades'''

    def __init__( self, bsp_path : str ):
        self.__bsp_path__ = bsp_path;

    def upgrade( self ):
        '''
        Apply map upgrades

        You can hook your own upgrades in ``__main__``

        ``def PreMapUpgrade( index : int, entity : Entity, map : str ):``

        ``def PostMapUpgrade( index : int, entity : Entity, map : str ):``

        These upgrades has been ported from C#

        https://github.com/twhl-community/HalfLife.UnifiedSdk-CSharp/tree/master/src/HalfLife.UnifiedSdk.MapUpgrader.Upgrades
        '''

        bsp = BSP( self.__bsp_path__ );

        entdata = bsp.read_entities();

        Logger.info( __Logger__[ '#upgrades_upgrading_map' ], [ bsp.name() ] );

        TempEntData = entdata.copy()

        from json import dumps
        import __main__ as main

        for i, entblock in enumerate( TempEntData ):

            try:
                entblock =  main.PreMapUpgrade( i, Entity( entblock ), bsp.name() )
            except:
                pass

            entblock = self.__upg_angle_to_angles__( i, Entity( entblock ), bsp.name() )
            if self.Upgrades.OpposingForce: # Pre __upg_remap_classnames__
                entblock = self.__upg_op4_TankPersistance__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_remap_classnames__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_worldspawn_format_wad__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_chargers_dmdelay__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_remap_world_items__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_update_human_hulls__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_ambient_generic_pitch__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_barney_dead_body__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_breakable_spawnobject__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_event_playerdie__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_event_playerleave__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_event_playerkill__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_event_playeractivate__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_event_playerjoin__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_event_playerspawn__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_fix_sounds_indexes__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_rendercolor_invalid__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_multi_manager_maxkeys__( i, Entity( entblock ), bsp.name() )
            entblock = self.__upg_env_message_to_game_text__( i, Entity( entblock ), bsp.name() )

            if self.Upgrades.OpposingForce:

                entblock = self.__upg_op4_FixMassnHeadSkin__( i, Entity( entblock ), bsp.name() )
                entblock = self.__upg_op4_OtisBodyState__( i, Entity( entblock ), bsp.name() )
                entblock = self.__upg_op4_ScientistBody__( i, Entity( entblock ), bsp.name() )
                entblock = self.__upg_op4_ItemSuit__( i, Entity( entblock ), bsp.name() )
                entblock = self.__upg_op4_RemoveGameModeSetting__( i, Entity( entblock ), bsp.name() )
                entblock = self.__upg_op4_MassnAnimations__( i, Entity( entblock ), bsp.name() )

            try:
                entblock =  main.PostMapUpgrade( i, Entity( entblock ), bsp.name() )
            except:
                pass

            tempentblock = entblock.copy()
            for e, v in tempentblock.items():
                if not v or v is None:
                    entblock.pop( e )

            entdata[i] = ( dumps( entblock ) if len( entblock ) > 0 else {} ) # type: ignore

        global __upgrades_new_entities__;
        for ae in __upgrades_new_entities__:
            entdata.append( dumps( ae ) ) # type: ignore

        __upgrades_new_entities__ = []

        bsp.write_data( entdata );

    class __TempData__:
        __upg_game_playerdie__ = False
        __upg_game_playerleave__ = False
        __upg_game_playerkill__ = False
        __upg_game_playeractivate__ = False
        __upg_game_playerjoin__ = False
        __upg_game_playerspawn__ = False

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

        # Add weapons and items above because game_playerequip will break and stop when get monster_ShockTrooper_dead
        "monster_ShockTrooper_dead": "monster_shocktrooper_dead",
        "button_target": "func_button_target",
        "momentary_rot_button": "func_button_rotating",
        "func_tank_of": "func_tank",
        "func_tanklaser_of": "func_tanklaser",
        "func_tankrocket_of": "func_tankrocket",
        "func_tankcontrols_of": "func_tankcontrols",
    }

    def __upg_remap_classnames__( self, index:int, entity:Entity, map:str ):
        '''Renames classnames to their new classname.'''
        if entity.classname in self.__upg_ItemMapping__:

            entity.classname = self.__upg_ItemMapping__.get( entity.classname );

        elif entity.classname == 'game_player_equip':

            for old, new in self.__upg_ItemMapping__.items():

                if old[0] in [ 'w', 'i', 'a' ] and old in entity:
                    entity[ new ] = entity.get( old );
                    entity.pop( old );

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
        def __init__( self, KeyName:str, DefaultValue:str = None, Names:list[str] = None, Optional:str = None ): # type: ignore
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
        "func_button_rotating": __upg_FixSoundsData__( "sounds", __upg_DefaultMomentaryButtonSound__, __upg_ButtonSounds__ ),
        "func_train": __upg_PlatData__,
        "func_plat": __upg_PlatData__,
        "func_platrot": __upg_PlatData__,
        "func_trackchange": __upg_PlatData__,
        "func_trackautochange": __upg_PlatData__,
        "env_spritetrain": __upg_PlatData__,
        "func_tracktrain": __upg_FixSoundsData__( "sounds", __upg_DefaultTrackTrainSound__, __upg_TrackTrainMoveSounds__ )
    }

    def __upg_angle_to_angles__( self, index : int, entity : Entity, map : str ) -> Entity:
        '''Converts the obsolete "angle" keyvalue to "angles"'''
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

    def __upg_worldspawn_format_wad__( self, index:int, entity:Entity, map:str ):
        '''Delete wad paths to prevent issues'''
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

    def __upg_chargers_dmdelay__( self, index:int, entity:Entity, map:str ):
        '''Removes the "dmdelay" keyvalue from charger entities.

        The original game ignores these.'''
        if entity.classname in [ 'func_healthcharger', 'func_recharge' ]:
            entity.dmdelay = None
        return entity

    def __upg_remap_world_items__( self, index:int, entity:Entity, map:str ):
        '''Converts world_items entities to their equivalent entity.'''
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
                keytypevalue = ' "' + entity.value + '"' if entity.value else '';
                Logger.warning( __Logger__[ '#upgrades_unknown_keyvalue' ], [ f'"type"{keytypevalue}', 'world_items' ] )
                entity.clear()
        return entity

    def __upg_update_human_hulls__( self, index:int, entity:Entity, map:str ):
        '''Sets a custom hull size for monster_generic entities that use a model that was originally hard-coded to use one.'''
        if entity.classname in [ 'monster_generic', 'monster_generic' ] and entity.model in [ 'models/player.mdl', 'models/holo.mdl' ]:
            entity.custom_hull_min = Vector( -16, -16, -36 )
            entity.custom_hull_max = Vector( 16, 16, 36 )
        return entity

    def __upg_ambient_generic_pitch__( self, index:int, entity:Entity, map:str ):
        '''Find all buttons/bell1.wav sounds that have a pitch set to 80.

        Change those to use an alternative sound and set their pitch to 100.'''
        if entity.classname == 'ambient_generic' and entity.message == 'buttons/bell1.wav' and entity.pitch == '80':
            entity.message = 'buttons/bell1_alt.wav'
            entity.pitch = 100
        return entity

    def __upg_barney_dead_body__( self, index:int, entity:Entity, map:str ):
        '''Converts monster_barney_dead entities with custom body value to use the new bodystate keyvalue.'''
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

    def __upg_breakable_spawnobject__( self, index:int, entity:Entity, map:str ):
        '''Converts func_breakable's spawn object keyvalue from an index to a classname.'''
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
                        Logger.warning( __Logger__[ '#upgrades_unknown_keyvalue' ], [ f'"spawnobject" "{i}"', entity.classname ] )
        return entity

    __upg_eventhandler__ = Entity( { "classname": "trigger_eventhandler", "m_Caller": "!activator" } )

    def __upg_event_playerdie__( self, index:int, entity:Entity, map:str ):
        '''Convert special targetnames to our new entity trigger_eventhandler'''
        if not self.__TempData__.__upg_game_playerdie__ and entity.targetname == 'game_playerdie':
            self.__upg_eventhandler__.target = entity.targetname
            self.__upg_eventhandler__.event_type = 1
            add_entity( self.__upg_eventhandler__ )
            self.__TempData__.__upg_game_playerdie__ = True
        return entity

    def __upg_event_playerleave__( self, index:int, entity:Entity, map:str ):
        '''Convert special targetnames to our new entity trigger_eventhandler'''
        if not self.__TempData__.__upg_game_playerleave__ and entity.targetname == 'game_playerleave':
            self.__upg_eventhandler__target = entity.targetname
            self.__upg_eventhandler__event_type = 2
            add_entity( self.__upg_eventhandler__ )
            self.__TempData__.__upg_game_playerleave__ = True
        return entity

    def __upg_event_playerkill__( self, index:int, entity:Entity, map:str ):
        '''Convert special targetnames to our new entity trigger_eventhandler'''
        if not self.__TempData__.__upg_game_playerkill__ and entity.targetname == 'game_playerkill':
            self.__upg_eventhandler__target = 'game_playerkill_check'
            self.__upg_eventhandler__event_type = 3
            add_entity( self.__upg_eventhandler__ )
            Newent = {
                "classname": "trigger_entity_condition",
                "targetname": "game_playerkill_check",
                "pass_target": "game_playerkill",
                "condition": "0"
            }
            add_entity( Entity( Newent ) )
            self.__TempData__.__upg_game_playerkill__ = True
        return entity

    def __upg_event_playeractivate__( self, index:int, entity:Entity, map:str ):
        '''Convert special targetnames to our new entity trigger_eventhandler'''
        if not self.__TempData__.__upg_game_playeractivate__ and entity.targetname == 'game_playeractivate':
            self.__upg_eventhandler__target = entity.targetname
            self.__upg_eventhandler__event_type = 4
            add_entity( self.__upg_eventhandler__ )
            self.__TempData__.__upg_game_playeractivate__ = True
        return entity

    def __upg_event_playerjoin__( self, index:int, entity:Entity, map:str ):
        '''Convert special targetnames to our new entity trigger_eventhandler'''
        if not self.__TempData__.__upg_game_playerjoin__ and entity.targetname == 'game_playerjoin':
            self.__upg_eventhandler__target = entity.targetname
            self.__upg_eventhandler__event_type = 5
            Newent = self.__upg_eventhandler__.copy()
            Newent[ "appearflag_multiplayer" ] = "1" # Only in multiplayer
            add_entity( Entity( Newent ) )
            self.__TempData__.__upg_game_playerjoin__ = True
        return entity

    def __upg_event_playerspawn__( self, index:int, entity:Entity, map:str ):
        '''Convert special targetnames to our new entity trigger_eventhandler'''
        if not self.__TempData__.__upg_game_playerspawn__ and entity.targetname == 'game_playerspawn':
            self.__upg_eventhandler__target = entity.targetname
            self.__upg_eventhandler__event_type = 6
            add_entity( self.__upg_eventhandler__ )
            self.__TempData__.__upg_game_playerspawn__ = True
        return entity

    def __upg_TryFixSoundsEnt__( self, entity:dict, Data:__upg_FixSoundsData__ ):
        #-TODO "func_rotating": __upg_FixSoundsData__( "sounds", __upg_DefaultSound__, __upg_RotatingMoveSounds__, "message" ),
        # [cl] [sound.cache] [error] Could not find sound file message
        name = Data.Optional
        if name is None:
            name = Data.DefaultValue
            if Data.KeyName in entity and entity.get( Data.KeyName, '' ).isnumeric():
                index = int( entity.get( Data.KeyName, '' ) )
                if index >= 0 and index < len( Data.Names ):
                    name = Data.Names[ index ]
        entity[ Data.KeyName ] = None
        if len( name ) > 0:
            entity[ Data.KeyName ] = name
        return Entity( entity )

    def __upg_fix_sounds_indexes__( self, index:int, entity:Entity, map:str ):
        '''Converts all entities that use sounds or sentences by index to use sound filenames or sentence names instead.'''
        if entity.classname in self.__upg_FixSoundsEntityData__:
            DataFix = self.__upg_FixSoundsEntityData__.get( entity.classname )
            if isinstance( DataFix, self.__upg_FixSoundsData__ ):
                entity = self.__upg_TryFixSoundsEnt__( entity, DataFix )
            else:
                for D in DataFix: # type: ignore
                    entity = self.__upg_TryFixSoundsEnt__( entity, D )
        return entity

    def __upg_rendercolor_invalid__( self, index:int, entity:Entity, map:str ):
        '''Fixes the use of invalid render color formats in some maps.'''
        if entity.rendercolor != None:
            entity.rendercolor = Vector( entity.rendercolor ).to_string()
        return entity

    def __upg_multi_manager_maxkeys__( self, index:int, entity:Entity, map:str ):
        '''Prunes excess keyvalues specified for multi_manager entities.

        In practice this only affects a handful of entities used in retinal scanner scripts.'''
        if entity.classname == 'multi_manager':
            KeySize = 16
            NewEnt = {}
            pEnt = entity.copy()
            ignorelist = { "targetname", "classname", "origin", "wait", "spawnflags" }
            for p in ignorelist:
                if p in entity:
                    NewEnt[ p ] = entity.get( p )
                    KeySize+=1
            for p, v in pEnt.items():
                NewEnt[ p ] = v
                if len( NewEnt ) >= KeySize:
                    break
            if len( entity ) > len( NewEnt ):
                for k, v in NewEnt.items():
                    if not k in ignorelist:
                        pEnt.pop( k, '' )
                pEnt[ "targetname" ] = entity.targetname + f'_{index}' # type: ignore
                AnotherEnt = self.__upg_multi_manager_maxkeys__( index, Entity( pEnt ), map );
                add_entity( AnotherEnt )
                NewEnt[ pEnt.get( "targetname" ) ] = 0
                Logger.info( __Logger__[ '#upgrades_multi_manager_exceds' ] )
            for k in ignorelist:
                if k in entity:
                    NewEnt[ k ] = entity.get( k, '' )
            entity = Entity( NewEnt )
        return entity

    def __upg_env_message_to_game_text__( self, index:int, entity:Entity, map:str ):
        if entity.classname == 'env_message':
            try:
                from __main__ import titles
                sztitles = open( titles, 'r' )
            except:
                s:str
                #logger( "No \"titles\" path defined in main", logger_level=LOGGER_LEVEL.IMPORTANT )
        return entity

    def __upg_op4_FixMassnHeadSkin__( self, index:int, entity:Entity, map:str ):
        '''Adjust monster_male_assassin NPCs to use the correct head and skin value.'''
        if entity.classname == 'monster_male_assassin':
            head = int( entity.head ) if entity.head else 0;
            skin = 0;
            if head == 1:
                head = 0;
                skin = 1
            elif head == 2:
                head = 1;
                skin = 1;
            entity.head = head;
            entity.skin = skin;
        return entity

    def __upg_op4_OtisBodyState__( self, index:int, entity:Entity, map:str ):
        '''Converts monster_otis bodystate keyvalues to no longer include the Random value, which is equivalent to Holstered.'''
        if entity.classname == 'monster_otis':
            if entity.bodystate and int( entity.bodystate ) == -1:
                entity.bodystate = 0;
        return entity

    def __upg_op4_ScientistBody__( self, index:int, entity:Entity, map:str ):
        '''Converts the Opposing Force scientist clipboard and stick heads to use the item body group instead.'''
        def DetermineValues( body ):
            values = {
                4: (1, 1),
                5: (3, 2)
            }
            return values.get( body, ( body, 0 ) );
        if entity.classname == 'monster_scientist' and entity.body:
            new_body, item = DetermineValues( entity.body )
            entity.item = item;
            entity.body = new_body;
        elif entity.classname == 'monster_generic' and entity.model == 'models/scientist.mdl':
            # Update any generics that use the model.
            new_body, item = DetermineValues( entity.body )
            entity.item = item;
            entity.body = new_body;
            StudioCount = 1;
            HeadsCount = 4;
            NeedleCount = 2;
            # This hardcoded stuff is pretty ugly, but there is no way around it without loading the model.
            new_body = int(new_body) + ( StudioCount * HeadsCount * NeedleCount * item );
            entity.body = new_body;
        return entity

    def __upg_op4_ItemSuit__( self, index:int, entity:Entity, map:str ):
        '''Converts item_suit's model to use w_pcv.mdl in Opposing Force maps.'''
        if entity.classname == 'item_suit':
            entity.model = 'models/w_pcv.mdl';
        return entity

    def __upg_op4_TankPersistance__( self, index:int, entity:Entity, map:str ):
        '''Disables the persistence behavior for all Opposing Force tank entities to match the original's behavior.'''
        if entity.classname in [ "func_tank_of", "func_tanklaser_of", "func_tankrocket_of", "func_tankmortar_of" ]:
            entity.persistence = 0;
        return entity

    def __upg_op4_RemoveGameModeSetting__( self, index:int, entity:Entity, map:str ):
        '''Removes the CTF game mode settings from Opposing Force maps.'''
        if entity.classname == 'worldspawn':
            entity.defaultctf = None;
        return entity

    def __upg_op4_MassnAnimations__( self, index:int, entity:Entity, map:str ):
        '''Renames certain animations referenced by <c>scripted_sequence</c>s targeting <c>monster_male_assassin</c> or entities using its model to use the new animation names.'''
        #if entity.classname == 'monster_male_assassin':
            # private static readonly ImmutableDictionary<string, string> AnimationRemap = new Dictionary<string, string>
            # {
            #     { "strafeleft", "strafeleft_cine" },
            #     { "straferight", "straferight_cine" }
            # }.ToImmutableDictionary();

            # protected override void ApplyCore(MapUpgradeContext context)
            # {
            #     ScriptedSequenceUtilities.RenameAnimations(context, "monster_male_assassin", "models/massn.mdl", AnimationRemap);
            # }
        return entity

    def __upg_op4_OtisAnimations__( self, index:int, entity:Entity, map:str ):
        '''Renames certain animations referenced by <c>scripted_sequence</c>s targeting <c>monster_otis</c> or entities using its model to use the new animation names.'''
        #if entity.classname == 'monster_otis':
            # private static readonly ImmutableDictionary<string, string> AnimationRemap = new Dictionary<string, string>
            # {
            #     { "fence", "otis_fence" },
            #     { "wave", "otis_wave" }
            # }.ToImmutableDictionary();

            # protected override void ApplyCore(MapUpgradeContext context)
            # {
            #     ScriptedSequenceUtilities.RenameAnimations(context, "monster_otis", "models/otis.mdl", AnimationRemap);
            # }
        return entity

class __ModPorting__:

    def __init__( self ):

        import os
        self.__workdir__ = '{}\\unity'.format( os.path.abspath( "" ) );

    __workdir__:str

    def workdir( self ) -> str:
        '''Working directory. consider this as unity_addon/ folder just before copying all within it'''
        return self.__workdir__;

    class maps:

        @staticmethod
        def copy( mod_path: str, ignore_maps: list[str] = [] ) -> dict[ str, str ]:
            '''
            Copy all the BSP files from ``mod_path`` to a working directory then returns a dicto of [ filename, file absolute path ]

            ``ignore_maps`` Maps to ignore
            '''

            from os import walk
            from shutil import copy2

            map_list = {};

            maps_mfolder = '{}\\maps'.format( mod_path );
            maps_dfolder = '{}\\maps'.format( mod.workdir() );

            makedirs( maps_dfolder+'\\' );

            for root, dirs, files in walk( maps_mfolder ):

                for file in files:

                    if file.endswith( '.bsp' ):

                        src = '{}\\{}'.format( maps_mfolder, file );

                        dest = '{}\\{}'.format( maps_dfolder, file );

                        map_list[file] = dest;

                        copy2( src, dest );

            return map_list;

global mod;
mod = __ModPorting__();
'''This class should be used when porting mods'''
