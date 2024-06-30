document.addEventListener( 'DOMContentLoaded', (event) =>
{
    // Link references for automatically adding href to these words
    let references = {};
    fetch( 'references.json' ).then( response => response.json() ).then( data =>
    {
        references = data;

    } ).catch( error => console.error( 'Couldn\'t load links from references.json', error ) );

    // Translations goes in sentences.json
    let translations = {};
    fetch( 'sentences.json' ).then( response => response.json() ).then( data =>
    {
        translations = data;

        // Get local language
        const userLang = navigator.language || navigator.userLanguage;

        // Check if the language has been already choosen or the local language exists
        const defaultLang = localStorage.getItem( 'language' ) ? localStorage.getItem( 'language' ) : translations[ userLang ] ? userLang : 'english';

        // Apply translations on load
        applyTranslations( defaultLang );

    } ).catch( error => console.error( 'Couldn\'t load translations from sentences.json', error ) );

    function applyTranslations( language )
    {
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




//i know it looks like yandev made this but it works
function showAlert() {
	hideAlert();
	document.getElementById("messagebox").style.display = "table";
	document.getElementById("line1").style.display = "inline";
	document.getElementById("line1").innerHTML = "<br>Alert box example";
	document.getElementById("githublink").style.display = "inline";
	document.getElementById("okbutton").display = "inline";
}

function showServerBrowser(){
	document.getElementById("serverbrowser").style.display = "table";
}

function hideServerBrowser(){
	document.getElementById("serverbrowser").style.display = "none";
}

//hide all - runs on page load
function hideAlert() {
	document.getElementById("messagebox").style.display = "none";
	document.getElementById("line1").style.display = "none";
	document.getElementById("line2").style.display = "none";
	document.getElementById("githublink").style.display = "none";
	document.getElementById("copybutton").style.display = "none";
	document.getElementById("okbutton").display = "none";
}

//copy string "IP" to clipboard
function copyIP(x){
	navigator.clipboard.writeText(x);
}

// shortcut key script
addEventListener( 'keyup', function(e)
{
	clickSound();
	//A - Active link
	if (e.keyCode == 65) location='https://www.half-life.com/';
	//B - show alert box
	if (e.keyCode == 66) showAlert();
	//M - Multiplayer - show server browser
	if (e.keyCode == 77) showServerBrowser();
	//ESC - Close server browser
	if (e.keyCode == 27) hideServerBrowser();
	//ESC - Close the Alert box
	if (e.keyCode == 27) hideAlert();
});

//click sound
function clickSound()
{
	document.getElementById('click').play();
}
