class Entity:
    def __init__( self, KeyValueData={} ):
        self.KeyValueData = KeyValueData

    def ToDict( self ):
        return self.KeyValueData

    def __getattr__( self, key ):
        return str( self.KeyValueData.get( key, "" ) ) if key in self.KeyValueData else None

    def __setattr__( self, key, value ):
        if key == 'KeyValueData':
            super().__setattr__( key, value )
        elif value == None:
            self.KeyValueData.pop( key, '' )
        else:
            self.KeyValueData[ key ] = str( value )
