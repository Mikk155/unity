import os, sys, json

terms = json.load( open( '{}\\terms_of_use.json'.format( os.path.abspath( "" ) ), 'r' ) );

md = open( '{}\\README.md'.format( os.path.abspath( "" ) ), 'w' );

script = open( '{}\\{}.py'.format( os.path.abspath( "" ), sys.argv[1] ), 'r+' );

Separator = '='
for i in range( 7 ):
    Separator += Separator;

md.write( "# Terms of Use\n" );
line = [ '#{}\n# Terms of Use\n'.format( Separator ) ];

for i, term in terms.items():
    line.append( '#{}\n'.format( Separator ) );
    md.write( "### {}\n```\n".format( i ) );
    line.append( '# {}\n'.format( i ) );
    line.append( '#{}\n'.format( Separator.replace( "=", '-' ) ) );

    for d in term:
        md.write( "{}\n".format( d ) );
        line.append( '#\t{}\n'.format( d ) );
    md.write( "```\n" );

line.append( '#{}\n\n'.format( Separator ) );

lines = line + script.readlines();
script.seek(0)
script.writelines( lines );
