function onError(error) {
  console.log(`Error: ${error}`);
}


function handlers() {

    $( "#castbtn" ).click(function(){
        browser.tabs.query({active: true, currentWindow: true})
        .then(function(tabs){
            browser.extension.getBackgroundPage().mkrequest("/stream?url=" + tabs[0].url
                                                   + "&slow="+localStorage.modeslow, 1);
            window.close();
        })
        .catch(onError);
    });

	$( "#addqueue" ).click(function() {
        browser.tabs.query({active: true, currentWindow: true})
        .then(function(tabs){
            browser.extension.getBackgroundPage().mkrequest("/queue?url=" + tabs[0].url
                                                   + "&slow="+localStorage.modeslow, 1);
            window.close();
        })
        .catch(onError);
    });

	$( "#pause" ).click(function() {
		browser.extension.getBackgroundPage().mkrequest("/video?control=pause", 0);
	});	

	$( "#stop" ).click(function() {
		browser.extension.getBackgroundPage().mkrequest("/video?control=stop", 0);
		window.close();
	});
	
	$( "#backward" ).click(function() {
		browser.extension.getBackgroundPage().mkrequest("/video?control=left", 0);
	});
	
	$( "#forward" ).click(function() {
		browser.extension.getBackgroundPage().mkrequest("/video?control=right", 0);
	});
	
	$( "#vol_down" ).click(function() {
		browser.extension.getBackgroundPage().mkrequest("/sound?vol=less", 0);
	});
	
	$( "#vol_up" ).click(function() {
		browser.extension.getBackgroundPage().mkrequest("/sound?vol=more", 0);
	});
}

function remote(toggle) {
	if (toggle == "show") {
		$("#remote").show();
		$("#whole").css("height","215px");
	} else {
		$("#remote").hide();
		$("#whole").css("height", "100px");
	}
	handlers();
}

function show(message) {
	$("#whole").html(message);
}

function test() {
	try {
		var newURL = "http://"+localStorage.getItem('raspip')+":2020/running";
		show("Loading...");
		var req = new XMLHttpRequest();
		req.open('GET', newURL, true);
		req.onreadystatechange = function (aEvt) {
			if (req.readyState == 4) {
				if (req.status == 200) {
					if (req.responseText == "1") {
						$("#whole").replaceWith(clonewhole.clone());
						remote("show");
					} else {
						$("#whole").replaceWith(clonewhole.clone());
						remote("hide");
					}
				} else {
					show("Error during accessing server. Make sure the ip/port are corrects, and the server is running.");
				}
			}
		};
		req.send(null);
	} 
	catch(err) {
		show("Error ! Make sure the ip/port are corrects, and the server is running.")
		return "0";
	}
}

$( document ).ready(function() {
	clonewhole = $("#whole").clone(); 
	test();	
});
