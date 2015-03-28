function popalert(msg) {
	$( "#whole" ).hide();
	$( "#popalert" ).show();
	$( "#popalert" ).html("<p>"+msg+"</p>");
	setTimeout(function() {
		window.close();
	}, 4000);
	
}

function mkrequestXML(url, response) {
	try {

		var newURL = "http://"+localStorage.getItem('raspip')+":2020"+url;
		if (response == True) {
			popalert("Trying to retrieve video stream URL. Please wait ~ 10-30 seconds.");
		}
		var req = new XMLHttpRequest();
		req.open('GET', newURL, true);
		req.onreadystatechange = function (aEvt) {
			if (req.readyState == 4) {
				if(req.status == 200) {
					if (req.responseText == "1") {
						var status = req.responseText;
						if (response == True) {
							popalert("Success ! Video should now be playing.");
						}
					} else {
						alert("An error occured during the treatment of the demand. Please make sure the link/action is compatible.");
					}
				} else {
					alert("Error during connecting requesting from server !");
				}
			}
		};
		req.send(null);

		
	}
	catch(){
		popalert("Error !. Make sure the ip/port are corrects, and the server is running.")
		return "wrong";
	}
	
}

function mkrequest(url, response) {
	// Send settings every time a connection is made
	mkrequestXML("/settings?audioout="+localStorage.audioout+"&modeslow="+localStorage.modeslow, False);
	mkrequestXML(url, response);
}


$(function() {

	if (localStorage.popcorn == "off") {
		$("#popcorn_form").hide();
		$("#whole").css("height","215px");
	} else {
		$("#popcorn_form").show();
		$("#popcorn_url").focus();
		$("#whole").css("height","240px");
	}	

	$("#popcorn_form").submit(function() {

		url = $("#popcorn_url").val();
		var url_encoded_url = encodeURIComponent(url);
	
		if (mkrequest("/popcorn?url=" + url_encoded_url, True) != "wrong") {
			popalert("The movie should be successfully sent to the Raspberry Pi ! Please wait a few seconds. If it doesn't works, please make sure the ip/ports are corrects, and the server is running.");
		}
	});

	$( "#castbtn" ).click(function() {
		chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
			var url_encoded_url = encodeURIComponent(tabs[0].url);

			if (mkrequest("/stream?url=" + url_encoded_url, True) != "wrong") {
				popalert("The video should be successfully sent to the Raspberry Pi ! Please wait ~ 15/20 seconds. If it doesn't works, please make sure the ip/ports are corrects, and the server is running.");
			}
		});
			
	});

	$( "#addqueue" ).click(function() {
		chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
			var url_encoded_url = encodeURIComponent(tabs[0].url);

			if (mkrequest("/queue?url=" + url_encoded_url, True) != "wrong") {
				popalert("The video should be successfully added to queue. If it doesn't works, please make sure the ip/ports are corrects, and the server is running.");
			}
		});
			
	});	

	$( "#pause" ).click(function() {
		mkrequest("/video?control=pause", False);
	});	

	$( "#stop" ).click(function() {
		mkrequest("/video?control=stop", False);
	});
	
	$( "#backward" ).click(function() {
		mkrequest("/video?control=left", False);
	});
	
	$( "#forward" ).click(function() {
		mkrequest("/video?control=right", False);
	});
	
	$( "#vol_down" ).click(function() {
		mkrequest("/sound?vol=less", False);
	});
	
	$( "#vol_up" ).click(function() {
		mkrequest("/sound?vol=more", False);
	});
	
	
});
