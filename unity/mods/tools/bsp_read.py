# ===============================================================================
# Export and import BSP entity data
# ===============================================================================

import os

def bsp_read( bsp_name, writedata = None ):

    with open( bsp_name, 'rb+' ) as bsp_file:

        bsp_file.read(4) # BSP version.
        entities_lump_start_pos = bsp_file.tell()
        read_start = int.from_bytes( bsp_file.read(4), byteorder='little' )
        read_len = int.from_bytes( bsp_file.read(4), byteorder='little' )
        bsp_file.seek( read_start )

        if writedata != None:
            writedata_bytes = writedata.encode('ascii')
            new_len = len(writedata_bytes)

            if new_len <= read_len:
                bsp_file.write(writedata_bytes)
                if new_len < read_len:
                    bsp_file.write(b'\x00' * (read_len - new_len))
            else:
                bsp_file.seek(0, os.SEEK_END)
                new_start = bsp_file.tell()
                bsp_file.write(writedata_bytes)

                bsp_file.seek(entities_lump_start_pos)
                bsp_file.write(new_start.to_bytes(4, byteorder='little'))
                bsp_file.write(new_len.to_bytes(4, byteorder='little'))
        else:
            entities_lump = bsp_file.read( read_len )
            try:
                return entities_lump.decode('ascii', errors='strict').splitlines()
            except UnicodeDecodeError:
                return entities_lump.decode('utf-8', errors='ignore').splitlines()
    return None
