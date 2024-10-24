

var staticCacheName = 'djangopwa-v1';

// define an array that hold all the resource that i need to caches during the resgistration of the SV
const appShell = [
    '/ads3/list',
];

// add event listener to tap in the registrations stage of SV and cachecs all the need resource
// so if user reapeditdlly vist the page we do not wont to get it from the server
self.addEventListener('install', function(event) {
    event.waitUntil(
	//open the caches and add the list to it
	caches.open(staticCacheName).then(function(cache) {
	    return cache.addAll([
		'/ads3/list',
		'/ads3/offline',
		
	    ]);
	})
    );
});


function isCacheable(request){
    const url = new URL(request.url);

    return ! url.pathname.endsWith('.json');

}

/*
async function cacheFirstWithRefresh(request) {
    const fetchResponsePromise = fetch(request).then(async (networkResponse) => {
	if (networkResponse.ok) {
	    const cache = await caches.open(staticCacheName);
	    cache.put(request, networkResponse.clone());
	}
	return networkResponse;
    });
    
    return (await caches.match(request)) || (await fetchResponsePromise);
}
*/



function cacheFirstWithRefresh(request){
    
    var  requestTocache = request.clone();
    const fetchPromis = fetch(requestTocache).then((response)=>{
	if(!response || response.status !== 200){
	    return response;
	}
	var responseToCache = response.clone();
	caches.open(staticCacheName)
	    .then((cache)=>{
		cache.put(requestTocache,responseToCache);
		
	    });

	return response;
	
	
    })
    return caches.match(request)
	.then((cachedResponse)=>{
	    return  cachedResponse || fetchPromis;
	})
	.catch((error)=>{
	    if(request.method == 'GET' && request.headers.get('accept').includes('text/html')){
		return caches.match('ads3/offline');
	    }

	});
    
}


// this algorithm try to retrieve the resource from the server if success update the cache and return the response
// if the newtork request fail return from the cache
function networkFirst(request){

    // ask the server for this resouce
    // (1)  the  (return fetch) becosue fetch is async operation it return promis and that make js continue excution
    // without completing the task that is inside the (then) handeler so
    // by using (return we force the js to wait until the promis resolve and complete his task)
    return fetch(request)
	.then((response)=>{
	    //if respond is valide
	    if(response.ok){
		// open cach [named staticCachename]  :read =>(1)
		return caches.open(staticCacheName)
		    .then((cache)=>{
			//after cache return store the request and response pair to the cache
			// (response.clone) it make copy of the response becosue we need to use it again for returning
			// request and response are send from server to client as stream of data they are arrive as chunck by chunck
			//so if we consume it in one place like in store in cache there are gone and we can not use it again
			cache.put(request,response.clone());
			// return responce form the network
			return response;  
		    })
	    }
	    // even of the response fail return it 
	    return response;  
	})
    // if there is an error in the fetch catch it
	.catch((error)=>{
	    //check if there is an cache for this resorce and return it : read(1) for couse of (return)
	    return caches.match(request)
		.then((cachedResponse)=>{
		    // return cache or error
		    return cachedResponse || error;
		});  

	});
    
}

/*
// this algorithm try to retrieve the resource from the server if success update the cache and return the response
// if the newtork request fail return from the cache
function networkFirst(request){

    // ask the server for this resouce
    // (1)  the  (return fetch) becosue fetch is async operation it return promis and that make js continue excution
    // without completing the task that is inside the (then) handeler so
    // by using (return we force the js to wait until the promis resolve and complete his task)
    return fetch(request)
	.then((response)=>{
	    //if respond is valide
	    if(response.ok){
		// open cach [named staticCachename]  :read =>(1)
		return caches.open(staticCacheName)
		    .then((cache)=>{
			//after cache return store the request and response pair to the cache
			// (response.clone) it make copy of the response becosue we need to use it again for returning
			// request and response are send from server to client as stream of data they are arrive as chunck by chunck
			//so if we consume it in one place like in store in cache there are gone and we can not use it again
			cache.put(request,response.clone());
			// return responce form the network
			return response;  
		    })
	    }
	    // even of the response fail return it 
	    return response;  
	})
    // if there is an error in the fetch catch it
	.catch((error)=>{
	    //check if there is an cache for this resorce and return it : read(1) for couse of (return)
	    return caches.match(request)
		.then((cachedResponse)=>{
		    // return cache or error
		    return cachedResponse || error;
		});  

	});
    
}
*/

// this algorithm try to retrieve the resource from the server if success update the cache and return the response
// if the newtork request fail return from the cache
function networkFirst(request){

    // ask the server for this resouce
    // (1)  the  (return fetch) becosue fetch is async operation it return promis and that make js continue excution
    // without completing the task that is inside the (then) handeler so
    // by using (return we force the js to wait until the promis resolve and complete his task)
    return fetch(request)
	.then((response)=>{
	    //if respond is valide
	    if(response.ok){
		// open cach [named staticCachename]  :read =>(1)
		return caches.open(staticCacheName)
		    .then((cache)=>{
			//after cache return store the request and response pair to the cache
			// (response.clone) it make copy of the response becosue we need to use it again for returning
			// request and response are send from server to client as stream of data they are arrive as chunck by chunck
			//so if we consume it in one place like in store in cache there are gone and we can not use it again
			cache.put(request,response.clone());
			// return responce form the network
			return response;  
		    })
	    }
	    // even of the response fail return it 
	    return response;  
	})
    // if there is an error in the fetch catch it
	.catch((error)=>{
	    //check if there is an cache for this resorce and return it : read(1) for couse of (return)
	    return caches.match(request)
		.then((cachedResponse)=>{
		    if(cachedResponse){
			return cachedResponse;
		    }
		    if(request.method == 'GET' && request.headers.get('accept').includes('text/html')){
			return caches.match('/ads3/offline');
			
		    }
		    
		});  

	});
    
}



function networkFirstWithCache(request){
    
    // check if this request match some thing in caches
    return caches.match(request)
	.then(function(response){
	    // if yeas
	    if(response){
		// return it from the caches
		return response;
	    }
	    // make copy of request
	    var requestToCache = request.clone();

	    // request the server
	    return fetch(requestToCache).then(function(response){
		
		if(!response || response.status !== 200 ){
		    //return response from server if is not ok
		    return response;
		}
		// copy the response
		var responseToCache  = response.clone();
		// open the cache
		return caches.open(staticCacheName)
		    .then(function(cache){
			//store the request response copy in the cache
			cache.put(requestToCache,responseToCache);
			// return the response
			return response;

		    });
		
	    });
	    
	}).catch((error)=>{
	    if(request.method == 'GET' && request.headers.get('accept').includes('text/html')){
		return caches.match('/ads3/offline');
		
	    }
	    
	});
}

// defien the custom timeout that take delay in ms
function timeout(delay){

    //we want to convert the normal call to setTimeout function into promise
    // so we rap it in side new Promise constructore
    // that will create promis and return it
    // Promis constructor take excuter function that take resolve and reject function as paramert
    //after the async operation finsh we call resolve or reject that will pass the value or the error to then() or catch()
    return new Promise(function(resolve,reject){
	// setTimeout take function to excute when the delay is finshed 
	setTimeout(function(){

	    console.log("we stopped this fetch");
	    // create new response object to return when the fetch take long time > 3sec
	    resolve(new Response('',{
		status:408,
		statusText:'Request timed out'
	    }));

	},delay);
    });

};






self.addEventListener('fetch',(event)=>{
    if(isCacheable(event.request)){
	console.log("URL is "+ event.request.url);
	if(event.request.url.includes('/ads3/list') || event.request.url.includes('/ads3/detail/')){
	    event.respondWith(cacheFirstWithRefresh(event.request));
	}
	
	else if(event.request.url.includes('/ads3/cart/list') ||
		event.request.url.includes('/ads3/order/list')||
		(event.request.url.includes('/ads3/customer/') && event.request.url.includes('/map'))||
		//driver part
		event.request.url.includes('ads3/all/order/list')||
		event.request.url.includes('ads3/driver/order/list')||
	       (event.request.url.includes('/ads3/driver/') && event.request.url.includes('/map'))){ 
		    console.log("start to respond with network first");
		    event.respondWith(networkFirst(event.request));
		}
	else if(event.request.url.includes('/ads3/order/') && event.request.url.includes('/detail')){
	    console.log("start to respond with newtorkfirst with cachce");
	    event.respondWith(networkFirstWithCache(event.request));
	}
	
	
	else if((/bootstrap/.test(event.request.url))||
		(/fontawesome/.test(event.request.url))){
	    //if the request resources is one of this two i responde with Promis.race
	    //which it take array of promiss and return promis it self this promis is resolve
	    //if one of the promises is resolve and reject if one of them is rejected
	    // the idea is race 2 promises against other and the fastes one win
	    //so if the request to the resource take longer then 3 sec the timeout function will won and resolve first
	    
	    event.respondWith(Promise.race([timeout(3000),fetch(event.request.url)]));
	}
	else{
	    event.respondWith(fetch(event.request));
	    }
	    
	
    }
});




//this listene for push event and use the payload come from server to construct the notification
//show notification by using showNotification
self.addEventListener('push',(event)=>{
    console.log("push event fired");
    var payload = event.data ? JSON.parse(event.data.text()) : 'no payload';
    var title = 'Saboady';

    event.waitUntil(
	self.registration.showNotification(title,{
	    body:payload.body,
	    icon:payload.icon,
	    data:{
		url:payload.url
	    },
	    vibrate: [300, 100, 400]

	})
    );

});

self.addEventListener('notificationclick', (event) => {
    var urlToOpen = event.notification.data.url;  // Accessing the URL from the data property
    event.notification.close();

    event.waitUntil(
        clients.matchAll({ type: 'window' }).then((clientList) => {
            for (var i = 0; i < clientList.length; i++) {
                var client = clientList[i];
                if (client.url == '/' && 'focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(urlToOpen);  // Now the correct URL will be used
            }
        })
    );
});






/*
// tap in to any fetch request and check if any thing need to be retrieve from the caches instead of server
self.addEventListener('fetch',function(event){

    event.respondWith(
	// check if this request match some thing in caches
	caches.match(event.request)
	    .then(function(response){
		// if yeas
		if(response){
		    // return it from the caches
		    return response;
		}
		//if not make request to a server
		var requestToCache = event.request.clone();

		return fetch(requestToCache).then(function(response){

		    if(!response || response.status !== 200 ){

			return response;
		    }
		    var responseToCache  = response.clone();

		    caches.open(staticCacheName)
			.then(function(cache){

			    cache.put(requestToCache,responseToCache);
			    });
		    return response;
		});
		
	    })
    );

});

*/

// implement run time caching for detail  page (stale while revalidate)
//cache first with refresh caches is tabe into request check if it in caches if it is go to server and
//add new response to a caches

/*
self.addEventListener('fetch',function(event){
    if(event.request.url.includes('/ads3/list') || event.request.url.includes('/ads3/detail/')){
	event.respondWith(
	    caches.match(event.request)
		.then(function(cachedResponse){
		    const fetchPromis = fetch(event.request).then(function(networkResponse){
			caches.open(staticCacheName)
			    .then(function(cache){
				cache.put(event.request,networkResponse.clone());
			    });
			return networkResponse;

		    });
		    return cachedResponse || fetchPromis;
		    

		})
	    
	);
	
	fetch(event.request)
	    .then(function(networkResponse){
		caches. open(staticCacheName)
		    .then(function (cache){
			cache.put(event.request,networkResponse.clone());

		    });
		return networkResponse;


 	    })

	    } });

*/





/*
self.addEventListener('fetch', function(event) {
var requestUrl = new URL(event.request.url);
	if (requestUrl.origin === location.origin) {
	if ((requestUrl.pathname === '/')) {
		event.respondWith(caches.match('/ads3/list'));
		return;
	}
	}
	event.respondWith(
	caches.match(event.request).then(function(response) {
		return response || fetch(event.request);
	})
	);
});


*/




/*
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

*/


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
    
    
}









self.addEventListener('sync', (event) => {
    if (event.tag === 'driver-location') {  // Fix condition here
        console.log('activate sync event');
        event.waitUntil(updateDriverLocation(event));
    }
});


//importing the idbkeyval library 

importScripts('https://cdn.jsdelivr.net/npm/idb-keyval@6/dist/umd.js');

function updateDriverLocation(event) {
    console.log('Updating driver location');

    idbKeyval.get('sendMessage')
	.then((value)=>{
	    fetch(value.url,{
		method:'POST',
		headers:{
		    'X-CSRFToken':value.csrfToken,
		    'Content-Type':'application/json'
		},
		body:JSON.stringify({
		    
                    'latitude': value.latitude,
                    'longitude': value.longitude,
                    'order_id': value.orderId
		    
		})
	    })
	    
		.then((response)=>response.json())
		.then((data)=>{
		    //remove the qued data from indexdb
		    idbKeyval.delete('sendMessage');
		    console.log('Driver location updated:', data);
		    
                    if (data.order_status === 'DE') {
			
			informMainPage(event);
			//navigator.geolocation.clearWatch(watchId);
			console.log('Order delivered. Stopped location tracking.');
		
                    }
		    
		    
		})
	    
		.catch(error => {
                    console.log('Failed to update driver location:', error);
                    
            });

	});
}
