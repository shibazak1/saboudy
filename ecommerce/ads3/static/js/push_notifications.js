// logic of pushing notifications

var endpoint;
var key;
var authSecret;

var vapidPublicKey = 'BO9VhfIdpJcQoOlt75zCigoAwMQIK4Atq58hTP98T0M9QcSkcHrTQB22HYp17XiD-SvI8mwuhgSQmigytW23egw';



function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
	  .replace(/\-/g, '+')
	  .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    
    for (let i = 0; i < rawData.length; ++i) {
	outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

//1st check if user is logged in to send prompet
// becouse we need user object in subscribe function
if(authinticated){
    
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready.then((registration) => {
	
        registration.pushManager.getSubscription()
            .then((subscription) => {
                if (subscription) {
                    console.log('Already subscribed:', subscription);
                    return;
                }

                console.log('Attempting to subscribe to push notifications...');

                return registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
                })
                .then((subscription) => {
                    console.log('Push subscription successful:', subscription);

                    var rawKey = subscription.getKey ? subscription.getKey('p256dh') : '';
                    key = rawKey ? btoa(String.fromCharCode.apply(null, new Uint8Array(rawKey))) : '';
                    var rawAuthSecret = subscription.getKey ? subscription.getKey('auth') : '';
                    authSecret = rawAuthSecret ? btoa(String.fromCharCode.apply(null, new Uint8Array(rawAuthSecret))) : '';

                    return fetch(subscribeUrl, {
                        method: 'POST',
                        headers: new Headers({
                            'content-type': 'application/json'
                        }),
                        body: JSON.stringify({
                            'endpoint': subscription.endpoint,
                            'key': key,
                            'authSecret': authSecret
                        }),
                    })
                    .then((response) => {
                        if (response.ok) {
                            console.log('Subscription sent to server successfully');
                        } else {
                            console.error('Failed to send subscription to server:', response);
                        }
                    });
                })
                .catch((error) => {
                    console.error('Push subscription failed:', error);
                });
            });

    }).catch((error) => {
        console.error('Service worker registration failed:', error);
    });

} else {
    console.error('Push messaging is not supported in this browser');
}



}
