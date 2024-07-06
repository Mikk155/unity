

document.addEventListener( 'DOMContentLoaded', (event) =>
{
    fetch('entities.html').then( response => response.text() ).then( content => {
        document.getElementById( 'entityguide-index-list' ).innerHTML = content;

    } ).catch( error => console.error( 'Couldn\'t load entities from entityguide/entities.html', error ) );

    fetch('changelog.html').then( response => response.text() ).then( content => {
        document.getElementById( 'changelog-container' ).innerHTML = content;

    } ).catch( error => console.error( 'Couldn\'t load changelog from changelog.html', error ) );

    fetch('credits.html').then( response => response.text() ).then( content => {
        document.getElementById( 'credits-container' ).innerHTML = content;

    } ).catch( error => console.error( 'Couldn\'t load credits from credits.html', error ) );

    // Link references for automatically adding href to these words
    let references = {};
    fetch( 'src/references.json' ).then( response => response.json() ).then( data => {
        references = data;

    } ).catch( error => console.error( 'Couldn\'t load links from references.json', error ) );

    // Translations goes in sentences.json
    let translations = {};
    fetch( 'src/sentences.json' ).then( response => response.json() ).then( data =>
    {
        translations = data;

        // Apply translations on load
        applyTranslations( '' );

    } ).catch( error => console.error( 'Couldn\'t load translations from sentences.json', error ) );

    function applyTranslations( language )
    {
        if( language == '' )
        {
            // Get local language
            const userLang = navigator.language || navigator.userLanguage;
            // Check if the language has been already choosen or the local language exists
            language = localStorage.getItem( 'language' ) ? localStorage.getItem( 'language' ) : translations[ userLang ] ? userLang : 'english';
        }

        // Save language for using on different html
        localStorage.setItem( 'language', language );

        // Replace all data
        document.querySelectorAll( "[pkvd]" ).forEach( element =>
        {
            const key = element.getAttribute( "pkvd" );

            element.innerText = translations[ key ][ language ];
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
    
        fetch( 'entities/' + entity + '.html' ).then( response => response.text() ).then( content => {
            document.getElementById( 'entityguide-entity-list' ).innerHTML = content;
    
        } ).catch( error => console.error( 'Couldn\'t load entity from entities/' + entity + '.html', error ) );
    
        applyTranslations('');
    }

    // Update language by the language button
    window.changeLanguage = function( language )
    {
        applyTranslations( language );
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
});

function SFX( sound )
{
	document.getElementById( sound ).play();
}

