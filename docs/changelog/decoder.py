import os

abs = os.path.abspath( '' )

FirstEntry = True

FirstClassEntry = True
FirstDataEntry = True
FirstChoiceEntry = True
IsChoice = False
InEnt = False
Class = ''
hullsizes = ''
color = ''
studio = ''
sprite = ''
iconsprite = ''
flags = ''
offset = ''
baseclasses = []
data = {}

with open( f'{abs}/halflife-unified.fgd', 'r' ) as FGD, open( f'{abs}/entitydata.json', 'w' ) as Json, open( f'{abs}/sentences.json', 'w' ) as sentence:

    lines = FGD.readlines()

    Json.write( '{\n' )
    sentence.write( '{\n' )

    for line in lines:

        l = line.strip()

        if l.startswith( '//' ) or not l or l == '':
            continue

        if l.startswith( '@' ):
            InEnt = True
            Class = l[ 1: l.find( 'Class' ) ]

            # ===============================================
            # classname
            classname = l[ l.find( '=' ) + 1 : ]
            if classname.find( ':' ) != -1:
                classname = classname[ : classname.find( ':' ) ]
            classname = classname.strip()
            # ===============================================

            # ===============================================
            # Ent title
            if Class != 'Base':
                Title = l[ l.find( ':' ) : ]
                Title = Title[ Title.find( '"' ) + 1 : ]
                TitleDescription = Title[ Title.find( '"' ) : ]
                Title = Title[ :Title.find( '"' ) ]

                if TitleDescription.find( ':' ) != -1:
                    TitleDescription = TitleDescription[ :TitleDescription.rfind('"') ]
                    TitleDescription = TitleDescription[ TitleDescription.rfind('"')+1: ]
                else:
                    TitleDescription = ''

                sentence.write( f'"{classname}::classname":\n' )
                sentence.write( '{\n' )
                sentence.write( f'"english": "{Title}",\n' )
                sentence.write( f'"spanish": ""\n' )
                sentence.write( '},\n' )
                sentence.write( f'"{classname}::classname::description":\n' )
                sentence.write( '{\n' )
                sentence.write( f'"english": "{TitleDescription}",\n' )
                sentence.write( f'"spanish": ""\n' )
                sentence.write( '},\n' )
            # ===============================================

            # ===============================================
            # size
            if l.find( 'size(' ) != -1:

                size = l[ l.find( 'size(' ) + 5 : ]
                size = size[ : size.find( ')' ) ]
                hulls = size.split( ',' )

                min = hulls[0].split()

                for n in min:
                    if hullsizes == '':
                        hullsizes += f'[ {n}'
                    else:
                        hullsizes += f', {n}'

                hullsizes += ' ]'

                if len(hulls) > 1:
                    hullsizes += ', ['
                    max = hulls[1].split()
                    for n in max:
                        if hullsizes.endswith( '[' ):
                            hullsizes += f' {n}'
                        else:
                            hullsizes += f', {n}'
                    hullsizes += ' ]'
            # ===============================================

            # ===============================================
            # base
            if l.find( 'base(' ) != -1:

                base = l[ l.find( 'base(' ) + 5 : ]
                base = base[ : base.find( ')' ) ]
                baseclasses = base.replace( " ", "" ).split( ',' )
            # ===============================================

            # ===============================================
            # color
            if l.find( 'color(' ) != -1:

                color = l[ l.find( 'color(' ) + 6 : ]
                color = color[ : color.find( ')' ) ]
            # ===============================================
            # ===============================================

            # ===============================================
            # studio
            if l.find( 'studio(' ) != -1:

                if l.find( 'studio()' ) != -1:
                    studio = 'true'
                else:
                    studio = l[ l.find( 'studio(' ) + 7 : ]
                    studio = studio[ : studio.find( '")' ) +1]
            # ===============================================

            # ===============================================
            # sprite
            if l.find( 'sprite(' ) != -1:

                if l.find( 'sprite()' ) != -1:
                    sprite = 'true'
                else:
                    sprite = l[ l.find( 'sprite(' ) + 7 : ]
                    sprite = sprite[ : sprite.find( '")' ) +1]
            # ===============================================

            # ===============================================
            # iconsprite
            if l.find( 'iconsprite(' ) != -1:

                iconsprite = l[ l.find( 'iconsprite(' ) + 11 : ]
                iconsprite = iconsprite[ : iconsprite.find( ')' ) ]
            # ===============================================

            # ===============================================
            # flags
            if l.find( 'flags(' ) != -1:

                flags = l[ l.find( 'flags(' ) + 6 : ]
                flags = flags[ : flags.find( ')' ) ]
            # ===============================================

            # ===============================================
            # offset
            if l.find( 'offset(' ) != -1:

                offset = l[ l.find( 'offset(' ) + 7 : ]
                offset = offset[ : offset.find( ')' ) ]
            # ===============================================

            if FirstEntry:
                FirstEntry = False
            else:
                Json.write( f',\n' )

            Json.write( f'\t"{classname}":\n' )
            Json.write( '\t{\n' )

            if FirstClassEntry:
                FirstClassEntry = False
            else:
                Json.write( f',\n' )

            Json.write( f'\t\t"Class": "{Class}"' )

            BaseClassesStr = str(baseclasses).replace( '\'', '"' )
            Json.write( f',\n\t\t"base": {BaseClassesStr}' )

            if hullsizes != '':
                Json.write( f',\n\t\t"size": [ {hullsizes} ]' )

            if color != '':
                color = str(color.split()).replace("'", "")
                Json.write( f',\n\t\t"color": {color}' )

            if studio != '':
                Json.write( f',\n\t\t"studio": {studio}' )

            if sprite != '':
                Json.write( f',\n\t\t"sprite": {sprite}' )

            if iconsprite != '':
                Json.write( f',\n\t\t"iconsprite": {iconsprite}' )

            if flags != '':
                Json.write( f',\n\t\t"flags": "{flags}"' )

            if offset != '':
                offseta = offset.split()
                offset = str(offseta).replace( "'", '')
                Json.write( f',\n\t\t"offset": {offset}' )

            Json.write( f',\n\t\t"data":\n' )
            Json.write( '\t\t{\n' )


        elif IsChoice:
            if l.startswith( ']' ):
                Json.write( '\n\t\t\t\t]\n\t\t\t}' )
                IsChoice = False
                FirstChoiceEntry = True
                continue
            elif l.startswith( '[' ):
                continue

            if FirstChoiceEntry:
                FirstChoiceEntry = False
            else:
                Json.write( f',' )

            choices = l.split( ':' )

            if len(choices) >= 0:
                choice = choices[0].strip().replace( '"', '' )
                Json.write( f'\n\t\t\t\t\t"{choice}"' )

                if len(choices) > 0:
                    choicedesc = choices[1].strip().replace( '"', '' )
                    choicedesc = choicedesc.replace( '"', '')
                    sentence.write( f'"{classname}::{key}::{choice}":\n' )
                    sentence.write( '{\n' )
                    sentence.write( f'"english": "{choicedesc}",\n' )
                    sentence.write( f'"spanish": ""\n' )
                    sentence.write( '},\n' )
                    sentence.write( f'"{classname}::{key}::{choice}::description":\n' )
                    sentence.write( '{\n' )
                    sentence.write( f'"english": "",\n' )
                    sentence.write( f'"spanish": ""\n' )
                    sentence.write( '},\n' )


        elif InEnt:

            if l.startswith( '[' ):
                continue
            elif l.startswith( ']' ):
                InEnt = False
                FirstClassEntry = True
                Class = ''
                classname = ''
                hullsizes = ''
                color = ''
                flags = ''
                offset = ''
                studio = ''
                sprite = ''
                iconsprite = ''
                baseclasses.clear()
                data.clear()
                Json.write( '\n\t\t}\n\t}' )
                FirstDataEntry = True
                continue

            key = l[ : l.find( '(' ) ]
            type = l[ l.find( '(' ) +1 : l.find( ')' ) ]
            title = l[ l.find( '"', l.find( ':' ) ) + 1: ]

            value = ''
            if title.find( ':' ):
                value = title[ title.find( ':' ) +1: ]
                value = value.strip()
                value = value.replace( '"', '' )
                if value.find( ':' ) != -1:
                    value = value[ 0: value.find( ':' ) ]
                title = title[ : title.find( ':' ) ]
                title = title.replace( '"', '' )


            if value == title: # idk
                value = ''

            if type == 'choices' or key == 'spawnflags':
                IsChoice = True
                value = value.replace( '=', '' )
                value = value.strip()
                if key == 'spawnflags':
                    value = ''

            if key:
                if FirstDataEntry:
                    FirstDataEntry = False
                else:
                    Json.write( f',\n' )
                Json.write( f'\t\t\t"{key}":' )
                Json.write( '\n\t\t\t{' )
                Json.write( f'\n\t\t\t\t"variable": "{type}",' )
                Json.write( f'\n\t\t\t\t"value": "{value}"' )
                if not IsChoice:
                    Json.write( '\n\t\t\t}' )
                else:
                    Json.write( ',\n\t\t\t\t"choices":\n\t\t\t\t[' )
                sentence.write( f'"{classname}::{key}":\n' )
                sentence.write( '{\n' )
                sentence.write( f'"english": "{title}",\n' )
                sentence.write( f'"spanish": ""\n' )
                sentence.write( '},\n' )
                sentence.write( f'"{classname}::{key}::description":\n' )
                sentence.write( '{\n' )
                sentence.write( f'"english": "",\n' )
                sentence.write( f'"spanish": ""\n' )
                sentence.write( '},\n' )

    Json.write( '\n}\n' )
    sentence.write( '\n"EOF": true\n}\n' )

exit(0)
