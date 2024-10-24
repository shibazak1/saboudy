
//1st get this dive element form the page bas_bootstrap
var offlineNotification = document.getElementById("offline");

function showOfflineNotification(){

    // remove class d-none to the dive so it show 
    offlineNotification.classList.remove('d-none');
    
   
}


function hideOfflineNotification(){
    // add class d-none to the dive so it disappear 
    offlineNotification.classList.add('d-none');

}


//we add an event listener for both when windo online and offline and run the appropiat function
window.addEventListener('offline',showOfflineNotification);
window.addEventListener('online',hideOfflineNotification);
