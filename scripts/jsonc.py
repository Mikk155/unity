import json

class jsonc:

    def __init__( self, FileLines : list[ str ] ):

        self.jsdata = ''

        for t, line in enumerate( FileLines ):

            line = line.strip()

            if line and line != '' and not line.startswith( '//' ):

                self.jsdata = f'{self.jsdata}\n{line}'

        self.data = json.loads( self.jsdata )

        self.data.pop( 'EOF', '' )

    def load(self):

        return self.data
