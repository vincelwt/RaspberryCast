chrome.contextMenus.onClicked.addListener(function(info) {
	try {
		var url_encoded_url = encodeURIComponent(info.linkUrl);
		var newURL = "http://"+localStorage.getItem('raspip')+":"+localStorage.getItem('rasport')+"/stream?url=" + url_encoded_url;

		var xmlHttp = null;

		xmlHttp = new XMLHttpRequest();
		xmlHttp.open( "GET", newURL, true);
		xmlHttp.send( null );
		alert('Video was successfully sent to the Raspberry Pi ! Please wait ~ 20/30 seconds.');	
	} 
	catch(err) {
		alert('Error while trying to send the video to the Raspberry Pi. Make sure the ip/port are corrects.');
		alert(err);
	}
});


chrome.browserAction.onClicked.addListener(function(tab) {
	try {
		var url_encoded_url = encodeURIComponent(tab.url);
		var newURL = "http://"+localStorage.getItem('raspip')+":"+localStorage.getItem('rasport')+"/stream?url=" + url_encoded_url;

		var xmlHttp = null;

		xmlHttp = new XMLHttpRequest();
		xmlHttp.open( "GET", newURL, true);
		xmlHttp.send( null );
		alert('Video was successfully sended to the Raspberry Pi ! Please wait ~ 20/30 seconds.');
			
	} 
	catch(err) {
		alert('Error while trying to send the video to the Raspberry Pi. Make sure the ip/port are corrects.');
		alert(err);
	}
});

chrome.runtime.onInstalled.addListener(function() {
	chrome.contextMenus.create({
		"title": "Cast now",
		"contexts" : ["link"],
		"id" : "Castnow"
	});
});

