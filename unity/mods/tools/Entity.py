class Entity:
    def __init__( self, KeyValueData=None ):
        self.KeyValueData = KeyValueData if KeyValueData is not None else {}

    def ToDict( self ):
        """
            Converts this Entity class to a dict.
            
            Can also be accessed as Entity.KeyValueData
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
