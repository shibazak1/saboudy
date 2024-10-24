

// this is will be the service worker
/*
let  order_id = null;
let  url = null;
let  csrfToken = null;


self.addEventListener('message',(event)=>{

    if(event.data && event.data.type === 'start-sync'){

	order_id = event.data.order_id;
	url = event.data.url;
	csrfToken = event.data.csrftoken;

	console.log("id - url - csrftoken - "+ order_id +''+ url +''+ csrfToken);
    }
    
});


self.addEventListener('sync',(event)=>{

    if(event.tag === 'sync-track-driver-location'){
	
	event.waitUntil(updateDriverLocation());
	console.log('i hear the sync event and i got it ');

    }
    

   
})


function updateDriverLocation() {

    console.log('i am in updatedriverlocation');
    return new Promise((resolve, reject) => {
        // Watch the driver's location continuously
        let watchId = navigator.geolocation.watchPosition(function(position){
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            // Perform the fetch to update the server with the driver's location
	    console.log('start fetch');
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
		    
                    'latitude': latitude,
                    'longitude': longitude,
                    'order_id': order_id
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Driver location updated successfully:', data);

                // Optionally stop watching when the order is delivered or under certain conditions
                if (data.order_status === 'DE') {
                    navigator.geolocation.clearWatch(watchId);  // Stop watching
                    console.log('Order delivered. Stopped location tracking.');
                    resolve();
                }
            })
            .catch(error => {
                console.log('Failed to update driver location:', error);
                reject(error);
            });
        }, function(error) {
            console.log('Geolocation error:', error);
            reject(error);
        });
    });
}
*/


let order_id = null;
let url = null;
let csrfToken = null;
let latitude = null;
let longitude = null;
let watchId;

self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'start-sync') {
        order_id = event.data.order_id;
        url = event.data.url;
        csrfToken = event.data.csrftoken;
	latitude = event.data.latitude;
	longitude  = event.data.longitude;
	watchId = event.data.watchId;
	console.log("json is "+ JSON.stringify({'latitude':latitude,'longitdue':longitude,'order_id':order_id}));
	
    }
});




function informMainPage(event) {


    self.clients.matchAll()
	.then(clients =>{

	    clients.forEach(client =>{

		
		client.postMessage({
                    'type': 'order-delivered',
                    'message': 'The order has been delivered'
		});
		

	    });
	    

	})
 /*   
      self.clients.get(event.clientId).then((client) => {
    if (client) {
    
            client.postMessage({
                'type': 'order-delivered',
                'message': 'The order has been delivered'
            });
        } else {
            console.error('Client not found');
        }
    }).catch((error) => {
        console.error('Error getting client:', error);
	});

 */

    
}






self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-track-driver-location') {  // Fix condition here
        console.log('Received sync event');
        event.waitUntil(updateDriverLocation(event));
    }
});

function updateDriverLocation(event) {
    console.log('Updating driver location');

    return new Promise((resolve, reject) => {
            fetch(url, {
                method: 'POST',
                headers: {
		    'X-CSRFToken': csrfToken,  // Make sure this is passed correctly
                    'Content-Type': 'application/json'
                    
                },
                body: JSON.stringify({
                    'latitude': latitude,
                    'longitude': longitude,
                    'order_id': order_id
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Driver location updated:', data);
                if (data.order_status === 'DE') {

		    informMainPage(event);
                    //navigator.geolocation.clearWatch(watchId);
                    console.log('Order delivered. Stopped location tracking.');
                    resolve();
                }
            })
            .catch(error => {
                console.log('Failed to update driver location:', error);
                reject(error);
            });

    });
}
