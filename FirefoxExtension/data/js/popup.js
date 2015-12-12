function handlers() {

	$( "#castbtn" ).click(function() {
		self.port.emit("mkrequest", "/stream");
	});

	$( "#addqueue" ).click(function() {
		self.port.emit("mkrequest", "/queue");
	});	

	$( "#pause" ).click(function() {
		self.port.emit("mkrequest","/video?control=pause");
	});	

	$( "#stop" ).click(function() {
		self.port.emit("mkrequest","/video?control=stop");
	});
	
	$( "#backward" ).click(function() {
		self.port.emit("mkrequest", "/video?control=left");
	});
	
	$( "#forward" ).click(function() {
		self.port.emit("mkrequest", "/video?control=right");
	});
	
	$( "#vol_down" ).click(function() {
		self.port.emit("mkrequest", "/sound?vol=less");
	});
	
	$( "#vol_up" ).click(function() {
		self.port.emit("mkrequest", "/sound?vol=more");
	});
}

function remote(toggle) {
	if (toggle == "show") {
		$("#remote").show();
	} else {
		$("#remote").hide();
	}
	handlers();
}

function show(message) {
	$("#whole").html(message);
	$("#whole").show();	
}

$( document ).ready(function() {
	clonewhole = $("#whole").clone(); 
	$("#whole").hide();
	self.port.on("state", function(state) {
	  if (state == "loading") {
	  	show("Loading...");
	  } else if (state == "playing") {
	  	$("#whole").replaceWith(clonewhole.clone());
		remote("show");
	  } else if (state == "idle") {
	  	$("#whole").replaceWith(clonewhole.clone());
		remote("hide");
	  } else {
	  	show("Error ! Make sure the ip is correct, and the server is running.")
	  }
	});
});
