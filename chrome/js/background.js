/*function currentStatus() {
	var req = new XMLHttpRequest();
	req.open('GET', "http://"+localStorage.raspip+":2020/status", true);
	req.onreadystatechange = function (aEvt) {
		if (req.readyState == 4) {
			if(req.status == 200) {
				var status = req.responseText;
				console.log(status);
			} else {
				return "error";
			}
		}
	};
	req.send(null);
}

currentStatus();


window.setInterval(function(){
	currentStatus();

	var status2 = currentStatus();
	console.log(status2);
	if (status1 != status2) {
		alert(status2);
	} else {
		console.log("style the same");	
	}

}, 1000);*/


function stopNote() {
	chrome.notifications.clear('notif1');
	chrome.notifications.clear('notif2');
}

function notif1() {
	var opt = {
		type: "basic",
		title: "Raspberry Pi",
		message: "Trying to retrieve video stream URL. Please wait ~ 10-30 seconds.",
		iconUrl: "48.png"
	};

	chrome.notifications.create('notif1', opt, function(id) { console.log("Last error:", chrome.runtime.lastError); });

	setTimeout(stopNote, 4000);		
}

function notif2() {
	var opt = {
		type: "basic",

		title: "Raspberry Pi",
		message: "Success ! Video should now be playing.",
		iconUrl: "48.png"
	};

	chrome.notifications.create('notif2', opt, function(id) { console.log("Last error:", chrome.runtime.lastError); });

	setTimeout(stopNote, 4000);		
}

function notif3() {
	var opt = {
		type: "basic",
		title: "Raspberry Pi",
		message: "An error occured during the treatment of the link. Please make sure the link is compatible",
		iconUrl: "48.png"
	};

	chrome.notifications.create('notif2', opt, function(id) { console.log("Last error:", chrome.runtime.lastError); });

	setTimeout(stopNote, 4000);		
}

chrome.contextMenus.onClicked.addListener(function(info) {	
	try {
		var url_encoded_url = encodeURIComponent(info.linkUrl);
		var newURL = "http://"+localStorage.raspip+":2020/"+localStorage.cmFunction+"?url=" + url_encoded_url;
		notif1();
		var req = new XMLHttpRequest();
		req.open('GET', newURL, true);
		req.onreadystatechange = function (aEvt) {
			if (req.readyState == 4) {
				if(req.status == 200) {
					if (req.responseText == "1") {
						var status = req.responseText;
						notif2();
					} else {
						notif3();
					}
				} else {
					alert("error!");
				}
			}
		};
		req.send(null);

		
	} 
	catch(err) {
		alert('Error! Please make sure the ip/port are corrects, and the server is running.');
		
	}
});

chrome.runtime.onInstalled.addListener(function() {
	chrome.tabs.create({url: "../options.html"});
	chrome.contextMenus.create({
		id: "Castnow",
		title: "Send to Rpi",
		contexts: ["link"]
	});
});


