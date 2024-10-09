// I don't really know JavaScript.
// Feel free to modify, optimize and improve any of this.

// Read a string and skip single-line commentary before parsing as a json object
function jsonc( obj ) { return JSON.parse( obj.split( '\n' ).filter( line => !line.trim().startsWith( '//' ) ).join( '\n' ) ); }

document.addEventListener( 'DOMContentLoaded', (event) =>
{
    // Print out a brute text of the credits file in within this window
    if( document.getElementById( 'credits-container' ) )
    {
        fetch('credits.html')
        .then( response => response.text() )
        .then( content =>
        {
            document.getElementById( 'credits-container' ).innerHTML = content;
        }
        ).catch( error => console.error( 'Couldn\'t load credits from credits.html', error ) );
    }

    // Link references for automatically adding href to these words
    let references = {};
    fetch( 'src/references.json' )
    .then( response => response.text() )
    .then( text =>
    {
        references = jsonc( text );
    }
    ).catch( error => console.error( 'Couldn\'t load links from references.json', error ) );

    // Translations goes in sentences.json
    let translations = {};
    fetch( 'src/sentences.json' )
    .then( response => response.text() )
    .then(text =>
    {
        translations = jsonc( text );

        if( document.getElementById( 'languageTable' ) )
        {
            add_language_buttons();
        }

        apply_translation();
    }
    ).catch( error => console.error( 'Couldn\'t load translations from sentences.json', error ) );

    // Add supported languages to the change language menu
    function add_language_buttons()
    {
        const languageTable = document.getElementById( 'languageTable' );

        const languages = translations[ "languages" ];

        languages.forEach( language => {
            const newRow = document.createElement('tr');
            const newCell = document.createElement('td');

            const button = document.createElement('button');
            button.textContent = language;

            button.setAttribute('onclick', `changeLanguage('${language}')`);

            newCell.appendChild(button);
            newRow.appendChild(newCell);

            languageTable.appendChild(newRow);
        });
    }

    function apply_translation( language )
    {
        // Get saved language
        if( language == '' )
        {
            language = localStorage.getItem( 'language' ) ? localStorage.getItem( 'language' ) : '';
        }

        // If first time get operative system's language
        if( !language || language == '' )
        {
            const NavLang = navigator.language || navigator.userLanguage;
            const userLang = new Intl.DisplayNames( [ 'en' ], { type: 'language' } ).of( NavLang.split('-')[0] ).toLowerCase();
            language = userLang ? userLang : '';
        }

        // If not supported use english
        if( !translations[ "languages" ][ language ] || language == '' )
        {
            language = 'english'; 
        }

        // Save language for using on different html
        localStorage.setItem( 'language', language );

        // Replace all data
        document.querySelectorAll( "[pkvd]" ).forEach( element =>
        {
            const key = element.getAttribute( "pkvd" );
            const value = translations[ key ] && translations[ key ][ language ] ? translations[ key ][ language ] : '';

            // innerHTML seems to add elements. not sure the difference with innerText
            element.innerHTML = value != '' ? value : 'Trans#' + key;

            if( value == '' )
                console.error( 'Missing message for label "' + key + '" in language "' + language + '"' );
        } );

        // Fill up with links if referenced
        for( let href in references )
        {
            let link = references[ href ];
            let regex = new RegExp( `#${href}\\b`, 'g' );
            document.body.innerHTML = document.body.innerHTML.replace(regex, `<a href="${link}" target="_blank">${href}</a>`);
        }
    }

    window.fetchent = function( entity )
    {
        openElement( 'EntityGuideEntity' );
    
        fetch( 'entityguide/entities/table/' + entity + '.html' )
        .then( response => response.text() )
        .then( content =>
        {
            document.getElementById( 'entityguide-entity-list' ).innerHTML = content;
            apply_translation();
        }
        ).catch( error => console.error( 'Couldn\'t load entity from entityguide/entities/table/' + entity + '.html', error ) );
    
        fetch( 'entityguide/entities/' + entity + '.html' )
        .then( response => response.text() )
        .then( content =>
        {
            document.getElementById( 'entityguide-extra' ).innerHTML = content;
            apply_translation();
        }
        ).catch( error => console.error( 'Couldn\'t load entity from entityguide/entities/' + entity + '.html', error ) );
    }

    // Update language by the language button
    window.changeLanguage = function( language )
    {
        apply_translation( language );
    };

    window.openElement = function( id )
    {
        document.getElementById( id ).style.display = "block";
    };

    window.closeElement = function( id )
    {
        document.getElementById( id ).style.display = "none";
    };

    window.onclick = function( event )
    {
        if( event.target.classList.contains( "emergent-window" ) )
        {
            event.target.style.display = "none";
        }
    };

    window.CopyElement = function( element )
    {
        fetch( element).then( response => response.text() ).then( content => {
            const tempTextArea = document.createElement('textarea');
            tempTextArea.value = content;
            document.body.appendChild(tempTextArea);
            tempTextArea.select();
            document.execCommand('copy');
            document.body.removeChild(tempTextArea);
        } ).catch( error => console.error( 'Couldn\'t copy text from ' + element, error ) );
    };
});

function SFX( sound )
{
	document.getElementById( sound ).play();
}
