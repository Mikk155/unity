# ===============================================================================
# Download additional third-party assets
# ===============================================================================

import os
import io
import zipfile
import requests

from tools.path import port

def download( urls ):

    links = []

    if isinstance( urls, str ):
        links.append( urls )
    else:
        links = urls

    for url in links:
        print( f'[download] Downloading third-party assets\n{url}' )

        response = requests.get( url )

        if response.status_code == 200:

            zip_file = zipfile.ZipFile( io.BytesIO( response.content ) )

            zip_file.extractall( "test" )

            for member in zip_file.namelist():

                filename = os.path.basename( member )

                if not filename:
                    continue

                source = zip_file.open( member )

                target = open( os.path.join( port, filename ), "wb" )

                with source, target:

                    target.write( source.read() )
                
            break # Break if one didn't fail

        else:

            print( f"WARNING! Error: {response.status_code} Failed downloading assets" )
