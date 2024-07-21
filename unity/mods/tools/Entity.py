class Entity:
    def __init__( self, KeyValueData={} ):
        self.KeyValueData = KeyValueData

    def ToDict( self ):
        """
            Converts this Entity class to a dict.
            
            Can also be accessed as Entity.KeyValueData
        """
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

    def remove( self ):
        """
        Removes this entity from the entity data
        """
        self.KeyValueData.clear()