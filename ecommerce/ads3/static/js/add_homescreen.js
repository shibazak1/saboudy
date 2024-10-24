// make the add to home screen button appear on the page


// when the page is loaded get the button
window.addEventListener('load', function () {
    var btnSave = document.getElementById('btnSave');
    // make varaible for the value of the prompt
    var savedPrompt;
    
    // when the service worker is active it fire an event to make prompt appear
    window.addEventListener('beforeinstallprompt', function (e) {
	// we prevent that prompt from appearing
        e.preventDefault();
	// save it the prompt event object to acaraible so we can use it later
        savedPrompt = e;
	
        // Show the button once the event is available
        btnSave.style.display = 'block';
        btnSave.removeAttribute('disabled');
    });
    
    // Handle the button click to prompt the installation
    btnSave.addEventListener('click', function () {
	//check for the value of saveprompt
        if (savedPrompt !== undefined) {
            savedPrompt.prompt();  // Show the installation prompt

	    //savedprompt has and object user choise that track how user choose and return promis
            savedPrompt.userChoice.then((result) => {
                if (result.outcome === 'dismissed') {
                    console.log('User dismissed the homescreen install');
                } else {
                    console.log('User installed the app to homescreen');
                }
                // Hide the button after the prompt
                btnSave.style.display = 'none';
                savedPrompt = null;
            });
        }
    });
});


