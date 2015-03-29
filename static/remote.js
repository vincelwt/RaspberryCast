function message(msg, importance) {
	$( "#message" ).html("");
	$( "#message" ).show("slow");
	if (importance == 1) {
		$( "#message" ).html("<p class='bg-success'>"+msg+"</p>");
	} else if (importance == 2) {
		$( "#message" ).html("<p class='bg-danger'>"+msg+"</p>");
	} else {
		$( "#message" ).html("<p class='bg-info'>"+msg+"</p>");
	}
	setTimeout(function() {
		$( "#message" ).hide("slow");
	}, 3000);
	
}

function mkrequest(url, response) {
	try {
		var newURL = document.location.origin+url;
		if (response == 1 ) {
			message("Trying to get video stream URL. Please wait ~ 10-30 seconds.", 0);
		} else if (response == 2 ) {
			message("Trying to add video to queue. ", 0);
		} else if (response == 3 ) {
			message("Trying to program shutdown. ", 0);
		}
		
		var req = new XMLHttpRequest();
		req.open('GET', newURL, true);
		req.onreadystatechange = function (aEvt) {
			if (req.readyState == 4) {
				if (req.status == 200) {
					if (req.responseText == "1") {
						if (response == 1) {
							message("Success ! Video should now be playing.", 1);	
						} else if (response == 2) {
							message("Success ! Video has been added to queue.", 1);	
						} else if (response == 3) {
							message("Success ! Shutdown has been successfully programmed.", 1);	
						}
						
					} else {
						message("An error occured during the treatment of the demand. Please make sure the link/action is compatible", 2);
					}
				} else {
					message("Error during connecting requesting from server !", 2);
				}
			}
		};
		req.send(null);
	} 
	catch(err) {
		message("Error ! Make sure the ip/port are corrects, and the server is running.")
	}
}

$(function() {

	$( "#castbtn" ).click(function() {
		if ( $( "#media_url" ).val() !== "" ) {
			var url = $( "#media_url" ).val();
			var url_encoded_url = encodeURIComponent(url);
			mkrequest("/stream?url=" + url_encoded_url, 1)
		} else {
			message("You must enter a link !", 2)
		}	
	});

	$( "#addqueue" ).click(function() {
		if ( $( "#media_url" ).val() !== "" ) {
			var url = $( "#media_url" ).val();
			var url_encoded_url = encodeURIComponent(url);
			mkrequest("/queue?url=" + url_encoded_url, 2)
		} else {
			message("You must enter a link !", 2)
		}		
	});

	$( "#shutbtn" ).click(function() {
		if ( $( "#media_url" ).val() !== "" ) {
			var time = $( "#time_shut" ).val();
			console.log($( "#time_shut" ).val());
			mkrequest("/shutdown?time=" + time, 3)
		} else {
			message("You must enter a duration !", 2)
		}
	});	

	$( "#pause" ).click(function() {
		mkrequest("/video?control=pause", 0);
	});	

	$( "#stop" ).click(function() {
		mkrequest("/video?control=stop", 0);
	});
	
	$( "#backward" ).click(function() {
		mkrequest("/video?control=left", 0);
	});
	
	$( "#forward" ).click(function() {
		mkrequest("/video?control=right", 0);
	});
	
	$( "#vol_down" ).click(function() {
		mkrequest("/sound?vol=less", 0);
	});
	
	$( "#vol_up" ).click(function() {
		mkrequest("/sound?vol=more", 0);
	});
	
	
});
