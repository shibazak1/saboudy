
//this is the implementation background sync of driver location when there is no connection



function getready(id) {
    const form = document.getElementById("order-" + id);
    if (!form) {
        console.error('Form not found for ID: order-' + id);
        return;
    }
    
    
    const url = form.action;
    console.log('I got the URL: ' + url);
    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    console.log('CSRF Token: ' + csrfToken);

    watchId = navigator.geolocation.watchPosition(success, error);

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        console.log('Latitude: ' + latitude + ', Longitude: ' + longitude);

	var payload = {
	    orderId:id,
	    url:url,
	    csrfToken:csrfToken,
	    latitude:latitude,
	    longitude:longitude
	    
	};

        // Now call triggerBackgroundSync with the geolocation data
        triggerBackgroundSync(payload);
    }
    
    function error(err) {
        alert("Geolocation error: " + err.message);
    }
    
    document.getElementById('row-' + id).innerHTML = "";

    
}


  function triggerBackgroundSync(payload) {
    console.log('I am in triggerBackgroundSync >|<');

    if ('serviceWorker' in navigator && 'SyncManager' in window) {
        navigator.serviceWorker.ready.then((registration)=>{
	    
	    console.log('register sync event');
	    //start listeneing to message from service worker
	       
	    navigator.serviceWorker.addEventListener('message',(event)=>{
		if(event.data && event.data.type === 'order-delivered'){
		    if(watchId !== null){	
			navigator.geolocation.clearWatch(watchId);
			console.log("now i stopped geolocation walla!");
		    }
		}
		
	    });
	    //end listening
	    
	    registration.sync.register('driver-location')
		.then(()=>{
		    console.log('store payload in idbkeyval ');
		    idbKeyval.set('sendMessage', payload);
		});
	})
	    .catch((error) => {
                console.log('Background sync failed: ' + error);
            });
    }
     
}


