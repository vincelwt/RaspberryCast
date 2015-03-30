function saveSettings() {
	localStorage.raspip = document.getElementById("raspip").value;

	var radios = document.getElementsByName('cmFunction');
	for (var i = 0, length = radios.length; i < length; i++) {
	    if (radios[i].checked) {
		localStorage.cmFunction = radios[i].value;
		break;
	    }
	}

	var radios = document.getElementsByName('mode_slow');
	for (var i = 0, length = radios.length; i < length; i++) {
	    if (radios[i].checked) {
		localStorage.modeslow = radios[i].value;
		break;
	    }
	}

	var radios = document.getElementsByName('audio_out');
	for (var i = 0, length = radios.length; i < length; i++) {
	    if (radios[i].checked) {
		localStorage.audioout = radios[i].value;
		break;
	    }
	}

	var radios = document.getElementsByName('popcorn');
	for (var i = 0, length = radios.length; i < length; i++) {
	    if (radios[i].checked) {
		localStorage.popcorn = radios[i].value;
		break;
	    }
	}

	alert("Settings were successfully saved !");
}

document.addEventListener("DOMContentLoaded", function() {
	if (localStorage.raspip != undefined) {
		document.getElementById("raspip").value = localStorage.raspip;
		
	}

	if (localStorage.cmFunction == undefined) {
		localStorage.cmFunction = "stream";
		document.getElementById("cmFstream").checked = true;
	} else {
		if (localStorage.cmFunction == "stream") {
			document.getElementById("cmFstream").checked = true;
		} else {
			document.getElementById("cmFqueue").checked = true;
		}
	}

	if (localStorage.modeslow == undefined) {
		localStorage.modeslow = "False";
		document.getElementById("high_qual").checked = true;
	} else {
		if (localStorage.modeslow == "False") {
			document.getElementById("high_qual").checked = true;
		} else {
			document.getElementById("bad_qual").checked = true;
		}
	}
	
	if (localStorage.popcorn == undefined) {
		localStorage.popcorn = "off";
		document.getElementById("popcorn_off").checked = true;
	} else {
		if (localStorage.popcorn == "off") {
			document.getElementById("popcorn_off").checked = true;
		} else {
			document.getElementById("popcorn_on").checked = true;
		}
	}
	
	if (localStorage.audioout == undefined) {
		document.getElementById("audio_both").checked = true;
	} else {
		if (localStorage.audioout == "both") {
			document.getElementById("audio_both").checked = true;
		} else if (localStorage.audioout == "hdmi") {
			document.getElementById("audio_hdmi").checked = true;
		} else {
			document.getElementById("audio_local").checked = true;
		}
	}

	var el = document.getElementById("saveButton");
	el.addEventListener("click", saveSettings, false);
});
