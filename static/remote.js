function popalert(msg) {
	$( "#whole" ).hide();
	$( "#popalert" ).show();
	$( "#popalert" ).html("<p>"+msg+"</p>");
	setTimeout(function() {
		window.close();
	}, 4000);
	
}

function mkrequest(url) {
	try {
		var newURL = document.location.origin+url;
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.open( "GET", newURL, true);
		xmlHttp.send();
	}
	catch(err){
		popalert("Something went wrong. Make sure the ip/port are corrects, and the server is running."+err)
		return "wrong";
	}
}

$(function() {

	$( "#castbtn" ).click(function() {

		var url = $( "#media_url" ).val();

		var url_encoded_url = encodeURIComponent(url);

		if (mkrequest("/stream?url=" + url_encoded_url) != "wrong") {
			popalert("The medi should be successfully sent to the Raspberry Pi ! Please wait ~ 15/20 seconds. If it doesn't works, please make sure the ip/ports are corrects, and the server is running.");
		}
			
	});

	$( "#addqueue" ).click(function() {
				
		var url = $( "#media_url" ).val();
		var url_encoded_url = encodeURIComponent(url);

		if (mkrequest("/queue?url=" + url_encoded_url) != "wrong") {
			popalert("The video should be successfully added to queue. If it doesn't works, please make sure the ip/ports are corrects, and the server is running.");
		}
			
	});

	$( "#shutbtn" ).click(function() {
				
		var time = $( "#time_shut" ).val();
		console.log($( "#time_shut" ).val());
		if (mkrequest("/shutdown?time=" + time) != "wrong") {
			popalert("The shutdown should be programmed. If it doesn't works, please make sure the ip/ports are corrects, and the server is running.");
		}
			
	});	

	$( "#pause" ).click(function() {
		mkrequest("/video?control=pause");
	});	

	$( "#stop" ).click(function() {
		mkrequest("/video?control=stop");
	});
	
	$( "#backward" ).click(function() {
		mkrequest("/video?control=left");
	});
	
	$( "#forward" ).click(function() {
		mkrequest("/video?control=right");
	});
	
	$( "#vol_down" ).click(function() {
		mkrequest("/sound?vol=less");
	});
	
	$( "#vol_up" ).click(function() {
		mkrequest("/sound?vol=more");
	});
	
	
});
