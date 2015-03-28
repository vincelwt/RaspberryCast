function stopNote1() {
	chrome.notifications.clear('notif1', function(id) { console.log("Last error:", chrome.runtime.lastError); });
}

function stopNote2() {
	chrome.notifications.clear('notif2', function(id) { console.log("Last error:", chrome.runtime.lastError); });
}

function stopNote3(n) {
	chrome.notifications.clear('notif3', function(id) { console.log("Last error:", chrome.runtime.lastError); });
}

function notif1() {
	var opt = {
		type: "basic",
		title: "Raspberry Pi",
		message: "Trying to get video stream URL. Please wait ~ 10-30 seconds.",
		iconUrl: "48.png"
	};

	chrome.notifications.create('notif1', opt, function(id) { console.log("Last error:", chrome.runtime.lastError); });

	setTimeout(stopNote1, 4000);		
}

function notif2() {
	var opt = {
		type: "basic",

		title: "Raspberry Pi",
		message: "Success ! Video should now be playing.",
		iconUrl: "48.png"
	};

	chrome.notifications.create('notif2', opt, function(id) { console.log("Last error:", chrome.runtime.lastError); });

	setTimeout(stopNote2, 4000);		
}

function notif3() {
	var opt = {
		type: "basic",
		title: "Raspberry Pi",
		message: "An error occured during the treatment of the link. Please make sure the link is compatible",
		iconUrl: "48.png"
	};

	chrome.notifications.create('notif3', opt, function(id) { console.log("Last error:", chrome.runtime.lastError); });

	setTimeout(stopNote3, 4000);		
}

function mkrequest(url, response) {
	try {
		var newURL = "http://"+localStorage.getItem('raspip')+":2020"+url;
		if (response == 1) {
			notif1();
			//window.close();
		}
		var req = new XMLHttpRequest();
		req.open('GET', newURL, true);
		req.onreadystatechange = function (aEvt) {
			if (req.readyState == 4) {
				if (req.status == 200) {
					if (req.responseText == "1") {
						if (response == 1) {
							notif2();	
						}
					} else {
						notif3();
					}
				} else {
					chrome.notifications.clear('notif1', function(id) { console.log("Last error:", chrome.runtime.lastError); });
					alert("Error during connecting requesting from server !");
				}
			}
		};
		req.send(null);
	} 
	catch(err) {
		alert("Error ! Make sure the ip/port are corrects, and the server is running.")
		return "wrong";
	}
}


chrome.contextMenus.onClicked.addListener(function(info) {
	var url_encoded_url = encodeURIComponent(info.linkUrl);	
	var url = "/"+localStorage.cmFunction+"?url="+url_encoded_url;
	mkrequest(url, 1);
});

chrome.runtime.onInstalled.addListener(function() {
	chrome.tabs.create({url: "../options.html"});
	chrome.contextMenus.create({
		id: "Castnow",
		title: "Send to Rpi",
		contexts: ["link"]
	});
});


