$( document ).ready(function() {
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
		chrome.extension.getBackgroundPage().mkrequest("/popcorn?url=" + url_encoded_url, 1);
		chrome.extension.getBackgroundPage().mkrequest("/settings?audioout="+localStorage.audioout+"&modeslow="+localStorage.modeslow, 0);
	});

	$( "#castbtn" ).click(function() {
		chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
			var url_encoded_url = encodeURIComponent(tabs[0].url);
			chrome.extension.getBackgroundPage().mkrequest("/stream?url=" + url_encoded_url, 1);
			//chrome.extension.getBackgroundPage().mkrequest("/settings?audioout="+localStorage.audioout+"&modeslow="+localStorage.modeslow, 0);
		});
			
	});

	$( "#addqueue" ).click(function() {
		chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
			var url_encoded_url = encodeURIComponent(tabs[0].url);
			chrome.extension.getBackgroundPage().mkrequest("/queue?url="+url_encoded_url, 1);
			//chrome.extension.getBackgroundPage().mkrequest("/settings?audioout="+localStorage.audioout+"&modeslow="+localStorage.modeslow, 0);
		});
			
	});	

	$( "#pause" ).click(function() {
		chrome.extension.getBackgroundPage().mkrequest("/video?control=pause", 0);
	});	

	$( "#stop" ).click(function() {
		chrome.extension.getBackgroundPage().mkrequest("/video?control=stop", 0);
	});
	
	$( "#backward" ).click(function() {
		chrome.extension.getBackgroundPage().mkrequest("/video?control=left", 0);
	});
	
	$( "#forward" ).click(function() {
		chrome.extension.getBackgroundPage().mkrequest("/video?control=right", 0);
	});
	
	$( "#vol_down" ).click(function() {
		chrome.extension.getBackgroundPage().mkrequest("/sound?vol=less", 0);
	});
	
	$( "#vol_up" ).click(function() {
		chrome.extension.getBackgroundPage().mkrequest("/sound?vol=more", 0);
	});	
});
