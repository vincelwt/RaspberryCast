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

function advanced() {
	$( "#advanced" ).toggle("fast");

	if($("#link-text").html() === "More options ▾") {
		$("#link-text").html("More options ▴");
	} else {
		$("#link-text").html("More options ▾");
	}
}


function showHistory() {
	//Only update history when div is being toggled ON
	if (!$( "#history-div" ).is(":visible"))
		updateHistoryDiv();

	$( "#history-div" ).toggle("fast");
}

function mkrequest(url, response) {
	try {
		var newURL = document.location.origin+url;
		if (response == 1 ) {
			message("Trying to get video stream URL. Please wait ~10 seconds.", 0);
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
							message("Success! Video should now be playing.", 1);	
						} else if (response == 2) {
							message("Success! Video has been added to queue.", 1);	
						} else if (response == 3) {
							message("Success! Shutdown has been successfully scheduled.", 1);	
						} else if (response == 4) {
							message("Success! Shutdown has been cancelled.", 1);	
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
		message("Error! Make sure the IP and port is correct, and that the server is running.")
	}
}

$(function() {

	$( "#castbtn" ).click(function() {
		if ( $( "#media_url" ).val() !== "" ) {
			var url = $( "#media_url" ).val();
			var url_encoded_url = encodeURIComponent(url);
			addToHistory(url);
			mkrequest("/stream?url=" + url_encoded_url, 1);
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

	$("#clear_search").click(function(){
		$("#media_url").val('');
		$("#clear_search").hide();
	});

	$("#media_url").keyup(function(){
		if($(this).val()) {
			$("#clear_search").show();
		} else {
			$("#clear_search").hide();
		}

	});

	$( "#shutbtn" ).click(function() {
		if ( $( "#time_shut" ).val() !== "" ) {
			var time = $( "#time_shut" ).val();
			console.log($( "#time_shut" ).val());
			mkrequest("/shutdown?time=" + time, 3)
		} else {
			message("You must enter a duration !", 2)
		}
	});	

	$( "#cancelshut" ).click(function() {
		mkrequest("/shutdown?time=cancel", 4)
	});

	$( "#nextqueue" ).click(function() {
		mkrequest("/video?control=next", 1)
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

	$( "#long-backward" ).click(function() {
		mkrequest("/video?control=longleft", 0);
	});
	
	$( "#long-forward" ).click(function() {
		mkrequest("/video?control=longright", 0);
	});
	
	$( "#vol_down" ).click(function() {
		mkrequest("/sound?vol=less", 0);
	});
	
	$( "#vol_up" ).click(function() {
		mkrequest("/sound?vol=more", 0);
	});
	
	
});
